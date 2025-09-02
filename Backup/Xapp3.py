import streamlit as st
from PIL import Image
import os

# Import your grading functions
from graders import grade_essay_questions  # adjust import name if different
from graders import grade_mcq_questions      # adjust import name if different

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
  page_title="Automatic Essay & MCQ Grading System",
  page_icon="🎓",
  layout="wide"
)

# ==============================
# CUSTOM STYLES
# ==============================
st.markdown("""
    <style>
        /* Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #e5e5e5, #15162c);
            color: white;
            font-family: 'Arial', sans-serif;
        }

        /* Hero Title */
        .hero-text {
            font-size: 3rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.5rem;
        }

        .hero-subtext {
            font-size: 1.2rem;
            color: #d1d5db;
            margin-bottom: 2rem;
        }

        /* Buttons */
        .stButton button {
            border-radius: 2rem;
            padding: 0.6rem 1.5rem;
            font-weight: bold;
            border: none;
            transition: all 0.2s ease-in-out;
        }

        .stButton button:first-child {
            background: #ec4899;
            color: white;
        }

        .stButton button:hover {
            transform: scale(1.05);
        }

        /* Card Style */
        .stCard {
            background: #1f2937;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            margin-top: 1rem;
        }

        /* Divider */
        hr {
            border: none;
            height: 2px;
            background: #9333ea;
            margin: 2rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
col1, col2 = st.columns([1.2, 1])

with col1:
  st.markdown("<div class='hero-text'>Automatic Grading System</div>", unsafe_allow_html=True)
  st.markdown("<div class='hero-subtext'>Leverage AI & NLP to grade Essays & Multiple Choice Questions instantly.</div>", unsafe_allow_html=True)

  c1, c2 = st.columns([0.4, 0.6])
  with c1:
    st.button("🚀 Try Now")
  with c2:
    st.button("📖 View Demo")

with col2:
  img_path = "NLP Grader Image.jpeg"
  if os.path.exists(img_path):
    img = Image.open(img_path)
    st.image(img, use_column_width=True)
  else:
    st.image("https://undraw.co/api/illustrations/education.svg", use_column_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==============================
# MAIN CONTENT (Essay + MCQ Tabs)
# ==============================
tab1, tab2 = st.tabs(["📝 Essay Grading", "❓ MCQ Grading"])

# ------------------------------
# ESSAY GRADING TAB
# ------------------------------
with tab1:
  st.subheader("📝 Essay Grading")
  st.write("Paste your essay or upload a `.txt` file below:")

  essay_text = st.text_area("Essay Text:", height=200, placeholder="Start typing or paste your essay...")

  uploaded_file = st.file_uploader("...or upload a .txt file", type=["txt"], key="essay_upload")
  if uploaded_file is not None:
    essay_text = uploaded_file.read().decode("utf-8")

  if st.button("🔍 Grade Essay"):
    if essay_text.strip() == "":
      st.warning("⚠️ Please provide an essay before grading.")
    else:
      score, feedback = essay_grader(essay_text)  # ✅ actual function
      st.markdown(f"""
            <div class="stCard">
                <h3>📊 Essay Results</h3>
                <p><b>Score:</b> {score}/100</p>
                <p><b>Feedback:</b> {feedback}</p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------
# MCQ GRADING TAB
# ------------------------------
with tab2:
  st.subheader("❓ MCQ Grading")
  st.write("Upload your MCQ answers in CSV format.")

  uploaded_mcq = st.file_uploader("Upload MCQ file", type=["csv"], key="mcq_upload")
  if uploaded_mcq is not None:
    try:
      score, report = mcq_grader(uploaded_mcq)  # ✅ actual function
      st.markdown(f"""
            <div class="stCard">
                <h3>📊 MCQ Results</h3>
                <p><b>Total Score:</b> {score}</p>
                <p><b>Details:</b> {report}</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
      st.error(f"⚠️ Error processing file: {e}")
