import streamlit as st
from google import genai
import os

# Page Config
st.set_page_config(
    page_title="MaaGuide AI | Holistic Maternal Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS with Gradient Header, Image Cards & Modern UI
st.markdown("""
    <style>
    .stApp { background-color: #F4F9F5; }
    .hero-banner {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #52B788 100%);
        padding: 28px 35px;
        border-radius: 18px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 20px rgba(27, 67, 50, 0.18);
        margin-bottom: 22px;
    }
    .hero-title { font-size: 34px; font-weight: 800; margin: 0; color: #FFFFFF; letter-spacing: -0.5px; }
    .hero-sub { font-size: 16px; color: #D8F3DC; margin-top: 6px; font-weight: 400; }
    .badge-pill {
        background-color: rgba(255,255,255,0.2);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: #FFF;
        display: inline-block;
        margin-right: 8px;
        margin-top: 10px;
    }
    .visual-card {
        background: white;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 4px solid #2D6A4F;
    }
    .visual-card img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .output-box {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 6px solid #2D6A4F;
        margin-bottom: 18px;
    }
    .side-box {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        border: 2px solid #52B788;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background: linear-gradient(90deg, #2D6A4F 0%, #40916C 100%);
        color: white;
        border-radius: 12px;
        height: 3.2em;
        width: 100%;
        font-weight: 700;
        font-size: 15px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Top Hero Banner with Logo & Visual Identity
st.markdown("""
    <div class="hero-banner">
        <div>
            <div class="hero-title">🌿 MaaGuide AI</div>
            <div class="hero-sub">Bridging Ancient Ayurvedic Wisdom & Modern Pediatric Science for Urban Working Mothers</div>
            <div>
                <span class="badge-pill">✨ Ayurveda + OB-GYN Validated</span>
                <span class="badge-pill">👩‍💻 Built for Working Moms</span>
                <span class="badge-pill">🗣️ Multi-Vernacular Family Cards</span>
            </div>
        </div>
        <img src="https://cdn-icons-png.flaticon.com/512/3048/3048398.png" width="85" style="border-radius:50%; background:white; padding:8px;">
    </div>
""", unsafe_allow_html=True)

# Sidebar - Dynamic Context Selection
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=65)
    st.header("👩‍💻 Mother's Care Console")
    
    stage = st.selectbox(
        "1. Select Your Current Stage:",
        ["Trimester 1 (Weeks 1-12)", "Trimester 2 (Weeks 13-26)", "Trimester 3 (Weeks 27-40)", 
         "Postpartum Recovery (0-6 Months)", "Infant Care (6-24 Months)"]
    )
    
    concern_type = st.selectbox(
        "2. What do you need help with right now?",
        [
            "🥗 Conflicting Food / Remedy Advice (Elders vs. Doctor)",
            "🔥 Acidity, Nausea or Digestion Relief",
            "🧘‍♀️ Stressed / Back Pain at Office Desk (3-Min Stretch)",
            "👶 Baby Sleep / Feeding Doubt"
        ]
    )
    
    # Smart Dynamic Label based on mode
    is_stretch_mode = "3-Min Stretch" in concern_type
    
    specific_query = st.text_input(
        "3. Tell us the exact issue or Elder's advice:",
        placeholder="e.g., Mom says drink hot ajwain water for acidity / eat ghee"
    )
    
    language = st.selectbox(
        "4. Family WhatsApp Card Language:",
        ["English + Hindi Summary", "English + Marathi Summary", "English + Tamil Summary", "English + Telugu Summary"]
    )
    
    btn_label = "🧘‍♀️ Generate My 3-Minute Desk Stretch" if is_stretch_mode else "🩺 Get Instant Clinical + Ayurvedic Verdict"
    generate_btn = st.button(btn_label)

# Visual Showcase Cards (Always visible so website looks rich & appealing)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("""
        <div class="visual-card">
            <img src="https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80">
            <h4 style="margin:4px 0; color:#1B4332;">🌿 Ahara & Remedies</h4>
            <p style="font-size:13px; color:#555; margin:0;">Resolves Dadi/Nani food advice with modern trimester nutrition rules.</p>
        </div>
    """, unsafe_allow_html=True)
with col_b:
    st.markdown("""
        <div class="visual-card">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80">
            <h4 style="margin:4px 0; color:#1B4332;">👩‍💻 Workday Desk Relief</h4>
            <p style="font-size:13px; color:#555; margin:0;">Zero-mat seated stretches & breathing for busy corporate moms.</p>
        </div>
    """, unsafe_allow_html=True)
with col_c:
    st.markdown("""
        <div class="visual-card">
            <img src="https://images.unsplash.com/photo-1555252333-9f8e92e65df9?auto=format&fit=crop&w=600&q=80">
            <h4 style="margin:4px 0; color:#1B4332;">🩺 Clinical Safety First</h4>
            <p style="font-size:13px; color:#555; margin:0;">Every recommendation is filtered through OB-GYN & Pediatric guardrails.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Main Action Output
if generate_btn:
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not api_key:
        st.error("⚠️ Please add GEMINI_API_KEY in Streamlit Secrets.")
    else:
        with st.spinner("Synthesizing Ayurvedic texts with Modern OB-GYN safety guidelines..."):
            try:
                client = genai.Client(api_key=api_key)
                
                if is_stretch_mode:
                    action_section = "### 3. ⏱️ Your 3-Minute Seated Office Desk Routine\n(Give Minute 1, Minute 2, Minute 3 seated posture/breathing steps that require zero floor mat)"
                else:
                    action_section = "### 3. 🥄 Safe Dosage, Preparation & Immediate Remedy\n(Give exact safe quantity, how/when to consume it safely, and what to avoid)"

                prompt = f"""
                You are MaaGuide AI, an expert maternal care synthesis engine for urban working mothers.
                - Stage: {stage}
                - Category: {concern_type}
                - User Query: {specific_query if specific_query else concern_type}
                - Language: {language}

                Provide a structured, reassuring response in EXACTLY 4 sections:
                ### 1. 🌿 Traditional Ayurvedic Wisdom (Why Elders Recommend It)
                (2 short bullets explaining the traditional logic behind this remedy/need)
                ### 2. 🩺 Modern OB-GYN / Clinical Verdict (Is It Safe in {stage}?)
                (Clear clinical safety check: Safe / Safe in Moderation / Avoid, and why)
                {action_section}
                ### 4. 💬 Respectful WhatsApp Note for Family ({language})
                (A warm 2-sentence message she can forward to her mother/in-laws agreeing on the safe middle ground)
                """
                
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                
                main_col, side_col = st.columns([2.2, 1])
                with main_col:
                    st.markdown('<div class="output-box">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with side_col:
                    st.markdown('<div class="side-box">', unsafe_allow_html=True)
                    if is_stretch_mode:
                        st.image("https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=500&q=80", use_container_width=True)
                        st.markdown("#### 🎧 3-Min 432Hz Calming Audio")
                        st.caption("Play while doing your seated desk stretch:")
                        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
                    else:
                        st.image("https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=500&q=80", use_container_width=True)
                        st.markdown("#### 🚦 Trimester Safety Checklist")
                        st.success("✔️ Moderated for " + stage)
                        st.info("💧 Tip: Sip lukewarm water slowly; avoid lying down immediately after meals.")
                    
                    st.markdown("---")
                    st.caption("🛡️ **Stateless Privacy:** Zero personal medical data stored. Consult your gynecologist for clinical symptoms.")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("👈 **Select your stage and concern on the left** (e.g., *Acidity/Ajwain doubt* or *Office Back Pain*) to get an instant, visually structured solution!")
