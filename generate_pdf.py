# -*- coding: utf-8 -*-
"""
Casal Investigador — PDF Generator
Gera o dossiê completo com 100 casos para casais investigarem juntos.
"""

import json, os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ─── COLORS ───────────────────────────────────────────────────────────────────
DARK_BG    = HexColor('#0a0a0a')
DARK_CARD  = HexColor('#0d0d0d')
DARK_SECT  = HexColor('#111111')
DARK_LINE  = HexColor('#161616')
CRIMSON    = HexColor('#c41e3a')
GOLD       = HexColor('#c9a84c')
GOLD_LIGHT = HexColor('#e8c96a')
TEXT       = HexColor('#e8e0d0')
TEXT_DIM   = HexColor('#8a8070')
BORDER     = HexColor('#2a2a2a')
CRIME_BG   = HexColor('#8b0000')
HORROR_BG  = HexColor('#2d0a4e')
OCUL_BG    = HexColor('#1a3a0a')
MIST_BG    = HexColor('#003366')
SUSP_BG    = HexColor('#4a3000')

THEME_COLORS = {
    "CRIME":     (CRIME_BG,  HexColor('#ffffff')),
    "HORROR":    (HORROR_BG, HexColor('#e0c0ff')),
    "OCULTISMO": (OCUL_BG,   HexColor('#c0e080')),
    "MISTÉRIO":  (MIST_BG,   HexColor('#a0d0ff')),
    "SUSPENSE":  (SUSP_BG,   HexColor('#ffd080')),
}

THEME_ICONS = {
    "CRIME":     "Crime",
    "HORROR":    "Horror",
    "OCULTISMO": "Ocultismo",
    "MISTÉRIO":  "Mistério",
    "SUSPENSE":  "Suspense",
}

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH   = os.path.join(OUTPUT_DIR, "casal_investigador_100_casos.pdf")
CASES_JSON = os.path.join(OUTPUT_DIR, "cases", "cases.json")

# ─── STYLES ───────────────────────────────────────────────────────────────────
def ps(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=10, textColor=TEXT, leading=14)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

cover_title   = ps('CoverTitle',  fontName='Helvetica-Bold', fontSize=34, textColor=GOLD,  alignment=TA_CENTER, leading=40, spaceAfter=8)
cover_sub     = ps('CoverSub',    fontSize=13,                textColor=TEXT_DIM, alignment=TA_CENTER, leading=18)
body_text     = ps('Body',        fontSize=10.5,                            leading=16, spaceAfter=4, alignment=TA_JUSTIFY)
hint_text     = ps('Hint',        fontName='Helvetica-Oblique', fontSize=10, textColor=GOLD, leading=14, spaceAfter=4, alignment=TA_CENTER)
label_text    = ps('Label',       fontName='Helvetica-Bold', fontSize=9,  textColor=TEXT_DIM, leading=12, spaceAfter=2, spaceBefore=6)
case_title    = ps('CaseTitle',   fontName='Helvetica-Bold', fontSize=15, textColor=GOLD_LIGHT, leading=19, spaceBefore=6, spaceAfter=4)
sol_text      = ps('SolText',     fontSize=10.5,                            leading=16, spaceAfter=6, alignment=TA_JUSTIFY)

# ─── HEADER / FOOTER ──────────────────────────────────────────────────────────
def add_header_footer(c, doc):
    c.saveState()
    W, H = A4
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(2*cm, H - 1.5*cm, W - 2*cm, H - 1.5*cm)
    c.line(2*cm, 1.8*cm,     W - 2*cm, 1.8*cm)
    c.setFont('Helvetica', 8)
    c.setFillColor(TEXT_DIM)
    c.drawCentredString(W/2, 1.1*cm, "- %d -" % doc.page)
    c.drawString(2*cm, H - 1.1*cm, "CASAL INVESTIGADOR")
    c.drawRightString(W - 2*cm, H - 1.1*cm, "100 CASOS PARA DESVENDAR")
    c.restoreState()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def divider(title):
    data = [[Paragraph('<font color="#c9a84c"><b>%s</b></font>' % title,
                        ps('s', fontName='Helvetica-Bold', fontSize=13,
                           alignment=TA_CENTER, textColor=GOLD))]]
    t = Table(data, colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), DARK_LINE),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEABOVE',     (0,0), (-1,0),  1,    GOLD),
        ('LINEBELOW',     (0,0), (-1,-1), 1,    GOLD),
    ]))
    return t

