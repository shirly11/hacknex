import os
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Ensure output directory
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_docs"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_chart_1():
    """Generates Production Efficiency Chart (Q1-Q4)"""
    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=150)
    quarters = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']
    efficiency = [78.5, 72.4, 84.1, 91.8] # Q2 dip, Q4 peak
    scrap_rate = [4.2, 7.8, 3.1, 1.9]

    x = np.arange(len(quarters))
    width = 0.35

    rects1 = ax.bar(x - width/2, efficiency, width, label='Efficiency (%)', color='#3b82f6')
    ax2 = ax.twinx()
    rects2 = ax2.plot(x + width/2, scrap_rate, label='Scrap Rate (%)', color='#ef4444', marker='o', linewidth=2.5)

    ax.set_ylabel('Efficiency (%)', color='#3b82f6', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Scrap Rate (%)', color='#ef4444', fontsize=10, fontweight='bold')
    ax.set_title('Plant Alpha: Quarterly Efficiency vs Scrap Rate (2025)', fontsize=11, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontweight='bold')
    ax.set_ylim(50, 100)
    ax2.set_ylim(0, 10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Annotations on Q2 and Q4
    ax.annotate('Tooling Defect\n(Efficiency: 72.4%)', xy=(1 - width/2, 72.4), xytext=(0.5, 60),
                arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=6),
                fontsize=8, color='#dc2626', fontweight='bold')
    ax.annotate('Automated AI Line\n(Efficiency: 91.8%)', xy=(3 - width/2, 91.8), xytext=(2.2, 94),
                arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6),
                fontsize=8, color='#059669', fontweight='bold')

    plt.tight_layout()
    chart_path = os.path.join(OUTPUT_DIR, "chart_q2_q4.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def create_chart_2():
    """Generates Energy Consumption Chart for Energy Whitepaper"""
    fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
    categories = ['Solar Grid', 'Wind Turbines', 'Hydroelectric', 'Thermal Backup']
    share_2024 = [30, 25, 35, 10]
    share_2025 = [42, 30, 23, 5]

    x = np.arange(len(categories))
    width = 0.35

    ax.bar(x - width/2, share_2024, width, label='2024 Energy Share (%)', color='#94a3b8')
    ax.bar(x + width/2, share_2025, width, label='2025 Energy Share (%)', color='#10b981')

    ax.set_ylabel('Percentage Share (%)', fontsize=10, fontweight='bold')
    ax.set_title('Regional Clean Energy Transition (2024 vs 2025)', fontsize=11, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.legend(loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    chart_path = os.path.join(OUTPUT_DIR, "chart_energy.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def build_q2_vs_q4_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "Q2_vs_Q4_Manufacturing_Report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor('#1e293b'), spaceAfter=12)
    heading_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#2563eb'), spaceBefore=14, spaceAfter=8)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#334155'), spaceAfter=8)
    callout_style = ParagraphStyle('Callout', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#1e40af'), backColor=colors.HexColor('#eff6ff'), borderPadding=8, spaceAfter=10)

    elements = []

    # Page 1: Executive Summary & Text Reasons
    elements.append(Paragraph("Global Operations Performance & Production Efficiency Report 2025", title_style))
    elements.append(Paragraph("<b>Document Ref:</b> MFG-2025-Q4-VAL | <b>Classification:</b> Confidential Operations Intelligence", body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. Executive Summary & Production Comparison", heading_style))
    elements.append(Paragraph(
        "This report provides a comprehensive analysis of Plant Alpha manufacturing throughput during fiscal year 2025. "
        "Notably, overall production efficiency experienced a dramatic rebound from a low of <b>72.4% in Q2 2025</b> to a record peak of <b>91.8% in Q4 2025</b>, "
        "representing a net efficiency gain of <b>+19.4 percentage points (+26.8% relative improvement)</b>.", body_style))

    elements.append(Paragraph("2. Three Primary Drivers of Q2 to Q4 Efficiency Transformation", heading_style))
    elements.append(Paragraph(
        "<b>Reason 1: Resolution of Conveyor Tooling Defect (Page 1, Section 2.1)</b><br/>"
        "In Q2 2025, Line B suffered from severe mechanical friction and thermal overheating caused by degraded conveyor bearings. "
        "This led to 142 hours of unscheduled downtime and inflated scrap rates to 7.8%. In Q3, all bearings were replaced with ceramic dynamic bearings.", body_style))

    elements.append(Paragraph(
        "<b>Reason 2: Implementation of Vision AI Quality Inspection (Page 1, Section 2.2)</b><br/>"
        "Manual inspection bottlenecks in Q2 delayed unit approval by an average of 4.2 minutes per batch. "
        "The deployment of automated Vision AI cameras in August reduced batch inspection latency to 0.4 minutes and reduced defect escapes by 82%.", body_style))

    elements.append(Paragraph(
        "<b>Reason 3: Shift Optimization and Predictive Maintenance Schedule (Page 1, Section 2.3)</b><br/>"
        "Real-time sensor monitoring was deployed across all CNC modules in early Q4, eliminating emergency shutdowns and optimizing shift handovers.", body_style))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Table 1: Quarterly Manufacturing KPI Breakdown</b>", ParagraphStyle('TableTitle', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.HexColor('#0f172a'), spaceAfter=4)))

    table_data = [
        ['Metric / Quarter', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'YoY Delta'],
        ['Production Efficiency (%)', '78.5%', '72.4%', '84.1%', '91.8%', '+13.3%'],
        ['Unscheduled Downtime (hrs)', '68 hrs', '142 hrs', '45 hrs', '12 hrs', '-56 hrs'],
        ['Scrap Rate (%)', '4.2%', '7.8%', '3.1%', '1.9%', '-2.3%'],
        ['Units Produced (k units)', '124.5k', '110.2k', '138.9k', '156.4k', '+31.9k'],
        ['Maintenance Cost ($k)', '$320k', '$540k', '$280k', '$190k', '-$130k']
    ]

    t = Table(table_data, colWidths=[1.8*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f1f5f9')])
    ]))
    elements.append(t)

    # Page 2: Visual Chart & Detailed Math Proof
    elements.append(PageBreak())
    elements.append(Paragraph("3. Visual Performance Trends & Evidence Analysis", heading_style))
    elements.append(Paragraph("The chart below illustrates the inverse correlation between production efficiency and scrap rate across 2025.", body_style))

    chart1_img = create_chart_1()
    elements.append(RLImage(chart1_img, width=5.8*inch, height=3.1*inch))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("4. Mathematical Proof & Audit Trail", heading_style))
    elements.append(Paragraph(
        "<b>Mathematical Formula:</b><br/>"
        "Efficiency Rebound = Efficiency(Q4) - Efficiency(Q2) = 91.8% - 72.4% = <b>+19.4%</b><br/>"
        "Relative Efficiency Increase = (19.4 / 72.4) * 100 = <b>26.79%</b><br/>"
        "Downtime Reduction = Downtime(Q2) - Downtime(Q4) = 142 hrs - 12 hrs = <b>130 hrs saved (91.5% decrease)</b>.", callout_style))

    doc.build(elements)
    print(f"Generated {pdf_path}")

def build_financial_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "TechCorp_Financial_Statements_2025.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#0f172a'), spaceAfter=12)
    heading_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=13, leading=16, textColor=colors.HexColor('#0d9488'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#334155'), spaceAfter=8)

    elements = []
    elements.append(Paragraph("TechCorp Systems Inc. - Annual Financial & R&D Report 2025", title_style))
    elements.append(Paragraph("<b>Document Ref:</b> FIN-2025-SEC10K | <b>Reporting Period:</b> Jan 1, 2025 - Dec 31, 2025", body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. Revenue & Operations Overview", heading_style))
    elements.append(Paragraph(
        "TechCorp achieved consolidated revenue of $485.2M in FY2025, representing a 22.4% year-over-year increase. "
        "Growth was driven primarily by Cloud AI Services and Enterprise Automation hardware.", body_style))

    table_data = [
        ['Segment', 'FY2024 Revenue ($M)', 'FY2025 Revenue ($M)', 'YoY Growth (%)', 'Gross Margin (%)'],
        ['Cloud AI Services', '$120.4M', '$185.6M', '+54.2%', '78.5%'],
        ['Enterprise Hardware', '$150.0M', '$168.2M', '+12.1%', '42.0%'],
        ['Software Licenses', '$95.6M', '$98.4M', '+2.9%', '89.2%'],
        ['Professional Support', '$30.8M', '$33.0M', '+7.1%', '35.4%'],
        ['Total Consolidated', '$396.8M', '$485.2M', '+22.3%', '62.8%']
    ]

    t = Table(table_data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 1.1*inch, 1.1*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0fdf4')])
    ]))
    elements.append(t)
    doc.build(elements)
    print(f"Generated {pdf_path}")

def build_scanned_messy_pdf():
    """Builds a simulated scanned, noisy, rotated/low quality PDF document"""
    pdf_path = os.path.join(OUTPUT_DIR, "Scanned_SupplyChain_Audit_Messy.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#451a03'), spaceAfter=10)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#78350f'), spaceAfter=6)

    elements = []
    elements.append(Paragraph("[SCANNED COPY - STAMPED APPROVED]", title_style))
    elements.append(Paragraph("Supplier Logistics Lead Time & Defect Rate Audit - Region East", body_style))
    elements.append(Spacer(1, 10))

    table_data = [
        ['Supplier ID', 'Component', 'Avg Lead Time (Days)', 'Defect Rate (PPM)', 'Audit Rating'],
        ['SUP-801', 'Semiconductor Chips', '42.5 days', '450 PPM', 'WARNING'],
        ['SUP-402', 'High-Temp Capacitors', '18.2 days', '120 PPM', 'PASS'],
        ['SUP-109', 'Lithium Battery Cells', '65.0 days', '1250 PPM', 'FAIL'],
        ['SUP-330', 'Aluminum Enclosures', '12.0 days', '45 PPM', 'OPTIMAL']
    ]

    t = Table(table_data, colWidths=[1.2*inch, 1.8*inch, 1.4*inch, 1.2*inch, 0.9*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#9a3412')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#fed7aa')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#fff7ed'))
    ]))
    elements.append(t)
    doc.build(elements)
    print(f"Generated {pdf_path}")

def build_energy_whitepaper_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "Global_Energy_Transition_Whitepaper.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#065f46'), spaceAfter=12)
    heading_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=13, leading=16, textColor=colors.HexColor('#047857'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#334155'), spaceAfter=8)

    elements = []
    elements.append(Paragraph("Global Energy Transition & Regional Efficiency Benchmarks", title_style))
    elements.append(Paragraph("<b>Author:</b> Sustainable Energy Institute | <b>Publication:</b> Q4 2025 Special Edition", body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. Regional Clean Energy Mix Shift", heading_style))
    elements.append(Paragraph("In 2025, regional grid adoption of solar power increased from 30% to 42%, while thermal backup reliance dropped from 10% to 5%.", body_style))

    chart_img = create_chart_2()
    elements.append(RLImage(chart_img, width=5.5*inch, height=2.7*inch))

    doc.build(elements)
    print(f"Generated {pdf_path}")

if __name__ == "__main__":
    build_q2_vs_q4_pdf()
    build_financial_pdf()
    build_scanned_messy_pdf()
    build_energy_whitepaper_pdf()
    print("All sample dataset PDFs successfully generated!")
