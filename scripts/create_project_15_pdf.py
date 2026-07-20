from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from pathlib import Path
import textwrap

OUT = Path(__file__).resolve().parents[1] / 'projects' / 'Kori_Pickle_Multi_Payer_Claim_Readiness_Case_Study_2026.pdf'
ORANGE = HexColor('#FF8200')
BLACK = HexColor('#000000')
WHITE = HexColor('#FFFFFF')
LIGHT = HexColor('#FFF6EC')
PALE = HexColor('#FFF9F2')

pdfmetrics.registerFont(TTFont('DVSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DVSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BrandLabel', fontName='DVSans-Bold', fontSize=8, leading=10, textColor=ORANGE, spaceAfter=8, uppercase=True))
styles.add(ParagraphStyle(name='CoverTitle', fontName='DVSerif-Bold', fontSize=31, leading=33, textColor=BLACK, spaceAfter=12))
styles.add(ParagraphStyle(name='CoverSub', fontName='DVSans', fontSize=11.2, leading=16, textColor=BLACK, spaceAfter=14))
styles.add(ParagraphStyle(name='H1Brand', fontName='DVSerif-Bold', fontSize=24, leading=27, textColor=BLACK, spaceAfter=12))
styles.add(ParagraphStyle(name='H2Brand', fontName='DVSerif-Bold', fontSize=16.5, leading=19, textColor=BLACK, spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name='H3Brand', fontName='DVSans-Bold', fontSize=10.5, leading=13, textColor=BLACK, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyBrand', fontName='DVSans', fontSize=9.2, leading=13.6, textColor=BLACK, spaceAfter=8))
styles.add(ParagraphStyle(name='SmallBrand', fontName='DVSans', fontSize=7.4, leading=10.5, textColor=BLACK, spaceAfter=5))
styles.add(ParagraphStyle(name='TinyBrand', fontName='DVSans', fontSize=6.5, leading=8.5, textColor=BLACK))
styles.add(ParagraphStyle(name='QuoteBrand', fontName='DVSerif-Bold', fontSize=16, leading=20, textColor=BLACK, leftIndent=16, rightIndent=12, spaceBefore=10, spaceAfter=10, borderColor=ORANGE, borderWidth=0, borderPadding=0))
styles.add(ParagraphStyle(name='WhiteH2', fontName='DVSerif-Bold', fontSize=21, leading=24, textColor=WHITE, spaceAfter=10))
styles.add(ParagraphStyle(name='WhiteBody', fontName='DVSans', fontSize=9.2, leading=13.5, textColor=WHITE, spaceAfter=7))
styles.add(ParagraphStyle(name='TableHead', fontName='DVSans-Bold', fontSize=7.4, leading=9, textColor=WHITE, alignment=TA_LEFT))
styles.add(ParagraphStyle(name='TableText', fontName='DVSans', fontSize=7.1, leading=9.3, textColor=BLACK))
styles.add(ParagraphStyle(name='TableTextBold', fontName='DVSans-Bold', fontSize=7.1, leading=9.3, textColor=BLACK))
styles.add(ParagraphStyle(name='CalloutWhite', fontName='DVSerif-Bold', fontSize=14.2, leading=18, textColor=WHITE, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='CalloutBlack', fontName='DVSerif-Bold', fontSize=14.2, leading=18, textColor=BLACK, alignment=TA_CENTER))

PAGE_W, PAGE_H = letter
LEFT = 0.62*inch
RIGHT = 0.62*inch
TOP = 0.62*inch
BOTTOM = 0.62*inch


def footer(canvas: Canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setFillColor(BLACK)
    canvas.rect(0, 0, PAGE_W, 0.34*inch, stroke=0, fill=1)
    canvas.setFont('DVSans', 6.4)
    canvas.setFillColor(WHITE)
    canvas.drawString(LEFT, 0.13*inch, 'Created by Kori Pickle, BSHA Candidate | Student-developed, simulated, no-PHI')
    canvas.setFillColor(ORANGE)
    canvas.drawRightString(PAGE_W-RIGHT, 0.13*inch, f'Healthcare Operations Intelligence Engine(TM) | {doc.page}')
    canvas.restoreState()


def label(text):
    return Paragraph(text.upper(), styles['BrandLabel'])


def section_title(text):
    return Paragraph(text, styles['H1Brand'])


def body(text):
    return Paragraph(text, styles['BodyBrand'])


def small(text):
    return Paragraph(text, styles['SmallBrand'])


def orange_rule(width='100%', thickness=1.2):
    return HRFlowable(width=width, thickness=thickness, color=ORANGE, spaceBefore=4, spaceAfter=9)


def callout(text, black=False):
    bg = BLACK if black else ORANGE
    fg_style = styles['CalloutWhite'] if black else styles['CalloutBlack']
    t = Table([[Paragraph(text, fg_style)]], colWidths=[7.1*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1, BLACK),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    return t


def card(title, text, width=3.44*inch, dark=False, tag=None):
    bg = BLACK if dark else WHITE
    title_style = ParagraphStyle('ct', parent=styles['H3Brand'], textColor=WHITE if dark else BLACK)
    body_style = ParagraphStyle('cb', parent=styles['SmallBrand'], textColor=WHITE if dark else BLACK)
    rows = []
    if tag:
        tag_style = ParagraphStyle('tag', parent=styles['TinyBrand'], fontName='DVSans-Bold', textColor=ORANGE)
        rows.append([Paragraph(tag.upper(), tag_style)])
    rows.append([Paragraph(title, title_style)])
    rows.append([Paragraph(text, body_style)])
    t = Table(rows, colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1, BLACK),
        ('LINEABOVE', (0,0), (-1,0), 5, ORANGE),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def bullets(items, level=0):
    return ListFlowable(
        [ListItem(Paragraph(i, styles['BodyBrand']), leftIndent=12) for i in items],
        bulletType='bullet', start='circle', leftIndent=18, bulletFontName='DVSans-Bold',
        bulletFontSize=7, bulletColor=ORANGE, spaceAfter=8
    )


def table(data, col_widths, header=True, font_size=7.1):
    converted = []
    for r, row in enumerate(data):
        converted.append([])
        for cell in row:
            style = styles['TableHead'] if (header and r == 0) else styles['TableText']
            converted[-1].append(Paragraph(str(cell), style))
    t = Table(converted, colWidths=col_widths, repeatRows=1 if header else 0, hAlign='LEFT')
    ts = [
        ('GRID', (0,0), (-1,-1), 0.75, BLACK),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]
    if header:
        ts += [('BACKGROUND', (0,0), (-1,0), BLACK)]
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0:
            ts.append(('BACKGROUND', (0,r), (-1,r), PALE))
    t.setStyle(TableStyle(ts))
    return t


def page_header(story, module, title, intro=None):
    story += [label(module), section_title(title), orange_rule()]
    if intro:
        story += [body(intro), Spacer(1, 4)]

story = []

cover_top = Table([[Paragraph('HEALTHCARE OPERATIONS INTELLIGENCE ENGINE(TM)', styles['BrandLabel'])]], colWidths=[7.1*inch])
cover_top.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),1.4,ORANGE),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [cover_top, Spacer(1, 0.22*inch)]
story += [Paragraph('Multi-Payer Rule Translation &<br/><font color="#FF8200">Claim Readiness Intelligence(TM)</font>', styles['CoverTitle'])]
story += [Paragraph('Medicare vs Medicaid vs Commercial Payers', ParagraphStyle('csub', parent=styles['CoverSub'], fontName='DVSans-Bold', fontSize=13, leading=16))]
story += [Paragraph('A recruiter-facing healthcare operations case study that converts payer differences into a controlled pre-service workflow, simulated denial analysis, user-acceptance tests, performance measures, and honest entry-level career proof.', styles['CoverSub'])]
story += [Spacer(1, 0.1*inch), callout('CORE QUESTION: Where did the workflow first lose control?', black=True), Spacer(1, 0.22*inch)]
cover_grid = Table([
    [card('Who is being billed?', 'Identify the program, exact plan, product, line of business, and correct payer order.', width=2.24*inch, tag='Control 01'),
     card('What rules apply?', 'Translate service-specific coverage, network, authorization, documentation, and routing requirements.', width=2.24*inch, tag='Control 02'),
     card('What proves readiness?', 'Capture evidence, timestamps, references, owners, deadlines, and unresolved exceptions.', width=2.24*inch, tag='Control 03')]
], colWidths=[2.34*inch]*3, hAlign='LEFT')
cover_grid.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),7)]))
story += [cover_grid, Spacer(1, 0.26*inch)]
disclaimer = Table([[Paragraph('<b>Portfolio boundary:</b> Created by Kori Pickle, BSHA Candidate, University of Phoenix. This project is educational, simulated, and does not use PHI, employer data, payer data, claims data, EHR data, or real patient information. It does not claim billing, coding, payer, compliance, or clinical authority.', styles['SmallBrand'])]], colWidths=[7.1*inch])
disclaimer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),1,BLACK),('LINEBEFORE',(0,0),(0,-1),5,ORANGE),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
story += [disclaimer, Spacer(1, 0.28*inch)]
story += [Paragraph('Portfolio Project 15 | 2026-2027 Career Readiness', ParagraphStyle('cv', parent=styles['SmallBrand'], fontName='DVSans-Bold', alignment=TA_CENTER, textColor=ORANGE))]
story += [PageBreak()]

