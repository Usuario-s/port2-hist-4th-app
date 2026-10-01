import os
import base64
import streamlit as st
import openai
import numpy as np

from openai import OpenAI
from PIL import Image
from streamlit_drawable_canvas import st_canvas


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Consultorio de Interpretación",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PALETA VINTAGE
# =========================================================

CREMA = "#F1EEE6"
CREMA_CLARO = "#F8F6F0"
BLANCO = "#FFFFFF"

AZUL_OSCURO = "#203A48"
AZUL = "#365B6B"
AZUL_MEDIO = "#5F7F8D"

TABLERO = "#B8CCD2"
TABLERO_HOVER = "#ACC3CA"

NEGRO = "#20282C"
GRIS = "#52616A"
GRIS_CLARO = "#D7DEE0"

BORDE = "#AEBCC1"


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "full_response" not in st.session_state:
    st.session_state.full_response = ""

if "base64_image" not in st.session_state:
    st.session_state.base64_image = ""


# =========================================================
# FUNCIONES
# =========================================================

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")
    except FileNotFoundError:
        return ""


def analizar_dibujo(canvas_data, api_key):

    input_numpy_array = np.array(canvas_data)

    input_image = Image.fromarray(
        input_numpy_array.astype("uint8")
    ).convert("RGBA")

    image_path = "img.png"
    input_image.save(image_path)

    base64_image = encode_image_to_base64(image_path)

    st.session_state.base64_image = base64_image

    prompt_text = """
Analiza este dibujo desde una perspectiva psicológica simbólica y reflexiva.

IMPORTANTE:
No hagas diagnósticos psicológicos, médicos o psiquiátricos.
No afirmes que un elemento demuestra una enfermedad,
trastorno, trauma o condición psicológica.

La interpretación debe utilizar expresiones como:
"podría representar", "puede sugerir", "una posible interpretación".

Organiza el análisis en estas categorías:

1. OBSERVACIÓN VISUAL
Describe brevemente qué aparece en el dibujo.

2. COMPOSICIÓN Y ESPACIO
Analiza la distribución de los elementos, tamaño,
posición, espacios vacíos y equilibrio visual.

3. TRAZOS Y FORMAS
Observa presión aparente, dirección, repetición,
curvas, formas geométricas, irregularidades y nivel de detalle.

4. COLOR
Analiza los colores utilizados y sus posibles asociaciones
simbólicas o emocionales.

5. POSIBLE SIMBOLISMO
Explica qué podrían representar los principales elementos
desde una interpretación simbólica.

6. POSIBLES TEMAS O EMOCIONES
Menciona temas o emociones que podrían estar relacionados
con el dibujo, dejando claro que son interpretaciones
y no conclusiones psicológicas.

7. PREGUNTAS DE REFLEXIÓN
Propón 3 preguntas que podrían ayudar a la persona
a explicar qué significa el dibujo para ella.

Sé claro, breve y respetuoso.
Responde en español.
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=700
    )

    return response.choices[0].message.content


# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* =========================
       FONDO GENERAL
       ========================= */

    .stApp {{
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(95,127,141,0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(54,91,107,0.10),
                transparent 30%
            ),
            {CREMA};
        color: {NEGRO};
    }}

    .main .block-container {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                {AZUL_OSCURO} 0%,
                {AZUL} 55%,
                {AZUL_MEDIO} 100%
            );
        border-right: 4px solid {TABLERO};
    }}

    section[data-testid="stSidebar"] * {{
        color: {BLANCO} !important;
    }}

    section[data-testid="stSidebar"] .stMarkdown {{
        color: {BLANCO};
    }}


    /* =========================
       TITULOS
       ========================= */

    h1, h2, h3 {{
        color: {AZUL_OSCURO} !important;
        letter-spacing: 0.3px;
    }}

    p, label {{
        color: {NEGRO};
    }}


    /* =========================
       CABECERA
       ========================= */

    .header-consultorio {{
        background:
            linear-gradient(
                135deg,
                {AZUL_OSCURO},
                {AZUL}
            );
        padding: 32px 38px;
        border-radius: 18px;
        margin-bottom: 26px;
        border: 2px solid rgba(255,255,255,0.35);
        box-shadow:
            0 12px 30px rgba(32,40,44,0.18);
        transition: all 0.25s ease;
    }}

    .header-consultorio:hover {{
        transform: translateY(-3px);
        box-shadow:
            0 18px 38px rgba(32,40,44,0.24);
    }}

    .header-titulo {{
        color: white;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }}

    .header-subtitulo {{
        color: #E5EEF1;
        font-size: 16px;
    }}

    .linea-decorativa {{
        width: 100%;
        height: 3px;
        margin-top: 20px;
        background: {TABLERO};
        border-radius: 20px;
    }}


    /* =========================
       TARJETAS
       ========================= */

    .card {{
        background: {BLANCO};
        border: 2px solid {BORDE};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow:
            0 7px 18px rgba(32,40,44,0.10);
        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }}

    .card:hover {{
        transform: translateY(-4px);
        border-color: {AZUL};
        box-shadow:
            0 14px 28px rgba(32,40,44,0.16);
    }}

    .card-title {{
        color: {AZUL_OSCURO};
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 8px;
    }}

    .card-text {{
        color: {GRIS};
        font-size: 15px;
        line-height: 1.6;
    }}


    /* =========================
       TABLERO
       ========================= */

    .tablero-wrapper {{
        background: {AZUL_OSCURO};
        padding: 10px;
        border-radius: 18px;
        border: 2px solid {BORDE};
        box-shadow:
            0 12px 25px rgba(32,40,44,0.18);
        transition: all 0.25s ease;
    }}

    .tablero-wrapper:hover {{
        border-color: {AZUL};
        box-shadow:
            0 18px 34px rgba(32,40,44,0.24);
    }}

    .tablero-label {{
        color: {AZUL_OSCURO};
        font-weight: 800;
        font-size: 18px;
        margin-bottom: 10px;
    }}


    /* =========================
       FICHA DERECHA
       ========================= */

    .ficha {{
        background:
            linear-gradient(
                145deg,
                {BLANCO},
                {CREMA_CLARO}
            );
        border: 2px solid {BORDE};
        border-radius: 16px;
        padding: 22px;
        box-shadow:
            0 8px 20px rgba(32,40,44,0.10);
        transition: all 0.25s ease;
    }}

    .ficha:hover {{
        transform: translateY(-4px);
        box-shadow:
            0 15px 28px rgba(32,40,44,0.16);
        border-color: {AZUL};
    }}

    .ficha-titulo {{
        color: {AZUL_OSCURO};
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 18px;
    }}

    .ficha-item {{
        background: {CREMA};
        border-left: 5px solid {AZUL};
        border-radius: 9px;
        padding: 13px;
        margin: 10px 0;
        color: {GRIS};
        transition: all 0.2s ease;
    }}

    .ficha-item:hover {{
        transform: translateX(5px);
        background: {TABLERO};
        border-left-color: {AZUL_OSCURO};
    }}

    .ficha-item b {{
        color: {AZUL_OSCURO};
    }}


    /* =========================
       PANEL REFLEXIVO
       ========================= */

    .reflexion {{
        background:
            linear-gradient(
                135deg,
                {TABLERO},
                #D7E2E5
            );
        border: 2px solid {BORDE};
        border-radius: 16px;
        padding: 22px;
        margin-top: 20px;
        box-shadow:
            0 7px 18px rgba(32,40,44,0.10);
        transition: all 0.25s ease;
    }}

    .reflexion:hover {{
        transform: translateY(-3px);
        box-shadow:
            0 14px 25px rgba(32,40,44,0.15);
    }}

    .reflexion-title {{
        color: {AZUL_OSCURO};
        font-weight: 800;
        font-size: 20px;
        margin-bottom: 8px;
    }}


    /* =========================
       BOTONES
       ========================= */

    .stButton > button {{
        background:
            linear-gradient(
                135deg,
                {AZUL},
                {AZUL_OSCURO}
            ) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 11px 22px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        box-shadow:
            0 5px 12px rgba(32,40,44,0.18) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow:
            0 9px 18px rgba(32,40,44,0.25) !important;
        filter: brightness(1.08);
    }}


    /* =========================
       INPUTS
       ========================= */

    .stTextInput input {{
        background: white !important;
        color: {NEGRO} !important;
        border: 2px solid {BORDE} !important;
        border-radius: 9px !important;
    }}

    .stTextInput input:focus {{
        border-color: {AZUL} !important;
        box-shadow:
            0 0 0 2px rgba(54,91,107,0.15) !important;
    }}


    /* =========================
       SLIDER
       ========================= */

    .stSlider {{
        padding-top: 5px;
    }}


    /* =========================
       RESULTADO
       ========================= */

    .resultado-header {{
        background:
            linear-gradient(
                135deg,
                {AZUL_OSCURO},
                {AZUL}
            );
        color: white;
        padding: 18px 22px;
        border-radius: 14px 14px 0 0;
        font-size: 21px;
        font-weight: 800;
    }}

    .resultado-body {{
        background: white;
        border: 2px solid {BORDE};
        border-top: none;
        border-radius: 0 0 14px 14px;
        padding: 25px;
        color: {NEGRO};
        line-height: 1.7;
    }}


    /* =========================
       DIVISOR
       ========================= */

    hr {{
        border: none;
        border-top: 2px solid {BORDE};
        margin: 30px 0;
    }}


    /* =========================
       SCROLLBAR
       ========================= */

    ::-webkit-scrollbar {{
        width: 9px;
    }}

    ::-webkit-scrollbar-track {{
        background: {CREMA};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {AZUL_MEDIO};
        border-radius: 10px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CABECERA
# =========================================================

st.markdown(
    """
    <div class="header-consultorio">
        <div class="header-titulo">
            🧠 CONSULTORIO DE INTERPRETACIÓN
        </div>

        <div class="header-subtitulo">
            Un espacio para explorar el significado simbólico
            de aquello que expresamos mediante el dibujo.
        </div>

        <div class="linea-decorativa"></div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🗂️ CONSULTORIO")

    st.markdown(
        """
        Esta herramienta utiliza inteligencia artificial
        para observar e interpretar simbólicamente
        un dibujo.

        <br>

        **No realiza diagnósticos psicológicos.**
        La interpretación funciona como una herramienta
        de reflexión.
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ⚙️ Herramientas")

    stroke_width = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=25,
        value=5
    )

    stroke_color = st.color_picker(
        "Color del trazo",
        "#20282C"
    )

    st.markdown("---")

    st.markdown("### 🔐 Acceso")

    ke = st.text_input(
        "Ingresa tu API Key",
        type="password"
    )


# =========================================================
# API
# =========================================================

api_key = ke.strip()

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    client = OpenAI(api_key=api_key)


# =========================================================
# CONTENIDO PRINCIPAL
# =========================================================

col_izq, col_der = st.columns(
    [2.2, 1],
    gap="large"
)


# =========================================================
# COLUMNA IZQUIERDA
# =========================================================

with col_izq:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                ✏️ Área de expresión
            </div>

            <div class="card-text">
                Dibuja libremente. No existe una forma correcta
                o incorrecta de hacerlo. Cuando termines,
                podrás solicitar una interpretación.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tablero-label">TABLERO DE EXPRESIÓN</div>',
        unsafe_allow_html=True
    )

    # Contenedor visual oscuro SOLAMENTE como marco.
    # El interior completo del canvas es azul grisáceo.
    st.markdown(
        '<div class="tablero-wrapper">',
        unsafe_allow_html=True
    )

    canvas_result = st_canvas(
        fill_color="rgba(32,40,44,0.04)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=TABLERO,
        height=430,
        width=700,
        drawing_mode="freedraw",
        key="canvas",
        display_toolbar=False
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    analizar_button = st.button(
        "🔎 ANALIZAR DIBUJO",
        use_container_width=True
    )


# =========================================================
# COLUMNA DERECHA
# =========================================================

with col_der:

    st.markdown(
        
        <div class="ficha">

            <div class="ficha-titulo">
                🔎 Ficha de observación
            </div>

            <div class="ficha-item">
                <b>01 · Elementos</b><br>
                Objetos, personas, animales y escenarios.
            </div>

            <div class="ficha-item">
                <b>02 · Composición</b><br>
                Distribución, tamaño y ubicación.
            </div>

            <div class="ficha-item">
                <b>03 · Trazos</b><br>
                Formas, líneas, repetición y detalles.
            </div>

            <div class="ficha-item">
                <b>04 · Color</b><br>
                Tonos y posibles asociaciones simbólicas.
            </div>

            <div class="ficha-item">
                <b>05 · Simbolismo</b><br>
                Posibles significados del dibujo.
            </div>

        </div>
        ,
        unsafe_allow_html=True
    )

    st.markdown(
        
        <div class="reflexion">

            <div class="reflexion-title">
                🌿 Mirada reflexiva
            </div>

            <div>
                El análisis busca generar preguntas
                e interpretaciones, no establecer
                diagnósticos.
            </div>

        </div>
        ,
        unsafe_allow_html=True
    )


# =========================================================
# ANALIZAR
# =========================================================

if analizar_button:

    if not api_key:

        st.warning(
            "🔐 Ingresa tu API Key en el panel lateral antes de analizar."
        )

    elif canvas_result.image_data is None:

        st.warning(
            "✏️ Primero realiza un dibujo en el tablero."
        )

    else:

        with st.spinner("Observando e interpretando el dibujo..."):

            try:

                full_response = analizar_dibujo(
                    canvas_result.image_data,
                    api_key
                )

                st.session_state.full_response = full_response
                st.session_state.analysis_done = True

            except Exception as e:

                st.error(
                    f"Ocurrió un error durante el análisis: {e}"
                )


# =========================================================
# RESULTADO
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(
        """
        <div class="resultado-header">
            🧠 Interpretación del dibujo
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="resultado-body">
            {st.session_state.full_response}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        
        <div class="card">

            <div class="card-title">
                📚 ¿Quieres continuar?
            </div>

            <div class="card-text">
                Puedes convertir la interpretación obtenida
                en una pequeña historia inspirada en el dibujo.
            </div>

        </div>
        ,
        unsafe_allow_html=True
    )

    if st.button(
        "✨ CREAR HISTORIA INFANTIL",
        use_container_width=True
    ):

        if not api_key:

            st.warning("Ingresa tu API Key.")

        else:

            with st.spinner("Creando historia..."):

                try:

                    story_prompt = f"""
                    Basándote en esta descripción:

                    {st.session_state.full_response}

                    Crea una historia infantil breve,
                    creativa y entretenida inspirada en
                    los elementos descritos.
                    """

                    story_response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": story_prompt
                            }
                        ],
                        max_tokens=500
                    )

                    story = (
                        story_response
                        .choices[0]
                        .message
                        .content
                    )

                    st.markdown(
                        """
                        <div class="resultado-header">
                            📖 Historia inspirada en tu dibujo
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="resultado-body">
                            {story}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"No fue posible crear la historia: {e}"
                    )
