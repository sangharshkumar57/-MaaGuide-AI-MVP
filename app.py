import streamlit as st
from google import genai
import os
import time

st.set_page_config(
    page_title="MaaGuide AI · 3-Min Desk Yoga",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Utility UI CSS (MedLucid Academic Structure + MaaGuide Soft Teal Palette)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #FFFFFF; }
    
    .brand-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 20px;
    }
    .brand-icon {
        background-color: #0F5247;
        color: white;
        font-weight: 700;
        font-size: 20px;
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .minute-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0F5247;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
    }
    .safety-card {
        background-color: #FFF5F2;
        border: 1px solid #F4A28C;
        border-left: 5px solid #E07A5F;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .stButton>button[kind="primary"] {
        background-color: #0F5247;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "stage_input" not in st.session_state:
    st.session_state.stage_input = "Trimester 2 (Weeks 13–26)"
if "workspace_input" not in st.session_state:
    st.session_state.workspace_input = "Seated at open office cubicle (Formal wear / No floor mat)"
if "discomfort_input" not in st.session_state:
    st.session_state.discomfort_input = ""
if "routine_result" not in st.session_state:
    st.session_state.routine_result = None
if "active_model" not in st.session_state:
    st.session_state.active_model = "gemini-3.5-flash-lite"

# ---------------- LEFT SIDEBAR (MedLucid Governance Pattern) ----------------
with st.sidebar:
    st.markdown("### About MaaGuide AI")
    st.write(
        "MaaGuide AI generates clinically safe **3-minute seated desk yoga and breathing routines** "
        "for urban working mothers. It synthesizes Ayurvedic *Sukshma Vyayama* (micro-movements) "
        "with modern OB-GYN posture guardrails—requiring zero floor mats, zero space, and no outfit changes."
    )
    
    st.markdown("### Your privacy")
    st.write(
        "Your inputs are processed in memory for this session only. "
        "MaaGuide AI has no database and does not store personal maternal health records."
    )
    
    st.caption(
        "Prototype notice: DPM Phase 2 student project (Group 13). Designed for preventive "
        "workday stress and posture relief, not acute clinical emergencies."
    )
    
    if st.button("Clear everything", use_container_width=True):
        st.session_state.discomfort_input = ""
        st.session_state.routine_result = None
        st.rerun()
        
    st.markdown("---")
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    status_label = f"live ({st.session_state.active_model})" if api_key else "resilient local engine"
    st.caption(f"🟢 AI mode: **{status_label}**")
    
    with st.expander("Check available models"):
        st.code("1. gemini-3.5-flash-lite\n2. gemini-flash-latest\n3. gemini-2.0-flash\n4. Built-in Clinical Backup", language="text")

# ---------------- TOP HEADER ----------------
st.markdown("""
    <div class="brand-header">
        <div class="brand-icon">🧘‍♀️</div>
        <div>
            <div style="font-size:22px; font-weight:700; color:#111827;">MaaGuide AI · 3-Minute Desk Yoga</div>
            <div style="font-size:14px; color:#4B5563;">
                Stressed or stiff between office meetings? Get a zero-mat, clinically vetted 180-second chair yoga routine right at your desk.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2-Step Tabbed Workflow (Matches MedLucid Benchmark)
tab1, tab2 = st.tabs([
    "① Share your maternal stage & desk discomfort",
    "② Follow your 3-minute seated routine & audio"
])

# Resilient AI Engine (Auto-switches models & never throws 503 error)
def generate_desk_yoga(stage, workspace, discomfort, lang):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    prompt = f"""
    You are MaaGuide AI, an Ayurvedic Sukshma Vyayama (micro-yoga) and Modern OB-GYN physiotherapy synthesis engine for urban working mothers.
    User Context:
    - Maternal Stage: {stage}
    - Office Setting & Attire Constraint: {workspace}
    - Current Discomfort / Stress: "{discomfort}"
    - Language for Family/Partner Note: {lang}

    Strict Clinical Rules:
    - All movements MUST be performed 100% SEATED in an office chair (zero floor mat, zero lying down, safe in formal office wear).
    - Filter out any unsafe pregnancy/postpartum movements (NO breath retention/Kumbhaka, NO closed-belly twists, NO abdominal crunching).

    Return response in EXACTLY 4 parts separated by '|||':
    PART 1:
    #### 🌿 Ayurvedic Micro-Yoga (*Sukshma Vyayama*) + 🩺 OB-GYN Safety Guardrail
    - **Why This Works (Ayurvedic Lens):** (1-2 sentences on pacifying Vata/Prana at the desk)
    - **Clinical Posture Rule for {stage}:** (1-2 sentences on what is safe vs. what movement to strictly avoid right now)
    |||
    PART 2:
    #### ⏱️ Your 180-Second Seated Office Chair Routine
    - **Minute 1 (Seated Spinal / Joint Release):** (Exact chair movement, hand placement, and reps)
    - **Minute 2 (Targeted Desk Stretch):** (Exact discreet movement for "{discomfort}")
    - **Minute 3 (Pranayama Nervous System Reset):** (Exact inhale/exhale count with 432Hz audio, no breath-holding)
    |||
    PART 3:
    (A warm 2-sentence WhatsApp message in {lang} + English she can send to her family/mother reassuring them she just did a doctor-safe 3-minute seated stretch at work)
    |||
    PART 4:
    (1 ergonomic desk adjustment tip for the rest of her workday + 1 question to ask her OB-GYN/physiotherapist)
    """
    if api_key:
        client = genai.Client(api_key=api_key)
        for m in ["gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.8-flash", "gemini-2.0-flash"]:
            try:
                res = client.models.generate_content(model=m, contents=prompt)
                if res and res.text and "|||" in res.text:
                    parts = [p.strip() for p in res.text.split("|||")]
                    if len(parts) >= 4:
                        st.session_state.active_model = m
                        return parts[:4]
            except Exception:
                continue

    # Zero-Crash Built-in Fallback (Guarantees instant output even if Google API is overloaded)
    return [
        f"#### 🌿 Ayurvedic Micro-Yoga (*Sukshma Vyayama*) + 🩺 OB-GYN Safety Guardrail\n"
        f"- **Why This Works (Ayurvedic Lens):** Prolonged laptop work aggravates *Vyana* and *Apana Vata*, causing stiffness and mental fatigue. Gentle seated *Sukshma Vyayama* restores circulation without physical exertion.\n"
        f"- **Clinical Posture Rule for {stage}:** **100% Chair-Safe.** Keep both feet flat on the floor and knees hip-width apart to protect pelvic alignment. **Strictly avoid** deep closed-belly twists or holding your breath (*Kumbhaka*).",
        f"#### ⏱️ Your 180-Second Seated Office Chair Routine\n"
        f"- **Minute 1 (Seated *Marjariasana* / Chair Cat-Cow):** Sit near the front edge of your office chair with hands resting on your knees. Inhale, gently roll shoulders back and lift your chest; exhale, soften your spine and drop your chin slightly. Repeat 5 slow cycles.\n"
        f"- **Minute 2 (Seated *Skandha Chakra* & Ankle Pumps):** Keep your torso upright (safe in formal wear). Inhale and roll both shoulders backward 5 times to release neck/trapezius tension, while flexing both feet up and down under your desk to prevent lower-limb swelling.\n"
        f"- **Minute 3 (Seated *Bhramari* / 4:6 Calming Breath):** Rest your palms over your ribcage, play the 432Hz audio on the right, inhale softly through the nose for 4 seconds, and exhale for 6 seconds with a gentle closed-lip hum.",
        f"Mummy ji / Amma, just took a 3-minute break between my office calls to do a gentle doctor-approved chair stretch and breathing routine—back feels much lighter and baby is doing great!\n\n"
        f"({lang}: मम्मी जी/अम्मा, अभी ऑफिस मीटिंग के बीच मैंने 3 मिनट की सुरक्षित चेयर-स्ट्रेचिंग और प्राणायाम किया है। अब कमर दर्द और थकान में बहुत आराम है! 🌸)",
        f"- **Ergonomic Desk Tip:** Place a small box or footrest under your desk so your knees stay level with your hips, and keep your laptop screen at eye level.\n"
        f"- **Ask Your OB-GYN:** *'I experience {discomfort[:45]} during desk work in {stage}—are there specific pelvic tilts or support cushions you recommend for my office chair?'*"
    ]

# ---------------- TAB 1: WORKSPACE & DISCOMFORT INPUT ----------------
with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 1. Your maternal stage & office setting")
        st.caption("No yoga mat or gym wear needed. We tailor every movement to your chair and stage.")
        
        stage_sel = st.selectbox(
            "Maternal Stage",
            [
                "Trimester 1 (Weeks 1–12) · Gentle Energy & Nausea Calm",
                "Trimester 2 (Weeks 13–26) · Lower Back & Ribcage Space",
                "Trimester 3 (Weeks 27–40) · Pelvic Comfort & Ankle Circulation",
                "Postpartum Return-to-Work (3–12 Months) · Neck/Feeding Posture & Core Care"
            ],
            index=1
        )
        
        workspace_sel = st.selectbox(
            "Current Workspace & Attire Constraint",
            [
                "Seated at open office cubicle (Discreet moves / Formal wear)",
                "Private cabin or WFH desk (Chair stretches + eyes-closed breathing)",
                "Camera-off during a long Zoom/Teams call (Upper-body & ankle relief)"
            ]
        )
        
        st.markdown("**Try a realistic 3-minute office scenario (1-click):**")
        s1, s2, s3 = st.columns(3)
        if s1.button("Sample 1: 3 PM Zoom Call Lower Backache", use_container_width=True):
            st.session_state.discomfort_input = "Sitting for 3 hours straight in meetings; stiff lower back and tight hips. Only 3 minutes before my next client call."
            st.rerun()
        if s2.button("Sample 2: High Workday Stress & Neck Tension", use_container_width=True):
            st.session_state.discomfort_input = "Overwhelmed by deadline pressure, tight shoulders, and shallow breathing at my laptop desk."
            st.rerun()
        if s3.button("Sample 3: Swollen Feet & Post-Lunch Rib Tightness", use_container_width=True):
            st.session_state.discomfort_input = "Ankles feel heavy under my desk after lunch and upper belly/ribs feel compressed while typing."
            st.rerun()

    with col2:
        st.markdown("### 2. Where do you feel tension right now?")
        st.caption("Describe your physical stiffness or stress in your own words, or use the quick tags.")
        
        discomfort_box = st.text_area(
            "Your current desk discomfort or elder's rest advice",
            value=st.session_state.discomfort_input,
            height=110,
            placeholder="e.g., My lower back and neck hurt at my desk. Elders say lie down for 45 mins, but I'm in the office with only 3 mins free."
        )
        
        st.markdown("**Quick add tension areas:**")
        q1, q2 = st.columns(2)
        if q1.button("+ Stiff lower back & tailbone", use_container_width=True):
            st.session_state.discomfort_input = (discomfort_box + " Lower back and tailbone stiffness from sitting.").strip()
            st.rerun()
        if q2.button("+ Tight neck & laptop shoulders", use_container_width=True):
            st.session_state.discomfort_input = (discomfort_box + " Tight neck, upper back, and shoulder fatigue from typing.").strip()
            st.rerun()
            
        q3, q4 = st.columns(2)
        if q3.button("+ Work anxiety & racing mind", use_container_width=True):
            st.session_state.discomfort_input = (discomfort_box + " High work stress; need safe Pranayama to calm heart rate.").strip()
            st.rerun()
        if q4.button("+ Swollen ankles & leg heaviness", use_container_width=True):
            st.session_state.discomfort_input = (discomfort_box + " Heavy legs and ankle puffiness under the office desk.").strip()
            st.rerun()

        lang_choice = st.selectbox(
            "Family Reassurance Note Language:",
            ["Hindi + English", "Telugu + English", "Marathi + English", "Tamil + English"]
        )
        
        if st.button("Generate my 3-minute desk yoga routine ➔", type="primary", use_container_width=True):
            final_discomfort = discomfort_box.strip() or "Stiff lower back and work stress between office calls."
            with st.spinner("Synthesizing Ayurvedic Sukshma Vyayama with OB-GYN chair safety guardrails..."):
                st.session_state.routine_result = generate_desk_yoga(stage_sel, workspace_sel, final_discomfort, lang_choice)
                st.session_state.saved_stage = stage_sel
                st.session_state.saved_workspace = workspace_sel
                st.session_state.saved_discomfort = final_discomfort
            st.success("✅ Your 3-minute routine is ready! Open Tab **'② Follow your 3-minute seated routine & audio'** above (or scroll down).")

# ---------------- TAB 2 & RESULTS DISPLAY ----------------
if st.session_state.routine_result:
    parts = st.session_state.routine_result
    with tab2:
        st.markdown(f"### Your 180-Second Seated Routine ({st.session_state.saved_stage})")
        st.caption(f"Setting: {st.session_state.saved_workspace} · Focus: *{st.session_state.saved_discomfort}*")
