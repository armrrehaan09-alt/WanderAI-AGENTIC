import html
import json
import os
import re
import time
import requests
import unicodedata
import streamlit as st
import streamlit.components.v1 as components

from agent import TravelAgent
from pdf_utils import build_trip_pdf

IMAGE_TIMEOUT = 6


@st.cache_data(ttl=86400, show_spinner=False)
def _image_json(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=IMAGE_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# VERIFIED IMAGE ENGINE
# ---------------------------------------------------------------------------
# Rule: a card is not allowed onto the page merely because Wikimedia returned
# an image. The image title/description must also agree with the item being
# shown. If it does not, that item is rejected and an image-backed alternative
# is searched for.
#
# Wikimedia's API exposes image URLs and extmetadata, which we use for this
# semantic validation. See:
# https://www.mediawiki.org/wiki/API:Imageinfo
# ---------------------------------------------------------------------------

IMAGE_BAD_WORDS = {
    "document", "report", "pdf", "book", "cover", "scan", "scanned",
    "article", "newspaper", "wikileaks", "cia", "assessment", "hearing",
    "testimony", "map", "locator", "diagram", "chart", "graph", "table",
    "logo", "flag", "seal", "screenshot", "manuscript", "thesis", "paper",
    "poster", "page", "database", "archive", "file", "template", "letter",
    "press release", "spreadsheet", "form", "dossier", "transcript",
}

GENERIC_WORDS = {
    "the", "and", "of", "in", "at", "on", "a", "an", "to", "for",
    "place", "local", "experience", "area", "city", "central", "stay",
    "hotel", "resort", "residency", "option", "planning", "reference",
    "food", "dish", "specialty", "regional", "tourist", "attraction",
    "market", "walk", "time", "cafe", "leisure",
}

def _norm_words(value):
    value = unicodedata.normalize("NFKD", _safe_text(value)).lower()
    return [w for w in re.split(r"[^a-z0-9]+", value) if len(w) >= 3 and w not in GENERIC_WORDS]

def _clean_html_text(value):
    value = re.sub(r"<[^>]+>", " ", _safe_text(value))
    return re.sub(r"\s+", " ", value).strip()

def _image_metadata_text(page):
    info = (page.get("imageinfo") or [{}])[0]
    meta = info.get("extmetadata") or {}
    pieces = [
        re.sub(r"^file:\s*", "", _clean_html_text(page.get("title", "")), flags=re.I),
        _clean_html_text((meta.get("ImageDescription") or {}).get("value", "")),
        _clean_html_text((meta.get("Categories") or {}).get("value", "")),
        _clean_html_text((meta.get("ObjectName") or {}).get("value", "")),
    ]
    return " ".join(pieces).lower()

def _image_candidate_score(page, query, kind, destination="", subject=""):
    info = (page.get("imageinfo") or [{}])[0]
    url = info.get("thumburl") or info.get("url")
    mime = _safe_text(info.get("mime")).lower()
    if not url or not str(url).startswith(("http://", "https://")):
        return -999, None
    if mime and not mime.startswith("image/"):
        return -999, None

    title = re.sub(r"^file:\s*", "", _clean_html_text(page.get("title", "")), flags=re.I).lower()
    blob = re.sub(r"\bfile:\s*", " ", _image_metadata_text(page), flags=re.I)

    if any(bad in title or bad in blob for bad in IMAGE_BAD_WORDS):
        return -999, None

    subject_words = _norm_words(subject)
    dest_words = _norm_words(destination)
    query_words = _norm_words(query)

    # Strong semantic anchors. For a named subject we require at least one
    # distinctive subject word in the source title/metadata.
    subject_hits = sum(1 for w in subject_words if w in blob)
    dest_hits = sum(1 for w in dest_words if w in blob)
    query_hits = sum(1 for w in query_words if w in blob)

    if kind in {"place", "itinerary"}:
        if subject_words and subject_hits == 0:
            return -999, None
        if len(subject_words) >= 2 and subject_hits == 0:
            return -999, None
    elif kind == "food":
        if subject_words and subject_hits == 0:
            return -999, None
    elif kind == "hotel":
        # Fake/local placeholder hotels must never inherit a city photograph.
        if "placeholder" in subject.lower() or not subject_words:
            return -999, None
        if subject_hits == 0 and dest_hits == 0:
            return -999, None
    elif kind == "flight":
        # Passenger-flight cards must never use military aircraft. For real
        # airline names we prefer an airline/airliner match; for planning
        # placeholders we require commercial/passenger aviation imagery.
        military_terms = (
            "military", "fighter", "warplane", "combat", "bomber",
            "air force", "navy", "attack aircraft", "trainer aircraft",
            "military aircraft",
        )
        if any(x in blob for x in military_terms):
            return -999, None
        commercial_terms = (
            "commercial", "airliner", "airplane", "aircraft",
            "aviation", "civil aviation", "airline",
        )
        if subject_words and subject_hits == 0 and not any(x in blob for x in commercial_terms):
            return -999, None
        if not subject_words and not any(x in blob for x in commercial_terms):
            return -999, None

    score = 0
    score += subject_hits * 10
    score += dest_hits * 3
    score += query_hits * 2
    if "photograph" in blob or "photo" in blob:
        score += 1
    if "aircraft" in blob or "airplane" in blob:
        score += 2 if kind == "flight" else 0
    if "food" in blob or "dish" in blob or "cuisine" in blob:
        score += 2 if kind == "food" else 0

    # Exact subject phrase in title is a very strong signal.
    normalized_subject = " ".join(subject_words)
    if normalized_subject and normalized_subject in title:
        score += 18

    return score, {
        "url": url,
        "title": page.get("title", ""),
        "score": score,
    }

@st.cache_data(ttl=86400, show_spinner=False)
def _wikimedia_candidates(query, limit=12):
    payload = _image_json(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": min(20, max(5, limit)),
            "prop": "imageinfo",
            "iiprop": "url|mime|extmetadata",
            "iiurlwidth": 1000,
            "format": "json",
        },
    )
    if not payload:
        return []
    return list((payload.get("query", {}).get("pages", {}) or {}).values())