page_header(story, '01 | Executive Breakdown', 'What the LinkedIn post is really teaching', 'The visible message is that Medicare, Medicaid, and commercial claims do not operate under one universal rulebook. The deeper operations lesson is that the front-end workflow must translate the correct payer logic before the claim is created.')
story += [callout('A clean claim is not only a coding outcome. It is the final output of accurate payer identification, coverage interpretation, authorization readiness, documentation control, claim routing, and verified closure.')]
story += [Spacer(1, 10)]
exec_grid = Table([
    [card('Medicare', 'Federal health insurance with nationally defined program structures, plus coverage rules that can depend on benefit category, national coverage determinations, local coverage determinations, and coordination-of-benefits status.', tag='Program logic'),
     card('Medicaid', 'A joint federal-state program administered by states. Managed care can add plan-level contracts, networks, authorization rules, and operational requirements.', tag='State + plan logic')],
    [card('Commercial', 'Employer-sponsored, Marketplace, and other private plans operate under contracts, benefit designs, networks, utilization-management policies, and payer-specific submission rules.', tag='Contract + product logic'),
     card('Shared risk', 'Eligibility alone does not establish complete readiness. A claim can still fail because the wrong payer was selected, the service was not authorized, the network was not verified, documentation was incomplete, or payer order was unresolved.', dark=True, tag='Workflow lesson')]
], colWidths=[3.5*inch,3.5*inch], hAlign='LEFT')
exec_grid.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
story += [exec_grid]
story += [small('<b>Career translation:</b> Recruiters do not need you to claim years of billing experience. They need evidence that you can distinguish payer types, identify control points, document uncertainty, escalate exceptions, and avoid treating one green eligibility response as proof that everything else is complete.')]
story += [PageBreak()]

