import streamlit as st
import joblib
import numpy as np
from datetime import datetime
from modules.agriculture_nlp import (
    predict_agriculture_symptom,
    clean_text,
    get_model_status
)
from sentence_transformers import SentenceTransformer
import os

from modules.weather import (
    get_weather,
    weather_description,
    get_coordinates
)
import pandas as pd
from modules.yield_prediction import predict_yield
from modules.disease_detection import predict_disease
from modules.chatbot import get_chatbot_response


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DISEASE_INFO_PATH = os.path.join(
    BASE_DIR,
    "data",
    "disease_information.csv"
)

disease_info_df = pd.read_csv(DISEASE_INFO_PATH)

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AgriMind AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# HTML HELPER
# =========================================================

def show_html(content):
    st.html(content)


def show_sidebar_html(content):
    st.sidebar.html(content)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);


/* =====================================================
   GLOBAL
   ===================================================== */

html,
body,
[class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(46,125,50,0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(76,175,80,0.08),
            transparent 30%
        ),
        #f5faf7;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}


/* =====================================================
   NORMAL TEXT
   ===================================================== */

.stApp p,
.stApp span,
.stApp label,
.stApp div {
    color: #173d25;
}

/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(53, 153, 77, 0.18),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #062a15 0%,
            #073d1d 52%,
            #052512 100%
        ) !important;

    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar content spacing */

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.7rem;
}

/* Navigation heading */

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: rgba(255,255,255,0.60) !important;

    font-size: 10px !important;

    font-weight: 800 !important;

    letter-spacing: 1.4px;

    text-transform: uppercase;

    margin: 5px 8px 8px;
}

/* Navigation options */

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 12px;

    padding: 9px 10px;

    margin: 3px 4px;

    transition: all 0.18s ease;
}

/* Hover effect */

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.08);

    transform: translateX(2px);
}

/* Selected navigation */

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background:
        linear-gradient(
            90deg,
            rgba(55,180,88,0.24),
            rgba(55,180,88,0.07)
        );

    box-shadow:
        inset 3px 0 0 #63d77c;
}

/* Navigation text */

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 13px;

    font-weight: 600;
}

/* Sidebar divider */

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15);

    margin: 15px 8px;
}

/* =====================================================
   HERO
   ===================================================== */

.hero {
    position: relative;
    overflow: hidden;

    padding: 45px 48px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            #0c351b 0%,
            #176b36 50%,
            #2e8b57 100%
        );

    color: white !important;

    box-shadow:
        0 18px 45px rgba(15,70,35,0.20);

    margin-bottom: 28px;
}

.hero * {
    color: white !important;
}

.hero-small {
    color: #bceac7 !important;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 48px;
    margin: 8px 0 10px 0;
    font-weight: 800;
    color: white !important;
}

.hero-text {
    font-size: 16px;
    color: #e7f6eb !important;
    max-width: 850px;
    line-height: 1.7;
    margin: 0;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.section-title {
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #173d25 !important;

    margin-top: 30px;
    margin-bottom: 17px;

    line-height: 1.4;
}


/* =====================================================
   STAT CARDS
   ===================================================== */

.stat-card {
    background: white;

    border-radius: 20px;

    padding: 22px;

    border: 1px solid #deebe1;

    box-shadow:
        0 8px 25px rgba(25,70,35,0.07);

    min-height: 125px;
}

.stat-card * {
    color: #173d25 !important;
}

.stat-icon {
    font-size: 28px;
}

.stat-number {
    font-size: 29px;
    font-weight: 800;
    color: #14532d !important;
    margin-top: 4px;
}

.stat-label {
    font-size: 12px;
    color: #718078 !important;
    margin-top: 2px;
}


/* =====================================================
   FEATURE CARDS
   ===================================================== */

.feature-card {
    background: white;

    padding: 28px;

    border-radius: 22px;

    border: 1px solid #e0ece3;

    min-height: 230px;

    box-shadow:
        0 8px 28px rgba(22,65,35,0.06);
}

.feature-card * {
    color: #173d25 !important;
}

.feature-icon {
    font-size: 42px;
}

.feature-title {
    font-size: 20px;
    font-weight: 800;
    color: #173d25 !important;
    margin-top: 10px;
}

.feature-text {
    color: #64746a !important;
    line-height: 1.65;
    font-size: 14px;
}


/* =====================================================
   INFO CARDS
   ===================================================== */

.info-card {
    background: white;

    padding: 24px;

    border-radius: 20px;

    border: 1px solid #e0ece3;

    min-height: 165px;

    box-shadow:
        0 7px 22px rgba(30,75,40,0.05);

    margin-bottom: 15px;
}

.info-card h3 {
    color: #173d25 !important;
    margin-top: 0;
    font-size: 18px;
}

.info-card p {
    color: #64746a !important;
    line-height: 1.65;
    font-size: 14px;
}


/* =====================================================
   RESULT CARD
   ===================================================== */

.result-card {
    background:
        linear-gradient(
            135deg,
            #ffffff,
            #eff9f2
        );

    border: 1px solid #cce2d1;

    border-radius: 24px;

    padding: 28px;

    margin-top: 20px;

    box-shadow:
        0 12px 32px rgba(25,70,35,0.09);
}

.result-card * {
    color: #173d25 !important;
}

.result-title {
    color: #718078 !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.result-value {
    color: #14532d !important;
    font-size: 32px;
    font-weight: 800;
    margin-top: 6px;
}

.result-confidence {
    color: #2e7d32 !important;
    font-size: 30px;
    font-weight: 800;
    margin-top: 5px;
}


/* =====================================================
   AI BADGE
   ===================================================== */

.ai-badge {
    display: inline-block;

    background: #e2f5e7;

    color: #176b36 !important;

    border-radius: 30px;

    padding: 7px 15px;

    font-size: 12px;
    font-weight: 700;

    margin-bottom: 12px;
}


/* =====================================================
   PREDICTION ROW
   ===================================================== */

.prediction-row {
    background: white;

    border: 1px solid #e0ece3;

    border-radius: 15px;

    padding: 14px 18px;

    margin-bottom: 8px;

    box-shadow:
        0 4px 14px rgba(30,70,40,0.04);
}

.prediction-row * {
    color: #173d25 !important;
}


/* =====================================================
   INPUTS
   ===================================================== */

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] span {
    color: #173d25 !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] {
    background: white !important;
}

div[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid #cfe0d3 !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] * {
    color: #173d25 !important;
}

div[data-testid="stNumberInput"] input {
    background: white !important;
    color: #173d25 !important;
    border: 1px solid #cfe0d3 !important;
    border-radius: 12px !important;
}

div[data-testid="stNumberInput"] button {
    color: #173d25 !important;
    background: white !important;
}

div[data-testid="stTextArea"] textarea {
    border-radius: 16px !important;

    border: 1px solid #cfe0d3 !important;

    background: white !important;

    color: #173d25 !important;

    padding: 15px !important;

    font-size: 15px !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #7a897f !important;
}


/* =====================================================
   FILE UPLOADER
   ===================================================== */

[data-testid="stFileUploader"] {
    background: white !important;

    border-radius: 16px !important;

    border: 1px solid #d8e8dc !important;

    padding: 10px !important;
}

[data-testid="stFileUploader"] * {
    color: #173d25 !important;
}


/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {
    border-radius: 13px !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #176b36,
            #2e8b57
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    min-height: 48px;

    box-shadow:
        0 7px 18px rgba(35,120,65,0.18);

    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 10px 25px rgba(35,120,65,0.25);
}

.stButton > button p,
.stButton > button span {
    color: white !important;
}


/* =====================================================
   WEATHER BUTTON
   ===================================================== */

.weather-button-area {
    text-align: center;
    margin: 10px 0 20px 0;
}

.weather-button-area p {
    color: #64746a !important;
}


/* =====================================================
   REAL WEATHER MAIN CARD
   ===================================================== */

.weather-main-card {
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #1674a5 0%,
            #2697c8 45%,
            #63c5e8 100%
        );

    border-radius: 28px;

    padding: 30px;

    margin-top: 20px;

    color: white !important;

    box-shadow:
        0 15px 40px rgba(20,100,145,0.20);
}

.weather-main-card * {
    color: white !important;
}

.weather-location {
    font-size: 18px;
    font-weight: 700;
}

.weather-date {
    font-size: 13px;
    opacity: 0.85;
    margin-top: 4px;
}

.weather-condition {
    font-size: 18px;
    font-weight: 600;
    margin-top: 8px;
}

.weather-temperature {
    font-size: 76px;
    line-height: 1;
    font-weight: 800;
    margin-top: 18px;
}

