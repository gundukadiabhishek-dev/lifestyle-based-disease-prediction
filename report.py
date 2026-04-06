from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4


def generate_pdf(user_data, risk, timeframe, disease_probs, advice):

    # Better margins
    doc = SimpleDocTemplate(
        "health_report.pdf",
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    content = []

    # ================================
    # 🎨 CLEAN STYLES (TIMES FONT)
    # ================================
    title_style = ParagraphStyle(
        name="Title",
        fontName="Times-Bold",
        fontSize=22,
        alignment=1,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        name="Subtitle",
        fontName="Times-Roman",
        fontSize=10,
        alignment=1,
        textColor=colors.grey,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        name="Section",
        fontName="Times-Bold",
        fontSize=14,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        name="Normal",
        fontName="Times-Roman",
        fontSize=11,
        leading=16,   # 🔥 fixes line spacing
        spaceAfter=6
    )

    # ================================
    # 🏥 HEADER
    # ================================
    content.append(Paragraph("AI HEALTH REPORT", title_style))
    content.append(Paragraph("Preventive Health Analysis System", subtitle_style))

    content.append(HRFlowable(width="100%", thickness=1.5, color=colors.grey))
    content.append(Spacer(1, 12))

    # ================================
    # 🔥 RISK COLOR
    # ================================
    if risk > 0.7:
        risk_color = colors.red
        risk_label = "HIGH RISK"
    elif risk > 0.4:
        risk_color = colors.orange
        risk_label = "MODERATE RISK"
    else:
        risk_color = colors.green
        risk_label = "LOW RISK"

    # ================================
    # 📊 SUMMARY
    # ================================
    content.append(Paragraph("Overall Health Summary", section_style))

    risk_data = [
        ["Metric", "Value"],
        ["Risk Score", f"{risk*100:.2f}%"],
        ["Risk Level", risk_label],
        ["Timeframe", timeframe]
    ]

    risk_table = Table(risk_data, colWidths=[200, 200], hAlign='LEFT')

    risk_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("BACKGROUND", (1, 2), (1, 2), risk_color),
        ("TEXTCOLOR", (1, 2), (1, 2), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    content.append(risk_table)
    content.append(Spacer(1, 15))

    # ================================
    # 🦠 DISEASES
    # ================================
    content.append(Paragraph("Disease Risk Breakdown", section_style))

    disease_data = [["Disease", "Risk (%)"]]

    for d, val in disease_probs.items():
        disease_data.append([d, f"{val*100:.2f}%"])

    disease_table = Table(disease_data, colWidths=[200, 200], hAlign='LEFT')

    disease_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    content.append(disease_table)
    content.append(Spacer(1, 15))

    # ================================
    # 🧍 USER DATA
    # ================================
    content.append(Paragraph("Patient Health Data", section_style))

    for key, value in user_data.items():
        content.append(Paragraph(f"<b>{key}:</b> {value}", normal_style))

    content.append(Spacer(1, 10))

    # ================================
    # 💡 GUIDANCE
    # ================================
    content.append(Paragraph("Doctor Recommendations", section_style))

    for a in advice:
        content.append(Paragraph(f"• {a}", normal_style))

    content.append(Spacer(1, 10))

    # ================================
    # 📌 FOOTER
    # ================================
    content.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    content.append(Spacer(1, 6))

    content.append(Paragraph(
        "<i>This report is AI-generated for preventive guidance only. "
        "Consult a certified medical professional for diagnosis.</i>",
        subtitle_style
    ))

    content.append(Paragraph(
        "Generated by Lifestyle Disease Prediction System",
        subtitle_style
    ))

    # ================================
    # BUILD
    # ================================
    doc.build(content)

    return "health_report.pdf"