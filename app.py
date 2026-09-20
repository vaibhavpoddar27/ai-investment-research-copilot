
import streamlit as st
from urllib.parse import quote_plus
import re

st.set_page_config(page_title="AI Investment Research Copilot", page_icon="🔎", layout="wide")

st.title("🔎 AI Investment Research Copilot")
st.caption("Evidence-first startup research workflow • no API key required")

st.markdown("""
This prototype separates **evidence collection** from **AI reasoning**.
It creates a structured research workspace and a ready-to-run AI analysis prompt.
Use public sources only and keep confidential/client information out of the tool.
""")

if "sources" not in st.session_state:
    st.session_state.sources = []
if "notes" not in st.session_state:
    st.session_state.notes = ""

with st.sidebar:
    st.header("1. Startup")
    company = st.text_input("Startup / company", value="Quintrans")
    context = st.text_input("Sector / context", value="Industrial automation / precision motion control")
    st.divider()
    st.write("**Workflow**")
    st.write("1. Search public sources")
    st.write("2. Record evidence")
    st.write("3. Generate AI research brief")
    st.write("4. Challenge the thesis")

if company.strip():
    q = quote_plus(company.strip())
    st.subheader("2. Research the company")
    st.write("Open these searches and collect evidence from primary/reputable sources.")

    cols = st.columns(3)
    searches = [
        ("Official / company", f"https://www.google.com/search?q={q}+official+website+founders+product"),
        ("Funding / investors", f"https://www.google.com/search?q={q}+funding+investors+startup"),
        ("Customers / traction", f"https://www.google.com/search?q={q}+customers+deployments+partnerships"),
        ("Market / competitors", f"https://www.google.com/search?q={q}+market+competitors+industry"),
        ("Technology", f"https://www.google.com/search?q={q}+technology+product+engineering"),
        ("Risks / challenges", f"https://www.google.com/search?q={q}+risks+challenges+startup"),
    ]
    for i, (label, url) in enumerate(searches):
        with cols[i % 3]:
            st.link_button(label, url, use_container_width=True)

    st.info("Source hierarchy: company/founder/investor/government/regulator first; then reputable business/technology publications; databases as supporting evidence. Do not treat search snippets alone as verified facts.")

st.subheader("3. Add evidence")

url = st.text_input("Source URL", placeholder="https://...")
title = st.text_input("Source title / publisher", placeholder="e.g., Company website — Quintrans")
evidence = st.text_area("What does this source establish?", height=100,
                         placeholder="Write only what the source actually supports.")

if st.button("➕ Add source"):
    if url.strip() and evidence.strip():
        st.session_state.sources.append({
            "title": title.strip() or url.strip(),
            "url": url.strip(),
            "evidence": evidence.strip()
        })
        st.success(f"Added source S{len(st.session_state.sources)}")
    else:
        st.warning("Add both a URL and evidence.")

if st.session_state.sources:
    st.write(f"**Sources captured: {len(st.session_state.sources)}**")
    for i, s in enumerate(st.session_state.sources, 1):
        with st.expander(f"[S{i}] {s['title']}"):
            st.write(s["url"])
            st.write(s["evidence"])

st.subheader("4. Investment-research framework")

sections = [
    "Executive Snapshot",
    "Company & Product",
    "Problem & Customer",
    "Market & Market Dynamics",
    "Technology / Business Inflection Point",
    "Competitive Landscape",
    "Business Model & Scalability",
    "Investment Thesis — 3 to 5 hypotheses",
    "Challenge the Thesis",
    "Key Risks",
    "VC Diligence Questions",
    "What I Would Verify Next",
    "Source Register"
]

selected = st.multiselect(
    "Sections to analyse",
    sections,
    default=sections
)

source_packet = ""
for i, s in enumerate(st.session_state.sources, 1):
    source_packet += f"\n[S{i}] {s['title']}\nURL: {s['url']}\nEvidence: {s['evidence']}\n"

prompt = f"""Act as an evidence-grounded Indian VC research analyst.

Company: {company}
Context: {context}

Use ONLY the evidence below for company-specific factual claims.
Never invent funding, customers, revenue, valuation, market size, competitors, partnerships or product capabilities.
If a material fact is not established, write "Not publicly verified" or "Not publicly disclosed".
Distinguish FACT, INFERENCE and HYPOTHESIS.
If sources disagree, show the disagreement.
Cite factual claims using [S1], [S2], etc.
Do not give Buy/Hold/Sell, investment scores, rankings or an overall recommendation.

For every investment thesis hypothesis provide:
- Hypothesis
- Evidence supporting it
- Evidence against / unknown
- What must be true
- Diligence test

Actively try to disprove the thesis.

Produce these sections:
{chr(10).join("- " + x for x in selected)}

SOURCE EVIDENCE:
{source_packet if source_packet else "[No sources added yet — do not invent evidence.]"}
"""

st.subheader("5. AI analysis prompt")
st.caption("Copy this prompt into ChatGPT after you have added your public-source evidence.")
st.code(prompt, language="text")

st.download_button(
    "⬇️ Download research prompt",
    prompt,
    file_name=f"{re.sub(r'[^A-Za-z0-9_-]+','_',company or 'startup')}_VC_research_prompt.txt",
    mime="text/plain"
)

if st.session_state.sources:
    report = f"# {company} — Evidence Pack\n\nContext: {context}\n\n"
    for i, s in enumerate(st.session_state.sources, 1):
        report += f"## [S{i}] {s['title']}\n{s['url']}\n\n{s['evidence']}\n\n"
    report += "\n## AI Analysis Prompt\n\n" + prompt
    st.download_button(
        "⬇️ Download complete evidence pack",
        report,
        file_name=f"{re.sub(r'[^A-Za-z0-9_-]+','_',company or 'startup')}_evidence_pack.md",
        mime="text/markdown"
    )

st.divider()
st.caption("Proof-of-work prototype. Public sources only. Human review remains responsible for conclusions.")
