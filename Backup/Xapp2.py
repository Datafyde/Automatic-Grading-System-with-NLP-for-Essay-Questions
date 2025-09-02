# app.py — Streamlit UI for "Automatic Grading System with NLP for Essay Questions"
# Modeled after: https://preview--grade-it-yourself-ai.lovable.app/
# ----------------------------------------------------------------------------------
# How to integrate with your backend:
# 1) Replace the `backend_grade_essay(...)` stub with your project’s actual grader.
#    For example, if your repo exposes something like:
#       from src.grader import grade_essay
#       result = grade_essay(question, essay_text)
#    then return a dict matching the schema used below.
# 2) Keep the return structure consistent so the UI renders correctly.
# 3) Deploy as usual to Streamlit Cloud.
# ----------------------------------------------------------------------------------

import os
import time
import json
import textwrap
from typing import Dict, List, Optional

import streamlit as st

# -----------------------------
# Page Config & Theming
# -----------------------------
st.set_page_config(
  page_title="AutoGrader • Essay Grading with NLP",
  page_icon="🎓",
  layout="wide",
  initial_sidebar_state="expanded",
)

# Custom CSS to mirror the clean, card-based aesthetic
st.markdown(
  """
  <style>
      :root {
          --bg: #0b0f19;           /* deep slate */
          --panel: #0f172a;        /* slightly lighter for panels */
          --ink: #e5e7eb;          /* text */
          --muted: #94a3b8;        /* muted text */
          --accent: #7c3aed;       /* purple */
          --accent-2: #22d3ee;     /* cyan */
          --success: #22c55e;
          --warning: #f59e0b;
          --danger: #ef4444;
          --border: #1f2937;
          --card-radius: 18px;
          --shadow: 0 10px 30px rgba(0,0,0,0.35);
      }
      html, body, [data-testid="stAppViewContainer"] {
          background: linear-gradient(180deg, #0b0f19 0%, #0f172a 100%) !important;
          color: var(--ink) !important;
      }
      [data-testid="stSidebar"] {
          background: linear-gradient(180deg, #0b0f19 0%, #0f172a 100%) !important;
          color: var(--ink) !important;
          border-right: 1px solid var(--border);
      }
      .block-container {
          padding-top: 1.8rem !important;
          padding-bottom: 2rem !important;
      }
      .hero {
          background: radial-gradient(1000px 600px at 10% -10%, rgba(124,58,237,0.25) 0%, rgba(124,58,237,0.0) 60%),
                      radial-gradient(800px 500px at 90% 0%, rgba(34,211,238,0.2) 0%, rgba(34,211,238,0.0) 55%);
          border: 1px solid var(--border);
          border-radius: 28px;
          padding: 24px 28px;
          box-shadow: var(--shadow);
      }
      .card {
          background: rgba(255,255,255,0.02);
          border: 1px solid var(--border);
          border-radius: var(--card-radius);
          padding: 18px 18px;
          box-shadow: var(--shadow);
      }
      .metric {
          display: grid;
          grid-template-columns: 1fr 1fr 1fr;
          gap: 12px;
      }
      .metric .tile {
          background: rgba(255,255,255,0.02);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 14px 16px;
          text-align: center;
      }
      .grade-badge {
          display: inline-flex; align-items: center; gap: 10px;
          font-weight: 700; font-size: 28px;
          padding: 8px 14px; border-radius: 12px;
          background: linear-gradient(90deg, var(--accent), var(--accent-2));
          color: white; box-shadow: var(--shadow);
      }
      .muted { color: var(--muted); }
      .rubric-item { border-bottom: 1px dashed var(--border); padding: 10px 0; }
      .pill {
          display:inline-block; padding:6px 10px; border-radius: 999px;
          background: rgba(124,58,237,0.15); border:1px solid rgba(124,58,237,0.35);
          font-size:12px; margin-right:6px;
      }
      .code-chip {
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
          font-size: 12px; color: #e2e8f0; background: #0b1220; border: 1px solid var(--border);
          border-radius: 8px; padding: 4px 8px;
      }
      .kudos { color: var(--success); }
      .warn { color: var(--warning); }
      .err  { color: var(--danger); }
      .small { font-size: 12px; }
      .smaller { font-size: 11px; }
      .tight { line-height: 1.2; }
      .ghost-input textarea { background: rgba(255,255,255,0.02) !important; border-radius: 14px !important; }
      .ghost-input textarea::placeholder { color: #9aa4b2 !important; }
      .bordered { border: 1px solid var(--border); border-radius: 12px; padding: 10px; }
      .footer { color: var(--muted); }
  </style>
  """,
  unsafe_allow_html=True,
)

