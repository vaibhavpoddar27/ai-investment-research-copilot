import os, re
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Investment Research Copilot", page_icon="🔎", layout="wide")

SYSTEM_PROMPT = """
You are an evidence-grounded Indian startup investment research analyst.
Research startups using Google Search grounding and produce a VC-oriented research brief.

NON-NEGOTIABLE:
- Use live/public web research; do not rely on memory when a fact can be searched.
- Prefer primary sources: company/founder/investor/government/regulator.
- Then reputable financial/business/technology publications.
- Databases such as Crunchbase, Tracxn and LinkedIn are supporting sources.
- Never invent facts, funding, customers, revenue, market size, valuation, margins or competitors.
- If a material fact cannot be verified publicly, say "Not publicly verified" or "Not publicly disclosed".
- If credible sources disagree, show the disagreement.
- Distinguish FACT, INFERENCE and HYPOTHESIS.
- Cite material factual claims using the grounded search citations available to you and provide a Source Register.
- Do not give Buy/Hold/Sell, investment scores, rankings, or pretend to know an unverified valuation.
- Focus on VC questions: market, inflection points, customer pain, product, GTM, competition, moat, scalability, capital intensity, risks and diligence.
- For market sizes, state definition and geography and do not mix TAM with forecasts.
- For funding/traction/customers, distinguish announced facts from inferred target customers.
- End with what needs verification and concrete founder diligence questions.
- This is research support, not investment advice.

OUTPUT:
1. Executive Snapshot
2. Company & Product
3. Problem & Customer
4. Market & Market Dynamics
5. Technology / Business Inflection Point
6. Competitive Landscape
7. Business Model & Scalability
8. Investment Thesis (3-5 hypotheses)
9. Challenge the Thesis
10. Key Risks
11. VC Diligence Questions
12. What I Would Verify Next
13. Source Register

For every thesis hypothesis include: Hypothesis; Evidence supporting it; Evidence against/unknown; What must be true; Diligence test.
"""

def client():
    key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    if not key: return None
    return genai.Client(api_key=key)

def research(company, context):
    c=client()
    if not c: raise RuntimeError("GEMINI_API_KEY is not configured. Add it under Streamlit → Settings → Secrets.")
    prompt=f"""
Research this startup/company using Google Search grounding.

Company: {company}
Optional context: {context or "None"}

Find and verify:
- official website and exact product
- founding, founders, location, funding/investors if public
- customer problem and target customer
- India/global market evidence, with dates and definitions
- technology/business/industry inflection point
- direct competitors, substitutes and incumbent threats
- public evidence of customers, deployments, partnerships, traction, pricing/economics
- VC investment hypotheses, then actively try to disprove them
- concrete founder diligence questions

Use conservative language. Missing information must be explicitly marked as unavailable/unverified.
"""
    cfg=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(google_search=types.GoogleSearch())],
    )
    r=c.models.generate_content(model="gemini-3.6-flash", contents=prompt, config=cfg)
    return r.text

st.title("🔎 AI Investment Research Copilot")
st.caption("Evidence-grounded startup research • investment thesis • counter-thesis • VC diligence")

with st.sidebar:
    st.header("Research")
    company=st.text_input("Startup / company", placeholder="e.g., Quintrans")
    context=st.text_input("Optional sector/context", placeholder="e.g., industrial automation")
    st.divider()
    st.write("**Evidence policy:** public web sources only; unsupported facts are marked rather than invented.")
    st.caption("Research prototype — not investment advice.")

if "report" not in st.session_state: st.session_state.report=None
if "company" not in st.session_state: st.session_state.company=""

st.info("Enter a startup name. The copilot researches public sources and builds a source-grounded VC research brief.")
if st.button("🔎 Research startup", type="primary"):
    if not company.strip(): st.error("Enter a startup/company name.")
    else:
        with st.spinner("Researching public sources and building the brief…"):
            try:
                st.session_state.report=research(company.strip(), context.strip())
                st.session_state.company=company.strip()
            except Exception as e: st.error(str(e))

if st.session_state.report:
    st.success(f"Research completed for {st.session_state.company}.")
    st.markdown(st.session_state.report)
    st.download_button("⬇️ Download research brief",
        st.session_state.report,
        file_name=f"{re.sub(r'[^A-Za-z0-9_-]+','_',st.session_state.company)}_investment_research.md",
        mime="text/markdown")