.weather-feels {
    font-size: 14px;
    opacity: 0.9;
    margin-top: 8px;
}

.weather-big-icon {
    font-size: 85px;
    text-align: center;
    padding-top: 15px;
}


/* =====================================================
   WEATHER DETAIL CARDS
   ===================================================== */

.weather-detail-card {
    background: white;

    border: 1px solid #dce9df;

    border-radius: 18px;

    padding: 20px;

    min-height: 120px;

    box-shadow:
        0 7px 20px rgba(30,70,40,0.06);
}

.weather-detail-icon {
    font-size: 27px;
}

.weather-detail-value {
    color: #14532d !important;
    font-size: 24px;
    font-weight: 800;
    margin-top: 7px;
}

.weather-detail-label {
    color: #718078 !important;
    font-size: 12px;
    margin-top: 4px;
}


/* =====================================================
   FORECAST
   ===================================================== */

.forecast-card {
    background: white;

    border: 1px solid #dce9df;

    border-radius: 18px;

    padding: 17px 10px;

    text-align: center;

    min-height: 190px;

    box-shadow:
        0 6px 18px rgba(30,70,40,0.06);

    transition: 0.2s ease;
}

.forecast-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 10px 25px rgba(30,70,40,0.10);
}

.forecast-day {
    color: #14532d !important;
    font-size: 13px;
    font-weight: 800;
}

.forecast-date {
    color: #718078 !important;
    font-size: 11px;
    margin-top: 3px;
}

.forecast-icon {
    font-size: 38px;
    margin: 12px 0;
}

.forecast-condition {
    color: #52705b !important;
    font-size: 11px;
    min-height: 30px;
}

.forecast-temp {
    color: #14532d !important;
    font-size: 16px;
    font-weight: 800;
    margin-top: 10px;
}

.forecast-rain {
    color: #2586b5 !important;
    font-size: 11px;
    margin-top: 7px;
}


/* =====================================================
   ADVISORY
   ===================================================== */

.advisory-card {
    background:
        linear-gradient(
            135deg,
            #e8f5e9,
            #f1f8f3
        );

    border: 1px solid #c8e6c9;

    border-left: 5px solid #2e7d32;

    border-radius: 14px;

    padding: 16px 20px;

    margin-bottom: 12px;

    color: #173d25;

    font-size: 14px;

    line-height: 1.6;

    box-shadow:
        0 5px 15px rgba(25,70,35,0.06);
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;

    color: #7a897f !important;

    font-size: 13px;

    padding: 40px 20px 20px 20px;
}

.footer * {
    color: #7a897f !important;
}


/* =====================================================
   FLOATING CHATBOT
   ===================================================== */

.st-key-floating_chat_button {
    position: fixed;
    right: 25px;
    bottom: 25px;
    z-index: 999999;
}

.st-key-floating_chat_button button {
    width: 65px;
    height: 65px;

    border-radius: 50% !important;

    background:
        linear-gradient(
            135deg,
            #2e7d32,
            #66bb6a
        ) !important;

    color: white !important;

    border: 3px solid white !important;

    font-size: 28px !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.35);
}


/* =====================================================
   CHAT WINDOW
   ===================================================== */
.st-key-floating_chat_window {
    position: fixed;

    right: 25px;
    bottom: 100px;

    width: 380px;
    height: 560px;

    z-index: 999998;

    background: rgba(255,255,255,0.97);

    backdrop-filter: blur(18px);

    border-radius: 22px;

    border: 1px solid rgba(255,255,255,0.7);

    box-shadow:
        0 15px 50px rgba(0,0,0,0.30);

    padding: 0.5rem;

    overflow-y: auto;
    overflow-x: hidden;

    scrollbar-width: thin;
}

/* =====================================================
   CHAT HEADER
   ===================================================== */

.chat-header {
    background:
        linear-gradient(
            135deg,
            #14532d,
            #2e7d32
        );

    color: white;

    padding: 16px 18px;

    border-radius: 17px 17px 10px 10px;

    margin-bottom: 10px;
}

.chat-header-title {
    font-size: 20px;
    font-weight: 800;
    color: white !important;
}

.chat-header-status {
    font-size: 12px;
    opacity: 0.85;
    color: white !important;
}


/* =====================================================
   HIDE STREAMLIT DEFAULT UI
   ===================================================== */
/* HIDE STREAMLIT DEFAULT UI */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
header {
    visibility: hidden;
    }

    
/* DO NOT HIDE HEADER COMPLETELY */

/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .hero {
        padding: 30px 25px;
    }

    .hero-title {
        font-size: 35px;
    }

    .hero-text {
        font-size: 14px;
    }

    .weather-temperature {
        font-size: 55px;
    }

    .weather-big-icon {
        font-size: 60px;
    }

    .st-key-floating_chat_window {
        right: 10px;
        left: 10px;
        bottom: 90px;
        width: auto;
    }
}



/* =========================================================
   AGRIMIND PREMIUM UI OVERRIDES
   ========================================================= */

:root {
    --agri-dark: #083b1b;
    --agri-green: #137a35;
    --agri-mid: #239b4b;
    --agri-light: #eaf7ed;
    --agri-text: #163b23;
    --agri-muted: #6c7f72;
}

/* ---------- APP CANVAS ---------- */
.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(77, 180, 102, .10), transparent 25%),
        radial-gradient(circle at 5% 55%, rgba(38, 151, 72, .07), transparent 24%),
        #f7faf8 !important;
}

.block-container {
    max-width: 1220px !important;
    padding-top: 1.15rem !important;
    padding-bottom: 2rem !important;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 50% 0%, rgba(53, 153, 77, .18), transparent 28%),
        linear-gradient(180deg, #062a15 0%, #073d1d 52%, #052512 100%) !important;
    border-right: 1px solid rgba(255,255,255,.08) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.7rem !important;
}

[data-testid="stSidebar"] hr {
    margin: 12px 8px !important;
    border-color: rgba(255,255,255,.10) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: rgba(255,255,255,.60) !important;
    font-size: 10px !important;
    font-weight: 800 !important;
    letter-spacing: 1.4px !important;
    text-transform: uppercase !important;
    margin: 5px 8px 8px !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 12px !important;
    padding: 9px 10px !important;
    margin: 3px 4px !important;
    transition: all .18s ease !important;
    background: transparent !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.08) !important;
    transform: translateX(2px);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(55,180,88,.24), rgba(55,180,88,.07)) !important;
    box-shadow: inset 3px 0 0 #63d77c !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* ---------- HERO ---------- */
.hero {
    min-height: 225px !important;
    padding: 32px 38px !important;
    margin-bottom: 20px !important;
    border-radius: 26px !important;
    background:
        radial-gradient(circle at 88% 20%, rgba(126,235,148,.20), transparent 20%),
        radial-gradient(circle at 72% 100%, rgba(77,190,101,.16), transparent 28%),
        linear-gradient(135deg, #07391b 0%, #0e6c31 50%, #23934a 100%) !important;
    box-shadow: 0 18px 45px rgba(8,75,31,.18) !important;
}

.hero::after {
    content: "🌾";
    position: absolute;
    right: 40px;
    bottom: 12px;
    font-size: 108px;
    opacity: .16;
    filter: blur(.2px);
    transform: rotate(-8deg);
}

.hero-small {
    font-size: 11px !important;
    letter-spacing: 2.1px !important;
    opacity: .86;
}

.hero-title {
    font-size: clamp(36px, 4vw, 52px) !important;
    line-height: 1.03 !important;
    margin: 9px 0 12px !important;
    letter-spacing: -1.5px !important;
}

.hero-text {
    font-size: 14px !important;
    line-height: 1.65 !important;
    max-width: 760px !important;
    opacity: .92;
}

/* ---------- SECTION TITLES ---------- */
.section-title {
    font-size: 22px !important;
    margin-top: 20px !important;
    margin-bottom: 8px !important;
    letter-spacing: -.3px !important;
}

/* ---------- STATS ---------- */
.stat-card {
    position: relative !important;
    min-height: 118px !important;
    padding: 18px 19px !important;
    border-radius: 18px !important;
    border: 1px solid #e0eae2 !important;
    box-shadow: 0 8px 24px rgba(20,70,35,.055) !important;
    overflow: hidden !important;
    transition: transform .2s ease, box-shadow .2s ease !important;
}

.stat-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #147333, #61c978);
}

.stat-card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 14px 30px rgba(20,70,35,.10) !important;
}

.stat-icon {
    font-size: 25px !important;
}

.stat-number {
    font-size: 27px !important;
    margin-top: 2px !important;
}

