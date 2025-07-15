import streamlit as st
from home import home_page
from grading_system import grading_system_page
from user_guide import user_guide_page
from about import about_page

# Set page config
st.set_page_config(layout="wide")

# Initialize navigation state
if 'page' not in st.session_state:
  st.session_state.page = "Home"

# Page Switching Logic
def navigate(page_name):
  st.session_state.page = page_name
  st.rerun()

# Page Functions
def home_page():
  # Navbar
  st.markdown("""
        <style>
            .nav-container {
                background-color: #add8f7;
                padding: 10px;
                border-radius: 15px;
                border: 2px solid black;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .nav-logo {
                height: 50px;
            }
            .nav-links a {
                margin: 0 20px;
                text-decoration: none;
                color: black;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Comic Sans MS', cursive, sans-serif;
                cursor: pointer;
            }
            .nav-links span.active {
                padding: 2px 10px;
                border: 2px solid red;
                border-radius: 8px;
            }
        </style>
        <div class="nav-container">
            <img src="https://i.imgur.com/kxKMbDT.png" class="nav-logo" alt="Logo">
            <div class="nav-links">
                <a onclick="window.location.reload(true);">🏠</a>
                <a href="#" onclick="window.parent.postMessage('Grading System', '*')">Grading System</a>
                <a href="#" onclick="window.parent.postMessage('User Guide', '*')">User Guide</a>
                <a href="#" onclick="window.parent.postMessage('About', '*')">About</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

  # Two column layout
  col1, col2 = st.columns([1, 2])
  with col1:
    # Adding space from the top margin
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.markdown("""
            <style>
                .welcome-text {
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                    font-size: 24px;
                }
                .autograding {
                    font-size: 36px;
                    font-weight: bold;
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                }
                .system {
                    font-size: 72px;
                    font-weight: bold;
                    color: black;
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                }
                .subtitle {
                    background-color: #cce6ff;
                    display: inline-block;
                    padding: 5px 15px;
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                    border: 2px solid black;
                    border-radius: 10px;
                    font-size: 18px;
                }
            </style>
            <div class="welcome-text">Welcome to</div>
            <div class="autograding">AutoGrading</div>
            <div class="system">System</div>
            <div class="subtitle">Making grading simple and smarter!</div>
        """, unsafe_allow_html=True)
    if st.button("Get started", use_container_width=False):
      navigate("Grading System")

  with col2:
    st.image("homepage.jpeg", use_column_width=True)


def grading_system_page():
  st.title("📝 Grading System")
  st.markdown("Welcome to the Grading System page. Here, you'll grade assignments using the AutoGrading tool.")

def user_guide_page():
  st.title("📘 User Guide")
  st.markdown("Here you'll find how to use the AutoGrading System.")

def about_page():
  st.title("ℹ️ About")
  st.markdown("This system was built to simplify grading for educators using automation.")

# Navigation Switch
page = st.session_state.page
if page == "Home":
  home_page()
elif page == "Grading System":
  grading_system_page()
elif page == "User Guide":
  user_guide_page()
elif page == "About":
  about_page()

# JavaScript Bridge (simulate message-passing from links)
st.markdown("""
<script>
    window.addEventListener("message", (event) => {
        if (event.data === "Grading System") {
            parent.postMessage({streamlitSetComponentValue: {"page": "Grading System"}}, "*");
        } else if (event.data === "User Guide") {
            parent.postMessage({streamlitSetComponentValue: {"page": "User Guide"}}, "*");
        } else if (event.data === "About") {
            parent.postMessage({streamlitSetComponentValue: {"page": "About"}}, "*");
        }
    });
</script>
""", unsafe_allow_html=True)