@st.cache_data(ttl=86400, show_spinner=False)
def _verified_wikimedia_image(queries_tuple, kind, destination, subject):
    """Return one semantically verified image, never merely the first search hit."""
    for query in queries_tuple:
        if not query:
            continue
        pages = _wikimedia_candidates(query, 14)
        ranked = []
        for page in pages:
            score, candidate = _image_candidate_score(
                page, query, kind, destination, subject
            )
            if candidate and score >= 8:
                ranked.append(candidate)
        ranked.sort(key=lambda x: x["score"], reverse=True)
        if ranked:
            return {
                "url": ranked[0]["url"],
                "label": "Verified reference image · Wikimedia Commons",
                "title": ranked[0]["title"],
            }
    return None

def _safe_text(value):
    return str(value or "").strip()


def _candidate_queries(item, destination, kind):
    item = item if isinstance(item, dict) else {}
    name = _safe_text(item.get("name") or item.get("airline"))
    area = _safe_text(item.get("area"))
    category = _safe_text(item.get("category"))
    planning = _safe_text(destination)

    if kind == "flight":
        airline = name if name and "flight option" not in name.lower() else ""
        return [
            (f"{airline} commercial airliner exterior", airline or "commercial airliner"),
            (f"{airline} passenger airplane exterior", airline or "commercial airliner"),
            ("commercial airliner aircraft exterior", "commercial airliner"),
        ]

    if kind == "hotel":
        # Only real/listing-backed hotel names are eligible. A planning
        # placeholder is not allowed to masquerade as a real hotel.
        source = _safe_text(item.get("source")).lower()
        if "placeholder" in source:
            return []
        return [
            (f"{name} {planning}", name),
            (f"{name} hotel {planning}", name),
            (f"{area} hotel {planning}", area or name),
        ]

    if kind == "food":
        return [
            (f"{name} {planning} food", name),
            (f"{name} {planning} dish", name),
            (f"{name} cuisine {planning}", name),
            (f"{name} traditional food", name),
        ]

    generic = {"city highlights", "local market", "scenic area", "local exploration",
               "flexible experience", "neighbourhood walk", "neighborhood walk",
               "local food experience", "cafe & leisure time", "café & leisure time"}
    if name.lower() in generic:
        return []
    return [
        (f"{name} {planning}", name),
        (f"{name} {planning} attraction", name),
        (f"{name} {planning} landmark", name),
    ]


def _discover_image_backed_alternatives(destination, kind, existing_names, needed=3):
    """Discover replacement subjects directly from image-backed Commons results.

    This is deliberately conservative: the returned subject comes from the
    source image title itself, so the displayed content and image remain tied.
    """
    existing = {re.sub(r"\s+", " ", _safe_text(x).lower()) for x in existing_names}
    if kind == "food":
        queries = [
            f"{destination} traditional food",
            f"{destination} cuisine dishes",
            f"{destination} local food",
        ]
    elif kind == "flight":
        queries = [f"{destination} airport aircraft", f"{destination} aviation"]
    elif kind == "hotel":
        queries = [f"{destination} hotel", f"{destination} accommodation"]
    else:
        queries = [
            f"{destination} tourist attractions",
            f"{destination} landmarks",
            f"{destination} places to visit",
        ]

    found = []
    seen_titles = set()
    for query in queries:
        for page in _wikimedia_candidates(query, 20):
            title = re.sub(r"^File:\s*", "", _safe_text(page.get("title")), flags=re.I)
            title_clean = re.sub(r"\.[a-z0-9]{2,5}$", "", title, flags=re.I)
            key = re.sub(r"\s+", " ", title_clean.lower()).strip()
            if not key or key in existing or key in seen_titles:
                continue

            # Candidate subject must itself produce a high-confidence image.
            score, candidate = _image_candidate_score(
                page, query, kind, destination, title_clean
            )
            if not candidate or score < 8:
                continue

            # Remove obviously non-place/file-title noise.
            if any(bad in key for bad in IMAGE_BAD_WORDS):
                continue

            seen_titles.add(key)
            found.append({
                "name": title_clean,
                "category": "Image-backed alternative",
                "image_url": candidate["url"],
                "image_label": "Verified source image · Wikimedia Commons",
                "source": "image-backed alternative",
            })
            if len(found) >= needed:
                return found
    return found