# -----------------------------
# Session State
# -----------------------------
if "history" not in st.session_state:
  st.session_state.history = []  # list of dicts (question, essay, result)
if "rubric" not in st.session_state:
  st.session_state.rubric = [
    {"criterion": "Thesis & Focus", "weight": 0.25},
    {"criterion": "Evidence & Examples", "weight": 0.25},
    {"criterion": "Organization & Coherence", "weight": 0.20},
    {"criterion": "Grammar & Style", "weight": 0.15},
    {"criterion": "Originality & Insight", "weight": 0.15},
  ]
if "samples" not in st.session_state:
  st.session_state.samples = {
    "Question": "Explain the causes and consequences of urbanization in the 20th century.",
    "Essay": (
      "Urbanization in the 20th century accelerated due to industrialization, improved transportation, and demographic shifts. "
      "Cities offered jobs, services, and social mobility. However, rapid growth strained housing, sanitation, and infrastructure, "
      "fueling inequality and environmental degradation. Over time, policy responses like zoning, public transit, and welfare programs "
      "attempted to mitigate harms while preserving agglomeration benefits."
    ),
  }

# -----------------------------
# Utilities
# -----------------------------

def letter_grade(score_pct: float) -> str:
  if score_pct >= 93: return "A"
  if score_pct >= 90: return "A-"
  if score_pct >= 87: return "B+"
  if score_pct >= 83: return "B"
  if score_pct >= 80: return "B-"
  if score_pct >= 77: return "C+"
  if score_pct >= 73: return "C"
  if score_pct >= 70: return "C-"
  if score_pct >= 67: return "D+"
  if score_pct >= 63: return "D"
  if score_pct >= 60: return "D-"
  return "F"