.stat-label {
    font-size: 11px !important;
}

/* ---------- FEATURE CARDS ---------- */
.feature-card {
    min-height: 205px !important;
    padding: 22px !important;
    border-radius: 19px !important;
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease !important;
}

.feature-card:hover {
    transform: translateY(-5px) !important;
    border-color: #b9d9c0 !important;
    box-shadow: 0 16px 32px rgba(20,80,35,.10) !important;
}

.feature-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #eef8f0;
    font-size: 28px !important;
}

.feature-title {
    font-size: 18px !important;
    margin-top: 12px !important;
}

.feature-text {
    font-size: 13px !important;
    line-height: 1.55 !important;
}

/* ---------- INFO / RESULT ---------- */
.info-card {
    padding: 20px !important;
    min-height: 145px !important;
    border-radius: 18px !important;
}

.result-card {
    padding: 24px !important;
    border-radius: 20px !important;
}

/* ---------- STREAMLIT ALERT / TECH CARDS ---------- */
[data-testid="stAlert"] {
    border-radius: 16px !important;
    border: 1px solid #dce9df !important;
    box-shadow: 0 7px 20px rgba(20,70,35,.05) !important;
}

/* ---------- WEATHER ---------- */
.weather-main-card {
    min-height: 205px !important;
    padding: 25px !important;
    border-radius: 22px !important;
}

.weather-temperature {
    font-size: 66px !important;
}

.weather-detail-card {
    min-height: 105px !important;
    padding: 17px !important;
    border-radius: 16px !important;
    transition: transform .2s ease !important;
}

.weather-detail-card:hover {
    transform: translateY(-3px) !important;
}

.forecast-card {
    min-height: 170px !important;
    border-radius: 16px !important;
    padding: 14px 8px !important;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    border-radius: 12px !important;
    min-height: 44px !important;
    font-size: 13px !important;
    transition: all .2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
}

/* ---------- INPUTS ---------- */
div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea,
[data-testid="stFileUploader"] {
    border-color: #d6e4d9 !important;
    box-shadow: 0 2px 8px rgba(20,70,35,.025) !important;
}
/* =====================================================
   CHAT INPUT - VISIBILITY FIX
   ===================================================== */

[data-testid="stChatInput"] {
    background: white !important;
    border: 1px solid #cfe0d3 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background: white !important;
    color: #173d25 !important;
    caret-color: #173d25 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #718078 !important;
    opacity: 1 !important;
}

/* Send button */
[data-testid="stChatInput"] button {
    color: #ffffff !important;
    background: #137a35 !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] button:hover {
    background: #0e612b !important;
}
/* ---------- FOOTER ---------- */
.footer {
    padding: 25px 20px 10px !important;
    font-size: 11px !important;
    opacity: .78;
}