page_header(story, '02 | Payer Comparison', 'Medicare vs Medicaid vs commercial payers', 'The purpose of this comparison is not to memorize every payer rule. It is to learn where to look, what to verify, and how to keep separate decisions from being collapsed into one vague status.')
comparison = [
    ['Control area','Medicare','Medicaid','Commercial'],
    ['Primary structure','Federal health insurance; Original Medicare and Medicare Advantage are operationally different pathways.','Joint federal-state program; may be fee-for-service or managed care through state-contracted plans.','Private coverage through employers, unions, Marketplace plans, or individual contracts.'],
    ['Who is commonly covered','People age 65 or older, certain younger people with disabilities, and people with ESRD.','Eligible low-income adults, children, pregnant women, seniors, and people with disabilities; eligibility and benefits vary by state.','Members enrolled in a specific employer, group, Marketplace, or individual product.'],
    ['Critical rule sources','CMS guidance, Medicare manuals, benefit category rules, NCDs/LCDs, MAC instructions, and plan rules for Medicare Advantage.','Federal requirements, state Medicaid guidance, state plan/waiver rules, and the exact managed-care plan manual or contract requirements.','Plan document, Summary of Benefits and Coverage, provider contract, payer policy, network directory, portal response, and payer manual.'],
    ['High-risk readiness questions','Is Medicare primary or secondary? Is the service within a benefit category and reasonable and necessary? Are documentation and frequency rules met?','Which state program and exact plan apply? Is the service covered? Is authorization required? Is the provider/facility enrolled or in network?','Is the exact product active? Are provider, facility, and ancillary services in network? Are referral, preauthorization, and contract rules met?'],
    ['Common false-ready signal','"Medicare is active" without resolving payer order, coverage criteria, or documentation.','"Medicaid is active" without identifying the exact managed plan and service-specific rules.','"Commercial insurance is active" without confirming the exact product, network, authorization, or payer routing.'],
]
story += [table(comparison, [1.23*inch,1.91*inch,1.91*inch,1.91*inch]), Spacer(1,8)]
story += [small('<b>Official grounding:</b> CMS identifies Medicare eligibility categories and explains that Medicare coverage generally depends on benefit category and whether the service is reasonable and necessary. Medicaid.gov explains that Medicaid is administered by states under federal requirements and that managed care is delivered through contracts between states and managed-care organizations. HealthCare.gov defines private coverage as contract-based and provides plan-specific resources such as networks and the Summary of Benefits and Coverage. Sources [1]-[7].')]
story += [PageBreak()]

