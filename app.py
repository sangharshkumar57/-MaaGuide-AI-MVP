import streamlit as st
from google import genai
import os
import time
import io
import wave
import struct
import math

st.set_page_config(
    page_title="MaaGuide AI · 3-Min Desk Yoga",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .brand-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 12px;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 16px;
    }
    .brand-icon {
        background-color: #0F5247;
        color: white;
        font-weight: 700;
        font-size: 22px;
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
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

# Built-in 432Hz Calming Audio Generator (Never fails or gets blocked!)
@st.cache_data
def generate_432hz_audio(duration_sec=30):
    sample_rate = 22050
    num_samples = duration_sec * sample_rate
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            # Soothing 432Hz + 216Hz warm harmonic with gentle breathing pulse (10s cycle)
            breath_envelope = 0.55 + 0.3