def _resolve_verified_cards(items, destination, kind, max_items=6):
    """Resolve cards and replace failed subjects with image-backed alternatives."""
    original = [x for x in (items or []) if isinstance(x, dict)]
    accepted = []
    rejected_names = []
    seen = set()

    for item in original:
        name = _safe_text(item.get("name") or item.get("airline"))
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())

        queries = _candidate_queries(item, destination, kind)
        image = None
        if item.get("image_url"):
            # Existing provider images are accepted only for non-placeholder
            # items; source-specific semantic validation is not possible here.
            if "placeholder" not in _safe_text(item.get("source")).lower():
                image = {"url": item["image_url"], "label": item.get("image_label") or "Verified source image"}

        if not image and queries:
            image = _verified_wikimedia_image(
                tuple(q for q, _ in queries), kind, destination, name
            )

        if image:
            accepted.append({**item, "image_url": image["url"], "image_label": image["label"]})
        else:
            rejected_names.append(name)

        if len(accepted) >= max_items:
            break

    # Fill the missing slots with actual image-backed alternatives.
    remaining = max_items - len(accepted)
    if remaining > 0 and kind in {"place", "food", "hotel"}:
        alternatives = _discover_image_backed_alternatives(
            destination, kind, list(seen) + rejected_names, remaining
        )
        accepted.extend(alternatives[:remaining])

    return accepted[:max_items]