page_header(story, '03 | Denial Logic', 'Why claims can fail even when coding is correct', 'Correct coding matters, but the claim inherits every unresolved control defect that occurred before submission. The downstream denial is often only the first visible evidence of an upstream failure.')
failures = [
    ['Failure type','First loss of control','Downstream effect','Operational safeguard'],
    ['Wrong payer or payer order','Other coverage or Medicare Secondary Payer status was not resolved before service.','Rejection, denial, recoupment risk, delayed payment, or repeat billing work.','Collect other-insurance data, determine primary/secondary order, document source, and recheck after coverage changes.'],
    ['Eligibility-only verification','Active enrollment was treated as full benefit and service readiness.','Service exclusion, inactive-on-date issue, benefit-limit problem, or patient confusion.','Separate eligibility, benefits, network, authorization, and financial-readiness statuses.'],
    ['Authorization not confirmed','Requirement was not checked for the exact payer, plan, service, provider, and date.','Denial, postponement, rework, appeal preparation, or patient delay.','Capture requirement, status, reference, approved service, dates, owner, deadline, and escalation path.'],
    ['Network not confirmed','The exact provider, facility, or ancillary service was not matched to the exact plan product.','Higher patient responsibility, out-of-network denial, or unexpected bill.','Verify the exact plan and each relevant service location or entity; communicate uncertainty accurately.'],
    ['Coverage/documentation mismatch','Coverage criteria or supporting documentation were not translated into a readiness check.','Medical-necessity denial, record request, payment delay, or incomplete appeal record.','Link payer policy to required evidence and block "ready" when required items are unresolved.'],
    ['Routing/timely filing error','Payer ID, claim destination, submission path, or deadline was not controlled.','Rejection, filing-limit denial, or manual correction.','Use payer-specific routing rules, audit fields, exception queues, and deadline monitoring.'],
]
story += [table(failures, [1.2*inch,1.85*inch,1.7*inch,2.25*inch])]
story += [Spacer(1,8), callout('The denial category is not always the root cause. Trace the visible issue backward until the first control was skipped, merged, misread, or left without an owner.', black=True)]
story += [PageBreak()]

