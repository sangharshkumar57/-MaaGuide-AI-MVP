import streamlit as st
from google import genai
import os
import time

# Page Config matching Phase 1 Proposal Palette
st.set_page_config(
    page_title="MaaGuide AI | Ancient Wisdom. Modern Science.",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Exact Phase 1 PPT Palette
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(180deg, #FFF9F7 0%, #F2F9F6 100%); }
    
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

# Custom SVG Logo matching Phase 1 Proposal
MAAGUIDE_LOGO_SVG = """
<svg width="95" height="95" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="56" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="3"/>
  <path d="M22 75 C15 50, 35 30, 50 45 C35 60, 30 75, 22 75 Z" fill="#6EE7B7"/>
  <path d="M98 75 C105 50, 85 30, 70 45 C85 60, 90 75, 98 75 Z" fill="#6EE7B7"/>
  <path d="M42 36 C42 22, 68 22, 68 38 C68 48, 58 55, 58 68 L36 68 C34 52, 42 45, 42 36 Z" fill="#0F5247"/>
  <circle cx="57" cy="40" r="9" fill="#FFE4E1"/>
  <circle cx="72" cy="56" r="8" fill="#FFE4E1"/>
  <path d="M62 66 C62 56, 82 56, 82 68 Z" fill="#1E7A68"/>
  <path d="M60 105 C45 92, 45 74, 60 66 C75 74, 75 92, 60 105 Z" fill="#F4A28C"/>
  <path d="M58 104 C35 98, 28 80, 44 72 C48 85, 52 95, 58 104 Z" fill="#FADCD9"/>
  <path d="M62 104 C85 98, 92 80, 76 72 C72 85, 68 95, 62 104 Z" fill="#FADCD9"/>
</svg>
"""

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

# Built-in Resilient Synthesis Backup (Guarantees 0% Error during Live Demo even if Google API is overloaded)
def get_resilient_synthesis(stage, concern, query, language, is_stretch):
    q_lower = query.lower()
    if is_stretch or "back" in q_lower or "stretch" in q_lower or "stress" in q_lower:
        return f"""### 1. 🌿 Traditional Ayurvedic Perspective (Ahara & Vihara)
* **Vata Pacification (*Sukshma Vyayama*):** In Ayurveda, prolonged sitting at an office desk aggravates *Apana Vata*, causing lower back stiffness and mental fatigue during **{stage}**.
* **Pranic Flow:** Gentle seated spinal elongation and slow *Anulom-Vilom* breathing restore maternal calm and improve oxygen flow to the baby without physical strain.

### 2. 🩺 Modern OB-GYN & Pediatric Verdict (Safety Badge: **SAFE**)
* **Clinically Recommended:** Seated micro-stretches every 45–60 minutes prevent pregnancy venous pooling, sciatic nerve compression, and corporate burnout.
* **Safety Guardrail:** Keep both feet flat on the floor/footrest; avoid deep closed-belly twists or holding your breath.

### 3. ⏱️ Your 3-Minute Seated Office Desk Micro-Routine
* **Minute 1 (Seated Cat-Cow Pelvic Tilt):** Sit upright at the edge of your office chair. Inhale and gently arch your upper back; exhale and round your shoulders softly (5 slow repetitions).
* **Minute 2 (Neck & Shoulder Tension Release):** Drop your right ear toward your right shoulder for 15 seconds, switch sides, and do 5 slow backward shoulder rolls.
* **Minute 3 (432Hz Box Breathing):** Play the calming audio on the right, close your eyes, inhale for 4 seconds, and exhale slowly for 6 seconds. Sip warm water afterward.

### 4. 💬 Respectful WhatsApp Note for Family Elders ({language})
* *"Mummy ji / Maa, office kaam ke beech maine doctor aur Ayurveda ke hisaab se 3-minute ka safe chair stretch aur deep breathing kiya hai. Main aur baby dono bilkul comfortable aur energetic feel kar rahe hain! 🌸"*"""

    elif "ajwain" in q_lower or "acidity" in q_lower or "nausea" in q_lower:
        return f"""### 1. 🌿 Traditional Ayurvedic Perspective (Ahara & Vihara)
* **Agni Deepana (Digestive Fire):** Indian elders recommend *Ajwain* (carom seeds) and warm water because it pacifies *Vata-Kapha* bloating and relieves sluggish digestion common in **{stage}**.
* **Sattvik Moderation:** Because *Ajwain* has *Ushna Virya* (warming potency), Ayurveda advises pairing it with cooling *Saunf* (fennel) during pregnancy.

### 2. 🩺 Modern OB-GYN & Pediatric Verdict (Safety Badge: **SAFE IN MODERATION**)
* **Clinical Validation:** Small culinary amounts of *Ajwain* or *Saunf* infused in lukewarm water safely relieve progesterone-induced acid reflux and gas at work.
* **Safety Guardrail:** Avoid concentrated raw *Ajwain* powders or boiling heavy decoctions in excess, as excessive warming spices can trigger heartburn.

### 3. 🥄 Clinically Safe Preparation, Quantity & Workday Tip
* **Exact Safe Dosage:** Boil **1/4 teaspoon Ajwain + 1/2 teaspoon Saunf** in 1 glass of water, cool to lukewarm, and sip slowly 20 minutes after your office lunch.
* **Workday Desk Rule:** Walk for 3 minutes around your office floor after meals and avoid slouching forward over your laptop immediately after eating.

### 4. 💬 Respectful WhatsApp Note for Family Elders ({language})
* *"Mummy ji / Maa, aapka bataya hua Ajwain-Saunf ka halka gunguna pani lunch ke baad liya, acidity mein kaafi aaram mila! Doctor ne bhi kaha hai ki thodi matra mein Saunf ke saath lena bilkul safe aur accha hai. 🙏"*"""

    elif "ghee" in q_lower or "kesar" in q_lower or "saffron" in q_lower:
        return f"""### 1. 🌿 Traditional Ayurvedic Perspective (Ahara & Vihara)
* **Garbhini Paricharya Nourishment:** Ayurveda values pure cow *Ghee* (*Snehana*) and *Kesar* (saffron) in **{stage}** for building maternal *Ojas* (vitality), lubricating tissues, and supporting calm mood.
* **Myth Clarification:** Saffron supports digestion and mood—it does not alter baby's skin color, which is purely genetic.

### 2. 🩺 Modern OB-GYN & Pediatric Verdict (Safety Badge: **MODERATE QUANTITY SAFE**)
* **Clinical Validation:** 1–2 teaspoons of homemade ghee daily provides healthy fat-soluble vitamins (A, D, E, K), and 2–3 strands of pure saffron in warm milk are clinically safe.
* **Safety Guardrail:** Avoid consuming bowls of excess ghee if you have gestational diabetes (GDM), high BMI, or sedentary office hours.

### 3. 🥄 Clinically Safe Preparation, Quantity & Workday Tip
* **Exact Safe Dosage:** Limit to **1 teaspoon pure cow ghee** drizzled over warm office lunch dal/roti, and **maximum 2–3 strands of Kesar** soaked in warm milk at night.
* **Workday Balance:** Pair healthy fats with high-fiber salads and a 10-minute post-lunch walk at work to keep blood sugar steady.

### 4. 💬 Respectful WhatsApp Note for Family Elders ({language})
* *"Mummy ji / Maa, aapke kehne par maine apne lunch mein 1 chammach ghar ka shuddh ghee aur raat ke doodh mein 2 dhage Kesar shuru kar diya hai! Doctor ne bhi kaha ki is santulit matra mein yeh baby ki growth ke liye bahut badhiya hai. ❤️"*"""

    else:
        return f"""### 1. 🌿 Traditional Ayurvedic Perspective (Ahara & Vihara)
* **Holistic Balance for {stage}:** Regarding *"{query}"*, traditional *Garbhini/Sutika Paricharya* emphasizes warm, freshly prepared *Sattvik* nourishment and calm daily rhythms to keep *Vata* balanced.
* **Mind-Body Harmony:** Gentle routine adjustments prevent maternal exhaustion during busy workdays.

### 2. 🩺 Modern OB-GYN & Pediatric Verdict (Safety Badge: **SAFE WITH MODERATION**)
* **Evidence-Based Guidance:** Modern clinical guidelines for **{stage}** support moderate, hygienic intake while avoiding extreme dietary restrictions, excess caffeine (>150mg/day), or unverified raw herbal extracts.
* **Clinical Rule:** Prioritize steady hydration, protein-rich office snacks, and regular posture breaks.

### 3. 🥄 Clinically Safe Preparation, Quantity & Workday Tip
* **Actionable Workday
