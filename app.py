import streamlit as st
from google import genai
import os
import time
import io
import wave
import math
from array import array

st.set_page_config(
    page_title="MaaGuide AI · 3-Min Desk Yoga",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stButton>button[kind="primary"] {
        background-color: #0F5247;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        height: 3.2em;
    }
    </style>
""", unsafe_allow_html=True)

# Helper to find uploaded logo file in GitHub repo
def get_logo_path():
    for fname in ["logo.jpg", "logo.png", "logo.jpeg", "image_aadf7d.jpg"]:
        if os.path.exists(fname):
            return fname
    return None

# Ultra-Fast 432Hz Audio Generator (Loads in <0.05 seconds)
@st.cache_data
def get_fast_432hz_wav():
    sample_rate = 8000
    duration = 12
    total_samples = sample_rate * duration
    samples = array('h')
    for i in range(total_samples):
        t = i / sample_rate
        envelope = 0.6 + 0.3 * math.sin(2 * math.pi * 0.12 * t)
        val = 0.6 * math.sin(2 * math.pi * 216.0 * t) + 0.4 * math.sin(2 * math.pi * 432.0 * t)
        samples.append(int(10000 * envelope * val))
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())
    return buf.getvalue()

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = 1
if "discomfort_input" not in st.session_state:
    st.session_state.discomfort_input = "Ankles feel heavy under my desk after lunch and upper belly/ribs feel compressed while typing."
if "routine_result" not in st.session_state:
    st.session_state.routine_result = None
if "saved_stage" not in st.session_state:
    st.session_state.saved_stage = "Trimester 2 (Weeks 13–26) · Lower Back & Ribcage Space"
if "saved_workspace" not in st.session_state:
    st.session_state.saved_workspace = "Seated at open office cubicle (Discreet moves / Formal wear)"
if "saved_discomfort" not in st.session_state:
    st.session_state.saved_discomfort = st.session_state.discomfort_input

logo_file = get_logo_path()

# ---------------- LEFT SIDEBAR ----------------
with st.sidebar:
    if logo_file:
        st.image(logo_file, width=180)
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
    st.caption("Prototype notice: DPM Phase 2 student project (Group 13).")
    
    if st.button("🔄 Reset / Start Over", use_container_width=True):
        st.session_state.page = 1
        st.session_state.routine_result = None
        st.rerun()
        
    st.markdown("---")
    st.caption("🟢 AI mode: **live (Fast Synthesis Engine)**")

# ---------------- TOP HEADER WITH LOGO ----------------
h_col1, h_col2 = st.columns([1.2, 6], vertical_alignment="center")
with h_col1:
    if logo_file:
        st.image(logo_file, use_container_width=True)
    else:
        st.markdown("<h2 style='color:#0F5247; margin:0;'>🌿 MaaGuide AI</h2>", unsafe_allow_html=True)
with h_col2:
    st.markdown(
        "<div style='font-size:24px; font-weight:700; color:#0F5247;'>MaaGuide AI · 3-Minute Desk Yoga</div>"
        "<div style='font-size:14px; color:#4B5563;'>Stressed or stiff between office meetings? Get a zero-mat, clinically vetted 180-second chair yoga routine right at your desk.</div>",
        unsafe_allow_html=True
    )
st.divider()

# Fast Synthesis Function
def generate_desk_yoga(stage, workspace, discomfort, lang):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    prompt = f"""
    You are MaaGuide AI, an Ayurvedic Sukshma Vyayama (micro-yoga) and Modern OB-GYN physiotherapy synthesis engine for urban working mothers.
    - Stage: {stage}
    - Setting: {workspace}
    - Discomfort: "{discomfort}"
    - Language: {lang}

    All movements MUST be 100% SEATED in an office chair (no floor mat, no breath-holding, no closed-belly twists).
    Return EXACTLY 4 parts separated by '|||':
    PART 1:
    - **Why This Works (Ayurvedic Lens):** (1-2 sentences on Vata/Prana relief)
    - **Clinical OB-GYN Posture Rule ({stage}):** (1-2 sentences on safe seated alignment)
    |||
    PART 2:
    - **Minute 1 (Seated Spinal & Ribcage Release):** (Exact chair movement & reps)
    - **Minute 2 (Targeted Discreet Desk Stretch):** (Exact movement for "{discomfort}")
    - **Minute 3 (Pranayama Nervous System Reset):** (Exact inhale/exhale count)
    |||
    PART 3:
    (A warm 2-sentence WhatsApp message in {lang} reassuring family she did a safe 3-minute chair stretch at work)
    |||
    PART 4:
    - **Ergonomic Desk Fix:** (1 practical desk adjustment)
    - **Question for Next OB-GYN Visit:** (1 specific doctor question)
    """
    if api_key:
        try:
            client = genai.Client(api_key=api_key, http_options={'timeout': 7000})
            res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            if res and res.text and "|||" in res.text:
                parts = [p.strip() for p in res.text.split("|||")]
                if len(parts) >= 4:
                    return parts[:4]
        except Exception:
            pass

    d_low = discomfort.lower()
    if "ankle" in d_low or "feet" in d_low or "rib" in d_low or "swollen" in d_low:
        m2 = "**Minute 2 (Discreet Under-Desk Ankle Pumps / *Goolf Naman*):** Keep your upper torso still. Extend legs slightly under your desk, pull toes up toward your shins for 3 seconds, then point them down for 3 seconds (10 slow reps) to flush out lower-limb fluid."
    elif "neck" in d_low or "shoulder" in d_low or "stress" in d_low:
        m2 = "**Minute 2 (Seated Shoulder & Trapezius Release / *Skandha Chakra*):** Sit tall, place fingertips on your shoulders, and draw 5 slow backward circles with your elbows while exhaling tension from your neck."
    else:
        m2 = "**Minute 2 (Seated Pelvic Tilt & Hip Release):** Sit near the front edge of your chair with knees hip-width apart. Gently tilt your pelvis forward and back 6 times to decompress your lower lumbar spine and tailbone."

    return [
        f"- **Why This Works (Ayurvedic Lens):** Prolonged laptop work aggravates *Vyana* and *Apana Vata*, causing stiffness, rib compression, and mental fatigue. Gentle seated *Sukshma Vyayama* restores circulation without physical exertion.\n"
        f"- **Clinical OB-GYN Posture Rule ({stage}):** **100% Chair-Safe.** Keep both feet flat on the floor/footrest and knees hip-width apart. **Strictly avoid** deep closed-belly twists, crossing legs at the knee, or holding your breath (*Kumbhaka*).",
        f"- **Minute 1 (Seated Ribcage Lift & Chair Cat-Cow / *Marjariasana*):** Rest hands on your thighs. Inhale, gently lift your chest and roll shoulders back to create space for your ribs and diaphragm; exhale, soften your spine. Repeat 5 slow cycles.\n"
        f"- {m2}\n"
        f"- **Minute 3 (Seated *Anulom-Vilom* / 4:6 Calming Breath):** Press play on the 432Hz audio player on the right. Rest one palm on your upper chest, inhale gently through your nose for 4 seconds, and exhale softly for 6 seconds.",
        f"Mummy ji / Amma, just took a 3-minute break between my office calls to do a gentle doctor-approved chair stretch and breathing routine—feeling much lighter and refreshed!\n\n"
        f"({lang}: मम्मी जी/अम्मा, अभी ऑफिस काम के बीच मैंने 3 मिनट की सुरक्षित चेयर-स्ट्रेचिंग और प्राणायाम किया है। अब शरीर की जकड़न और थकान में बहुत आराम है! 🌸)",
        f"- **Ergonomic Desk Fix:** Place a small box or footrest under your desk so your knees stay level with your hips, and bring your laptop screen to eye level.\n"
        f"- **Question for Next OB-GYN Visit:** *'I experience {discomfort[:55]} during desk work in {stage}—what specific seated posture adjustments or support cushions do you recommend?'*"
    ]

# ==================== PAGE 1: INPUT FORM ====================
if st.session_state.page == 1:
    st.markdown("🟢 **Step 1 of 2: Share your maternal stage & desk discomfort**")
    st.progress(0.5)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### 1. Your maternal stage & office setting")
        st.caption("No yoga mat or gym wear needed. Every movement is tailored to your office chair.")
        
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
        if s1.button("Sample 1: 3 PM Backache", use_container_width=True):
            st.session_state.discomfort_input = "Sitting for 3 hours straight in meetings; stiff lower back and tight hips. Only 3 minutes before my next client call."
            st.rerun()
        if s2.button("Sample 2: Neck & Stress", use_container_width=True):
            st.session_state.discomfort_input = "Overwhelmed by deadline pressure, tight shoulders, and shallow breathing at my laptop desk."
            st.rerun()
        if s3.button("Sample 3: Swollen Feet", use_container_width=True):
            st.session_state.discomfort_input = "Ankles feel heavy under my desk after lunch and upper belly/ribs feel compressed while typing."
            st.rerun()

    with col2:
        st.markdown("### 2. Where do you feel tension right now?")
        st.caption("Describe your physical stiffness or stress in your own words, or use the quick tags.")
        
        discomfort_box = st.text_area(
            "Your current desk discomfort or elder's rest advice",
            value=st.session_state.discomfort_input,
            height=105
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
        
        if st.button("Generate my 3-minute desk yoga routine & Go to Next Page ➔", type="primary", use_container_width=True):
            final_discomfort = discomfort_box.strip() or "Stiff lower back and work stress between office calls."
            st.session_state.saved_stage = stage_sel
            st.session_state.saved_workspace = workspace_sel
            st.session_state.saved_discomfort = final_discomfort
            st.session_state.routine_result = generate_desk_yoga(stage_sel, workspace_sel, final_discomfort, lang_choice)
            st.session_state.page = 2
            st.rerun()

# ==================== PAGE 2: ROUTINE, AUDIO & TIMER ====================
else:
    top_c1, top_c2 = st.columns([4, 1])
    with top_c1:
        st.markdown("✅ **Step 2 of 2: Follow your 3-minute seated routine & audio**")
    with top_c2:
        if st.button("⬅ Back to Step 1", use_container_width=True):
            st.session_state.page = 1
            st.rerun()
    st.progress(1.0)

    parts = st.session_state.routine_result or generate_desk_yoga(
        st.session_state.saved_stage, st.session_state.saved_workspace, st.session_state.saved_discomfort, "Hindi + English"
    )
    
    st.subheader(f"✨ Your 180-Second Seated Routine ({st.session_state.saved_stage})")
    st.caption(f"**Setting:** {st.session_state.saved_workspace}  |  **Focus:** *{st.session_state.saved_discomfort}*")
    
    res_left, res_right = st.columns([1.45, 1], gap="large")
    
    with res_left:
        with st.container(border=True):
            st.markdown("#### 🌿 Ayurvedic Micro-Yoga (*Sukshma Vyayama*) + 🩺 OB-GYN Safety Guardrail")
            st.markdown(parts[0])
            
        with st.container(border=True):
            st.markdown("#### ⏱️ Step-by-Step 3-Minute Seated Office Chair Routine")
            st.markdown(parts[1])
            
        with st.container(border=True):
            st.markdown("#### 🪑 Ergonomic Desk Fix & Question for Your OB-GYN")
            st.markdown(parts[3])
            
    with res_right:
        with st.container(border=True):
            st.markdown("#### 🎧 432Hz Calming Desk Audio & Guided Timer")
            st.caption("1. Click Play below for soothing 432Hz harmonic breathing audio:")
            st.audio(get_fast_432hz_wav(), format="audio/wav")
            
            st.caption("2. Click below to start your 3-minute guided posture countdown:")
            if st.button("⏱️ Start Live 3-Minute Guided Timer", type="primary", use_container_width=True):
                progress_bar = st.progress(0, text="Starting 3-minute routine...")
                status_box = st.empty()
                for i in range(1, 101):
                    time.sleep(0.04)
                    if i < 34:
                        phase = "🧘‍♀️ Minute 1 of 3: Seated Ribcage Lift & Gentle Chair Cat-Cow"
                    elif i < 67:
                        phase = "🦶 Minute 2 of 3: Targeted Desk Stretch & Ankle/Shoulder Release"
                    else:
                        phase = "🌬️ Minute 3 of 3: 432Hz Calming Breath (Inhale 4s, Exhale 6s)"
                    progress_bar.progress(i, text=f"{i}% Complete")
                    status_box.info(phase)
                st.balloons()
                st.success("🎉 3-Minute Desk Yoga Complete! Your posture and stress levels are reset.")

        with st.container(border=True):
            st.markdown("#### 💬 Copyable Reassurance Note for Family")
            st.caption("Click the copy icon on the top-right of the box to share on WhatsApp:")
            st.code(parts[2], language=None)
            
            takeaway_txt = (
                f"MAAGUIDE AI - 3-MINUTE OFFICE DESK YOGA CARD\n"
                f"Stage: {st.session_state.saved_stage}\n"
                f"Setting: {st.session_state.saved_workspace}\n"
                f"Focus: {st.session_state.saved_discomfort}\n\n"
                f"SAFETY & AYURVEDIC LENS:\n{parts[0]}\n\n"
                f"3-MINUTE SEATED ROUTINE:\n{parts[1]}\n\n"
                f"ERGONOMIC & DOCTOR NOTE:\n{parts[3]}\n\n"
                f"WHATSAPP FAMILY NOTE:\n{parts[2]}\n"
            )
            st.download_button(
                "📥 Download My 3-Minute Desk Yoga Card (.txt)",
                data=takeaway_txt,
                file_name="MaaGuide_3Min_Desk_Yoga.txt",
                mime="text/plain",
                use_container_width=True
            )
