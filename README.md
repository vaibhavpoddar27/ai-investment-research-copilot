# AI Investment Research Copilot

Evidence-grounded startup research prototype for venture-capital style analysis.

## Output
Executive snapshot; company/product; problem/customer; market; technology/business inflection; competition; business model/scalability; investment hypotheses; challenge-the-thesis; risks; diligence questions; what to verify next; source register.

## Evidence policy
Prefer primary sources, then reputable secondary sources. Never invent unavailable facts. Distinguish facts, inferences and hypotheses. Surface conflicting evidence. This is research support, not investment advice.

## Run
`pip install -r requirements.txt`
`streamlit run app.py`

Set `GEMINI_API_KEY` as an environment variable or Streamlit secret.

## Deploy
Upload `app.py`, `requirements.txt`, `README.md`, `.gitignore` to a public GitHub repository. Deploy `app.py` using Streamlit Community Cloud and add `GEMINI_API_KEY` under the app's Secrets. Never commit the key.
