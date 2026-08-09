"""Build the one-page CV distributed with the portfolio site."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "marcell_molnar_cv.pdf"

NAVY = colors.HexColor("#172033")
BLUE = colors.HexColor("#2563EB")
MUTED = colors.HexColor("#667085")
LIGHT = colors.HexColor("#D9E1EC")
GOLD = colors.HexColor("#B8862D")


def register_fonts() -> tuple[str, str]:
    regular = Path(r"C:\Windows\Fonts\arial.ttf")
    bold = Path(r"C:\Windows\Fonts\arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("CVRegular", regular))
        pdfmetrics.registerFont(TTFont("CVBold", bold))
        return "CVRegular", "CVBold"
    return "Helvetica", "Helvetica-Bold"


REGULAR, BOLD = register_fonts()


def style(name: str, size: float, leading: float, color=NAVY, bold=False, align=TA_LEFT):
    return ParagraphStyle(
        name,
        fontName=BOLD if bold else REGULAR,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
    )


BODY = style("body", 7.7, 9.7)
SMALL = style("small", 7.2, 9.1, MUTED)
META = style("meta", 7.3, 9.2, BLUE, bold=True)
TITLE = style("title", 9.2, 11.1, bold=True)
RIGHT_TITLE = style("right-title", 8.7, 10.5, bold=True)


def paragraph(c: canvas.Canvas, text: str, x: float, y: float, width: float, pstyle) -> float:
    item = Paragraph(text, pstyle)
    _, height = item.wrap(width, 200 * mm)
    item.drawOn(c, x, y - height)
    return y - height


def section(c: canvas.Canvas, label: str, x: float, y: float, width: float) -> float:
    c.setFont(BOLD, 8.2)
    c.setFillColor(BLUE)
    c.drawString(x, y, label.upper())
    label_width = pdfmetrics.stringWidth(label.upper(), BOLD, 8.2)
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.65)
    c.line(x + label_width + 8, y + 2.2, x + width, y + 2.2)
    return y - 14


def bullet_list(c: canvas.Canvas, bullets: list[str], x: float, y: float, width: float) -> float:
    for text in bullets:
        y = paragraph(c, f"<font color='#2563EB'>-</font> {text}", x + 4, y, width - 4, BODY)
        y -= 1.5
    return y


def entry(
    c: canvas.Canvas,
    title: str,
    meta: str,
    bullets: list[str],
    x: float,
    y: float,
    width: float,
) -> float:
    y = paragraph(c, title, x, y, width, TITLE)
    y = paragraph(c, meta, x, y - 1, width, META)
    y = bullet_list(c, bullets, x, y - 3, width)
    return y - 5


def compact_entry(
    c: canvas.Canvas,
    title: str,
    text: str,
    x: float,
    y: float,
    width: float,
) -> float:
    y = paragraph(c, title, x, y, width, RIGHT_TITLE)
    y = paragraph(c, text, x, y - 1, width, SMALL)
    return y - 7


def build() -> None:
    page_width, page_height = A4
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("Marcell Molnár - CV")
    c.setAuthor("Marcell Molnár")
    c.setSubject("Quantitative finance, model validation, statistics, and machine learning")

    margin = 38
    left_x = margin
    left_w = 314
    right_x = 379
    right_w = page_width - right_x - margin

    # Header
    c.setFillColor(NAVY)
    c.setFont(BOLD, 24)
    c.drawString(margin, page_height - 51, "Marcell Molnár")
    c.setFont(REGULAR, 9.4)
    c.setFillColor(MUTED)
    c.drawString(margin, page_height - 69, "Quantitative Model Validator | Statistical & ML Research")

    contact_y = page_height - 43
    contacts = [
        ("+36 70 281 2610", None),
        ("marcellmolnar005@gmail.com", "mailto:marcellmolnar005@gmail.com"),
        ("LinkedIn", "https://www.linkedin.com/in/marcell-moln%C3%A1r-b77717249/"),
        ("momarci13.github.io", "https://momarci13.github.io/"),
    ]
    c.setFont(REGULAR, 7.5)
    for label, url in contacts:
        label_width = pdfmetrics.stringWidth(label, REGULAR, 7.5)
        x = page_width - margin - label_width
        c.setFillColor(BLUE if url else NAVY)
        c.drawString(x, contact_y, label)
        if url:
            c.linkURL(url, (x, contact_y - 1, x + label_width, contact_y + 8), relative=0)
        contact_y -= 11

    c.setStrokeColor(BLUE)
    c.setLineWidth(1.1)
    c.line(margin, page_height - 82, page_width - margin, page_height - 82)

    # Left column
    y = page_height - 104
    y = section(c, "Experience", left_x, y, left_w)
    y = entry(
        c,
        "Model Validator - Raiffeisen | Full Time",
        "2026 - Present",
        [
            "Independently review quantitative and statistical models, methodology, assumptions, performance, implementation, controls, and documentation.",
            "Communicate analytical findings and practical recommendations in model-risk and regulatory contexts.",
        ],
        left_x,
        y,
        left_w,
    )
    y = entry(
        c,
        "Risk Model Validator - OTP Group",
        "June 2025 - May 2026",
        [
            "Built a configurable Python time-series validation tool and validated credit, market, and liquidity risk models.",
            "Co-developed group-level non-credit risk model validation and development regulation.",
        ],
        left_x,
        y,
        left_w,
    )
    y = entry(
        c,
        "Teaching Assistant - Corvinus University of Budapest",
        "February 2024 - June 2025",
        ["Supported Econometrics, Time-Series Analysis, and Statistics courses."],
        left_x,
        y,
        left_w,
    )

    y = section(c, "Selected Research", left_x, y - 1, left_w)
    y = compact_entry(
        c,
        "Symbolic Survival Credit Risk",
        "Auditable discrete-time hazard modelling with time-based validation, calibration, benchmark models, and reproducible public data.",
        left_x,
        y,
        left_w,
    )
    y = compact_entry(
        c,
        "Regional Educational Inequality in the EU",
        "Spatial panel modelling, spatial autocorrelation, convergence analysis, and machine learning across European regions.",
        left_x,
        y,
        left_w,
    )
    y = compact_entry(
        c,
        "Budapest Markov Passenger-Flow Framework",
        "GTFS-derived continuous-time Markov chains, stochastic simulation, and network-resilience analysis.",
        left_x,
        y,
        left_w,
    )

    y = section(c, "Professional Activities", left_x, y - 1, left_w)
    y = paragraph(c, "Vice President of Finance & Corporate Relations", left_x, y, left_w, TITLE)
    y = paragraph(c, "FAKT College for Advanced Studies | July 2025 - June 2026", left_x, y - 1, left_w, META)
    y = bullet_list(
        c,
        ["Led annual financial planning and budgeting; organized competitions and lectures; managed two teams of 10-15 members."],
        left_x,
        y - 3,
        left_w,
    )

    # Right column
    ry = page_height - 104
    ry = section(c, "Education", right_x, ry, right_w)
    ry = compact_entry(
        c,
        "Corvinus University of Budapest",
        "MSc Economic and Financial Mathematical Analysis<br/><font color='#2563EB'><b>2023 - 2028 (expected)</b></font>",
        right_x,
        ry,
        right_w,
    )
    ry = paragraph(
        c,
        "<b>Relevant courses</b><br/>Quantitative Finance, Time-Series Analysis, Econometrics, Deep Learning, Algorithm Theory, Probability, Statistics",
        right_x,
        ry,
        right_w,
        SMALL,
    )

    ry = section(c, "Technical Skills", right_x, ry - 12, right_w)
    skills = [
        ("Languages", "Python, R, SQL, C++, VBA"),
        ("Modelling", "Risk models, time series, Bayesian methods, survival analysis, spatial econometrics"),
        ("ML / research", "PyTorch, Stan (MCMC), scikit-learn, reproducible experiments"),
        ("Tools", "Git, LaTeX, Tableau"),
    ]
    for heading, text in skills:
        ry = compact_entry(c, heading, text, right_x, ry, right_w)

    ry = section(c, "Competitions", right_x, ry - 2, right_w)
    ry = compact_entry(
        c,
        "GEM x Morgan Stanley Statistics Competition",
        "2nd place | 2025",
        right_x,
        ry,
        right_w,
    )
    ry = compact_entry(c, "Everesteer Hackathon", "Participant", right_x, ry, right_w)
    ry = compact_entry(c, "IMC Prosperity", "Participant", right_x, ry, right_w)

    ry = section(c, "Languages", right_x, ry - 2, right_w)
    ry = paragraph(
        c,
        "<b>Hungarian</b> - Native<br/><b>English</b> - C1 Advanced<br/><b>German</b> - B2 Upper-Intermediate",
        right_x,
        ry,
        right_w,
        SMALL,
    )

    ry = section(c, "Core Strengths", right_x, ry - 12, right_w)
    ry = bullet_list(
        c,
        [
            "Quantitative problem-solving",
            "Independent model challenge",
            "Research design and communication",
            "Cross-functional leadership",
        ],
        right_x,
        ry,
        right_w,
    )

    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.5)
    c.line(margin, 29, page_width - margin, 29)
    c.setFont(REGULAR, 6.7)
    c.setFillColor(MUTED)
    c.drawString(margin, 17, "Selected public work and current CV: momarci13.github.io")
    c.drawRightString(page_width - margin, 17, "Updated August 2026")

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