/* ---------- MOBILE ---------- */
@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .hero {
        padding: 28px 24px !important;
        min-height: 205px !important;
    }

    .hero::after {
        right: 15px;
        font-size: 75px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# WEATHER HELPER FUNCTIONS
# =========================================================

def get_weather_icon(code):
    """
    Convert Open-Meteo weather code into a realistic icon.
    """

    code = int(code)

    if code == 0:
        return "☀️"

    elif code in [1, 2]:
        return "🌤️"

    elif code == 3:
        return "☁️"

    elif code in [45, 48]:
        return "🌫️"

    elif code in [51, 53, 55]:
        return "🌦️"

    elif code in [56, 57]:
        return "🌧️"

    elif code in [61, 63, 65]:
        return "🌧️"

    elif code in [66, 67]:
        return "🌧️"

    elif code in [71, 73, 75, 77]:
        return "❄️"

    elif code in [80, 81, 82]:
        return "🌦️"

    elif code in [85, 86]:
        return "🌨️"

    elif code in [95, 96, 99]:
        return "⛈️"

    return "🌤️"


def get_day_name(date_string, index):
    """
    Return Today/Tomorrow or weekday.
    """

    try:
        date_obj = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        if index == 0:
            return "Today"

        if index == 1:
            return "Tomorrow"

        return date_obj.strftime("%A")

    except Exception:
        return date_string


# =========================================================
# LOAD NLP MODELS
# =========================================================


@st.cache_resource
def load_nlp_models():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    classifier_path = os.path.join(
        BASE_DIR,
        "models",
        "agriculture_classifier.pkl"
    )

    classifier = joblib.load(classifier_path)

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return classifier, embedding_model

try:

    nlp_classifier, nlp_embedding_model = (
        load_nlp_models()
    )

except Exception as e:

    st.error(
        f"❌ Unable to load NLP model: {str(e)}"
    )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if "weather_location" not in st.session_state:
    st.session_state.weather_location = None

if "weather_location_name" not in st.session_state:
    st.session_state.weather_location_name = None

if "weather_dialog_open" not in st.session_state:
    st.session_state.weather_dialog_open = False


# =========================================================
# SIDEBAR
# =========================================================

show_sidebar_html(
    """
    <div style="
        text-align:center;
        padding:20px 5px 15px 5px;
    ">

        <div style="
            font-size:48px;
        ">
            🌾
        </div>

        <div style="
            font-size:25px;
            font-weight:800;
            margin-top:5px;
        ">
            AgriMind AI
        </div>

        <div style="
            font-size:10px;
            opacity:0.75;
            margin-top:5px;
            letter-spacing:1px;
        ">
            INTELLIGENT AGRICULTURE PLATFORM
        </div>

    </div>
    """
)

st.sidebar.markdown("---")


page = st.sidebar.radio(
    "🌐 NAVIGATION",
    [
        "🏠 Home",
        "🌿 Disease Detection",
        "📊 Yield Prediction",
        "💰 Crop Profit Calculator",
        "💬 Symptom Analysis"
    ]
)


st.sidebar.markdown("---")


show_sidebar_html(
    """
    <div style="padding:5px 10px;">

        <h4>
            🤖 AI TECHNOLOGY
        </h4>

        <p>🌿 Computer Vision</p>
        <p>🧠 Deep Learning</p>
        <p>📊 Machine Learning</p>
        <p>💬 Natural Language Processing</p>
        <p>⚡ Sentence Transformers</p>
        <p>🌦️ Weather Intelligence</p>

        <hr>

        <b>AgriMind AI</b>

        <p style="
            font-size:12px;
            opacity:0.8;
        ">
            Smart farming through
            artificial intelligence.
        </p>

    </div>
    """
)


# =========================================================
# WEATHER LOCATION DIALOG
# =========================================================

@st.dialog("🌦️ Weather Intelligence")
def weather_location_dialog():

    show_html(
        """
        <div style="
            text-align:center;
            padding:5px 0 15px 0;
        ">

            <div style="
                font-size:55px;
            ">
                🌦️
            </div>

            <h2 style="
                color:#14532d;
                margin-bottom:5px;
            ">
                Check Local Weather
            </h2>

            <p style="
                color:#64746a;
                font-size:14px;
            ">
                Enter your farm, village or city to
                get live weather conditions and a
                7-day forecast.
            </p>

        </div>
        """
    )

    location = st.text_input(
        "📍 Farm Location",
        placeholder="Example: Bikaner, Jaipur, Delhi...",
        key="weather_location_input"
    )

    st.caption(
        "💡 You can enter a city, village or nearby location."
    )

    col1, col2 = st.columns(2)

    with col1:

        get_weather_clicked = st.button(
            "🌦️ Get Live Weather",
            use_container_width=True,
            type="primary"
        )

    with col2:

        cancel_clicked = st.button(
            "Cancel",
            use_container_width=True
        )

    if cancel_clicked:

        st.session_state.weather_dialog_open = False
        st.rerun()

    if get_weather_clicked:

        if not location.strip():

            st.warning(
                "⚠️ Please enter your location."
            )

        else:

            with st.spinner(
                "🌍 Finding your location and weather..."
            ):

                try:

                    location_data = get_coordinates(
                        location.strip()
                    )

                    if location_data is None:

                        st.error(
                            "❌ Location not found. "
                            "Please try another city or village."
                        )

                    else:

                        weather_data = get_weather(
                            location_data["latitude"],
                            location_data["longitude"]
                        )

                        if (
                            weather_data is None
                            or "error" in weather_data
                        ):

                            error_message = (
                                weather_data.get(
                                    "error",
                                    "Weather service unavailable."
                                )
                                if isinstance(
                                    weather_data,
                                    dict
                                )
                                else "Weather service unavailable."
                            )

                            st.error(
                                f"❌ {error_message}"
                            )

                        else:

                            st.session_state.weather_data = (
                                weather_data
                            )

                            st.session_state.weather_location = (
                                location_data
                            )

                            st.session_state.weather_location_name = (
                                location.strip()
                            )

                            st.session_state.weather_dialog_open = (
                                False
                            )

                            st.success(
                                "✅ Weather loaded successfully!"
                            )

                            st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Unable to fetch weather: {str(e)}"
                    )


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    # =====================================================
    # HERO
    # =====================================================

    show_html(
        """
        <div class="hero">

            <div class="hero-small">
                🌱 NEXT GENERATION AGRICULTURE • AI POWERED
            </div>

            <div class="hero-title">
                AgriMind AI
            </div>

            <p class="hero-text">
                Your intelligent farming companion for crop health,
                yield prediction, symptom analysis and live weather
                intelligence — all in one platform.
            </p>

        </div>
        """
    )


    # =====================================================
    # WEATHER SECTION
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🌦️ Live Weather Intelligence
        </div>

        <p style="
            color:#64746a !important;
            margin-bottom:15px;
            font-size:15px;
        ">
            Check real-time weather conditions for your
            farm or location.
        </p>
        """
    )


    # -----------------------------------------------------
    # WEATHER BUTTON ONLY
    # -----------------------------------------------------

    weather_button_col1, weather_button_col2, weather_button_col3 = (
        st.columns([2, 2, 2])
    )

    with weather_button_col2:

        if st.button(
            "🌦️ Check Weather",
            use_container_width=True,
            type="primary"
        ):

            weather_location_dialog()


    # =====================================================
    # DISPLAY WEATHER
    # =====================================================

    if (
        st.session_state.weather_data is not None
        and st.session_state.weather_location is not None
    ):

        weather_data = st.session_state.weather_data
        location_data = st.session_state.weather_location


        # =================================================
        # CURRENT WEATHER
        # =================================================

        try:

            current = weather_data.get(
                "current",
                {}
            )

            temperature = float(
                current.get(
                    "temperature_2m",
                    0
                )
            )

            humidity = float(
                current.get(
                    "relative_humidity_2m",
                    0
                )
            )

            apparent_temperature = float(
                current.get(
                    "apparent_temperature",
                    temperature
                )
            )

            precipitation = float(
                current.get(
                    "precipitation",
                    0
                )
            )

            wind_speed = float(
                current.get(
                    "wind_speed_10m",
                    0
                )
            )

            weather_code = int(
                current.get(
                    "weather_code",
                    0
                )
            )

            description = weather_description(
                weather_code
            )

        except Exception as e:

            st.error(
                f"❌ Unable to read weather data: {str(e)}"
            )

            temperature = 0
            humidity = 0
            apparent_temperature = 0
            precipitation = 0
            wind_speed = 0
            weather_code = 0
            description = "Weather unavailable"


        weather_icon = get_weather_icon(
            weather_code
        )


        # =================================================
        # LOCATION
        # =================================================

        location_name = location_data.get(
            "name",
            st.session_state.get(
                "weather_location_name",
                "Unknown Location"
            )
        )

        admin1 = location_data.get(
            "admin1",
            ""
        )

        country = location_data.get(
            "country",
            ""
        )


        location_text = location_name

        if admin1:
            location_text += f", {admin1}"

        if country:
            location_text += f", {country}"


        # =================================================
        # REALISTIC WEATHER MAIN CARD
        # =================================================

        weather_left, weather_right = st.columns(
            [2, 1]
        )


        with weather_left:

            show_html(
                f"""
                <div class="weather-main-card">

                    <div class="weather-location">
                        📍 {location_text}
                    </div>

                    <div class="weather-date">
                        Live weather conditions
                    </div>

                    <div class="weather-condition">
                        {description}
                    </div>

                    <div class="weather-temperature">
                        {temperature:.0f}°
                    </div>

                    <div class="weather-feels">
                        Feels like {apparent_temperature:.0f}°C
                    </div>

                </div>
                """
            )


        with weather_right:

            show_html(
                f"""
                <div class="weather-main-card">

                    <div class="weather-big-icon">
                        {weather_icon}
                    </div>

                    <div style="
                        text-align:center;
                        font-size:16px;
                        font-weight:700;
                        margin-top:10px;
                    ">
                        {description}
                    </div>

                    <div style="
                        text-align:center;
                        font-size:13px;
                        opacity:0.9;
                        margin-top:8px;
                    ">
                        Real-time conditions
                    </div>

                </div>
                """
            )


        # =================================================
        # WEATHER DETAILS
        # =================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        d1, d2, d3, d4 = st.columns(4)


        with d1:

            show_html(
                f"""
                <div class="weather-detail-card">

                    <div class="weather-detail-icon">
                        💧
                    </div>

                    <div class="weather-detail-value">
                        {humidity:.0f}%
                    </div>

                    <div class="weather-detail-label">
                        Humidity
                    </div>

                </div>
                """
            )


        with d2:

            show_html(
                f"""
                <div class="weather-detail-card">

                    <div class="weather-detail-icon">
                        💨
                    </div>

                    <div class="weather-detail-value">
                        {wind_speed:.1f}
                    </div>

                    <div class="weather-detail-label">
                        Wind km/h
                    </div>

                </div>
                """
            )


        with d3:

            show_html(
                f"""
                <div class="weather-detail-card">

                    <div class="weather-detail-icon">
                        🌧️
                    </div>

                    <div class="weather-detail-value">
                        {precipitation:.1f}
                    </div>

                    <div class="weather-detail-label">
                        Rain mm
                    </div>

                </div>
                """
            )


        with d4:

            show_html(
                f"""
                <div class="weather-detail-card">

                    <div class="weather-detail-icon">
                        🌡️
                    </div>

                    <div class="weather-detail-value">
                        {apparent_temperature:.0f}°
                    </div>

                    <div class="weather-detail-label">
                        Feels Like
                    </div>

                </div>
                """
            )


        # =================================================
        # FARM WEATHER SUMMARY
        # =================================================

        show_html(
            """
            <div class="section-title">
                🌱 Farm Weather Summary
            </div>
            """
        )


        show_html(
            f"""
            <div class="info-card">

                <h3>
                    🌾 Current Farming Conditions
                </h3>

                <p>

                    Current temperature is
                    <b>{temperature:.1f}°C</b>
                    with humidity of
                    <b>{humidity:.0f}%</b>.

                    <br><br>

                    The current weather condition is
                    <b>{description}</b>.

                    <br><br>

                    Wind speed is
                    <b>{wind_speed:.1f} km/h</b>
                    and current precipitation is
                    <b>{precipitation:.1f} mm</b>.

                </p>

            </div>
            """
        )


        # =================================================
        # AI FARM ADVISORY
        # =================================================

        show_html(
            """
            <div class="section-title">
                🌱 AI Farm Advisory
            </div>
            """
        )


        recommendations = []


        # -------------------------------------------------
        # TEMPERATURE
        # -------------------------------------------------

        if temperature >= 40:

            recommendations.append(
                "🔥 <b>Extreme Heat:</b> High temperatures "
                "may cause serious crop heat stress. "
                "Monitor soil moisture and provide adequate "
                "water during cooler hours."
            )

        elif temperature >= 35:

            recommendations.append(
                "🌡️ <b>High Temperature:</b> Crops may "
                "experience heat stress. Check soil moisture "
                "and avoid unnecessary water loss."
            )

        elif temperature >= 30:

            recommendations.append(
                "☀️ <b>Warm Conditions:</b> Monitor irrigation "
                "requirements, especially for young plants."
            )

        elif temperature < 10:

            recommendations.append(
                "🥶 <b>Cold Conditions:</b> Sensitive crops "
                "may experience cold stress. Monitor crops "
                "during nighttime."
            )

        elif temperature < 15:

            recommendations.append(
                "❄️ <b>Cool Conditions:</b> Monitor "
                "temperature-sensitive crops for slow growth."
            )

        else:

            recommendations.append(
                "🟢 <b>Temperature:</b> Current temperature "
                "is generally favorable for crop growth."
            )


        # -------------------------------------------------
        # HUMIDITY
        # -------------------------------------------------

        if humidity >= 85:

            recommendations.append(
                "🦠 <b>Very High Humidity:</b> Fungal and "
                "bacterial disease risk may increase. "
                "Inspect leaves and maintain field ventilation."
            )

        elif humidity >= 75:

            recommendations.append(
                "💧 <b>High Humidity:</b> Monitor crops for "
                "fungal disease symptoms and excessive leaf moisture."
            )

        elif humidity <= 30:

            recommendations.append(
                "🏜️ <b>Very Dry Air:</b> Plants may lose "
                "water quickly. Check soil moisture frequently."
            )

        elif humidity <= 40:

            recommendations.append(
                "💧 <b>Low Humidity:</b> Monitor crop "
                "water requirements carefully."
            )

        else:

            recommendations.append(
                "🟢 <b>Humidity:</b> Current humidity is "
                "within a moderate range."
            )


        # -------------------------------------------------
        # PRECIPITATION
        # -------------------------------------------------

        if precipitation >= 10:

            recommendations.append(
                "🌧️ <b>Heavy Rain:</b> Avoid unnecessary "
                "irrigation and inspect drainage to prevent "
                "waterlogging."
            )

        elif precipitation > 2:

            recommendations.append(
                "🌦️ <b>Rainfall:</b> Recent rain has been "
                "detected. Consider reducing irrigation "
                "until soil moisture is checked."
            )

        else:

            recommendations.append(
                "💧 <b>Irrigation:</b> Little current rainfall. "
                "Check soil moisture before deciding irrigation needs."
            )


        # -------------------------------------------------
        # DISPLAY ADVISORY
        # -------------------------------------------------

        for recommendation in recommendations:

            show_html(
                f"""
                <div class="advisory-card">
                    {recommendation}
                </div>
                """
            )


        # =================================================
        # 7 DAY FORECAST
        # =================================================

        show_html(
            """
            <div class="section-title">
                📅 7-Day Weather Forecast
            </div>

            <p style="
                color:#64746a !important;
                font-size:14px;
                margin-bottom:18px;
            ">
                Plan irrigation and farm activities
                using the upcoming weather conditions.
            </p>
            """
        )


        daily = weather_data.get(
            "daily",
            {}
        )


        forecast_dates = daily.get(
            "time",
            []
        )

        max_temperatures = daily.get(
            "temperature_2m_max",
            []
        )

        min_temperatures = daily.get(
            "temperature_2m_min",
            []
        )

        rain_probabilities = daily.get(
            "precipitation_probability_max",
            []
        )

        weather_codes = daily.get(
            "weather_code",
            []
        )


        available_days = min(
            7,
            len(forecast_dates),
            len(max_temperatures),
            len(min_temperatures)
        )


        if available_days > 0:

            forecast_cols = st.columns(
                available_days
            )


            for i in range(
                available_days
            ):

                date = forecast_dates[i]

                max_temp = float(
                    max_temperatures[i]
                )

                min_temp = float(
                    min_temperatures[i]
                )


                if i < len(
                    rain_probabilities
                ):

                    rain_probability = (
                        rain_probabilities[i]
                    )

                else:

                    rain_probability = 0


                if i < len(
                    weather_codes
                ):

                    forecast_code = (
                        weather_codes[i]
                    )

                else:

                    forecast_code = 0


                forecast_icon = get_weather_icon(
                    forecast_code
                )


                forecast_description = (
                    weather_description(
                        forecast_code
                    )
                )


                day_name = get_day_name(
                    date,
                    i
                )


                with forecast_cols[i]:

                    show_html(
                        f"""
                        <div class="forecast-card">

                            <div class="forecast-day">
                                {day_name}
                            </div>

                            <div class="forecast-date">
                                {date}
                            </div>

                            <div class="forecast-icon">
                                {forecast_icon}
                            </div>

                            <div class="forecast-condition">
                                {forecast_description}
                            </div>

                            <div class="forecast-temp">
                                {max_temp:.0f}° /
                                {min_temp:.0f}°
                            </div>

                            <div class="forecast-rain">
                                🌧️ {rain_probability}%
                                rain chance
                            </div>

                        </div>
                        """
                    )

        else:

            st.warning(
                "⚠️ 7-day forecast is not available."
            )


        # =================================================
        # CHANGE LOCATION
        # =================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        change_col1, change_col2, change_col3 = (
            st.columns([2, 2, 2])
        )


        with change_col2:

            if st.button(
                "📍 Change Location",
                use_container_width=True
            ):

                weather_location_dialog()


    else:

        # =================================================
        # WEATHER EMPTY STATE
        # =================================================

        show_html(
            """
            <div class="info-card"
                 style="
                    text-align:center;
                    margin-top:25px;
                    padding:35px;
                 ">

                <div style="
                    font-size:60px;
                    margin-bottom:10px;
                ">
                    🌦️
                </div>

                <h3>
                    Your Weather Dashboard
                </h3>

                <p>
                    Click <b>Check Weather</b> above
                    and enter your farm location to see
                    live weather conditions, a 7-day forecast
                    and AI-powered farming recommendations.
                </p>

            </div>
            """
        )


    # =====================================================
    # PROJECT STATS
    # =====================================================

    show_html(
        """
        <div class="section-title">
            📈 AgriMind AI Overview
        </div>
        """
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        show_html(
            """
            <div class="stat-card">

                <div class="stat-icon">
                    🌿
                </div>

                <div class="stat-number">
                    20+
                </div>

                <div class="stat-label">
                    Crop Disease Classes
                </div>

            </div>
            """
        )


    with col2:

        show_html(
            """
            <div class="stat-card">

                <div class="stat-icon">
                    📚
                </div>

                <div class="stat-number">
                    2,000+
                </div>

                <div class="stat-label">
                    NLP Training Samples
                </div>

            </div>
            """
        )


    with col3:

        show_html(
            """
            <div class="stat-card">

                <div class="stat-icon">
                    🤖
                </div>

                <div class="stat-number">
                    4
                </div>

                <div class="stat-label">
                    AI Modules
                </div>

            </div>
            """
        )


    with col4:

        show_html(
            """
            <div class="stat-card">

                <div class="stat-icon">
                    🌦️
                </div>

                <div class="stat-number">
                    LIVE
                </div>

                <div class="stat-label">
                    Weather Intelligence
                </div>

            </div>
            """
        )


    # =====================================================
    # AI MODULES
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🚀 AI Modules
        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        show_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🌿
                </div>

                <div class="feature-title">
                    Plant Disease Detection
                </div>

                <p class="feature-text">
                    Upload a crop leaf image and use
                    computer vision and deep learning
                    to identify possible plant diseases.
                </p>

                <b>
                    Deep Learning • Computer Vision
                </b>

            </div>
            """
        )


    with col2:

        show_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📊
                </div>

                <div class="feature-title">
                    Crop Yield Prediction
                </div>

                <p class="feature-text">
                    Analyze soil, weather and agricultural
                    parameters to estimate expected crop
                    yield using machine learning.
                </p>

                <b>
                    Machine Learning • Data Analytics
                </b>

            </div>
            """
        )


    with col3:

        show_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💬
                </div>

                <div class="feature-title">
                    AI Symptom Analysis
                </div>

                <p class="feature-text">
                    Describe crop symptoms naturally.
                    Semantic NLP analyzes the description
                    and predicts the most likely disease.
                </p>

                <b>
                    NLP • Sentence Transformers
                </b>

            </div>
            """
        )


    # =====================================================
    # TECHNOLOGY
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🧠 Technology Behind AgriMind
        </div>
        """
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.info(
            "🐍 **Python**\n\n"
            "Core AI development"
        )


    with col2:

        st.info(
            "🧠 **Deep Learning**\n\n"
            "Image disease detection"
        )


    with col3:

        st.info(
            "💬 **NLP**\n\n"
            "Semantic symptom analysis"
        )


    with col4:

        st.info(
            "📊 **Machine Learning**\n\n"
            "Yield prediction"
        )


# =========================================================

# DISEASE DETECTION

# =========================================================
# =========================================================
# DISEASE DETECTION
# =========================================================

elif page == "🌿 Disease Detection":

    st.markdown("""
    <div class="section-title">
        🌿 AI Plant Disease Detection
    </div>
    """, unsafe_allow_html=True)

    st.write(
        "Upload a clear image of a plant leaf. "
        "Our AI model will detect the disease and provide detailed information."
    )

    uploaded_file = st.file_uploader(
        "Upload Leaf Image",
        type=["jpg", "jpeg", "png"],
        key="disease_image_uploader"
    )

    if uploaded_file is not None:

        # Show uploaded image
        col1, col2 = st.columns(2)

        with col1:
            st.image(
                uploaded_file,
                caption="Uploaded Leaf Image",
                use_container_width=True
            )

        with col2:

            st.markdown("### 🔍 AI Analysis")

            with st.spinner("Analyzing plant leaf using AI..."):

                try:

                    # Reset file pointer
                    uploaded_file.seek(0)

                    # Predict disease
                    prediction = predict_disease(
                    uploaded_file.getvalue()
                    )

                    # Debug prediction
                    st.write("### Model Prediction")
                    st.code(str(prediction))

                    # Handle different prediction formats
                    if isinstance(prediction, dict):

                        disease = prediction.get(
                            "disease",
                            prediction.get(
                                "prediction",
                                prediction.get(
                                    "class",
                                    "Unknown"
                                )
                            )
                        )

                        confidence = prediction.get(
                            "confidence",
                            None
                        )

                    elif isinstance(prediction, tuple):

                        disease = prediction[0]

                        confidence = (
                            prediction[1]
                            if len(prediction) > 1
                            else None
                        )

                    else:

                        disease = prediction
                        confidence = None


                    # Clean disease name
                    disease = str(disease).strip()


    


                    # Display prediction
                    st.success("Disease Detection Completed!")


                    # Disease Name
                    readable_disease = disease.replace(
                        "___",
                        " - "
                    ).replace(
                        "_",
                        " "
                    )

                    st.markdown(f"""
                    <div class="result-card">
                        <h3>🌱 Detected Disease</h3>
                        <h2>{readable_disease}</h2>
                    </div>
                    """, unsafe_allow_html=True)


                    # Confidence
                    if confidence is not None:

                        try:

                            confidence_value = float(confidence)

                            if confidence_value <= 1:
                                confidence_value *= 100

                            st.metric(
                                "AI Confidence",
                                f"{confidence_value:.2f}%"
                            )

                        except:
                            st.write(
                                f"Confidence: {confidence}"
                            )


                    # Disease Information
                    st.markdown("---")

                    st.markdown("## 🦠 Disease Information")


                    # Symptoms
                    st.markdown("""
                    <div class="info-box">
                    <h4>🔍 Symptoms</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write(
                        disease_info.get(
                            "symptoms",
                            "Information not available."
                        )
                    )


                    # Cause
                    st.markdown("""
                    <div class="info-box">
                    <h4>⚠️ Cause</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write(
                        disease_info.get(
                            "cause",
                            "Information not available."
                        )
                    )


                    # Prevention
                    st.markdown("""
                    <div class="info-box">
                    <h4>🛡️ Prevention</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write(
                        disease_info.get(
                            "prevention",
                            "Information not available."
                        )
                    )


                    # Management
                    st.markdown("""
                    <div class="info-box">
                    <h4>🌾 Management</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write(
                        disease_info.get(
                            "management",
                            "Information not available."
                        )
                    )


                except Exception as e:

                    st.error(
                        f"Error during disease detection: {str(e)}"
                    )

                    st.exception(e)
# =========================================================
# YIELD PREDICTION
# =========================================================

elif page == "📊 Yield Prediction":

    show_html(
        """
        <div class="hero">

            <div class="hero-small">
                MACHINE LEARNING • DATA ANALYTICS
            </div>

            <div class="hero-title">
                📊 Crop Yield Prediction
            </div>

            <p class="hero-text">
                Enter soil, weather and agricultural information
                to estimate the expected crop yield.
            </p>

        </div>
        """
    )


    # =====================================================
    # CROP INFORMATION
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🌾 Crop Information
        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        crop = st.selectbox(
            "Crop Type",
            [
                "Wheat",
                "Rice",
                "Maize",
                "Cotton",
                "Potato",
                "Mustard"
            ]
        )


    with col2:

        region = st.selectbox(
            "Region",
            [
                "North",
                "South",
                "East",
                "West",
                "Central"
            ]
        )


    with col3:

        season = st.selectbox(
            "Season",
            [
                "Spring",
                "Summer",
                "Autumn",
                "Winter"
            ]
        )


    st.divider()


    # =====================================================
    # SOIL INFORMATION
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🧪 Soil Information
        </div>
        """
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        soil_ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1
        )


    with col2:

        soil_moisture = st.number_input(
            "Soil Moisture",
            min_value=0.0,
            value=30.0
        )


    with col3:

        nitrogen = st.number_input(
            "Nitrogen",
            min_value=0.0,
            value=50.0
        )


    with col4:

        phosphorus = st.number_input(
            "Phosphorus",
            min_value=0.0,
            value=40.0
        )


    col1, col2 = st.columns(2)


    with col1:

        potassium = st.number_input(
            "Potassium",
            min_value=0.0,
            value=40.0
        )


    with col2:

        fertilizer = st.number_input(
            "Fertilizer Amount",
            min_value=0.0,
            value=100.0
        )


    st.divider()


    # =====================================================
    # WEATHER INFORMATION
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🌦️ Weather & Environment
        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        temperature = st.number_input(
            "Temperature (°C)",
            value=25.0
        )


    with col2:

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=500.0
        )


    with col3:

        sunlight = st.number_input(
            "Sunlight Hours",
            min_value=0.0,
            value=8.0
        )


    col1, col2 = st.columns(2)


    with col1:

        pesticide = st.number_input(
            "Pesticide Usage",
            min_value=0.0,
            value=20.0
        )


    with col2:

        irrigation = st.number_input(
            "Irrigation Frequency",
            min_value=0.0,
            value=5.0
        )


    st.divider()


    # =====================================================
    # HARVEST INFORMATION
    # =====================================================

    show_html(
        """
        <div class="section-title">
            📅 Harvest Information
        </div>
        """
    )


    col1, col2 = st.columns(2)


    with col1:

        harvest_year = st.number_input(
            "Harvest Year",
            min_value=2000,
            max_value=2100,
            value=2026
        )


    with col2:

        harvest_month = st.selectbox(
            "Harvest Month",
            list(range(1, 13)),
            format_func=lambda x: [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ][x - 1]
        )


    st.divider()


    # =====================================================
    # PREDICT
    # =====================================================

    if st.button(
        "🔮 Predict Crop Yield",
        use_container_width=True,
        type="primary"
    ):

        try:

            with st.spinner(
                "🧠 Calculating expected crop yield..."
            ):

                prediction = predict_yield(

                    soil_ph=soil_ph,

                    soil_moisture=soil_moisture,

                    avg_temperature=temperature,

                    total_rainfall=rainfall,

                    fertilizer_amount=fertilizer,

                    pesticide_usage=pesticide,

                    sunlight_hours=sunlight,

                    nitrogen_content=nitrogen,

                    phosphorus_content=phosphorus,

                    potassium_content=potassium,

                    irrigation_frequency=irrigation,

                    crop_type=crop,

                    region=region,

                    season=season,

                    harvest_year=harvest_year,

                    harvest_month=harvest_month
                )


            show_html(
                f"""
                <div class="result-card">

                    <div class="result-title">
                        PREDICTED CROP YIELD
                    </div>

                    <div class="result-value">
                        🌾 {prediction:.2f}
                        tons/hectare
                    </div>

                    <p style="
                        color:#64746a !important;
                        margin-top:10px;
                        font-size:14px;
                    ">
                        Estimated agricultural productivity
                        based on the supplied crop, soil and
                        environmental conditions.
                    </p>

                </div>
                """
            )


            st.success(
                "✅ Yield prediction completed successfully!"
            )


        except Exception as e:

            st.error(
                f"❌ Prediction failed: {str(e)}"
            )