def theme_badge(theme, level, num):
    icon  = THEME_ICONS.get(theme, "??")
    bg, fg = THEME_COLORS.get(theme, (CRIME_BG, HexColor('#ffffff')))
    fgstr = '#%02x%02x%02x' % (int(fg.red*255), int(fg.green*255), int(fg.blue*255))
    data = [[
        Paragraph('<font color="%s"><b>%s %s</b></font>' % (fgstr, icon, theme),
                  ps('tb', fontName='Helvetica-Bold', fontSize=10, alignment=TA_CENTER, textColor=fg)),
        Paragraph('<font color="#c9a84c"><b>Caso #%03d</b></font>' % num,
                  ps('tc', fontName='Helvetica-Bold', fontSize=10, alignment=TA_CENTER, textColor=GOLD)),
        Paragraph('<font color="#c9a84c"><b>%s</b></font>' % level,
                  ps('td', fontName='Helvetica-Bold', fontSize=10, alignment=TA_CENTER, textColor=GOLD)),
    ]]
    t = Table(data, colWidths=[5.5*cm, 5*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ]))
    return t

def clue_row(text, idx):
    return Paragraph(
        '<font color="#c9a84c"><b>  Pista %d:</b></font> <font color="#e8e0d0">%s</font>' % (idx, text),
        ps('clue', fontSize=10.5, leading=16, leftIndent=4, spaceAfter=5, alignment=TA_LEFT)
    )

def suspects_table(suspects):
    header = [
        Paragraph('<font color="#c9a84c"><b>NOME</b></font>',
                  ps('sh', fontName='Helvetica-Bold', fontSize=9, textColor=GOLD)),
        Paragraph('<font color="#c9a84c"><b>MOTIVO CONHECIDO</b></font>',
                  ps('sm', fontName='Helvetica-Bold', fontSize=9, textColor=GOLD)),
    ]
    rows = [header]
    for s in suspects:
        rows.append([
            Paragraph('<font color="#e8c96a"><b>%s</b></font>' % s['name'],
                      ps('sn', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD_LIGHT)),
            Paragraph('<font color="#8a8070">%s</font>' % s['motive'],
                      ps('sm2', fontSize=9.5, textColor=TEXT_DIM, leading=14)),
        ])
    t = Table(rows, colWidths=[5.5*cm, 10*cm])
    style = [
        ('BACKGROUND',    (0,0), (-1,0),  DARK_SECT),
        ('LINEABOVE',     (0,0), (-1,0),  1,       GOLD),
        ('LINEBELOW',     (0,-1),(-1,-1), 0.5,     BORDER),
        ('LINEBEFORE',    (1,0), (1,-1),  0.5,     BORDER),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]
    for i in range(1, len(rows)):
        style.append(('BACKGROUND', (0,i), (-1,i), DARK_CARD))
    t.setStyle(TableStyle(style))
    return t

def solution_box(case_num, solution):
    icon = unichr(128275) if hasattr(unichr(128275), 'encode') else "[SOL]"
    data = [[
        Paragraph('SOLUCAO', ps('si', fontName='Helvetica-Bold', fontSize=13,
                                  alignment=TA_CENTER, textColor=CRIMSON)),
    ]]
    t = Table(data, colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), DARK_SECT),
        ('LINEABOVE',     (0,0), (-1,0),  2,    CRIMSON),
        ('LINEBELOW',     (0,0), (-1,-1), 1,    CRIMSON),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

