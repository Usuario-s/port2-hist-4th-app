```python
import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
from streamlit_drawable_canvas import st_canvas

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Tablero Inteligente",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILOS FUTURISTAS
# =========================================================

st.markdown(
<style>

    /* ---------- FONDO GENERAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(0, 110, 255, 0.15), transparent 30%),
            radial-gradient(circle at 85% 80%, rgba(0, 180, 255, 0.10), transparent 30%),
            linear-gradient(135deg, #02040a 0%, #050b16 50%, #02040a 100%);
        color: #e8f4ff;
    }

    /* ---------- CONTENEDOR PRINCIPAL ---------- */

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* ---------- TITULO ---------- */

    h1 {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: 3px;
        text-shadow:
            0 0 8px rgba(0, 153, 255, 0.9),
            0 0 25px rgba(0, 110, 255, 0.5);
    }

    h2, h3 {
        color: #7dcfff !important;
        letter-spacing: 1px;
    }

    p, label {
        color: #c8ddf0 !important;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #030812 0%,
                #061326 50%,
                #02050c 100%
            );
        border-right: 1px solid #087cff;
        box-shadow: 5px 0 30px rgba(0, 110, 255, 0.15);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #38a9ff !important;
        text-shadow: 0 0 10px rgba(0, 140, 255, 0.7);
    }

    /* ---------- BOTONES ---------- */

    .stButton > button {
        background: linear-gradient(135deg, #0066ff, #00aaff);
        color: white;
        border: 1px solid #39bfff;
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        font-weight: 700;
        letter-spacing: 1px;
        box-shadow:
            0 0 10px rgba(0, 140, 255, 0.35),
            inset 0 0 8px rgba(255, 255, 255, 0.08);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 0 20px rgba(0, 160, 255, 0.65),
            0 0 35px rgba(0, 100, 255, 0.25);
        border-color: #8bddff;
    }

    /* ---------- INPUTS ---------- */

    .stTextInput input {
        background-color: #050c18 !important;
        color: #dff3ff !important;
        border: 1px solid #087cff !important;
        border-radius: 7px !important;
    }

    .stTextInput input:focus {
        border-color: #38bfff !important;
        box-shadow: 0 0 12px rgba(0, 150, 255, 0.45) !important;
    }

    /* ---------- SLIDER ---------- */

    div[data-baseweb="slider"] {
        color: #168cff;
    }

    /* ---------- CAJAS ---------- */

    .futuristic-card {
        background: linear-gradient(
            145deg,
            rgba(5, 17, 34, 0.95),
            rgba(2, 8, 18, 0.95)
        );
        border: 1px solid rgba(0, 140, 255, 0.55);
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        box-shadow:
            0 0 20px rgba(0, 110, 255, 0.12),
            inset 0 0 20px rgba(0, 80, 160, 0.05);
    }

    .analysis-card {
        background: linear-gradient(
            145deg,
            rgba(4, 15, 30, 0.98),
            rgba(1, 5, 12, 0.98)
        );
        border-left: 3px solid #00aaff;
        border-top: 1px solid rgba(0, 170, 255, 0.35);
        border-right: 1px solid rgba(0, 170, 255, 0.2);
        border-bottom: 1px solid rgba(0, 170, 255, 0.2);
        border-radius: 10px;
        padding: 22px;
        margin-top: 15px;
        box-shadow: 0 0 25px rgba(0, 130, 255, 0.15);
    }

    /* ---------- DIVISORES ---------- */

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #087cff,
            transparent
        );
        margin: 30px 0;
    }

    /* ---------- ALERTAS ---------- */

    div[data-testid="stAlert"] {
        background-color: rgba(3, 15, 30, 0.9);
        border: 1px solid #087cff;
        color: #dff5ff;
    }
```