# =========================================================
# CROP PROFIT CALCULATOR
# =========================================================

elif page == "💰 Crop Profit Calculator":

    show_html(
        """
        <div class="hero">

            <div class="hero-small">
                AGRICULTURAL FINANCIAL INTELLIGENCE
            </div>

            <div class="hero-title">
                💰 Crop Profit Calculator
            </div>

            <p class="hero-text">
                Estimate your farm revenue, production cost,
                expected profit and return on investment.
            </p>

        </div>
        """
    )

    # =====================================================
    # CROP INFORMATION
    # =====================================================

    show_html(
        """
        <div class="section-title">
            🌾 Crop & Farm Information
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        profit_crop = st.selectbox(
            "Crop",
            [
                "Wheat",
                "Rice",
                "Maize",
                "Cotton",
                "Potato",
                "Mustard"
            ],
            key="profit_crop"
        )

    with col2:

        farm_area = st.number_input(
            "Farm Area (acres)",
            min_value=0.1,
            value=5.0,
            step=0.1,
            key="farm_area"
        )

    with col3:

        expected_yield = st.number_input(
            "Expected Yield (quintal/acre)",
            min_value=0.0,
            value=18.5,
            step=0.5,
            key="expected_yield"
        )

    col1, col2 = st.columns(2)

    with col1:

        market_price = st.number_input(
            "Market Price (₹/quintal)",
            min_value=0.0,
            value=2500.0,
            step=100.0,
            key="market_price"
        )

    with col2:

        st.info(
            "💡 Enter the current local market price "
            "for a more realistic estimate."
        )

    st.divider()

    # =====================================================
    # FARM EXPENSES
    # =====================================================

    show_html(
        """
        <div class="section-title">
            💸 Farm Expenses
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        seed_cost = st.number_input(
            "🌱 Seed Cost (₹)",
            min_value=0.0,
            value=10000.0,
            step=500.0,
            key="seed_cost"
        )

    with col2:

        fertilizer_cost = st.number_input(
            "🧪 Fertilizer Cost (₹)",
            min_value=0.0,
            value=20000.0,
            step=500.0,
            key="fertilizer_cost"
        )

    with col3:

        pesticide_cost = st.number_input(
            "🐛 Pesticide Cost (₹)",
            min_value=0.0,
            value=8000.0,
            step=500.0,
            key="pesticide_cost"
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        irrigation_cost = st.number_input(
            "💧 Irrigation Cost (₹)",
            min_value=0.0,
            value=12000.0,
            step=500.0,
            key="irrigation_cost"
        )

    with col2:

        labor_cost = st.number_input(
            "👷 Labor Cost (₹)",
            min_value=0.0,
            value=30000.0,
            step=500.0,
            key="labor_cost"
        )

    with col3:

        machinery_cost = st.number_input(
            "🚜 Machinery Cost (₹)",
            min_value=0.0,
            value=25000.0,
            step=500.0,
            key="machinery_cost"
        )

    col1, col2 = st.columns(2)

    with col1:

        transportation_cost = st.number_input(
            "🚚 Transportation Cost (₹)",
            min_value=0.0,
            value=10000.0,
            step=500.0,
            key="transportation_cost"
        )

    with col2:

        other_cost = st.number_input(
            "📦 Other Expenses (₹)",
            min_value=0.0,
            value=5000.0,
            step=500.0,
            key="other_cost"
        )

    st.divider()

    # =====================================================
    # CALCULATE
    # =====================================================

    if st.button(
        "💰 Calculate Farm Profit",
        use_container_width=True,
        type="primary"
    ):

        # Total production
        total_production = (
            farm_area * expected_yield
        )

        # Revenue
        total_revenue = (
            total_production * market_price
        )

        # Total expenses
        total_cost = (
            seed_cost
            + fertilizer_cost
            + pesticide_cost
            + irrigation_cost
            + labor_cost
            + machinery_cost
            + transportation_cost
            + other_cost
        )

        # Profit
        estimated_profit = (
            total_revenue - total_cost
        )

        # Profit per acre
        profit_per_acre = (
            estimated_profit / farm_area
            if farm_area > 0
            else 0
        )

        # ROI
        roi = (
            (estimated_profit / total_cost) * 100
            if total_cost > 0
            else 0
        )

        # =================================================
        # RESULT HEADER
        # =================================================

        show_html(
            """
            <div class="section-title">
                📊 Financial Analysis
            </div>
            """
        )

        # =================================================
        # RESULT CARDS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            show_html(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        🌾
                    </div>

                    <div class="stat-number">
                        {total_production:,.1f}
                    </div>

                    <div class="stat-label">
                        Total Production (quintal)
                    </div>

                </div>
                """
            )

        with col2:

            show_html(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        💵
                    </div>

                    <div class="stat-number">
                        ₹{total_revenue:,.0f}
                    </div>

                    <div class="stat-label">
                        Expected Revenue
                    </div>

                </div>
                """
            )

        with col3:

            show_html(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        💸
                    </div>

                    <div class="stat-number">
                        ₹{total_cost:,.0f}
                    </div>

                    <div class="stat-label">
                        Total Farm Cost
                    </div>

                </div>
                """
            )

        with col4:

            profit_class = (
                "#14532d"
                if estimated_profit >= 0
                else "#b91c1c"
            )

            show_html(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        {"📈" if estimated_profit >= 0 else "📉"}
                    </div>

                    <div class="stat-number"
                         style="color:{profit_class} !important;">

                        ₹{estimated_profit:,.0f}

                    </div>

                    <div class="stat-label">
                        Estimated Profit
                    </div>

                </div>
                """
            )

        # =================================================
        # MAIN PROFIT RESULT
        # =================================================

        if estimated_profit >= 0:

            show_html(
                f"""
                <div class="result-card">

                    <div class="result-title">
                        ESTIMATED FARM PROFIT
                    </div>

                    <div class="result-value">
                        📈 ₹{estimated_profit:,.0f}
                    </div>

                    <p style="
                        color:#64746a;
                        margin-top:10px;
                        font-size:14px;
                    ">

                        Your estimated profit after
                        subtracting all entered farming
                        expenses from the expected revenue.

                    </p>

                </div>
                """
            )

            st.success(
                "🟢 Your estimated farm operation is profitable."
            )

        else:

            show_html(
                f"""
                <div class="result-card"
                     style="
                        border-color:#fecaca;
                        background:#fff7f7;
                     ">

                    <div class="result-title">
                        ESTIMATED FARM LOSS
                    </div>

                    <div class="result-value"
                         style="color:#b91c1c !important;">

                        📉 ₹{abs(estimated_profit):,.0f} Loss

                    </div>

                    <p style="
                        color:#64746a;
                        margin-top:10px;
                        font-size:14px;
                    ">

                        Based on the entered assumptions,
                        estimated costs are higher than
                        expected revenue.

                    </p>

                </div>
                """
            )

            st.warning(
                "🟡 Consider reviewing production costs "
                "or expected market price."
            )

        # =================================================
        # ROI + PROFIT PER ACRE
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            show_html(
                f"""
                <div class="info-card">

                    <h3>
                        📈 Return on Investment
                    </h3>

                    <p style="
                        font-size:28px;
                        font-weight:800;
                        color:#14532d !important;
                    ">

                        {roi:.2f}%

                    </p>

                    <p>
                        ROI represents estimated profit
                        compared with total farming cost.
                    </p>

                </div>
                """
            )

        with col2:

            show_html(
                f"""
                <div class="info-card">

                    <h3>
                        🌾 Profit Per Acre
                    </h3>

                    <p style="
                        font-size:28px;
                        font-weight:800;
                        color:#14532d !important;
                    ">

                        ₹{profit_per_acre:,.0f}

                    </p>

                    <p>
                        Estimated profit generated
                        from each acre of farmland.
                    </p>

                </div>
                """
            )

        # =================================================
        # EXPENSE BREAKDOWN
        # =================================================

        show_html(
            """
            <div class="section-title">
                💸 Expense Breakdown
            </div>
            """
        )

        expense_data = {
            "Seeds": seed_cost,
            "Fertilizer": fertilizer_cost,
            "Pesticides": pesticide_cost,
            "Irrigation": irrigation_cost,
            "Labor": labor_cost,
            "Machinery": machinery_cost,
            "Transportation": transportation_cost,
            "Other": other_cost
        }

        for expense_name, expense_value in expense_data.items():

            percentage = (
                (expense_value / total_cost) * 100
                if total_cost > 0
                else 0
            )

            show_html(
                f"""
                <div class="prediction-row">

                    <b>
                        {expense_name}
                    </b>

                    <span style="
                        float:right;
                        font-weight:700;
                        color:#176b36;
                    ">

                        ₹{expense_value:,.0f}
                        &nbsp; ({percentage:.1f}%)

                    </span>

                </div>
                """
            )

        # =================================================
        # SUMMARY
        # =================================================

        show_html(
            f"""
            <div class="info-card">

                <h3>
                    🌱 Farm Financial Summary
                </h3>

                <p>

                    <b>Crop:</b> {profit_crop}
                    <br><br>

                    <b>Farm Area:</b> {farm_area:.1f} acres
                    <br><br>

                    <b>Expected Yield:</b>
                    {expected_yield:.1f} quintal/acre
                    <br><br>

                    <b>Total Production:</b>
                    {total_production:,.1f} quintal
                    <br><br>

                    <b>Market Price:</b>
                    ₹{market_price:,.0f}/quintal
                    <br><br>

                    <b>Expected Revenue:</b>
                    ₹{total_revenue:,.0f}
                    <br><br>

                    <b>Total Cost:</b>
                    ₹{total_cost:,.0f}
                    <br><br>

                    <b>Estimated Profit:</b>
                    ₹{estimated_profit:,.0f}

                </p>

            </div>
            """
        )

        # =================================================
        # DISCLAIMER
        # =================================================

        st.warning(
            """
            ⚠️ This calculator provides an estimate based on
            the values entered by the user. Actual profit may
            vary because of market prices, weather, production
            losses, transportation costs and local farming
            conditions.
            """
        )
        
# =========================================================
# SYMPTOM ANALYSIS
# =========================================================

elif page == "💬 Symptom Analysis":

    show_html(
        """
        <div class="hero">

            <div class="hero-small">
                NATURAL LANGUAGE PROCESSING
            </div>

            <div class="hero-title">
                💬 AI Crop Symptom Analyzer
            </div>

            <p class="hero-text">
                Describe what you observe on your crop in
                natural language. The Sentence Transformer
                model will understand the symptoms and predict
                the most likely disease.
            </p>

        </div>
        """
    )


    st.markdown(
        "### 📝 Describe Your Crop Symptoms"
    )


    symptoms = st.text_area(
        "Crop symptoms",
        placeholder=(
            "Example:\n\n"
            "My tomato leaves have white powdery spots. "
            "The leaves are becoming weak and yellow."
        ),
        height=180,
        label_visibility="collapsed"
    )


    st.caption(
        "💡 Tip: Include leaf color, spots, insects, "
        "wilting, curling, mold, stem damage, etc."
    )


    if st.button(
        "🔍 Analyze Symptoms",
        use_container_width=True,
        type="primary"
    ):

        if not symptoms.strip():

            st.warning(
                "⚠️ Please describe the crop symptoms first."
            )

        else:
                with st.spinner(
                    "🧠 Understanding crop symptoms..."
                ):

                    # =========================================================
                    # CLEAN USER SYMPTOMS
                    # =========================================================

                    cleaned_symptoms = clean_text(
                        symptoms
                    )

                    # Must match training prefix exactly
                    model_input = (
                        "crop plant symptoms: "
                        + cleaned_symptoms
                    )


# =========================================================
# CREATE EMBEDDING
# =========================================================

                    embedding = nlp_embedding_model.encode(
                        [model_input],
                        convert_to_numpy=True,
                        normalize_embeddings=True
                    )


                    probabilities = (
                        nlp_classifier.predict_proba(
                            embedding
                        )[0]
                    )


                    classes = (
                        nlp_classifier.classes_
                    )


                    indices = np.argsort(
                        probabilities
                    )[::-1]


                    best_index = indices[0]


                    disease = classes[
                        best_index
                    ]


                    confidence = (
                        probabilities[
                            best_index
                        ] * 100
                    )


                # =================================================
                # RESULT
                # =================================================

                show_html(
                    f"""
                    <div class="result-card">

                        <div class="result-title">
                            AI PREDICTION
                        </div>

                        <div class="result-value">
                            🌿 {disease}
                        </div>

                        <br>

                        <div class="result-title">
                            CONFIDENCE
                        </div>

                        <div class="result-confidence">
                            {confidence:.2f}%
                        </div>

                    </div>
                    """
                )


                st.progress(
                    min(
                        int(confidence),
                        100
                    )
                )


                if confidence >= 80:

                    st.success(
                        "🟢 Very High Confidence"
                    )

                elif confidence >= 60:

                    st.info(
                        "🟡 High Confidence"
                    )

                elif confidence >= 40:

                    st.warning(
                        "🟠 Moderate Confidence"
                    )

                else:

                    st.error(
                        "🔴 Low Confidence"
                    )


                # =================================================
                # TOP 3
                # =================================================

                show_html(
                    """
                    <div class="section-title">
                        🏆 Top 3 Predictions
                    </div>
                    """
                )


                top_predictions = min(
                    3,
                    len(indices)
                )


                for rank, index in enumerate(
                    indices[:top_predictions],
                    start=1
                ):

                    prediction_name = (
                        classes[index]
                    )


                    prediction_probability = (
                        probabilities[index] * 100
                    )


                    show_html(
                        f"""
                        <div class="prediction-row">

                            <b>
                                {rank}.
                                {prediction_name}
                            </b>

                            <span style="
                                float:right;
                                font-weight:700;
                                color:#176b36;
                            ">
                                {prediction_probability:.2f}%
                            </span>

                        </div>
                        """
                    )


                    st.progress(
                        min(
                            int(
                                prediction_probability
                            ),
                            100
                        )
                    )


                # =================================================
                # DISEASE INFORMATION
                # =================================================
                # =================================================
# DISEASE INFORMATION
# =================================================

                matched_info = disease_info_df[
                    disease_info_df["disease"].astype(str).str.strip().str.lower()
                    == disease.strip().lower()
                ]

                if not matched_info.empty:

                    info = matched_info.iloc[0].to_dict()

                    show_html(
        """
        <div class="section-title">
            📚 Disease Information
        </div>
        """
                    )

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:

                        show_html(
                        f"""
            <div class="info-card">
                <h3>🌾 Crop</h3>
                <p>{info["crop"]}</p>
            </div>
                        """
                    )

                        show_html(
                        f"""
            <div class="info-card">
                <h3>📖 Description</h3>
                <p>{info["description"]}</p>
            </div>
                        """
                    )

                        show_html(
                        f"""
            <div class="info-card">
                <h3>🩺 Common Symptoms</h3>
                <p>{info["symptoms"]}</p>
            </div>
                        """
                    )

                        show_html(
                        f"""
            <div class="info-card">
                <h3>🔬 Possible Cause</h3>
                <p>{info["causes"]}</p>
            </div>
                        """
                    )

                    with info_col2:

                        show_html(
                            f"""
            <div class="info-card">
                <h3>🌦️ Favorable Conditions</h3>
                <p>{info["favorable_conditions"]}</p>
            </div>
            """
                        )

                        show_html(
                            f"""
            <div class="info-card">
                <h3>🛡️ Prevention</h3>
                <p>{info["prevention"]}</p>
            </div>
            """
                        )

                        show_html(
                            f"""
            <div class="info-card">
                <h3>🌱 Management</h3>
                <p>{info["management"]}</p>
            </div>
            """
                        )

                        show_html(
            f"""
            <div class="info-card">
                <h3>💊 Treatment</h3>
                <p>{info["treatment"]}</p>
            </div>
            """
                    )

                else:

                    st.warning(
                        f"No detailed information found for: {disease}"
                        )


# =========================================================
# FLOATING AI CHATBOT
# =========================================================

if "chat_open" not in st.session_state:

    st.session_state.chat_open = False


if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = [

        {
            "role": "system",

            "content": """
You are AgriMind AI, an intelligent agriculture assistant.

You help farmers and agriculture students with:

- Crop cultivation
- Plant diseases
- Soil management
- Irrigation
- Fertilizers
- Pest management
- Crop yield
- Sustainable farming
- General agriculture questions

Give simple, practical and easy-to-understand answers.

If a user describes crop symptoms, explain possible causes
and suggest safe next steps.

Do not claim certainty when the diagnosis is uncertain.

Do not provide dangerous chemical instructions.

For serious crop disease or pesticide-related decisions,
recommend consulting a local agriculture expert.
"""
        }

    ]


# =========================================================
# CHAT BUTTON
# =========================================================

with st.container(
    key="floating_chat_button"
):

    if st.button(
        "🤖",
        key="open_chat",
        help="Chat with AgriMind AI"
    ):

        st.session_state.chat_open = (
            not st.session_state.chat_open
        )

        st.rerun()


# =========================================================
# CHAT WINDOW
# =========================================================

if st.session_state.chat_open:

    with st.container(
        key="floating_chat_window"
    ):

        show_html(
            """
            <div class="chat-header">

                <div class="chat-header-title">
                    🌾 AgriMind AI
                </div>

                <div class="chat-header-status">
                    ● AI Agriculture Assistant
                </div>

            </div>
            """
        )


        # =================================================
        # DISPLAY MESSAGES
        # =================================================

        for message in (
            st.session_state.chat_messages
        ):

            if message["role"] == "system":
                continue


            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )


        # =================================================
        # CHAT INPUT
        # =================================================

        user_message = st.chat_input(
            "Ask about farming, crops, diseases...",
            key="chat_input"
        )


        if user_message:

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )


            with st.spinner(
                "🌱 Thinking..."
            ):

                try:

                    response = (
                        get_chatbot_response(
                            st.session_state.chat_messages
                        )
                    )

                except Exception as e:

                    response = (
                        "Sorry, I could not process "
                        "your question right now.\n\n"
                        f"Error: {str(e)}"
                    )


            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )


            st.rerun()


# =========================================================
# FOOTER
# =========================================================

show_html(
    """
    <div class="footer">

        🌾 <b>AgriMind AI</b>

        <br><br>

        Intelligent Agriculture • Machine Learning •
        Deep Learning • NLP • Weather Intelligence

        <br><br>

        Built for smart and sustainable agriculture.

    </div>
    """
)
