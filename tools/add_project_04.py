from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
project_url = "./projects/837-835-revenue-cycle-control-intelligence.html"

if project_url in text:
    print("Project 04 is already linked from index.html")
    raise SystemExit(0)

text = text.replace(
    ".project-grid { display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:18px; }",
    ".project-grid { display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:18px; }",
)

card = '''

        <article class="project-card" style="background:#000000;color:#ffffff;border-color:#000000;">
          <span class="project-number">PROJECT 04 · NEW</span>
          <h3>837 → 835 Revenue Cycle Control Intelligence™</h3>
          <p>Follows a simulated institutional claim from upstream readiness through X12 837 submission, payer adjudication, X12 835 remittance, payment posting, exception handling, and verified closure. The case identifies a balanced-dollar responsibility-mapping defect and designs controls that protect both the patient and revenue integrity.</p>
          <div class="project-tags"><span>X12 EDI</span><span>Payment Posting</span><span>UAT</span><span>Patient Impact</span></div>
          <a href="./projects/837-835-revenue-cycle-control-intelligence.html" style="display:inline-block;margin-top:22px;color:#ff8200;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-decoration:none;text-transform:uppercase;border-bottom:1px solid #ff8200;">Open branded case study →</a>
        </article>'''

project_03 = text.index("PROJECT 03")
insert_at = text.index("      </div>\n    </div>\n  </section>", project_03)
text = text[:insert_at] + card + "\n" + text[insert_at:]
path.write_text(text, encoding="utf-8")
print("Project 04 linked from index.html")
