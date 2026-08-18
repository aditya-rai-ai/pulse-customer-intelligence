"""Pulse — a simple web UI for the Customer Intelligence Agent."""
import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="Pulse — Customer Intelligence Agent", page_icon="📊")

# Load the OpenAI key BEFORE importing Pulse (its modules read the key at import time).
load_dotenv()  # local: reads your .env
try:
    if "OPENAI_API_KEY" in st.secrets:            # hosted: read from Streamlit secrets
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass

if not os.environ.get("OPENAI_API_KEY"):
    st.error(
        'No OpenAI API key found. On Streamlit Cloud, open the ⋮ menu → Settings → Secrets '
        'and add exactly:\n\nOPENAI_API_KEY = "sk-...your key..."\n\nthen reboot the app.'
    )
    st.stop()

import src.pulse_customer_intelligence.tracing as tracing
tracing.ENABLED = False  # no step-tracing noise in the web app

from src.pulse_customer_intelligence.agents_team import build_coordinator
from src.pulse_customer_intelligence.models import Triage
from src.pulse_customer_intelligence.guardrails import check_input, check_output


def clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[len("json"):]
    return text.strip()


@st.cache_resource
def get_coordinator():
    return build_coordinator()


st.title("📊 Pulse — Customer Intelligence Agent")
st.caption("A multi-agent AI system that triages customer feedback: sentiment, category, "
           "routing, a policy-grounded reply, and safety guardrails.")

feedback = st.text_area(
    "Customer feedback",
    placeholder="e.g. The tomatoes I got yesterday were mushy and not fresh.",
    height=120,
)

if st.button("Analyze", type="primary"):
    problem = check_input(feedback)
    if problem:
        st.warning(f"⚠️ Blocked by input guardrail: {problem}")
    else:
        with st.spinner("The agent team is working…"):
            result = asyncio.run(get_coordinator().run(feedback))
            triage = Triage.model_validate_json(clean_json(result.text))
            flags = check_output(triage.suggested_response, triage.priority)

        color = {"High": "red", "Medium": "orange", "Low": "green"}.get(triage.priority, "gray")
        st.markdown(f"### :{color}[{triage.priority} priority] · {triage.sentiment.value} · {triage.category}")
        st.markdown(f"**Route to:** {triage.owning_department}")
        st.markdown(f"**Summary:** {triage.summary}")
        st.markdown(f"**Suggested reply:** {triage.suggested_response}")
        if flags:
            st.error("🚩 Needs human review:")
            for f in flags:
                st.write(f"- {f}")