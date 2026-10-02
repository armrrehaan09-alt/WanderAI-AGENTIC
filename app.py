import html
import json
import re
import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

from agent import TravelAgent
from pdf_utils import build_trip_pdf


def _safe_text(value):
    return str(value or "").strip()


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
    # Initial estimate only; the frame resizes itself to its content once images resolve.
    height = ((len(cards) + 2) // 3) * 340 + 24

    html_template = r"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:transparent}
body{font-family:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#0F2A3D;padding:4px 3px 12px;-webkit-font-smoothing:antialiased}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.card{display:flex;flex-direction:column;overflow:hidden;border-radius:18px;background:#fff;border:1px solid rgba(15,42,61,.08);box-shadow:0 1px 2px rgba(15,42,61,.04),0 8px 24px rgba(15,42,61,.06);transition:transform .2s ease,box-shadow .2s ease}
.card:hover{transform:translateY(-3px);box-shadow:0 2px 4px rgba(15,42,61,.05),0 16px 36px rgba(15,42,61,.12)}
.media{position:relative;aspect-ratio:16/10;overflow:hidden;background:#EEF3F2}
.photo{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease}
.card:hover .photo{transform:scale(1.04)}
.body{display:flex;flex-direction:column;gap:4px;flex:1;padding:14px 16px 15px}
.title{font-weight:700;font-size:15.5px;line-height:1.35;color:#0F2A3D;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sub{font-size:12.5px;color:#5B7083;line-height:1.4}
.details{font-size:12.5px;font-weight:600;color:#0F766E;margin-top:2px;line-height:1.45}
.source{font-size:10.5px;color:#8A9AA8;margin-top:auto;padding-top:10px;letter-spacing:.01em}
.status{grid-column:1/-1;padding:22px 18px;text-align:center;color:#5B7083;font-size:13px;border:1px dashed rgba(15,42,61,.16);border-radius:16px;background:rgba(255,255,255,.6)}
.skeleton .media,.sk-line{background:linear-gradient(90deg,#EEF3F2 0%,#F8FBFA 50%,#EEF3F2 100%);background-size:200% 100%;animation:shimmer 1.3s ease-in-out infinite}
.sk-line{height:11px;border-radius:6px;margin:5px 0}.sk-line.w70{width:70%}.sk-line.w40{width:40%}
.skeleton:hover{transform:none}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
@media(max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:540px){.grid{grid-template-columns:1fr}}
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
function renderCard(item,img){return `<article class="card"><div class="media"><img class="photo" src="${esc(img.url)}" alt="${esc(item.name)}" loading="lazy" referrerpolicy="no-referrer" onload="fit()" onerror="this.closest('.card').remove();fit()"></div><div class="body"><div class="title">${esc(item.name)}</div><div class="sub">${esc(item.subtitle)}</div>${item.details?`<div class="details">${esc(item.details)}</div>`:''}<div class="source">${esc(img.label)}</div></div></article>`;}
function skeleton(n){return Array.from({length:n},()=>'<div class="card skeleton"><div class="media"></div><div class="body"><div class="sk-line w70"></div><div class="sk-line w40"></div></div></div>').join('');}
// Same-origin srcdoc frame: size the host iframe to the real content to avoid empty gaps.
function fit(){try{const f=window.frameElement;if(!f)return;const g=document.getElementById('grid');const h=g.childElementCount?Math.ceil(g.getBoundingClientRect().bottom+14):0;f.style.height=h+'px';f.setAttribute('height',h);const host=f.closest('[data-testid="stElementContainer"],.element-container');if(host)host.style.display=h?'':'none';}catch(e){}}
async function main(){const grid=document.getElementById('grid');grid.innerHTML=skeleton(ITEMS.length);fit();const results=[];const usedUrls=new Set();const usedSources=new Set();for(const item of ITEMS){const img=await resolve(item,usedUrls,usedSources);if(img){usedUrls.add(img.url);if(img.sourceTitle)usedSources.add(norm(img.sourceTitle));results.push({item,img});}}if(!results.length){grid.innerHTML=(ITEMS[0]&&ITEMS[0].kind==='itinerary')?'':'<div class="status">No verified matching images were available from the connected image sources.</div>';fit();return;}grid.innerHTML=results.map(x=>renderCard(x.item,x.img)).join('');fit();}
if(window.ResizeObserver)new ResizeObserver(()=>fit()).observe(document.getElementById('grid'));
window.addEventListener('resize',fit);
main();
</script></body></html>"""
    html_out = html_template.replace("__PAYLOAD__", payload).replace("__DEST__", json.dumps(destination))
    components.html(html_out, height=height, scrolling=False)
    return len(cards)


st.set_page_config(page_title="WanderAI", page_icon="✈️", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root{
  --ink:#0F2A3D;--muted:#5B7083;--brand:#0F766E;--brand-deep:#0F4C5C;--accent:#E9A23B;
  --surface:#FFFFFF;--surface-soft:#F6F9F8;--line:rgba(15,42,61,.08);--line-strong:rgba(15,42,61,.14);
  --radius-lg:22px;--radius:16px;
  --shadow-sm:0 1px 2px rgba(15,42,61,.04),0 4px 14px rgba(15,42,61,.05);
  --shadow:0 2px 4px rgba(15,42,61,.04),0 14px 34px rgba(15,42,61,.08);
  --font-sans:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --font-display:'Playfair Display',Georgia,'Times New Roman',serif;
}
/* ---------- Base ---------- */
html,body,.stApp{font-family:var(--font-sans);-webkit-font-smoothing:antialiased}
.stApp{color:var(--ink);background:
  radial-gradient(1100px 520px at -5% -10%,rgba(233,162,59,.12),transparent 60%),
  radial-gradient(900px 520px at 105% 0%,rgba(15,118,110,.10),transparent 55%),#F7F6F2}
.stApp p,.stApp li,.stApp label,.stApp input,.stApp textarea,.stApp button{font-family:var(--font-sans)}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stDecoration"],footer{display:none}
.block-container{max-width:1180px;padding:2.25rem 1.5rem 5rem}
/* Style-only markdown blocks should not occupy layout space. */
[data-testid="stElementContainer"]:has(style),.element-container:has(style){display:none}
[data-testid="stHeaderActionElements"]{display:none}
.stApp [data-testid="stMarkdownContainer"] h2{font-family:var(--font-display);font-weight:700;font-size:1.7rem;line-height:1.25;letter-spacing:-.01em;color:var(--ink);margin:2.25rem 0 .2rem;padding:0 0 .65rem;border-bottom:1px solid var(--line)}
.stApp [data-testid="stMarkdownContainer"] h3{font-weight:700;font-size:1.12rem;color:var(--ink);margin:.4rem 0 0;padding:0}
.stApp [data-testid="stCaptionContainer"]{color:var(--muted);font-size:.9rem}
/* ---------- Hero ---------- */
.hero{position:relative;overflow:hidden;padding:2.6rem 2.75rem 2.4rem;border-radius:28px;margin-bottom:.75rem;color:#fff;
  background:linear-gradient(135deg,#0F4C5C 0%,#0F766E 58%,#14958A 100%);box-shadow:0 24px 60px rgba(15,76,92,.24)}
.hero::before{content:"";position:absolute;right:-140px;top:-160px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(233,162,59,.38),transparent 65%)}
.hero::after{content:"";position:absolute;left:-80px;bottom:-180px;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.10),transparent 65%)}
.hero>*{position:relative;z-index:1}
.hero-eyebrow{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;padding:.38rem .8rem;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22)}
.stApp .hero h1{font-family:var(--font-display);font-weight:700;font-size:3.2rem;line-height:1.08;letter-spacing:-.015em;color:#fff;margin:.9rem 0 .35rem;padding:0}
.stApp .hero .hero-lead{font-size:1.2rem;font-weight:600;color:rgba(255,255,255,.95);margin:0 0 .45rem}
.stApp .hero .hero-sub{max-width:720px;font-size:1rem;line-height:1.65;color:rgba(255,255,255,.80);margin:0}
.hero-chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.4rem}
.hero-chips span{font-size:.8rem;font-weight:600;padding:.42rem .85rem;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);color:#fff}
/* ---------- Surfaces ---------- */
.glass-card,.metric,.agent-card{background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow-sm)}
.glass-card{padding:1.15rem 1.35rem;border-radius:var(--radius);margin:.25rem 0 .75rem;line-height:1.6;color:var(--ink)}
.glass-card h3,.glass-card h4{color:var(--brand-deep)}
.approval-card{border-left:4px solid var(--accent)}
.metric{padding:1.05rem 1.2rem;border-radius:var(--radius)}
.metric-title{color:var(--muted);font-size:.7rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase}
.metric-value{color:var(--ink);font-size:1.3rem;font-weight:700;margin-top:.35rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.agent-card{display:flex;flex-wrap:wrap;gap:.5rem;padding:1rem 1.1rem;border-radius:var(--radius);margin:.25rem 0 .75rem}
.agent-step{display:inline-flex;align-items:center;gap:.45rem;padding:.42rem .85rem;border-radius:999px;background:#F1F7F6;border:1px solid rgba(15,118,110,.14);color:#1F4E5A;font-size:.84rem;font-weight:600}
.agent-step .tick{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;background:var(--brand);color:#fff;font-size:.65rem}
.live-pill,.partial-pill{display:inline-flex;align-items:center;gap:.35rem;padding:.38rem .85rem;border-radius:999px;font-weight:700;font-size:.76rem;letter-spacing:.02em}
.live-pill{background:#DDF5EF;color:#0F766E;border:1px solid rgba(15,118,110,.18)}
.partial-pill{background:#FFF1DB;color:#8A5A16;border:1px solid rgba(233,162,59,.30)}
.info-box,.warn-box{padding:.95rem 1.2rem;border-radius:14px;margin:.5rem 0 .75rem;font-size:.93rem;line-height:1.6}
.info-box{background:#EFF7F6;border:1px solid rgba(15,118,110,.14);border-left:4px solid var(--brand);color:#1F4E5A}
.warn-box{background:#FFF7EA;border:1px solid rgba(233,162,59,.28);border-left:4px solid var(--accent);color:#7A4E12}
/* ---------- Native widgets ---------- */
[data-testid="stMetric"]{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:1rem 1.15rem;box-shadow:var(--shadow-sm)}
[data-testid="stMetricLabel"] p{font-size:.7rem!important;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
[data-testid="stMetricValue"]{font-size:1.4rem;font-weight:700;color:var(--ink)}
[data-testid="stAlertContainer"]{border-radius:14px}
[data-baseweb="textarea"],[data-baseweb="input"]{background:#fff!important;border:1px solid var(--line-strong)!important;border-radius:14px!important;box-shadow:var(--shadow-sm);transition:border-color .15s ease,box-shadow .15s ease}
[data-baseweb="textarea"]:focus-within,[data-baseweb="input"]:focus-within{border-color:var(--brand)!important;box-shadow:0 0 0 3px rgba(15,118,110,.14)!important}
[data-testid="stTextArea"] textarea,[data-testid="stTextInput"] input{background:#fff!important;color:var(--ink)!important;caret-color:var(--brand)!important;font-size:.98rem!important;line-height:1.55!important;padding:.85rem 1rem!important}
[data-testid="stTextArea"] textarea::placeholder,[data-testid="stTextInput"] input::placeholder{color:#8A9AA8!important;opacity:1!important}
.stButton>button,.stDownloadButton>button{font-family:var(--font-sans);font-weight:600;font-size:.95rem;min-height:2.85rem;padding:.6rem 1.1rem;border-radius:12px;transition:transform .15s ease,box-shadow .15s ease,background .15s ease,border-color .15s ease,color .15s ease}
.stButton>button[kind="primary"],.stDownloadButton>button[kind="primary"]{background:linear-gradient(135deg,#0F766E 0%,#0F4C5C 100%);color:#fff;border:0;box-shadow:0 8px 20px rgba(15,118,110,.22)}
.stButton>button[kind="primary"]:hover,.stDownloadButton>button[kind="primary"]:hover{transform:translateY(-1px);box-shadow:0 12px 26px rgba(15,118,110,.30);color:#fff}
.stButton>button[kind="primary"]:focus,.stButton>button[kind="primary"]:active,.stDownloadButton>button[kind="primary"]:focus,.stDownloadButton>button[kind="primary"]:active{color:#fff!important}
.stButton>button[kind="secondary"],.stDownloadButton>button[kind="secondary"]{background:var(--surface);color:var(--ink);border:1px solid var(--line-strong);box-shadow:var(--shadow-sm)}
.stButton>button[kind="secondary"]:hover,.stDownloadButton>button[kind="secondary"]:hover{border-color:var(--brand);color:var(--brand);background:#F1F8F7}
.stButton>button:focus-visible,.stDownloadButton>button:focus-visible{outline:3px solid rgba(15,118,110,.35);outline-offset:2px}
/* ---------- Weather ---------- */
.forecast-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(138px,1fr));gap:.75rem;margin:.9rem 0 .25rem}
.forecast-tile{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:.85rem .95rem;box-shadow:var(--shadow-sm)}
.forecast-date{font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.forecast-temp{font-size:1.05rem;font-weight:700;color:var(--ink);margin:.3rem 0 .15rem}
.forecast-temp span{color:var(--muted);font-weight:500}
.forecast-rain{font-size:.8rem;color:#2C6E8F}
/* ---------- Itinerary ---------- */
.day-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);padding:1.5rem 1.6rem 1.25rem;margin:1.1rem 0 .5rem;box-shadow:var(--shadow)}
.day-card-header{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:1.1rem}
.day-label{font-size:.7rem;font-weight:800;letter-spacing:.16em;color:var(--brand)}
.stApp .day-card h3{font-family:var(--font-display);font-size:1.55rem;font-weight:700;line-height:1.25;color:var(--ink);margin:.3rem 0 .15rem;padding:0}
.day-theme{color:var(--muted);font-size:.93rem}
.day-badge{white-space:nowrap;background:#FFF4E2;color:#9A5B0B;border:1px solid rgba(233,162,59,.35);border-radius:999px;padding:.35rem .8rem;font-size:.68rem;font-weight:800;letter-spacing:.08em}
.day-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem}
.day-section{background:var(--surface-soft);border:1px solid var(--line);border-radius:var(--radius);padding:1rem 1.05rem .6rem}
.stApp .day-section h4{margin:0 0 .35rem;padding:0;font-size:.76rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--brand-deep)}
.itinerary-item{padding:.6rem 0;border-bottom:1px dashed rgba(15,42,61,.10);font-size:.93rem;line-height:1.45;color:var(--ink)}
.itinerary-item:last-child{border-bottom:0}
.itinerary-item span{color:var(--muted);font-size:.85rem}
.day-footer{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;margin-top:1rem;padding-top:.9rem;border-top:1px solid var(--line);font-size:.9rem;color:var(--ink)}
.day-note{margin-top:.5rem;color:var(--muted);font-size:.85rem}
/* ---------- Responsive ---------- */
@media(max-width:900px){.day-grid{grid-template-columns:1fr}}
@media(max-width:640px){
  .block-container{padding:1.25rem .9rem 4rem}
  .hero{padding:1.8rem 1.4rem;border-radius:22px}
  .stApp .hero h1{font-size:2.3rem}
  .day-card{padding:1.15rem}
  .day-card-header{flex-direction:column}
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
<span class="hero-eyebrow">AI Travel Concierge</span>
<h1>WanderAI</h1>
<p class="hero-lead">Your AI-Powered Travel Agent</p>
<p class="hero-sub">Describe your trip naturally. WanderAI resolves the destination, checks connected live travel sources and prepares the information needed for planning.</p>
<div class="hero-chips"><span>🌦️ Live weather</span><span>✈️ Flights &amp; stays</span><span>🗺️ Day-by-day itinerary</span><span>📄 Approved PDF export</span></div>
</div>
""",
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

create_plan = st.button("✨ Create My Travel Plan", use_container_width=True, type="primary")

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
                "".join(f'<div class="agent-step"><span class="tick">✓</span>{html.escape(item)}</div>' for item in shown) +
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
        f'<div class="agent-step"><span class="tick">✓</span>{html.escape(step)}</div>' for step in steps
    ) + "</div>",
    unsafe_allow_html=True,
)

if result.get("live_sources"):
    st.markdown(
        f'<span class="live-pill">● LIVE DATA: {html.escape(", ".join(map(str, result["live_sources"])))}</span>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<span class="partial-pill">● Some live travel sources still need to be connected</span>',
        unsafe_allow_html=True,
    )

# Weather
weather = results.get("weather") or {}
if weather.get("available"):
    st.markdown("## 🌦️ Current Weather & Forecast")
    current = weather.get("current", {})
    a, b, c = st.columns(3)
    with a: st.metric("Temperature", f"{current.get('temperature_2m', '—')} °C")
    with b: st.metric("Feels Like", f"{current.get('apparent_temperature', '—')} °C")
    with c: st.metric("Wind", f"{current.get('wind_speed_10m', '—')} km/h")
    tiles = []
    for row in weather.get("daily", [])[:min(7, nights + 2)]:
        raw_date = str(row.get("date", ""))
        try:
            label = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%a, %d %b")
        except ValueError:
            label = raw_date
        tiles.append(
            f'<div class="forecast-tile"><div class="forecast-date">{html.escape(label)}</div>'
            f'<div class="forecast-temp">{html.escape(str(row.get("high", "—")))}° '
            f'<span>/ {html.escape(str(row.get("low", "—")))}°</span></div>'
            f'<div class="forecast-rain">💧 {html.escape(str(row.get("rain_probability", "—")))}% rain</div></div>'
        )
    if tiles:
        st.markdown(f'<div class="forecast-grid">{"".join(tiles)}</div>', unsafe_allow_html=True)

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
    label_visibility="collapsed",
)
replan_button = st.button("🔄 Re-plan My Trip", use_container_width=True, type="primary")

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
        travel_note = _safe_text(day.get("travel_note"))
        note_block = f'<div class="day-note">🚗 {html.escape(travel_note)}</div>' if travel_note else ""

        st.markdown(
            f"""<div class="day-card">
<div class="day-card-header">
<div><div class="day-label">DAY {day_num}</div><h3>{title}</h3><div class="day-theme">{theme}</div></div>
<div class="day-badge">✨ EXPLORE</div>
</div>
<div class="day-grid">
<div class="day-section"><h4>☀️ Morning</h4>{render_items(day.get("morning"))}</div>
<div class="day-section"><h4>🌤️ Afternoon</h4>{render_items(day.get("afternoon"))}</div>
<div class="day-section"><h4>🌙 Evening</h4>{render_items(day.get("evening"))}</div>
</div>
<div class="day-footer">
<span>🍽️ <strong>Food:</strong> {html.escape(str(day.get("food") or "Local food experience"))}</span>
<span>💰 <strong>Day estimate:</strong> {html.escape(str(day.get("estimated_day_cost") or "Not specified"))}</span>
</div>{note_block}
</div>""",
            unsafe_allow_html=True,
        )
        if itinerary_image_items:
            _render_browser_image_cards(itinerary_image_items, destination, "itinerary", max_items=3)
else:
    st.info("A day-wise itinerary could not be generated for this request.")

# ---------------------------------------------------------------------------
# HUMAN-IN-THE-LOOP APPROVAL
# The agent prepares the plan first. PDF export is blocked until the human
# explicitly approves the current plan. A rejection sends the user to the
# existing re-planning flow, and any revised plan requires approval again.
# ---------------------------------------------------------------------------
approval_state = st.session_state.get("approval_state", "pending")
st.markdown("## 👤 Human Approval")
if approval_state in ("pending", "pdf_error"):
    if approval_state == "pdf_error":
        st.error(st.session_state.get("approval_message") or "The PDF could not be generated.")
    st.markdown(
        f"""<div class="glass-card approval-card"><strong>WanderAI has prepared your trip.</strong><br>
        Destination: <strong>{html.escape(str(destination))}</strong> ·
        {html.escape(str(nights + 1))} days / {html.escape(str(nights))} nights.<br>
        Review the plan above. <strong>The PDF will only be enabled after you approve it.</strong></div>""",
        unsafe_allow_html=True,
    )
    approve_col, change_col = st.columns(2)
    with approve_col:
        approve_clicked = st.button("✅ Yes, approve this trip", use_container_width=True, key="approve_trip", type="primary")
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
        st.session_state.approval_message = "Use “Refine This Trip” above to tell WanderAI what you want changed, then approve the revised plan."
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
            type="primary",
        )
elif approval_state == "changes_requested":
    st.info(st.session_state.get("approval_message") or "Tell WanderAI what you want changed.")