def normalize_score(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
  x = max(lo, min(hi, x))
  return round(100 * (x - lo) / (hi - lo), 1)


# -----------------------------
# Backend Integration Stub
# -----------------------------

def backend_grade_essay(
  question: str,
  essay_text: str,
  rubric: List[Dict[str, float]],
  model_choice: str = "Classical (Scikit)",
  max_words: int = 400,
  temperature: float = 0.2,
  api_key: Optional[str] = None,
) -> Dict:
  """
  Replace this stub with your repo's actual grading logic.
  Must return a dict with the following keys:
    - overall_score: float in [0,1]
    - criteria: List[ {criterion:str, score:float in [0,1], notes:str} ] (mirrors `rubric` order)
    - strengths: List[str]
    - improvements: List[str]
    - feedback: str (rich paragraph)
    - confidence: float in [0,1]
    - metadata: dict (optional)
  """
  # Example: attempt to import your real function (feel free to adjust path/name)
  try:
    # from src.pipeline import grade_essay  # <- EDIT to your project structure
    # return grade_essay(question=question, essay=essay_text, rubric=rubric,
    #                    model=model_choice, max_words=max_words,
    #                    temperature=temperature, api_key=api_key)
    pass
  except Exception:
    # Fall back to a lightweight mock so the UI is usable before wiring
    pass

  # --- Mocked scoring for demo purposes ---
  import random
  random.seed(len(essay_text) + len(question))

  # Heuristic base: length & basic structure
  length_bonus = min(len(essay_text.split()) / max(120, max_words), 1.0)
  base = 0.55 * 0.6 + 0.45 * length_bonus

  crit_results = []
  for item in rubric:
    jitter = random.uniform(-0.08, 0.08)
    score = max(0.0, min(1.0, base + jitter))
    note = f"Assessment for {item['criterion']}: solid coverage with room to deepen analysis."
    crit_results.append({"criterion": item["criterion"], "score": score, "notes": note})

  overall = sum(c["score"] * w["weight"] for c, w in zip(crit_results, rubric))
  conf = min(1.0, 0.65 + random.uniform(-0.1, 0.1))

  strengths = [
    "Clear central thesis maintained across paragraphs.",
    "Relevant examples support key claims.",
    "Logical progression with effective signposting.",
  ]
  improvements = [
    "Integrate more quantitative evidence or citations.",
    "Tighten topic sentences to sharpen focus.",
    "Vary sentence structures and reduce passive voice.",
  ]
  feedback = (
    "Your essay demonstrates a coherent argument and appropriate supporting evidence. "
    "To elevate the work, expand on counterarguments and include specific data or citations where appropriate. "
    "Refining transitions and reducing redundancy will further improve readability."
  )

  return {
    "overall_score": float(overall),
    "criteria": crit_results,
    "strengths": strengths,
    "improvements": improvements,
    "feedback": feedback,
    "confidence": float(conf),
    "metadata": {
      "model": model_choice,
      "max_words": max_words,
      "temperature": temperature,
    },
  }


# -----------------------------
# Sidebar — Controls
# -----------------------------
with st.sidebar:
  st.markdown("""
    <div class="card">
        <h2 class="tight">🎓 AutoGrader</h2>
        <p class="muted">Automatic grading for essay questions — NLP powered.</p>
    </div>
    """, unsafe_allow_html=True)

  st.markdown("""
    <div class="card">
        <div class="smaller muted">MODEL</div>
    """, unsafe_allow_html=True)
  model_choice = st.radio(
    "Model",
    options=["Classical (Scikit)", "Transformer (HF)", "OpenAI"],
    index=0,
    label_visibility="collapsed",
  )
  st.markdown("</div>", unsafe_allow_html=True)

  st.markdown("""
    <div class="card">
        <div class="smaller muted">PARAMETERS</div>
    """, unsafe_allow_html=True)
  max_words = st.slider("Max words (LLM summarization cap)", 150, 800, 400, 50)
  temperature = st.slider("Creativity / Temperature", 0.0, 1.0, 0.2, 0.05)
  api_key = None
  if model_choice == "OpenAI":
    api_key = st.text_input("OpenAI API Key", type="password")
  st.markdown("</div>", unsafe_allow_html=True)

  st.markdown("""
    <div class="card">
        <div class="smaller muted">RUBRIC</div>
        <div class="smaller muted">(weights must sum to 1.0)</div>
    """, unsafe_allow_html=True)
  # Editable rubric weights
  weights = []
  total = 0.0
  for i, item in enumerate(st.session_state.rubric):
    w = st.number_input(
      f"{item['criterion']}",
      min_value=0.0,
      max_value=1.0,
      value=float(item["weight"]),
      step=0.05,
      key=f"rubric_{i}",
    )
    weights.append({"criterion": item["criterion"], "weight": w})
    total += w
  if abs(total - 1.0) > 1e-6:
    st.warning(f"Rubric weights sum to {total:.2f}. Consider adjusting to 1.00.")
  st.markdown("</div>", unsafe_allow_html=True)

  st.markdown("""
    <div class="card">
        <div class="smaller muted">ACTIONS</div>
    """, unsafe_allow_html=True)
  use_sample = st.button("Load Sample", type="secondary")
  clear_all = st.button("Clear", type="secondary")
  st.markdown("</div>", unsafe_allow_html=True)

# Update session rubric if edited
st.session_state.rubric = weights

# -----------------------------
# Main — Hero Header
# -----------------------------
colH1, colH2 = st.columns([3, 2])
with colH1:
  st.markdown(
    """
    <div class="hero">
        <div class="pill">Streamlit Demo UI</div>
        <h1 class="tight">Grade It Yourself — <span class="muted">Essay AutoGrader</span></h1>
        <p class="muted">Paste your essay, pick the question, and get structured feedback across a customizable rubric.</p>
    </div>
    """,
    unsafe_allow_html=True,
  )
with colH2:
  st.markdown(
    """
    <div class="hero">
        <div class="metric">
            <div class="tile">
                <div class="smaller muted">Avg. Grade</div>
                <div style="font-size:22px; font-weight:700;">B+</div>
            </div>
            <div class="tile">
                <div class="smaller muted">Essays Graded</div>
                <div style="font-size:22px; font-weight:700;">{}</div>
            </div>
            <div class="tile">
                <div class="smaller muted">Latency</div>
                <div style="font-size:22px; font-weight:700;">~1.2s</div>
            </div>
        </div>
    </div>
    """.format(len(st.session_state.history)),
    unsafe_allow_html=True,
  )

st.markdown("\n")

# -----------------------------
# Input / Output Columns
# -----------------------------
left, right = st.columns([7, 8], gap="large")

with left:
  st.markdown("<div class='card'>", unsafe_allow_html=True)
  st.subheader("🧠 Question")
  question = st.text_input(
    "Enter the essay prompt/question",
    placeholder=st.session_state.samples["Question"],
  )

  st.subheader("✍🏽 Essay")
  default_essay = st.session_state.samples["Essay"] if use_sample else ""
  if clear_all:
    default_essay = ""
    question = ""
  essay_text = st.text_area(
    label="Paste or type your essay here",
    value=default_essay,
    height=280,
    placeholder="Write your essay...",
    help="Tip: aim for clarity, evidence, and coherent structure.",
  )

  # Character / word counters
  words = len(essay_text.split()) if essay_text else 0
  chars = len(essay_text) if essay_text else 0
  st.caption(f"{words} words • {chars} characters")

  submit = st.button("🔎 Grade Essay", type="primary")
  st.markdown("</div>", unsafe_allow_html=True)

with right:
  st.markdown("<div class='card'>", unsafe_allow_html=True)
  st.subheader("📊 Results")

  if submit:
    if not essay_text.strip() or not (question.strip() or st.session_state.samples["Question"]):
      st.error("Please provide both a question and an essay.")
    else:
      q = question.strip() or st.session_state.samples["Question"]
      with st.spinner("Grading in progress..."):
        start = time.time()
        result = backend_grade_essay(
          question=q,
          essay_text=essay_text,
          rubric=st.session_state.rubric,
          model_choice=model_choice,
          max_words=max_words,
          temperature=temperature,
          api_key=api_key,
        )
        latency = time.time() - start

      overall_pct = round(result["overall_score"] * 100, 1)
      letter = letter_grade(overall_pct)
      conf_pct = round(result.get("confidence", 0.0) * 100)

      # Topline
      st.markdown(
        f"<div class='grade-badge'>Final Grade: {letter} · {overall_pct}%</div>",
        unsafe_allow_html=True,
      )
      st.caption(f"Model: {result.get('metadata', {}).get('model', model_choice)} • Confidence: {conf_pct}% • ~{latency:.2f}s")

      # Criteria breakdown
      st.markdown("### Rubric Breakdown")
      for crit in result["criteria"]:
        pct = normalize_score(crit["score"])  # 0-100
        bar = st.progress(pct/100.0, text=f"{crit['criterion']} — {pct}%")
        # tiny pause for nicer visual
        time.sleep(0.02)
        st.markdown(
          f"<div class='smaller muted'>{crit['notes']}</div>",
          unsafe_allow_html=True,
        )

      st.divider()

      # Feedback blocks
      colA, colB = st.columns(2)
      with colA:
        st.markdown("#### ✅ Strengths")
        for s in result.get("strengths", []):
          st.markdown(f"- <span class='kudos'>{s}</span>", unsafe_allow_html=True)
      with colB:
        st.markdown("#### ✏️ Improvements")
        for imp in result.get("improvements", []):
          st.markdown(f"- <span class='warn'>{imp}</span>", unsafe_allow_html=True)

      st.markdown("#### 📝 Overall Feedback")
      st.markdown(
        f"<div class='bordered'>{result.get('feedback','')}</div>",
        unsafe_allow_html=True,
      )

      # Save to history
      st.session_state.history.append({
        "question": q,
        "essay": essay_text,
        "result": result,
        "latency": latency,
      })

      # Download feedback
      export_payload = {
        "question": q,
        "essay": essay_text,
        "grade_percent": overall_pct,
        "grade_letter": letter,
        "confidence": conf_pct,
        "rubric": st.session_state.rubric,
        "criteria": result["criteria"],
        "strengths": result.get("strengths", []),
        "improvements": result.get("improvements", []),
        "feedback": result.get("feedback", ""),
        "metadata": result.get("metadata", {}),
      }
      st.download_button(
        label="⬇️ Download Report (JSON)",
        data=json.dumps(export_payload, indent=2),
        file_name="autograde_report.json",
        mime="application/json",
      )
  else:
    st.info("Submit an essay to see results here.")
  st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# History Drawer
# -----------------------------
with st.expander("📚 History (current session)", expanded=False):
  if not st.session_state.history:
    st.caption("No essays graded yet in this session.")
  else:
    for i, item in enumerate(reversed(st.session_state.history), start=1):
      res = item["result"]
      pct = round(res["overall_score"] * 100, 1)
      letter = letter_grade(pct)
      st.markdown(
        f"**{i}. {letter} · {pct}%** — <span class='muted smaller'>{len(item['essay'].split())} words • {item['latency']:.2f}s</span>",
        unsafe_allow_html=True,
      )
      with st.popover("View details"):
        st.write("**Question**", item["question"])
        st.write("**Essay (truncated)**", (item["essay"][:400] + "...") if len(item["essay"]) > 400 else item["essay"])
        st.write("**Feedback**", res.get("feedback", ""))

# -----------------------------
# Footer
# -----------------------------
st.markdown(
  """
  <br/>
  <div class="footer small">Built with ❤️ using Streamlit. UI modeled after Grade-It-Yourself-AI preview. Hook up your backend in <span class="code-chip">backend_grade_essay()</span>.</div>
  """,
  unsafe_allow_html=True,
)