page_header(story, '04 | Simulated Case', 'One outpatient service. Three payer paths. Three different risks.', 'A simulated scheduling team uses one generic checkbox labeled "insurance verified" for all patients. The same diagnostic service is scheduled for three people, but the workflow does not branch by payer type or preserve separate evidence.')
case_data = [
    ['Patient','Coverage path','What staff confirmed','What remained unresolved','Simulated consequence'],
    ['A','Original Medicare + employer group coverage','Medicare eligibility appeared active.','Whether the employer plan was primary, whether Medicare was secondary, and whether crossover information was current.','Claim billed to the wrong primary payer and returned for correction.'],
    ['B','Tennessee Medicaid managed care','State-level coverage appeared active.','The exact managed-care plan, authorization requirement, approved service, and effective dates.','Service proceeded without plan-level authorization evidence and the claim was denied.'],
    ['C','Commercial PPO','The member ID and eligibility date matched.','Whether the facility and ancillary provider were in network for the exact product and whether preauthorization applied.','Patient-facing financial risk and a payer dispute after service.'],
]
story += [table(case_data, [0.55*inch,1.35*inch,1.55*inch,2.2*inch,1.55*inch])]
story += [Spacer(1,10)]
root_grid = Table([
    [card('Visible issue', 'Three different downstream problems: incorrect payer order, missing authorization evidence, and network uncertainty.', width=2.24*inch, tag='What appeared'),
     card('Shared root cause', 'One generic status represented payer identity, eligibility, benefits, network, authorization, coordination of benefits, and claim readiness.', width=2.24*inch, tag='Where control failed', dark=True),
     card('Control redesign', 'Create payer-specific branches with separate statuses, evidence fields, ownership, deadlines, and patient-communication safeguards.', width=2.24*inch, tag='What changes')]
], colWidths=[2.34*inch]*3)
root_grid.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),7)]))
story += [root_grid, Spacer(1,8)]
story += [callout('FIRST LOSS OF CONTROL: The workflow asked "Is insurance active?" when it needed to ask "Which payer logic governs this service, and what evidence proves readiness?"')]
story += [PageBreak()]

page_header(story, '05 | Root-Cause Map', 'Trace the claim backward to the first uncontrolled decision')
steps = [
    ('01','Patient + coverage identity','Confirm patient, subscriber, member ID, date of service, program, exact plan, product, and line of business.'),
    ('02','Payer order','Resolve primary, secondary, tertiary, workers compensation, liability, or other coverage relationships.'),
    ('03','Eligibility + benefits','Separate enrollment status from service-specific benefit and limitation information.'),
    ('04','Network + participation','Verify provider, facility, and relevant ancillary entities against the exact plan product.'),
    ('05','Referral + authorization','Determine whether each requirement applies; capture evidence, dates, scope, and status.'),
    ('06','Coverage + documentation','Translate policy criteria into required records, forms, attestations, or supporting evidence.'),
    ('07','Patient communication','Explain confirmed facts, estimates, unresolved items, and next steps without promising payment.'),
    ('08','Claim routing + closure','Use correct payer ID, claim route, filing deadline, and denial feedback to verify that the process closed.'),
]
node_rows=[]
for n,t,d in steps:
    ncell = Table([[Paragraph(n, ParagraphStyle('num', parent=styles['H2Brand'], alignment=TA_CENTER, textColor=BLACK))]], colWidths=[0.48*inch], rowHeights=[0.48*inch])
    ncell.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WHITE),('BOX',(0,0),(-1,-1),3,ORANGE),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    desc = Paragraph(f'<b>{t}</b><br/>{d}', styles['SmallBrand'])
    node_rows.append([ncell, desc])
node_table = Table(node_rows, colWidths=[0.62*inch,6.38*inch], hAlign='LEFT')
node_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(1,0),(1,-2),0.65,BLACK),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story += [node_table, Spacer(1,8)]
story += [small('<b>Control principle:</b> "Ready" should be an output calculated from completed sub-controls. It should not be a manual checkbox that can hide unresolved payer-specific work.')]
story += [PageBreak()]

page_header(story, '06 | Control Matrix', 'Payer Rule Translation Matrix(TM)', 'This matrix is designed as a student portfolio framework. In a real organization, fields and rules would be configured to the employer-approved system, payer contracts, current manuals, and role permissions.')
matrix = [
    ['Field','Required evidence','Status values','Owner / escalation trigger'],
    ['Payer identity','Program, exact plan, product, payer ID, line of business, date verified.','Confirmed / mismatch / unresolved','Patient access; escalate when card, portal response, and registration data conflict.'],
    ['Payer order / COB','Other coverage responses, MSP questionnaire elements when applicable, primary/secondary decision, source.','Resolved / investigation / changed','Eligibility or billing support; escalate before service or claim release.'],
    ['Eligibility','Effective and termination dates, member match, date-of-service response, source/reference.','Active / inactive / unable to confirm','Patient access; escalate same day when appointment is near.'],
    ['Service benefits','Service category, exclusions, limitations, patient financial fields, response date.','Confirmed / limited / excluded / unclear','Benefits support; escalate unclear or contradictory responses.'],
    ['Network','Exact provider, facility, ancillary entity, and exact plan product.','In / out / unknown / exception','Patient access; escalate before financial estimate or service.'],
    ['Referral / authorization','Requirement, request/approval number, approved service, units, dates, rendering entity, status.','Not required / pending / approved / denied / expired','Authorization team; escalate based on appointment and payer turnaround.'],
    ['Coverage / documentation','Policy source, required documentation, received items, missing elements, review date.','Complete / incomplete / review needed','Documentation owner; escalate before service or claim submission.'],
    ['Claim routing','Claim type, payer ID, electronic route, filing deadline, attachments, COB data.','Ready / hold / corrected / submitted','Billing support; escalate approaching filing limits or repeated rejections.'],
    ['Patient communication','Facts shared, estimates, unresolved items, script, date, contact method.','Completed / follow-up due','Patient access; escalate when financial risk cannot be explained accurately.'],
]
story += [table(matrix, [1.1*inch,2.65*inch,1.35*inch,2.0*inch])]
story += [PageBreak()]