def _render_browser_image_cards(items, destination, kind, max_items=6):
    """Render only semantically verified images, resolving them in the browser.

    Browser-side lookup avoids a server/runtime DNS restriction preventing the
    image API from returning anything. Commons candidates are checked against
    the displayed subject before they are inserted into the card grid.
    """
    original = [x for x in (items or []) if isinstance(x, dict)]
    if not original:
        return 0

    cards = []
    for item in original[:max_items]:
        name = _safe_text(item.get("name") or item.get("airline") or "Travel option")
        if not name:
            continue
        subtitle = _safe_text(
            item.get("route") or item.get("area") or item.get("category") or
            ("Local dish" if kind == "food" else "Recommended place")
        )
        details = []
        if kind == "flight" and item.get("price") is not None:
            details.append(f"Fare: {_safe_text(item.get('currency') or '₹')} {item.get('price')}")
        elif kind == "hotel":
            price = item.get("price") if item.get("price") not in (None, "") else item.get("price_per_night")
            if price not in (None, ""):
                details.append(f"Nightly: {_safe_text(item.get('currency') or '₹')} {price}")
        elif kind == "food" and item.get("description"):
            details.append(_safe_text(item.get("description")))

        if kind == "flight":
            queries = [f"{name} aircraft", f"{name} airplane", "commercial aircraft aviation"]
        elif kind == "hotel":
            queries = [f"{name} {destination} hotel", f"hotel {destination}", f"accommodation {destination}"]
        elif kind == "food":
            queries = [f"{name} {destination} food", f"{name} {destination} dish", f"{name} traditional food"]
        else:
            queries = [f"{name} {destination}", f"{name} {destination} attraction", f"{name} landmark"]

        cards.append({
            "name": name, "subtitle": subtitle, "details": " · ".join(details),
            "queries": queries, "kind": kind, "destination": destination,
        })

    payload = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")
    height = max(285, ((len(cards) + 2) // 3) * 335 + 80)

    html_template = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box} body{margin:0;font-family:Arial,sans-serif;background:transparent;color:#17324D}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.card{overflow:hidden;border-radius:18px;background:rgba(255,255,255,.90);border:1px solid rgba(21,94,117,.12);box-shadow:0 8px 24px rgba(21,50,77,.08);min-height:285px}
.photo{width:100%;height:190px;object-fit:cover;display:block;background:#eef5f3}
.body{padding:12px 13px}.title{font-weight:750;font-size:16px;color:#155E75;margin-bottom:5px}
.sub{font-size:12px;color:#557080;min-height:17px}.details{font-size:12px;color:#31556B;margin-top:6px}.source{font-size:10px;color:#718096;margin-top:8px}
.status{padding:28px 16px;text-align:center;color:#718096;font-size:13px;grid-column:1/-1}
@media(max-width:800px){.grid{grid-template-columns:1fr}.photo{height:180px}}
</style></head><body><div id="grid" class="grid"></div>
<script>
const ITEMS = __PAYLOAD__;
const DEST = __DEST__;
const BAD = ['document','report','pdf','book','cover','scan','article','newspaper','wikileaks','cia','assessment','hearing','testimony','map','locator','diagram','chart','graph','table','logo','flag','seal','screenshot','manuscript','thesis','paper','poster','database','archive','template','letter','press release','spreadsheet','form','dossier','transcript','military','fighter','warplane','combat','bomber','air force','navy','attack aircraft','trainer aircraft','military aircraft','cabin','aircraft interior','passenger cabin','airline seats','airplane interior','inside the aircraft'];
const GENERIC = new Set(['the','and','of','in','at','on','a','an','to','for','place','local','experience','area','city','central','stay','hotel','resort','residency','option','planning','reference','food','dish','specialty','regional','tourist','attraction','market','walk','time','cafe','leisure']);
function norm(s){return String(s||'').normalize('NFKD').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function words(s){return norm(s).split(/\s+/).filter(w=>w.length>=3&&!GENERIC.has(w));}
function clean(s){return String(s||'').replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();}
function metadata(page){const ii=(page.imageinfo||[{}])[0]||{};const em=ii.extmetadata||{};return [String(page.title||'').replace(/^File:\s*/i,''),clean((em.ImageDescription||{}).value),clean((em.Categories||{}).value),clean((em.ObjectName||{}).value)].join(' ').toLowerCase();}
function score(page,item,query){
 const ii=(page.imageinfo||[{}])[0]||{};const url=ii.thumburl||ii.url;const mime=String(ii.mime||'').toLowerCase();
 if(!url||!/^https?:\/\//.test(url)||(mime&&!mime.startsWith('image/')))return -999;
 const title=String(page.title||'').replace(/^File:\s*/i,'').toLowerCase();const blob=metadata(page);
 if(BAD.some(x=>title.includes(x)||blob.includes(x)))return -999;
 const sw=words(item.name),dw=words(DEST),qw=words(query);const sh=sw.filter(w=>blob.includes(w)).length;const dh=dw.filter(w=>blob.includes(w)).length;const qh=qw.filter(w=>blob.includes(w)).length;
 if((item.kind==='place'||item.kind==='itinerary'||item.kind==='food')&&sw.length&&sh===0)return -999;
 const military=/(military|fighter|warplane|combat|bomber|air force|navy|attack aircraft|trainer aircraft|military aircraft)/.test(blob);
 if(item.kind==='flight'){
   if(military||/(cabin|aircraft interior|passenger cabin|airline seats|airplane interior|inside the aircraft)/.test(blob))return -999;
   const commercial=/(commercial|airliner|airplane|aircraft|aviation|civil aviation|airline)/.test(blob);
   if(!commercial)return -999;
 }
 if(item.kind==='hotel'){
   const ph=/placeholder|planning\s+option|central\s+stay|comfort\s+residency/i.test(item.name);
   if(ph){
     const lodging=/(hotel|accommodation|lodging|hostel|inn|guesthouse|resort|residence|stay)/.test(blob);
     if(!lodging || dh===0)return -999;
   }else if(sw.length&&sh===0&&dh===0)return -999;
 }
 let n=sh*12+dh*4+qh*2;if(sw.length&&norm(item.name)&&title.includes(norm(item.name)))n+=25;if(item.kind==='food'&&/(food|dish|cuisine|meal|croissant|crepe|soup|ratatouille)/.test(blob))n+=5;if(item.kind==='flight'&&/(commercial|passenger|airliner|airplane|aircraft|aviation|civil aviation|airline)/.test(blob))n+=4;return n;
}
async function commons(q){const url='https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch='+encodeURIComponent(q)+'&gsrnamespace=6&gsrlimit=12&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=1000&format=json&origin=*';try{const r=await fetch(url);if(!r.ok)return [];const j=await r.json();return Object.values((j.query&&j.query.pages)||{});}catch(e){return []}}
async function wiki(title){const url='https://en.wikipedia.org/api/rest_v1/page/summary/'+encodeURIComponent(title.replace(/\s+/g,'_'));try{const r=await fetch(url);if(!r.ok)return null;const j=await r.json();if(!j.thumbnail||!j.thumbnail.source)return null;return {url:j.thumbnail.source,title:j.title||title,description:j.extract||''};}catch(e){return null}}
function wikiScore(x,item){const blob=norm((x.title||'')+' '+(x.description||''));const sw=words(item.name),dh=words(DEST).filter(w=>blob.includes(w)).length,sh=sw.filter(w=>blob.includes(w)).length;if((item.kind==='place'||item.kind==='itinerary'||item.kind==='food')&&sw.length&&sh===0)return -999;if(item.kind==='hotel'&&dh===0)return -999;let n=sh*15+dh*3;if(norm(x.title||'').includes(norm(item.name)))n+=25;return n;}
async function resolve(item,usedUrls,usedSources){
 const placeholderHotel=item.kind==='hotel'&&/placeholder|planning\s+option|central\s+stay|comfort\s+residency/i.test(item.name);
 const placeholderFlight=item.kind==='flight'&&/flight planning option|alternative flight option/i.test(item.name);
 let queries=item.queries||[];
 if(placeholderHotel) queries=[`${DEST} historic hotel exterior`,`${DEST} hotel building exterior`,`${DEST} accommodation exterior`];
 if(placeholderFlight) queries=[`${DEST} commercial airliner exterior`,`${DEST} passenger airplane exterior`,`commercial airliner aircraft exterior`,`civil aviation passenger aircraft`];
 for(const q of queries){
   const pages=await commons(q);
   const ranked=pages.map(p=>({p,s:score(p,item,q)})).filter(x=>x.s>=8).sort((a,b)=>b.s-a.s);
   for(const row of ranked){
     const ii=(row.p.imageinfo||[{}])[0]||{}; const url=ii.thumburl||ii.url;
     const sourceTitle=String(row.p.title||'').replace(/^File:\s*/i,'');
     if(!url||usedUrls.has(url)||usedSources.has(norm(sourceTitle)))continue;
     return {url,sourceTitle,label: placeholderHotel ? 'Representative accommodation image · Wikimedia Commons' : (placeholderFlight ? 'Representative commercial aircraft image · Wikimedia Commons' : 'Verified reference image · Wikimedia Commons')};
   }
 }
 if(item.kind!=='flight'&&!placeholderHotel){for(const q of [item.name,item.name+' '+DEST]){const x=await wiki(q);if(x&&wikiScore(x,item)>=8&&!usedUrls.has(x.url)&&!usedSources.has(norm(x.title||'')))return {url:x.url,sourceTitle:x.title,label:'Verified reference image · Wikipedia'};}}
 return null;
}
function esc(v){return String(v??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function renderCard(item,img){return `<div class="card"><img class="photo" src="${esc(img.url)}" alt="${esc(item.name)}" loading="lazy" referrerpolicy="no-referrer" onerror="this.closest('.card').remove()"><div class="body"><div class="title">${esc(item.name)}</div><div class="sub">${esc(item.subtitle)}</div>${item.details?`<div class="details">${esc(item.details)}</div>`:''}<div class="source">${esc(img.label)}</div></div></div>`;}
async function main(){const grid=document.getElementById('grid');grid.innerHTML='<div class="status">Finding verified images…</div>';const results=[];const usedUrls=new Set();const usedSources=new Set();for(const item of ITEMS){const img=await resolve(item,usedUrls,usedSources);if(img){usedUrls.add(img.url);if(img.sourceTitle)usedSources.add(norm(img.sourceTitle));results.push({item,img});}}if(!results.length){grid.innerHTML='<div class="status">No verified matching images were available from the connected image sources.</div>';return;}grid.innerHTML=results.map(x=>renderCard(x.item,x.img)).join('');}
main();
</script></body></html>"""
    html_out = html_template.replace("__PAYLOAD__", payload).replace("__DEST__", json.dumps(destination))
    components.html(html_out, height=height, scrolling=False)
    return len(cards)


# ---------------------------------------------------------------------------
# Legacy helper kept for compatibility with any existing code paths.
# It now uses the verified resolver instead of first-hit search.
# ---------------------------------------------------------------------------
def _get_item_image(item, destination, kind):
    name = _safe_text((item or {}).get("name") or (item or {}).get("airline"))
    queries = _candidate_queries(item or {}, destination, kind)
    if not queries:
        return None
    return _verified_wikimedia_image(tuple(q for q, _ in queries), kind, destination, name)

def _itinerary_image(item, destination):
    return _get_item_image(item, destination, "itinerary")

def _render_media_card(item, destination, kind, subtitle=""):
    image = _get_item_image(item, destination, kind)
    if not image:
        return ""
    name = html.escape(_safe_text(item.get("name") or item.get("airline") or "Travel option"))
    sub = html.escape(subtitle or _safe_text(item.get("category") or item.get("area") or item.get("route")))
    return (
        f"<div class='media-card'><img src='{html.escape(image['url'], quote=True)}' alt='{name}' "
        f"loading='lazy' onerror='this.closest(\".media-card\").remove()'>"
        f"<div class='media-body'><h4>{name}</h4><p>{sub}</p></div></div>"
    )

st.set_page_config(page_title="WanderAI", page_icon="✈️", layout="wide")

st.markdown(
    '''
<style>
.day-card{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.20);border-radius:22px;padding:24px;margin:18px 0;box-shadow:0 12px 35px rgba(0,0,0,.14);backdrop-filter:blur(12px)}
.day-card-header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:20px}
.day-label{font-size:13px;font-weight:800;letter-spacing:1.5px;opacity:.78}
.day-card h3{margin:4px 0 3px 0;font-size:25px}.day-theme{opacity:.78}
.day-badge{border:1px solid rgba(64,224,208,.55);border-radius:999px;padding:7px 12px;font-size:11px;font-weight:800}
.day-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.day-section{background:rgba(255,255,255,.07);border-radius:16px;padding:15px}.day-section h4{margin:0 0 10px}
.itinerary-item{padding:9px 0;border-bottom:1px solid rgba(255,255,255,.10)}.itinerary-item:last-child{border-bottom:0}
.itinerary-item span{opacity:.76;font-size:13px}.day-footer{display:flex;flex-wrap:wrap;gap:18px;margin-top:16px;padding-top:14px;border-top:1px solid rgba(255,255,255,.12)}
.day-note{margin-top:12px;opacity:.72;font-size:13px}
.media-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}
.media-card{overflow:hidden;border-radius:18px;background:rgba(255,255,255,.72);border:1px solid rgba(21,94,117,.10);box-shadow:0 8px 24px rgba(21,50,77,.07)}
.media-card img{width:100%;height:190px;object-fit:cover;display:block}
.media-body{padding:12px 13px}.media-body h4{margin:0 0 5px;color:#155E75}.media-body p{margin:0;color:#557080;font-size:13px}
.itinerary-media{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}
.itinerary-media-card{overflow:hidden;border-radius:16px;background:rgba(255,255,255,.62);border:1px solid rgba(21,94,117,.10)}
.itinerary-media-card img{width:100%;height:145px;object-fit:cover;display:block}.itinerary-media-card div{padding:9px 11px;font-size:13px;font-weight:700;color:#31556B}
@media(max-width:800px){.day-grid,.media-grid,.itinerary-media{grid-template-columns:1fr}.day-card-header{flex-direction:column}}
@media(max-width:800px){.day-grid{grid-template-columns:1fr}.day-card-header{flex-direction:column}}
</style>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    '''
    <style>
    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(244,184,96,.22), transparent 25%),
            radial-gradient(circle at 88% 12%, rgba(15,118,110,.16), transparent 28%),
            linear-gradient(135deg, #FFF7ED 0%, #F4F8F4 45%, #E8F7F5 100%);
        color: #17324D;
    }
    .block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 4rem; }
    .hero, .glass-card, .metric, .agent-card {
        background: rgba(255,255,255,.72);
        border: 1px solid rgba(21,94,117,.12);
        box-shadow: 0 12px 35px rgba(21,50,77,.08);
        backdrop-filter: blur(14px);
    }
    .hero { padding: 2.2rem; border-radius: 30px; margin-bottom: 1.4rem; }
    .hero h1 { color: #155E75; font-size: 3rem; margin-bottom: .2rem; }
    .hero p { color: #557080; font-size: 1.08rem; margin: .25rem 0; }
    .glass-card { padding: 1.2rem; border-radius: 20px; margin-bottom: 1rem; }
    .glass-card h3, .glass-card h4 { color: #155E75; }
    .metric { padding: 1rem; border-radius: 18px; text-align: center; }
    .metric-title { color: #557080; font-size: .88rem; }
    .metric-value { color: #17324D; font-size: 1.35rem; font-weight: 750; margin-top: .25rem; }
    .agent-card { padding: 1rem 1.2rem; border-radius: 20px; margin: 1rem 0; }
    .agent-step { padding: .42rem 0; color: #31556B; }
    .live-pill { display:inline-block; padding:.25rem .65rem; border-radius:999px; background:#DDF5EF; color:#0F766E; font-weight:700; font-size:.78rem; }
    .partial-pill { display:inline-block; padding:.25rem .65rem; border-radius:999px; background:#FFF0D8; color:#8A5A16; font-weight:700; font-size:.78rem; }
    .info-box { padding:1rem 1.2rem; border-radius:18px; background:#EAF7F5; border:1px solid #B9E4DE; color:#24566A; margin:1rem 0; }
    .warn-box { padding:1rem 1.2rem; border-radius:18px; background:#FFF5E6; border:1px solid #F2D09A; color:#76531D; margin:1rem 0; }
    /* Keep the trip-request field consistent across light/dark browser themes. */
    div[data-testid="stTextArea"] textarea, textarea {
        background:#FFFFFF !important;
        color:#17324D !important;
        border:1px solid rgba(21,94,117,.20) !important;
        border-radius:18px !important;
        caret-color:#0F766E !important;
        box-shadow:0 8px 24px rgba(21,50,77,.06) !important;
    }
    div[data-testid="stTextArea"] textarea::placeholder, textarea::placeholder {
        color:#718096 !important;
        opacity:1 !important;
    }
    div[data-testid="stTextArea"] textarea:focus, textarea:focus {
        border-color:#0F766E !important;
        box-shadow:0 0 0 2px rgba(15,118,110,.12) !important;
    }
    div.stButton > button { border-radius:14px; border:0; color:white; font-weight:750; background:linear-gradient(90deg,#0F766E,#155E75); }
    </style>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    '''
    <div class="hero">
        <h1>✈️ WanderAI</h1>
        <p>Your AI-Powered Travel Agent</p>
        <p>Describe your trip naturally. WanderAI resolves the destination, checks connected live travel sources and prepares the information needed for planning.</p>
    </div>
    ''',
    unsafe_allow_html=True,
)

if "travel_result" not in st.session_state:
    st.session_state.travel_result = None
if "approval_state" not in st.session_state:
    st.session_state.approval_state = "pending"
if "approval_pdf" not in st.session_state:
    st.session_state.approval_pdf = None
if "approval_message" not in st.session_state:
    st.session_state.approval_message = ""
if "travel_agent" not in st.session_state:
    st.session_state.travel_agent = TravelAgent()

st.markdown("### 🌴 Tell WanderAI about your trip")
request = st.text_area(
    "Trip request",
    placeholder="Example: Plan a 5 night trip to Goa with beaches and a budget under ₹20000",
    height=120,
    label_visibility="collapsed",
)

create_plan = st.button("✨ Create My Travel Plan", use_container_width=True)

if create_plan:
    if not request.strip():
        st.warning("Please describe your trip first.")
    else:
        status_box = st.empty()
        status_steps = [
            "Understanding your request",
            "Resolving destination",
            "Searching travel options",
            "Finding stays",
            "Finding activities",
            "Calculating budget",
            "Building itinerary",
            "Plan ready",
        ]
        shown = []
        for step in status_steps:
            shown.append(step)
            status_box.markdown(
                '<div class="agent-card">' +
                "".join(f'<div class="agent-step">✓ {html.escape(item)}</div>' for item in shown) +
                '</div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.65 if step != "Plan ready" else 0.35)

        st.session_state.travel_result = st.session_state.travel_agent.run(request.strip())
        st.session_state.approval_state = "pending"
        st.session_state.approval_pdf = None
        st.session_state.approval_message = ""
        status_box.empty()
        st.rerun()

result = st.session_state.travel_result
if not result:
    st.stop()

if not result.get("success"):
    error_text = str(result.get("error", "We could not create the plan."))
    if "tell me where you want to travel" in error_text.lower():
        message = (
            "🌍 <strong>Where would you like to go?</strong><br>"
            "Give me a destination and I’ll build the trip around it — "
            "for example, <em>“5 days in Goa”</em> or <em>“a relaxed trip to Kerala”</em>."
        )
    else:
        message = f"⚠️ <strong>{html.escape(error_text)}</strong>"
    st.markdown(f'<div class="warn-box">{message}</div>', unsafe_allow_html=True)
    st.stop()

destination = result["destination"]
location = result.get("location", {})
nights = result["nights"]
budget_limit = result.get("budget_limit")
results = result.get("results", {})

st.markdown("## 🧭 Trip Snapshot")
c1, c2, c3, c4 = st.columns(4)
for col, title, value in [
    (c1, "Destination", destination),
    (c2, "Country", location.get("country", "—")),
    (c3, "Stay", f"{nights} nights"),
    (c4, "Data", "Live + planning" if result.get("live_sources") else "Planning data"),
]:
    with col:
        st.markdown(
            f'<div class="metric"><div class="metric-title">{html.escape(title)}</div><div class="metric-value">{html.escape(str(value))}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("## ⚡ WanderAI Agent")
steps = result.get("agent_steps", [])
st.markdown(
    '<div class="agent-card">' + "".join(
        f'<div class="agent-step">✓ {html.escape(step)}</div>' for step in steps
    ) + "</div>",
    unsafe_allow_html=True,
)

if result.get("live_sources"):
    st.markdown(
        f'<span class="live-pill">● LIVE DATA: {", ".join(result["live_sources"])}</span>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<span class="partial-pill">● Some live travel sources still need to be connected</span>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# HUMAN-IN-THE-LOOP APPROVAL
# The agent prepares the plan first. PDF export is blocked until the human
# explicitly approves the current plan. A rejection sends the user to the
# existing re-planning flow, and any revised plan requires approval again.
# ---------------------------------------------------------------------------
approval_state = st.session_state.get("approval_state", "pending")
st.markdown("## 👤 Human Approval")
if approval_state == "pending":
    st.markdown(
        f"""<div class="glass-card"><strong>WanderAI has prepared your trip.</strong><br>
        Destination: <strong>{html.escape(str(destination))}</strong> ·
        {html.escape(str(nights + 1))} days / {html.escape(str(nights))} nights.<br>
        Review the plan below. <strong>The PDF will only be enabled after you approve it.</strong></div>""",
        unsafe_allow_html=True,
    )
    approve_col, change_col = st.columns(2)
    with approve_col:
        approve_clicked = st.button("✅ Yes, approve this trip", use_container_width=True, key="approve_trip")
    with change_col:
        change_clicked = st.button("✏️ No, I want changes", use_container_width=True, key="reject_trip")
    if approve_clicked:
        try:
            st.session_state.approval_pdf = build_trip_pdf(result)
            st.session_state.approval_state = "approved"
            st.session_state.approval_message = "Trip approved. Your PDF is ready."
            st.rerun()
        except Exception as exc:
            st.session_state.approval_message = f"PDF generation failed: {exc}"
            st.session_state.approval_state = "pdf_error"
            st.rerun()
    if change_clicked:
        st.session_state.approval_state = "changes_requested"
        st.session_state.approval_message = "Tell WanderAI what you want changed, then approve the revised plan."
        st.rerun()
elif approval_state == "approved":
    st.success(st.session_state.get("approval_message") or "Trip approved.")
    pdf_bytes = st.session_state.get("approval_pdf")
    if pdf_bytes:
        safe_destination = re.sub(r"[^A-Za-z0-9]+", "_", str(destination)).strip("_") or "trip"
        st.download_button(
            "📄 Download Approved Trip Summary (PDF)",
            data=pdf_bytes,
            file_name=f"WanderAI_{safe_destination}_Trip_Summary.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_trip_pdf",
        )
elif approval_state == "changes_requested":
    st.info(st.session_state.get("approval_message") or "Tell WanderAI what you want changed.")
elif approval_state == "pdf_error":
    st.error(st.session_state.get("approval_message") or "The PDF could not be generated.")

# Weather
weather = results.get("weather") or {}
if weather.get("available"):
    st.markdown("## 🌦️ Current Weather & Forecast")
    current = weather.get("current", {})
    a, b, c = st.columns(3)
    with a: st.metric("Temperature", f"{current.get('temperature_2m', '—')} °C")
    with b: st.metric("Feels Like", f"{current.get('apparent_temperature', '—')} °C")
    with c: st.metric("Wind", f"{current.get('wind_speed_10m', '—')} km/h")
    for row in weather.get("daily", [])[:min(7, nights + 2)]:
        st.markdown(
            f'<div class="glass-card"><strong>{row["date"]}</strong> · {row.get("low", "—")}°C – {row.get("high", "—")}°C · Rain chance {row.get("rain_probability", "—")}%</div>',
            unsafe_allow_html=True,
        )

# Flights
flight = results.get("flight") or {}
st.markdown("## ✈️ Flight Options" if not flight.get("live") else "## ✈️ Live Flight Information")
if flight.get("available"):
    options = flight.get("options", [])
    _render_browser_image_cards(options, destination, "flight", max_items=4)
    # Flight details are included directly in the image cards above.
else:
    st.markdown(f'<div class="info-box">{html.escape(str(flight.get("message", "No flight data is available.")))}</div>', unsafe_allow_html=True)

# Hotels
hotel = results.get("hotel") or {}
st.markdown("## 🏨 Accommodation Options" if not hotel.get("live") else "## 🏨 Live Accommodation")
if hotel.get("available"):
    options = hotel.get("options", [])
    _render_browser_image_cards(options, destination, "hotel", max_items=6)
    # Hotel details are included directly in the image cards above.
else:
    st.markdown(f'<div class="info-box">{html.escape(str(hotel.get("message", "No accommodation data is available.")))}</div>', unsafe_allow_html=True)

# Activities
activities = results.get("activities") or {}
st.markdown("## 🎯 Recommended Attractions & Places" if not activities.get("live") else "## 🎯 Live Attractions & Places")
if activities.get("available"):
    options = activities.get("options", [])
    _render_browser_image_cards(options, destination, "place", max_items=8)
    # Attraction details are included directly in the image cards above.
else:
    st.markdown(f'<div class="info-box">{html.escape(str(activities.get("message", "No attraction data is available.")))}</div>', unsafe_allow_html=True)

# Food
food = results.get("food") or {}
if food.get("available"):
    st.markdown("## 🍛 Local Food Recommendations")
    verified_food_count = _render_browser_image_cards(
        food.get("options", []), destination, "food", max_items=4
    )
    if not verified_food_count:
        st.markdown(
            '<div class="info-box">No verified food photographs were found for this destination. '
            'The food names remain available in the itinerary and planning data.</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f"<div class='info-box'>{html.escape(str(food.get('message', 'Food suggestions for planning.')))}</div>",
        unsafe_allow_html=True,
    )

# Budget inputs only; live pricing is not fabricated.
budget = results.get("budget") or {}
st.markdown("## 💰 Available Pricing Information")
breakdown = budget.get("breakdown", {})
b1, b2, b3, b4, b5 = st.columns(5)
with b1: st.metric("Flight", f"₹{breakdown['flight']:,.0f}" if isinstance(breakdown.get("flight"), (int,float)) else "Unavailable")
with b2: st.metric("Hotel", f"₹{breakdown['hotel']:,.0f}" if isinstance(breakdown.get("hotel"), (int,float)) else "Unavailable")
with b3: st.metric("Activities", f"₹{breakdown.get('activities', 0):,.0f}")
with b4: st.metric("Food estimate", f"₹{breakdown.get('food_estimate', 0):,.0f}")
with b5: st.metric("Trip Budget", f"₹{budget_limit:,.0f}" if budget_limit else "Flexible")

st.markdown(
    '<div class="info-box">Food and local transport are transparent planning estimates and are not presented as live market pricing.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="glass-card"><strong>Travel information collected.</strong><br>WanderAI is ready to use these inputs for trip planning and optimization.</div>',
    unsafe_allow_html=True,
)


# Destination-independent day-wise exploration
itinerary = results.get("itinerary") or []
# Final UI safety gate: even if a stale session result or an unexpected model
# response reaches the page, never render a repeated/missing itinerary.
if itinerary:
    try:
        activity_options_for_itinerary = activities.get("options", []) if isinstance(activities, dict) else []
        itinerary = st.session_state.travel_agent._repair_itinerary(
            itinerary,
            max(1, int(nights) + 1),
            destination,
            activity_options_for_itinerary,
        )
        results["itinerary"] = itinerary
    except Exception:
        pass


# Adaptive re-planning: the user can refine the current trip without starting over.
st.markdown("## 🔄 Refine This Trip")
st.caption("Tell WanderAI what you want changed while keeping the rest of your trip intact.")

quick_cols = st.columns(4)
quick_prompts = [
    "Make the hotel cheaper",
    "Find a better hotel",
    "Add more beaches",
    "Make the trip more relaxing",
]
for col, prompt in zip(quick_cols, quick_prompts):
    with col:
        if st.button(prompt, use_container_width=True, key="quick_" + re.sub(r"[^a-z0-9]+", "_", prompt.lower())):
            st.session_state.replan_request = prompt

replan_request = st.text_input(
    "Trip refinement",
    value=st.session_state.get("replan_request", ""),
    placeholder="Example: make the hotel cheaper, add more beaches, or add 1 day",
)
replan_button = st.button("🔄 Re-plan My Trip", use_container_width=True)

if replan_button:
    if not replan_request.strip():
        st.warning("Tell WanderAI what you want to change first.")
    else:
        with st.spinner("WanderAI is adapting your trip..."):
            updated = st.session_state.travel_agent.replan(result, replan_request.strip())
        if updated.get("success"):
            st.session_state.travel_result = updated
            st.session_state.approval_state = "pending"
            st.session_state.approval_pdf = None
            st.session_state.approval_message = ""
            st.session_state.replan_request = ""
            st.rerun()
        else:
            st.warning(updated.get("error", "The trip could not be updated."))

st.markdown("## 🗺️ Your Day-by-Day Exploration")

if itinerary:
    for day in itinerary:
        day_num = html.escape(str(day.get("day", "")))
        title = html.escape(str(day.get("title") or f"Day {day_num}"))
        theme = html.escape(str(day.get("theme") or "Explore & Experience"))

        def render_items(items):
            rows=[]
            for item in items or []:
                name=html.escape(str(item.get("name") or "Explore"))
                desc=html.escape(str(item.get("description") or ""))
                rows.append(f"<div class='itinerary-item'><strong>{name}</strong><br><span>{desc}</span></div>")
            return "".join(rows) or "<div class='itinerary-item'>Free time / flexible exploration</div>"

        itinerary_image_items = []
        for slot in ("morning", "afternoon", "evening"):
            for plan_item in (day.get(slot) or []):
                if isinstance(plan_item, dict) and _safe_text(plan_item.get("name")):
                    itinerary_image_items.append({**plan_item, "category": slot.title()})
                    break
        media_block = ""

        st.markdown(
            f"""<div class="day-card">
<div class="day-card-header">
<div><div class="day-label">DAY {day_num}</div><h3>{title}</h3><div class="day-theme">{theme}</div></div>
<div class="day-badge">✨ EXPLORE</div>
</div>
{media_block}
<div class="day-grid">
<div class="day-section"><h4>☀️ Morning</h4>{render_items(day.get("morning"))}</div>
<div class="day-section"><h4>🌤️ Afternoon</h4>{render_items(day.get("afternoon"))}</div>
<div class="day-section"><h4>🌙 Evening</h4>{render_items(day.get("evening"))}</div>
</div>
<div class="day-footer">
<span>🍽️ <strong>Food:</strong> {html.escape(str(day.get("food") or "Local food experience"))}</span>
<span>💰 <strong>Day estimate:</strong> {html.escape(str(day.get("estimated_day_cost") or "Not specified"))}</span>
</div>
<div class="day-note">🚗 {html.escape(str(day.get("travel_note") or ""))}</div>
</div>""",
            unsafe_allow_html=True,
        )
        if itinerary_image_items:
            _render_browser_image_cards(itinerary_image_items, destination, "itinerary", max_items=3)
else:
    st.info("A day-wise itinerary could not be generated for this request.")
