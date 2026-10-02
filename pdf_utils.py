from io import BytesIO
from html import escape


def _text(value, default="—"):
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _money(value):
    if isinstance(value, (int, float)):
        return f"INR {value:,.0f}"
    return _text(value, "Unavailable")


def _paragraph(text, style):
    from reportlab.platypus import Paragraph
    return Paragraph(escape(_text(text)).replace("\n", "<br/>"), style)


def build_trip_pdf(result):
    """Build a self-contained human-approved WanderAI trip summary PDF."""
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
        KeepTogether,
    )

    if not isinstance(result, dict) or not result.get("success"):
        raise ValueError("A successful trip result is required to create the PDF.")

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="WanderAI Trip Summary",
        author="WanderAI",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "WanderTitle", parent=styles["Title"], fontSize=23, leading=28,
        alignment=TA_CENTER, spaceAfter=7, textColor=colors.HexColor("#155E75"),
    )
    subtitle = ParagraphStyle(
        "WanderSubtitle", parent=styles["Normal"], fontSize=10, leading=14,
        alignment=TA_CENTER, textColor=colors.HexColor("#52606D"), spaceAfter=16,
    )
    h1 = ParagraphStyle(
        "WanderH1", parent=styles["Heading1"], fontSize=15, leading=19,
        spaceBefore=12, spaceAfter=8, textColor=colors.HexColor("#0F766E"),
    )
    h2 = ParagraphStyle(
        "WanderH2", parent=styles["Heading2"], fontSize=11.5, leading=15,
        spaceBefore=7, spaceAfter=5, textColor=colors.HexColor("#155E75"),
    )
    body = ParagraphStyle(
        "WanderBody", parent=styles["BodyText"], fontSize=9.2, leading=13,
        textColor=colors.HexColor("#243B53"), spaceAfter=4,
    )
    small = ParagraphStyle(
        "WanderSmall", parent=body, fontSize=8, leading=11,
        textColor=colors.HexColor("#627D98"),
    )
    day_style = ParagraphStyle(
        "WanderDay", parent=h2, fontSize=12.5, leading=16,
        textColor=colors.HexColor("#0F766E"),
    )

    story = []
    destination = _text(result.get("destination"))
    location = result.get("location") or {}
    country = _text(location.get("country"), "")
    nights = result.get("nights")
    days = (int(nights) + 1) if isinstance(nights, int) else None
    budget_limit = result.get("budget_limit")
    results = result.get("results") or {}

    story.append(Paragraph("WanderAI", title))
    story.append(Paragraph("Human-Approved AI Travel Plan", subtitle))
    story.append(Paragraph(escape(destination), title))
    story.append(Spacer(1, 3 * mm))

    overview = [
        ["Destination", destination],
        ["Country", country or "Not specified"],
        ["Duration", f"{days} days / {nights} nights" if days else f"{nights} nights"],
        ["Budget limit", _money(budget_limit) if budget_limit else "Flexible"],
        ["Approval", "Approved by user"],
    ]
    table = Table(overview, colWidths=[42 * mm, 135 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E6FFFA")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#243B53")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C7D1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Paragraph("This PDF was generated only after human approval inside WanderAI.", small))

    # Weather
    weather = results.get("weather") or {}
    if weather.get("available"):
        story.append(Paragraph("Weather", h1))
        current = weather.get("current") or {}
        story.append(_paragraph(
            f"Current: {_text(current.get('temperature_2m'), '—')} C | "
            f"Feels like: {_text(current.get('apparent_temperature'), '—')} C | "
            f"Wind: {_text(current.get('wind_speed_10m'), '—')} km/h",
            body,
        ))

    # Travel options
    flight = results.get("flight") or {}
    hotel = results.get("hotel") or {}
    activities = results.get("activities") or {}
    food = results.get("food") or {}

    def add_options(title_text, data, fields):
        options = data.get("options") if isinstance(data, dict) else None
        if not options:
            return
        story.append(Paragraph(title_text, h1))
        rows = [[_text(label) for _, label in fields]]
        for item in options[:8]:
            row = []
            for key, _label in fields:
                value = item.get(key, "") if isinstance(item, dict) else ""
                if key in {"price", "price_per_night", "cost"}:
                    value = _money(value)
                row.append(_text(value, "—"))
            rows.append(row)
        widths = [177 * mm / max(1, len(fields))] * len(fields)
        t = Table(rows, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#155E75")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.7),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#C4CDD5")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5FAFC")]),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t)

    add_options("Flight Options", flight, [("airline", "Airline"), ("route", "Route"), ("price", "Price")])
    add_options("Accommodation Options", hotel, [("name", "Stay"), ("area", "Area"), ("price_per_night", "Per night")])
    add_options("Recommended Attractions", activities, [("name", "Place"), ("category", "Category"), ("cost", "Cost")])
    add_options("Local Food", food, [("name", "Dish"), ("category", "Category"), ("cost", "Cost")])

    budget = results.get("budget") or {}
    breakdown = budget.get("breakdown") or {}
    if breakdown:
        story.append(Paragraph("Budget Breakdown", h1))
        budget_rows = [["Component", "Estimated amount"]]
        labels = [
            ("flight", "Flight"), ("hotel", "Accommodation"),
            ("activities", "Activities"), ("food_estimate", "Food"),
            ("local_transport", "Local transport"),
        ]
        for key, label in labels:
            if key in breakdown:
                budget_rows.append([label, _money(breakdown.get(key))])
        if budget.get("estimated_total") is not None:
            budget_rows.append(["Estimated total", _money(budget.get("estimated_total"))])
        t = Table(budget_rows, colWidths=[90 * mm, 87 * mm], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#C4CDD5")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F5FAFC")]),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E6FFFA")),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t)

    # Day-by-day itinerary
    itinerary = results.get("itinerary") or []
    if itinerary:
        story.append(Paragraph("Day-by-Day Itinerary", h1))
        for day in itinerary:
            number = _text(day.get("day"), "")
            day_title = _text(day.get("title"), f"Day {number}")
            theme = _text(day.get("theme"), "Explore & Experience")
            block = [Paragraph(f"Day {number}: {escape(day_title)}", day_style)]
            block.append(_paragraph(f"Theme: {theme}", small))
            for slot, label in (("morning", "Morning"), ("afternoon", "Afternoon"), ("evening", "Evening")):
                items = day.get(slot) or []
                if not items:
                    continue
                block.append(Paragraph(label, h2))
                for item in items:
                    if isinstance(item, dict):
                        name = _text(item.get("name"), "Explore")
                        desc = _text(item.get("description"), "")
                        block.append(_paragraph(f"{name}: {desc}", body))
                    else:
                        block.append(_paragraph(str(item), body))
            block.append(_paragraph(f"Food: {_text(day.get('food'), 'Local food experience')}", small))
            block.append(_paragraph(f"Travel note: {_text(day.get('travel_note'), 'Plan local transfers between activities.')}", small))
            story.append(KeepTogether(block))
            story.append(Spacer(1, 3 * mm))

    tips = result.get("tips") or []
    if tips:
        story.append(Paragraph("Travel Tips", h1))
        for tip in tips[:10]:
            story.append(_paragraph("• " + str(tip), body))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "WanderAI planning note: prices or availability marked as planning data are estimates, not guaranteed live inventory.",
        small,
    ))

    doc.build(story)
    return buffer.getvalue()