page_header(story, '07 | Synthetic UAT', 'Test the workflow before a real patient or claim absorbs the defect', 'Synthetic user-acceptance testing demonstrates implementation thinking without using real patient information, payer portals, or employer systems.')
uat = [
    ['Test','Synthetic scenario','Expected control behavior','Pass evidence'],
    ['UAT-01','Original Medicare plus active employer group coverage.','System prevents Medicare-primary status until payer order is resolved.','Primary/secondary decision, source, timestamp, and owner captured.'],
    ['UAT-02','Medicare eligibility active but coverage criteria documentation incomplete.','Eligibility can remain active while service readiness stays on hold.','Separate eligibility and documentation statuses; missing evidence listed.'],
    ['UAT-03','State Medicaid active; exact managed plan not identified.','Workflow blocks authorization and claim-routing completion.','Plan mismatch exception routed with deadline.'],
    ['UAT-04','Managed Medicaid plan changes before date of service.','Re-verification trigger resets plan-dependent statuses.','New plan, new effective date, and previous evidence retained in audit trail.'],
    ['UAT-05','Commercial PPO active; facility in network but ancillary provider unknown.','Overall readiness remains unresolved; patient communication avoids a coverage guarantee.','Separate network statuses and documented follow-up.'],
    ['UAT-06','Prior authorization approved for wrong date or service scope.','Approval is rejected as insufficient; status remains pending correction.','Approved service, units, provider, and dates validated.'],
    ['UAT-07','Duplicate coverage appears after claim creation.','Claim release pauses until payer order and COB data are updated.','Exception queue, corrected payer order, and claim audit event.'],
    ['UAT-08','Payer portal response conflicts with payer phone verification.','Workflow records both sources and escalates rather than choosing silently.','Conflict status, source references, owner, and resolution timestamp.'],
]
story += [table(uat, [0.72*inch,2.05*inch,2.45*inch,1.88*inch])]
story += [Spacer(1,8), callout('A system passes UAT only when it handles the exception correctly - not merely when the happy path works.', black=True)]
story += [PageBreak()]

page_header(story, '08 | Measurement', 'KPIs that reveal payer-rule control before denials accumulate')
kpi_grid = Table([
    [card('Exact payer identification rate', 'Percent of accounts with program, exact plan, product, line of business, and payer ID confirmed before service.', width=2.24*inch, tag='Leading'),
     card('Payer-order resolution rate', 'Percent of multi-coverage accounts with primary and secondary responsibility resolved before claim creation.', width=2.24*inch, tag='Leading'),
     card('Authorization evidence completeness', 'Percent of required authorizations with approved service, dates, units, rendering entity, and reference captured.', width=2.24*inch, tag='Leading')],
    [card('Network uncertainty aging', 'Open hours or days for unresolved provider, facility, or ancillary network status.', width=2.24*inch, tag='Leading'),
     card('First-pass claim acceptance', 'Percent of claims accepted without front-end payer, routing, or formatting correction.', width=2.24*inch, tag='Outcome'),
     card('Preventable denial recurrence', 'Repeat denials linked to the same payer-rule root cause after a control change.', width=2.24*inch, tag='Outcome', dark=True)]
], colWidths=[2.34*inch]*3)
kpi_grid.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
story += [kpi_grid, Spacer(1,6)]
roadmap = [
    ['Phase','Focus','Student-developed deliverable'],
    ['Days 1-7','Map current control points and define payer identity fields.','Workflow map, glossary, source hierarchy, and false-ready risk inventory.'],
    ['Days 8-14','Separate statuses and establish exception ownership.','Control matrix, escalation table, evidence requirements, and patient-language guardrails.'],
    ['Days 15-21','Test high-risk payer scenarios.','Synthetic UAT scripts, expected results, defect log, and readiness criteria.'],
    ['Days 22-30','Measure and close the loop.','KPI definitions, denial feedback categories, review cadence, and improvement brief.'],
]
story += [Paragraph('30-Day Simulated Improvement Plan', styles['H2Brand']), table(roadmap, [0.8*inch,2.25*inch,4.05*inch])]
story += [PageBreak()]