# ─── BUILD ─────────────────────────────────────────────────────────────────────
def build_pdf(cases_data):
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Casal Investigador — 100 Casos para Desvendar",
        author="Casal Investigador",
        subject="100 casos criminais reais, misterios e enigmas para casais",
    )

    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3.5*cm))
    story.append(Paragraph("CASAL INVESTIGADOR", cover_title))
    story.append(Paragraph("100 Casos para Desvendar", cover_sub))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "A experiencia investigativa definitiva para casais",
        ps('s2', fontName='Helvetica-Oblique', fontSize=12,
           textColor=TEXT_DIM, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 1.5*cm))

    # stats
    stats_data = [[
        Paragraph('<font color="#c9a84c"><b>100</b></font><br/><font color="#8a8070" size="9">CASOS</font>',
                  ps('s3', alignment=TA_CENTER, leading=14)),
        Paragraph('<font color="#c9a84c"><b>5</b></font><br/><font color="#8a8070" size="9">TEMAS</font>',
                  ps('s4', alignment=TA_CENTER, leading=14)),
        Paragraph('<font color="#c9a84c"><b>3</b></font><br/><font color="#8a8070" size="9">NIVEIS</font>',
                  ps('s5', alignment=TA_CENTER, leading=14)),
        Paragraph('<font color="#c9a84c"><b>0</b></font><br/><font color="#8a8070" size="9">LIMITE</font>',
                  ps('s6', alignment=TA_CENTER, leading=14)),
    ]]
    st = Table(stats_data, colWidths=[3.875*cm]*4)
    st.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), DARK_SECT),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LINEAFTER',      (0,0), (2,0),   0.5, BORDER),
        ('BOX',           (0,0), (-1,-1), 1,   GOLD),
    ]))
    story.append(st)
    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width="80%", thickness=0.5, color=GOLD, spaceAfter=1*cm))

    themes_list = [
        ("CRIME",     "Homicidios, fraudes, crimes reais brasileiros"),
        ("HORROR",    "Casas mal-assombradas, instituicoes malditas"),
        ("OCULTISMO", "Tarot, espiritismo, rituais e enigmas"),
        ("MISTERIO",  "Casos reais que marcaram o Brasil"),
        ("SUSPENSE",  "Jogos mortais, Tragedias, misterios digitais"),
    ]
    for name, desc in themes_list:
        story.append(Paragraph(
            '<font color="#c9a84c"><b>%s</b></font>  <font color="#8a8070">%s</font>' % (name, desc),
            ps('tl', fontSize=10.5, leading=18, alignment=TA_CENTER)
        ))

    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(
        "Desenvolvido para casais que querem fugir da rotina,<br/>"
        "desenvolver o raciocinio logico e criar memorias juntos.",
        ps('note', fontName='Helvetica-Oblique', fontSize=10,
           textColor=TEXT_DIM, alignment=TA_CENTER, leading=16)
    ))
    story.append(PageBreak())

    # ── HOW TO PLAY ─────────────────────────────────────────────────────────
    story.append(divider("COMO JOGAR"))
    story.append(Spacer(1, 0.4*cm))

    steps = [
        ("01", "Escolha o Caso",
         "Selecione um dossiê por categoria e nivel de dificuldade que mais chamar sua atencao."),
        ("02", "Analise as Pistas",
         "Leia todas as evidencias, examine os detalhes e anote suas suspeitas. Cada pista importa."),
        ("03", "Interrogue os Suspeitos",
         "Estude o perfil de cada suspeito e seus motivos. Quem tinha mais a ganhar com o crime?"),
        ("04", "Formule sua Teoria",
         "Com base nas pistas e suspeitos, construa sua teoria do crime. Nao se precipite!"),
        ("05", "Reveja a Solucao",
         "Vire a pagina e descubra se voces acertaram. Compare com a explicacao completa."),
    ]

    for num, title, desc in steps:
        step_data = [[
            Paragraph('<font color="#c41e3a" size="18"><b>%s</b></font>' % num,
                      ps('n', alignment=TA_CENTER, leading=22)),
            Paragraph(
                '<font color="#c9a84c"><b>%s</b></font><br/>'
                '<font color="#8a8070">%s</font>' % (title, desc),
                ps('d', fontSize=10.5, leading=16, leftIndent=6)
            ),
        ]]
        s = Table(step_data, colWidths=[1.5*cm, 14*cm])
        s.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW',     (0,0), (-1,-1), 0.5, BORDER),
        ]))
        story.append(s)

    story.append(PageBreak())

    # ── CASES ───────────────────────────────────────────────────────────────
    theme_order = ["CRIME", "HORROR", "OCULTISMO", "MISTERIO", "SUSPENSE"]
    # normalize
    theme_map = {"CRIME":"CRIME","HORROR":"HORROR","OCULTISMO":"OCULTISMO",
                 "MISTÉRIO":"MISTERIO","SUSPENSE":"SUSPENSE"}

    for theme_key in theme_order:
        theme_cases = [c for c in cases_data["cases"]
                       if theme_map.get(c["theme"], c["theme"]) == theme_key]
        if not theme_cases:
            continue

        story.append(divider(theme_key))
        story.append(Spacer(1, 0.3*cm))

        for idx, case in enumerate(theme_cases):
            case_num = idx + 1

            # theme badge
            story.append(theme_badge(theme_key, case["level"], case_num))
            story.append(Spacer(1, 0.2*cm))

            # title
            story.append(Paragraph(case["title"], case_title))

            # synopsis
            story.append(Paragraph(
                '<font color="#c9a84c"><b>  Caso:</b></font> '
                '<font color="#e8e0d0"><i>%s</i></font>' % case["synopsis"],
                body_text
            ))
            story.append(Spacer(1, 0.1*cm))

            # clues
            story.append(Paragraph("EVIDENCIAS E PISTAS", label_text))
            for i, clue in enumerate(case["clues"], 1):
                story.append(clue_row(clue, i))

            story.append(Spacer(1, 0.15*cm))
            story.append(Paragraph("SUSPEITOS", label_text))
            story.append(suspects_table(case["suspects"]))
            story.append(Spacer(1, 0.25*cm))

            # hint
            story.append(Paragraph(
                'Dica: <i><font color="#8a8070">%s</font></i>' % case["answer_hint"],
                hint_text
            ))
            story.append(Spacer(1, 0.3*cm))
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
            story.append(PageBreak())

            # ── SOLUTION ──────────────────────────────────────────────────────
            sb_data = [[
                Paragraph('SOLUCAO DO CASO #%03d' % case_num,
                          ps('sl', fontName='Helvetica-Bold', fontSize=13,
                             alignment=TA_CENTER, textColor=CRIMSON)),
            ]]
            sol_t = Table(sb_data, colWidths=[15.5*cm])
            sol_t.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,-1), DARK_SECT),
                ('LINEABOVE',     (0,0), (-1,0),  2,    CRIMSON),
                ('LINEBELOW',     (0,0), (-1,-1), 1,    CRIMSON),
                ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
                ('TOPPADDING',    (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(sol_t)
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph(
                '<font color="#e8e0d0">%s</font>' % case["solution"],
                sol_text
            ))
            story.append(Spacer(1, 0.4*cm))
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=0.4*cm))

            if idx < len(theme_cases) - 1:
                story.append(PageBreak())

    # ── BACK COVER ──────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("CASAL INVESTIGADOR", cover_title))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        '"Todo mundo acha que seria um bom detetive.<br/>Hora de provar."',
        ps('q', fontName='Helvetica-Oblique', fontSize=14,
           textColor=TEXT_DIM, alignment=TA_CENTER, leading=22)
    ))
    story.append(Spacer(1, 2*cm))
    story.append(HRFlowable(width="60%", thickness=1, color=GOLD, spaceAfter=2*cm))
    story.append(Paragraph(
        "100 casos reais  |  5 categorias  |  3 niveis de dificuldade<br/>"
        "Para casais que querem fugir da rotina",
        ps('foot', fontSize=11, textColor=TEXT_DIM, alignment=TA_CENTER, leading=18)
    ))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "Gerado em %s" % datetime.now().strftime('%B %Y'),
        ps('date', fontSize=9, textColor=HexColor('#444444'), alignment=TA_CENTER)
    ))

    # build
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print("[OK] PDF gerado: %s" % PDF_PATH)


# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with open(CASES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    total = len(data["cases"])
    print("[LOAD] Casos carregados: %d" % total)
    print("[BUILD] Gerando PDF...")
    build_pdf(data)
    size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
    print("[SIZE] Tamanho: %.1f MB" % size_mb)
