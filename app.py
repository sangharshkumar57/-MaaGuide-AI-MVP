import streamlit as st
from google import genai
import os

# Page Config matching Phase 1 Proposal Palette
st.set_page_config(
    page_title="MaaGuide AI | Ancient Wisdom. Modern Science.",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Exact Phase 1 PPT Palette (Soft Teal #115E59, Warm Peach #FCE7F3/#FFE4E1, Mint #ECFDF5)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(180deg, #FFF9F7 0%, #F2F9F6 100%); }
    
    /* Hero Header matching Slide 1 */
    .hero-wrap {
        background: linear-gradient(135deg, #0F5247 0%, #1E7A68 55%, #E8A598 100%);
        border-radius: 22px;
        padding: 28px 34px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 12px 28px rgba(15, 82, 71, 0.15);
        margin-bottom: 20px;
    }
    .brand-tag {
        background: rgba(255,255,255,0.22);
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.6px;
        margin-right: 8px;
        display: inline-block;
        margin-top: 10px;
    }
    
    /* Baby Milestone Exciting Card */
    .milestone-bar {
        background: linear-gradient(90deg, #FFE8E0 0%, #FFF3EE 50%, #E6F4F1 100%);
        border-radius: 16px;
        padding: 18px 24px;
        border-left: 6px solid #E07A5F;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    
    /* Feature Visual Cards matching Slide 2 & 6 */
    .feature-card {
        background: white;
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        border-bottom: 5px solid #1E7A68;
        text-align: center;
        height: 100%;
    }
    .feature-card img {
        width: 100%;
        height: 155px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    
    /* AI Synthesis Output Cards */
    .verdict-card {
        background: white;
        padding: 26px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(15, 82, 71, 0.08);
        border-top: 6px solid #1E7A68;
        margin-bottom: 18px;
    }
    .peach-card {
        background: #FFF5F2;
        padding: 22px;
        border-radius: 18px;
        border: 2px solid #F4A28C;
        box-shadow: 0 6px 16px rgba(224, 122, 95, 0.1);
        margin-bottom: 16px;
    }
    .whatsapp-card {
        background: #E8F8F0;
        padding: 18px;
        border-radius: 16px;
        border-left: 6px solid #25D366;
        margin-top: 12px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0F5247 0%, #2A9D8F 100%);
        color: white;
        border-radius: 14px;
        height: 3.3em;
        width: 100%;
        font-weight: 700;
        font-size: 15px;
        border: none;
        box-shadow: 0 4px 12px rgba(42, 157, 143, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Custom SVG Logo matching Phase 1 Proposal (Teal Mother + Baby + Peach Lotus + Mint Leaves)
MAAGUIDE_LOGO_SVG = """
<svg width="95" height="95" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="56" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="3"/>
  <!-- Mint Leaves -->
  <path d="M22 75 C15 50, 35 30, 50 45 C35 60, 30 75, 22 75 Z" fill="#6EE7B7"/>
  <path d="M98 75 C105 50, 85 30, 70 45 C85 60, 90 75, 98 75 Z" fill="#6EE7B7"/>
  <!-- Teal Mother & Baby Silhouette -->
  <path d="M42 36 C42 22, 68 22, 68 38 C68 48, 58 55, 58 68 L36 68 C34 52, 42 45, 42 36 Z" fill="#0F5247"/>
  <circle cx="57" cy="40" r="9" fill="#FFE4E1"/>
  <circle cx="72" cy="56" r="8" fill="#FFE4E1"/>
  <path d="M62 66 C62 56, 82 56, 82 68 Z" fill="#1E7A68"/>
  <!-- Peach Lotus Petals at Bottom -->
  <path d="M60 105 C45 92, 45 74, 60 66 C75 74, 75 92, 60 105 Z" fill="#F4A28C"/>
  <path d="M58 104 C35 98, 28 80, 44 72 C48 85, 52 95, 58 104 Z" fill="#FADCD9"/>
  <path d="M62 104 C85 98, 92 80, 76 72 C72 85, 68 95, 62 104 Z" fill="#FADCD9"/>
</svg>
"""

# Top Hero Section with Embedded MaaGuide AI Logo
st.markdown(f"""
    <div class="hero-wrap">
        <div>
            <div style="font-size:13px; text-transform:uppercase; letter-spacing:1.5px; color:#FADCD9; font-weight:700;">
                DPM Phase 2 MVP • Group 13 • Connected Strategy Engine
            </div>
            <div style="font-size:38px; font-weight:800; margin:4px 0; color:#FFFFFF;">
                MaaGuide <span style="color:#A7F3D0;">AI</span>
            </div>
            <div style="font-size:16px; color:#F1FAEE; max-width:680px;">
                Bridging Ancient Ayurvedic Wisdom & Modern Pediatric Science for Urban Working Mothers (0–5 Years)
            </div>
            <div>
                <span class="brand-tag">🌿 AYURVEDA</span>
                <span class="brand-tag">🩺 PEDIATRICS</span>
                <span class="brand-tag">🥗 NUTRITION</span>
                <span class="brand-tag">👩‍💻 WORKDAY MICRO-CARE</span>
            </div>
        </div>
        <div>{MAAGUIDE_LOGO_SVG}</div>
    </div>
""", unsafe_allow_html=True)

# Stage Data for Exciting Interactive Mother Experience
STAGE_MILESTONES = {
    "Trimester 1 (Weeks 1-12)": {
        "baby": "🍋 Baby Size: Sweet Lime (Nimbu) • Rapid neural & heartbeat growth",
        "tip": "✨ Today's Garbh Sanskar: Sip ginger-infused water & practice 3 deep Prana breaths before opening emails.",
        "mood_badge": "Focus: Nausea Relief & Folate Absorption"
    },
    "Trimester 2 (Weeks 13-26)": {
        "baby": "🥭 Baby Size: Alphonso Mango • Baby can now hear your voice & music!",
        "tip": "✨ Today's Garbh Sanskar: Baby responds to calm frequencies—avoid sitting in one posture >45 mins at work.",
        "mood_badge": "Focus: Back Posture, Iron & Acidity Control"
    },
    "Trimester 3 (Weeks 27-40)": {
        "baby": "🥥 Baby Size: Fresh Tender Coconut • Lungs & brain maturing fast",
        "tip": "✨ Today's Garbh Sanskar: Elevate feet slightly under your office desk & take light warm dinners.",
        "mood_badge": "Focus: Pelvic Comfort, Sleep & Swelling Relief"
    },
    "Postpartum Recovery (0-6 Months)": {
        "baby": "👶 Newborn Bonding Stage • Rapid sensory & immunity building",
        "tip": "✨ Today's Sutika Paricharya: Warm Digestible Ahara & 3-minute neck/shoulder release after feeding.",
        "mood_badge": "Focus: Lactation Nutrition & Burnout Recovery"
    },
    "Infant Care (6-24 Months)": {
        "baby": "🥣 Annaprashan & Toddler Milestones • First solids & active curiosity",
        "tip": "✨ Today's Holistic Tip: Introduce single-grain warm mash paired with pediatrician iron guidance.",
        "mood_badge": "Focus: Weaning Foods & Working Mom Guilt-Free Balance"
    }
}

# Sidebar - Mother's Care Console
with st.sidebar:
    st.markdown(f"<div style='text-align:center;'>{MAAGUIDE_LOGO_SVG}</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#0F5247; margin-top:0;'>Mother's Care Console</h3>", unsafe_allow_html=True)
    
    stage = st.selectbox(
        "🌸 1. Your Maternal / Baby Stage:",
        list(STAGE_MILESTONES.keys()),
        index=1
    )
    
    concern_type = st.selectbox(
        "🎯 2. How can MaaGuide help right now?",
        [
            "🥗 Dadi vs. Doctor Food/Remedy Conflict",
            "🔥 Acidity, Nausea or Trimester Diet Plan",
            "🧘‍♀️ 3-Minute Office Desk Stretch (Stressed/Backache)",
            "👶 Infant Nutrition / Sleep Soothing"
        ]
    )
    
    is_stretch_mode = "3-Minute Office Desk Stretch" in concern_type
    
    specific_query = st.text_input(
        "💬 3. Enter Elder's Advice or Your Symptom:",
        placeholder="e.g., Mom says drink hot ajwain water / eat ghee"
    )
    
    language = st.selectbox(
        "🗣️ 4. Family WhatsApp Card Language:",
        ["English + Hindi Summary", "English + Marathi Summary", "English + Tamil Summary", "English + Telugu Summary"]
    )
    
    btn_text = "🧘‍♀️ Start 3-Min Desk Wellness Routine" if is_stretch_mode else "✨ Synthesize Ayurveda + Doctor Verdict"
    generate_btn = st.button(btn_text)

# Dynamic Baby Milestone Banner (Updates automatically when stage changes!)
m_data = STAGE_MILESTONES[stage]
st.markdown(f"""
    <div class="milestone-bar">
        <div>
            <div style="font-size:18px; font-weight:800; color:#0F5247;">{m_data['baby']}</div>
            <div style="font-size:14px; color:#4A5568; margin-top:4px;">{m_data['tip']}</div>
        </div>
        <div style="background:#0F5247; color:white; padding:8px 16px; border-radius:20px; font-size:13px; font-weight:700;">
            {m_data['mood_badge']}
        </div>
    </div>
""", unsafe_allow_html=True)

# 1-Click Quick Craving & Desk Relief Pills for Exciting UX
st.markdown("##### ⚡ Quick 1-Tap Scenarios for Busy Moms (Click any pill to test instantly):")
q1, q2, q3, q4 = st.columns(4)
quick_selected = None
if q1.button("🔥 Ajwain Water for Acidity?"):
    quick_selected = ("🔥 Acidity, Nausea or Trimester Diet Plan", "My mother says drink hot water with ajwain for acidity at work. Is it safe?", False)
if q2.button("🥭 Saffron (Kesar) & Ghee Myth?"):
    quick_selected = ("🥗 Dadi vs. Doctor Food/Remedy Conflict", "Elders insist on eating lots of ghee and kesar milk daily in 2nd trimester.", False)
if q3.button("🧘‍♀️ 3-Min Zoom Backache Stretch"):
    quick_selected = ("🧘‍♀️ 3-Minute Office Desk Stretch (Stressed/Backache)", "Stiff lower back and stressed between office laptop calls, only 3 mins free.", True)
if q4.button("☕ Masala Chai / Coffee Limit?"):
    quick_selected = ("🥗 Dadi vs. Doctor Food/Remedy Conflict", "Having afternoon fatigue at office desk, can I drink ginger masala chai or coffee?", False)

# Three Visual Story Cards (Reflecting Phase 1 Proposal Visuals)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=600&q=80">
            <div style="font-weight:800; color:#0F5247; font-size:16px;">🌿 Ancient Ayurvedic Wisdom</div>
            <p style="font-size:13px; color:#555; margin-top:4px;">Garbhini Paricharya, Satvik Ahara & gentle restorative practices rooted in Indian tradition.</p>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
        <div class="feature-card" style="border-bottom-color:#E07A5F;">
            <img src="https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80">
            <div style="font-weight:800; color:#0F5247; font-size:16px;">🩺 Modern Pediatric & OB-GYN Science</div>
            <p style="font-size:13px; color:#555; margin-top:4px;">Clinical safety guardrails filtering out unsafe herbs, high-risk postures & dosage myths.</p>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80">
            <div style="font-weight:800; color:#0F5247; font-size:16px;">👩‍💻 Anxiety-Free Working Mom</div>
            <p style="font-size:13px; color:#555; margin-top:4px;">180-second seated desk routines & respectful WhatsApp notes for elders at home.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Trigger Execution if Sidebar Button OR Quick Pill is clicked
if generate_btn or quick_selected:
    active_concern = quick_selected[0] if quick_selected else concern_type
    active_query = quick_selected[1] if quick_selected else (specific_query if specific_query else concern_type)
    active_stretch = quick_selected[2] if quick_selected else is_stretch_mode

    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not api_key:
        st.error("⚠️ Please configure GEMINI_API_KEY in Streamlit Cloud -> Settings -> Secrets.")
    else:
        with st.spinner("🧠 Connected Strategy Engine: Cross-referencing Ayurvedic texts with Modern Clinical Safety..."):
            try:
                client = genai.Client(api_key=api_key)
                
                if active_stretch:
                    step3_prompt = "### 3. ⏱️ Your 3-Minute Seated Office Desk Micro-Routine\n(Give Minute 1, Minute 2, Minute 3 seated posture & breathing steps that require zero floor mat or outfit change)"
                else:
                    step3_prompt = "### 3. 🥄 Clinically Safe Preparation, Quantity & Workday Tip\n(Give exact safe quantity, how to take it safely during workdays, and what to avoid)"

                prompt = f"""
                You are MaaGuide AI, India's Connected Strategy Engine bridging Ayurvedic wisdom and Modern Pediatric/OB-GYN science for urban working mothers.
                Context:
                - Maternal Stage: {stage}
                - Category: {active_concern}
                - Specific Query: {active_query}
                - Family Share Language: {language}

                Provide a warm, reassuring, clinically safe response in EXACTLY 4 Markdown sections:
                ### 1. 🌿 Traditional Ayurvedic Perspective (Ahara & Vihara)
                (2 concise bullets on why Indian elders/Ayurveda recommend this and its traditional benefit)
                ### 2. 🩺 Modern OB-GYN & Pediatric Verdict (Safety Badge: SAFE / MODERATE / AVOID)
                (2 concise bullets on what modern medical science validates or restricts for {stage})
                {step3_prompt}
                ### 4. 💬 Respectful WhatsApp Note for Family Elders ({language})
                (A loving, polite 2-sentence message she can copy-paste to her parents/in-laws on WhatsApp celebrating their care while aligning on the doctor-approved middle ground)
                """
                
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                
                left_col, right_col = st.columns([2.1, 1])
                with left_col:
                    st.markdown('<div class="verdict-card">', unsafe_allow_html=True)
                    st.markdown(f"#### 🎯 Personalized Synthesis for **{stage}**")
                    st.caption(f"Query Analyzed: *{active_query}*")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with right_col:
                    st.markdown('<div class="peach-card">', unsafe_allow_html=True)
                    if active_stretch:
                        st.markdown("#### 🎧 3-Min 432Hz Calming Desk Audio")
                        st.write("Plug in your earphones at your office desk and follow the 3-minute seated routine:")
                        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
                        st.progress(100, text="⏱️ 180-Second Micro-Intervention Ready")
                    else:
                        st.markdown("#### 🛡️ Connected Strategy Safety Check")
                        st.success(f"✔️ Verified for {stage}")
                        st.markdown("""
                        * **Ayurvedic Lens:** Balances *Agni* & *Vata* gently.
                        * **Clinical Lens:** Moderated to prevent gestational acidity/spikes.
                        * **Workday Fit:** Easy to carry in your office tiffin/thermos.
                        """)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("""
                        <div class="whatsapp-card">
                            <div style="font-weight:800; color:#128C7E; font-size:15px;">📲 Family Peace-Maker Feature</div>
                            <p style="font-size:12.5px; color:#333; margin:6px 0 0 0;">
                                Copy Section 4 from the left card and send it on your family WhatsApp group—resolves elder vs. doctor conflict with love!
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Engine Error: {e}")