page_header(story, '09 | Career Value', 'How this project supports your 2026-2027 healthcare career', 'This case study turns a basic payer-comparison post into evidence of workflow reasoning, documentation discipline, patient awareness, implementation thinking, and denial-prevention readiness.')
career = [
    ['Target role area','Portfolio proof created'],
    ['Patient access / insurance verification','Exact-plan identification, eligibility-benefit separation, network checks, patient communication, and exception routing.'],
    ['Prior authorization support','Requirement identification, evidence fields, date/service validation, aging, escalation, and false-ready prevention.'],
    ['Revenue-cycle support','Payer order, claim routing, preventable denial root cause, first-pass acceptance, and closed-loop correction.'],
    ['Documentation workflow support','Policy-to-evidence translation, missing-item controls, audit trail, and ownership.'],
    ['Health informatics / implementation support','Business requirements, status design, rule branching, synthetic UAT, defect handling, and KPIs.'],
    ['Quality improvement support','Process mapping, leading indicators, recurrence monitoring, and 30-day improvement planning.'],
]
story += [table(career, [2.05*inch,5.05*inch])]
story += [Spacer(1,10), callout('Recruiter message: I do not claim that I have billed Medicare, Medicaid, or commercial claims. I demonstrate that I understand how payer differences create workflow risk and how to design a controlled, testable, patient-aware process.', black=True)]
story += [Spacer(1,9)]
story += [Paragraph('Interview talking point', styles['H2Brand'])]
story += [body('"I developed a simulated no-PHI case study comparing Medicare, Medicaid, and commercial payer workflows. I traced three different claim-readiness failures back to one shared defect: a single insurance-verified status was being used to represent payer identity, eligibility, payer order, network, authorization, documentation, and routing. I redesigned the workflow with payer-specific branches, separate statuses, evidence requirements, exception ownership, synthetic testing, and KPIs. The project shows how I approach healthcare operations problems without claiming payer-system experience I have not earned."')]
story += [Paragraph('Resume project bullet', styles['H2Brand'])]
story += [body('Developed a student-led, simulated multi-payer claim-readiness case study comparing Medicare, Medicaid, and commercial workflows; mapped payer-order, eligibility, network, authorization, documentation, and routing controls; and produced synthetic UAT scenarios, KPIs, and denial-prevention recommendations.')]
story += [PageBreak()]

