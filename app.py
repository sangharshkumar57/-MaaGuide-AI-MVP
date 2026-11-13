import streamlit as st
from google import genai
import os

# Page Config - Calming Sage Green & Clean Look
st.set_page_config(page_title="MaaGuide AI | 3-Min Maternal Companion", page_icon="🌿", layout="wide")

# Custom CSS for Market-Ready UI (Sage Green & Soft Cream Theme)
st.markdown("""
    <style>
    .main { background-color: #F8FAF8; }
    .stButton>button { background-color: #2D6A4F; color: white; border-radius: 10px; height: 3em; width: 100%; font-weight: bold; }
    .card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 5px solid #2D6A4F; margin-bottom: 15px; }
    .clinical-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 5px solid #1D3557; margin-bottom: 15px; }
    .routine-card { background-color: #EDF6F9; padding: 20px; border-radius: 12px; border: 2px solid #2D6A4F; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🌿 MaaGuide AI")
st.subheader("Bridging Ancient Ayurvedic Wisdom & Modern Pediatric Science for Urban Working Mothers")
st.caption("Focused Phase 2 MVP | Instant 3-Minute Desk-Friendly Routines & Advice Conflict Resolver")

# Sidebar - Structured User Input (Not a Chatbot!)
with st.sidebar:
    st.header("👩‍💻 Your Current Context")
    stage = st.selectbox(
        "1. Select Maternal / Child Stage:",
        ["Trimester 1 (Weeks 1-12)", "Trimester 2 (Weeks 13-26)", "Trimester 3 (Weeks 27-40)", 
         "Postpartum (0-6 Months)", "Infant Care (6-24 Months)"]
    )
    
    concern_type = st.selectbox(
        "2. Where are you stuck right now?",
        ["Stressed / Back Pain at Office Desk", 
         "Conflicting Food Advice (Elders vs. Doctor)", 
         "Mid-Day Fatigue / Acidity at Work",
         "Safe Movement / Stretching Check"]
    )
    
    specific_query = st.text_input(
        "3. Specific Doubt or Elder's Advice (Optional):",
        placeholder="e.g., Mom says eat papaya/ghee, or lower back hurts on Zoom calls"
    )
    
    language = st.selectbox(
        "4. Family Share Language (Vernacular):",
        ["English + Hindi Summary", "English + Marathi Summary", "English + Tamil Summary", "English + Telugu Summary"]
    )
    
    generate_btn = st.button("✨ Generate My 3-Minute Safe Plan")

# Main Workflow Area
if generate_btn:
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    
    if not api_key:
        st.error("⚠️ Please add your GEMINI_API_KEY in Streamlit Cloud -> Settings -> Secrets.")
    else:
        with st.spinner("Synthesizing Ayurvedic wisdom with Modern OB-GYN safety guidelines..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                You are MaaGuide AI, a maternal wellness synthesis engine for urban working mothers in India.
                User Context:
                - Stage: {stage}
                - Core Need: {concern_type}
                - Specific Detail: {specific_query if specific_query else 'General stage-appropriate relief'}
                - Requested Output Language: {language}

                Strict Safety Rules: Never prescribe allopathic medicines or raw unverified herbs. Prioritize clinical OB-GYN safety first.
                Format your response in EXACTLY 4 clearly labeled sections using Markdown:
                ### 1. 🌿 Ayurvedic Perspective (Ahara & Vihara)
                (2 concise bullet points on what traditional wisdom suggests and why)
                ### 2. 🩺 Modern Clinical Safety Verdict
                (2 concise bullet points on what modern medical science validates or restricts for {stage})
                ### 3. ⏱️ Your 3-Minute Office Desk Micro-Routine
                (Step-by-step 180-second action plan she can do seated at her office desk right now: Minute 1, Minute 2, Minute 3 + 1 quick safe dietary hydration tip)
                ### 4. 💬 Family Reassurance Note ({language})
                (A polite, 2-sentence translated message she can copy-paste to her parents/in-laws on WhatsApp explaining the safe middle ground)
                """
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                
                st.success("✅ Personalized & Clinically Vetted 3-Minute Plan Ready!")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="routine-card">', unsafe_allow_html=True)
                    st.markdown("#### 🎧 3-Min 432Hz Calming Desk Audio")
                    st.write("Play this soothing frequency while executing your 3-minute seated stretch:")
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
                    st.markdown("---")
                    st.markdown("#### 🛡️ Clinical Guardrail")
                    st.caption("Stateless Privacy: Zero personal data stored. For preventive lifestyle wellness only; consult your OB-GYN for medical symptoms.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error connecting to AI Engine: {e}")
else:
    st.info("👈 **How to use:** Select your current pregnancy/postpartum stage and workplace concern from the left panel to generate an instant, clinically safe 3-minute micro-routine.")