page_header(story, '10 | LinkedIn Career Positioning', 'Turn the learning into visible, honest professional proof')
story += [Paragraph('Suggested comment for the original post', styles['H2Brand'])]
story += [callout('The biggest risk may be treating "insurance verified" as one decision. Medicare, Medicaid, and commercial plans require different rule sources, but the shared safeguard is the same: separate payer identity, eligibility, payer order, network, authorization, documentation, and claim-routing statuses. The question I keep returning to is: Where did the workflow first lose control?')]
story += [Spacer(1,10), Paragraph('Shorter backup comment', styles['H2Brand'])]
story += [body('Strong reminder that correct coding cannot repair an upstream payer-readiness failure. Knowing who is being billed, which exact plan rules apply, and what evidence proves readiness matters just as much as knowing what is being billed.')]
story += [Paragraph('LinkedIn post in Kori\'s voice', styles['H2Brand'])]
post_text = '''Not every claim denial begins with coding.<br/><br/>
Sometimes the claim is accurate, but the workflow applied the wrong payer logic.<br/><br/>
Medicare, Medicaid, and commercial plans do not use one universal readiness process. Each can introduce different questions about payer order, coverage criteria, network participation, authorization, documentation, and claim routing.<br/><br/>
What stood out to me is how easily one status - "insurance verified" - can hide several unresolved decisions.<br/><br/>
I turned that learning into a student-developed, simulated, no-PHI portfolio case study. I compared three payer paths, traced different downstream problems back to one shared workflow defect, and designed separate statuses, exception ownership, synthetic test cases, and KPIs.<br/><br/>
The visible issue may be a denial.<br/>
The first loss of control may have happened before the patient arrived.<br/><br/>
Where did the workflow first lose control?<br/><br/>
Created by Kori Pickle, BSHA Candidate.<br/>
Student-developed, simulated, and no PHI.<br/><br/>
#HealthcareOperations #RevenueCycle #PatientAccess #InsuranceVerification #PriorAuthorization #ClaimDenials #HealthInformatics'''
post_box = Table([[Paragraph(post_text, styles['SmallBrand'])]], colWidths=[7.1*inch])
post_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),1,BLACK),('LINEABOVE',(0,0),(-1,0),5,ORANGE),('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]))
story += [post_box, PageBreak()]

page_header(story, '11 | Source Notes', 'Official sources informing this educational project', 'The case study uses high-level official guidance. Actual operational decisions must follow the employer-approved workflow, current payer manuals, plan documents, contracts, regulations, and role permissions.')
sources = [
    ('[1] CMS - Original Medicare Part A and Part B Eligibility and Enrollment', 'https://www.cms.gov/medicare/enrollment-renewal/original-part-a-b'),
    ('[2] CMS - Medicare Coverage Determination Process', 'https://www.cms.gov/medicare/coverage/determination-process'),
    ('[3] CMS - Coordination of Benefits', 'https://www.cms.gov/medicare/coordination-benefits-recovery/overview/coordination-benefits'),
    ('[4] CMS - Medicare Secondary Payer', 'https://www.cms.gov/medicare/coordination-benefits-recovery/overview/secondary-payer'),
    ('[5] Medicaid.gov - Medicaid Program Overview', 'https://www.medicaid.gov/medicaid'),
    ('[6] Medicaid.gov - Managed Care', 'https://www.medicaid.gov/medicaid/managed-care'),
    ('[7] Medicaid.gov - Managed Care Authorities', 'https://www.medicaid.gov/medicaid/managed-care/managed-care-authorities'),
    ('[8] HealthCare.gov - Network', 'https://www.healthcare.gov/glossary/network/'),
    ('[9] HealthCare.gov - Preauthorization', 'https://www.healthcare.gov/glossary/preauthorization/'),
    ('[10] HealthCare.gov - Summary of Benefits and Coverage', 'https://www.healthcare.gov/health-care-law-protections/summary-of-benefits-and-coverage/'),
    ('[11] CMS - Health Plan Eligibility Benefit Inquiry and Response (270/271)', 'https://www.cms.gov/priorities/key-initiatives/burden-reduction/administrative-simplification/transactions/health-plan-eligibility-benefit-inquiry-response'),
]
for title,url in sources:
    p = Paragraph(f'<b>{title}</b><br/><font color="#FF8200">{url}</font>', styles['SmallBrand'])
    story += [p, Spacer(1,3)]
story += [Spacer(1,8), orange_rule(), body('<b>Educational note:</b> The original LinkedIn post and infographic were used as a learning prompt. Their wording and design were not reproduced. This case study is an original educational synthesis created for Kori Pickle\'s student portfolio.')]
story += [callout('Healthcare Operations Intelligence Engine(TM) - Where healthcare workflows break before patients, staff, and revenue feel the impact.', black=True)]

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=RIGHT, leftMargin=LEFT, topMargin=TOP, bottomMargin=0.5*inch,
                        title='Multi-Payer Rule Translation and Claim Readiness Intelligence - Kori Pickle',
                        author='Kori Pickle', subject='Student-developed simulated no-PHI healthcare operations portfolio case study')
doc.build(story, onFirstPage=lambda c,d: None, onLaterPages=footer)
print(OUT)
