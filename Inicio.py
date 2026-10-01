import os
import base64
import streamlit as st
from openai import OpenAI
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Tablero Inteligente",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# ESTILOS FUTURISTAS
# ============================================================

st.markdown("""
<style>

    /* FONDO GENERAL */
    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(0, 119, 255, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 85%,
                rgba(0, 183, 255, 0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #02050b 0%,
                #06101f 50%,
                #02050b 100%
            );

        color: #eaf6ff;
    }


    /* CONTENIDO */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* TITULO */
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3rem !important;
        letter-spacing: 4px;
        font-weight: 800 !important;

        text-shadow:
            0 0 8px #008cff,
            0 0 20px rgba(0, 140, 255, 0.7);
    }


    h2, h3 {
        color: #55c7ff !important;
        text-shadow: 0 0 8px rgba(0, 150, 255, 0.4);
    }


    p {
        color: #c8dff2;
    }


    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #02060d,
                #061427,
                #02060d
            );

        border-right: 1px solid #087cff;

        box-shadow:
            5px 0 25px rgba(0, 110, 255, 0.15);
    }


    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #38b9ff !important;
    }


    /* TARJETAS */
    .card {
        background:
            linear-gradient(
                145deg,
                rgba(5, 18, 35, 0.95),
                rgba(2, 8, 17, 0.95)
            );

        border: 1px solid rgba(0, 140, 255, 0.45);
        border-radius: 12px;

        padding: 20px;
        margin: 15px 0;

        box-shadow:
            0 0 20px rgba(0, 100, 255, 0.10),
            inset 0 0 20px rgba(0, 120, 255, 0.03);
    }


    /* BOTONES */
    .stButton > button {
        width: 100%;

        background:
            linear-gradient(
                135deg,
                #0057d9,
                #009dff
            );

        color: white;

        border: 1px solid #38c4ff;
        border-radius: 8px;

        padding: 0.7rem;

        font-weight: bold;
        letter-spacing: 1px;

        box-shadow:
            0 0 12px rgba(0, 140, 255, 0.35);

        transition: 0.2s;
    }


    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 0 20px rgba(0, 170, 255, 0.65);
    }


    /* INPUT */
    .stTextInput input {
        background-color: #030914 !important;
        color: white !important;

        border: 1px solid #087cff !important;
        border-radius: 7px !important;
    }


    .stTextInput input:focus {
        border-color: #39c3ff !important;

        box-shadow:
            0 0 12px rgba(0, 150, 255, 0.5) !important;
    }


    /* SLIDER */
    div[data-baseweb="slider"] {
        color: #008cff;
    }


    /* DIVISORES */
    hr {
        border: none;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #008cff,
                transparent
            );

        margin: 30px 0;
    }


    /* RESULTADO */
    .analysis {
        background:
            linear-gradient(
                145deg,
                rgba(4, 17, 34, 0.98),
                rgba(1, 6, 14, 0.98)
            );

        border-left: 4px solid #00aaff;

        border-top: 1px solid rgba(0, 170, 255, 0.3);
        border-right: 1px solid rgba(0, 170, 255, 0.2);
        border-bottom: 1px solid rgba(0, 170, 255, 0.2);

        border-radius: 10px;

        padding: 25px;

        margin-top: 20px;

        box-shadow:
            0 0 25px rgba(0, 130, 255, 0.15);
    }


    /* TEXTO PEQUEÑO */
    .system-text {
        color: #6bcaff;
        font-size: 0.85rem;
        letter-spacing: 2px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "full_response" not in st.session_state:
    st.session_state.full_response = ""

if "base64_image" not in st.session_state:
    st.session_state.base64_image = ""


# ============================================================
# FUNCIÓN PARA CONVERTIR IMAGEN A BASE64
# ============================================================

def encode_image_to_base64(image_path):

    try:

        with open(image_path, "rb") as image_file:

            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")

    except FileNotFoundError:

        return ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="system-text">SYSTEM / AI DRAWING ANALYZER</div>',
        unsafe_allow_html=True
    )

    st.header("⚙️ CONFIGURACIÓN")

    st.markdown(
        """
        <div class="card">

        <h3>🧠 TABLERO INTELIGENTE</h3>

        <p>
        Realiza un dibujo en el tablero y permite que
        la inteligencia artificial analice sus características
        visuales desde una perspectiva psicológica orientativa.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    stroke_width = st.slider(
        "✏️ Grosor del lápiz",
        min_value=1,
        max_value=30,
        value=5
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="card">

        <b>PROTOCOLO</b>

        <br><br>

        01 — Realiza un dibujo<br>
        02 — Introduce tu API Key<br>
        03 — Analiza el dibujo<br>
        04 — Consulta la interpretación<br>
        05 — Genera una historia

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div class="system-text" style="text-align:center;">
        ARTIFICIAL INTELLIGENCE / VISUAL ANALYSIS
    </div>
    """,
    unsafe_allow_html=True
)

st.title("◈ TABLERO INTELIGENTE ◈")

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:1.1rem;
        color:#70cfff;
    ">
        Dibuja · Analiza · Interpreta · Crea
    </p>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INSTRUCCIONES
# ============================================================

st.markdown(
    """
    <div class="card">

    <h3>✦ ÁREA DE DIBUJO</h3>

    <p>
    Realiza cualquier dibujo que quieras analizar.
    Puedes utilizar todo el espacio disponible del tablero.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABLERO
# ============================================================

stroke_color = "#000000"
background_color = "#FFFFFF"

canvas_result = st_canvas(

    fill_color="rgba(0, 0, 0, 0)",

    stroke_width=stroke_width,

    stroke_color=stroke_color,

    background_color=background_color,

    height=400,

    width=700,

    drawing_mode="freedraw",

    key="canvas"
)


# ============================================================
# API KEY
# ============================================================

st.markdown("### 🔐 CONEXIÓN CON INTELIGENCIA ARTIFICIAL")

api_key = st.text_input(
    "Ingresa tu OpenAI API Key",
    type="password",
    placeholder="sk-..."
)


# ============================================================
# BOTÓN ANALIZAR
# ============================================================

analyze_button = st.button(
    "◈ ANALIZAR DIBUJO",
    type="primary"
)


# ============================================================
# ANÁLISIS
# ============================================================

if analyze_button:

    if not api_key:

        st.warning(
            "⚠️ Primero debes ingresar tu API Key."
        )

    elif canvas_result.image_data is None:

        st.warning(
            "⚠️ Primero debes realizar un dibujo."
        )

    else:

        with st.spinner(
            "🧠 Analizando patrones visuales..."
        ):

            try:

                # ------------------------------------------------
                # CONVERTIR CANVAS EN IMAGEN
                # ------------------------------------------------

                input_numpy_array = np.array(
                    canvas_result.image_data
                )

                input_image = Image.fromarray(
                    input_numpy_array.astype("uint8")
                ).convert("RGBA")

                input_image.save("img.png")


                # ------------------------------------------------
                # CONVERTIR A BASE64
                # ------------------------------------------------

                base64_image = encode_image_to_base64(
                    "img.png"
                )

                st.session_state.base64_image = base64_image


                # ------------------------------------------------
                # CLIENTE OPENAI
                # ------------------------------------------------

                client = OpenAI(
                    api_key=api_key
                )


                # ------------------------------------------------
                # PROMPT PSICOLÓGICO
                # ------------------------------------------------

                prompt_text = """
                Analiza el dibujo proporcionado desde una
                perspectiva psicológica orientativa.

                IMPORTANTE:

                No realices un diagnóstico clínico.

                No afirmes que la persona tiene un trastorno,
                enfermedad mental o condición psicológica.

                El análisis debe diferenciar entre:

                A) ELEMENTOS OBSERVABLES
                Describe solamente aquello que puede verse
                directamente en el dibujo.

                B) INTERPRETACIONES POSIBLES
                Explica qué asociaciones psicológicas podrían
                relacionarse hipotéticamente con esos elementos.

                Analiza los siguientes aspectos:

                1. COMPOSICIÓN
                - Organización del dibujo.
                - Distribución de elementos.
                - Tamaño de las figuras.
                - Equilibrio o desequilibrio visual.

                2. USO DEL ESPACIO
                - Cantidad de espacio utilizado.
                - Zonas vacías.
                - Posición de los elementos.
                - Centralidad o lateralidad.

                3. TRAZO
                - Intensidad aparente.
                - Continuidad.
                - Dirección.
                - Repetición.
                - Rigidez o fluidez.

                4. FORMAS
                - Figuras geométricas.
                - Figuras orgánicas.
                - Simetría.
                - Repeticiones.
                - Elementos dominantes.

                5. DETALLES
                - Cantidad de detalles.
                - Elementos enfatizados.
                - Elementos ausentes o poco desarrollados.

                6. COLOR
                Si existen colores, analiza su distribución
                y presencia.

                7. INTERPRETACIÓN PSICOLÓGICA ORIENTATIVA
                Explica posibles asociaciones psicológicas,
                utilizando lenguaje probabilístico como:

                "podría estar relacionado con..."
                "puede asociarse con..."
                "una posible interpretación sería..."

                No presentes ninguna interpretación como
                un hecho comprobado.

                Finalmente proporciona una breve síntesis
                general del dibujo.

                Responde en español.
                Sé claro, estructurado y conciso.
                """


                # ------------------------------------------------
                # PETICIÓN A OPENAI
                # ------------------------------------------------

                response = client.chat.completions.create(

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
                                        "url":
                                        f"data:image/png;base64,{base64_image}"
                                    }
                                }

                            ]
                        }
                    ],

                    max_tokens=800
                )


                # ------------------------------------------------
                # OBTENER RESPUESTA
                # ------------------------------------------------

                full_response = (
                    response.choices[0]
                    .message
                    .content
                )


                if full_response:

                    st.session_state.full_response = (
                        full_response
                    )

                    st.session_state.analysis_done = True


                    # ------------------------------------------------
                    # MOSTRAR RESULTADO
                    # ------------------------------------------------

                    st.markdown(
                        """
                        <div class="analysis">

                        <h3>
                        🧠 INTERPRETACIÓN PSICOLÓGICA
                        </h3>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        full_response
                    )


            except Exception as e:

                st.error(
                    f"❌ Ocurrió un error: {e}"
                )


# ============================================================
# HISTORIA INFANTIL
# ============================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(
        """
        <div class="card">

        <h3>📚 MÓDULO NARRATIVO</h3>

        <p>
        Utiliza la interpretación del dibujo para crear
        automáticamente una historia infantil.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "✦ CREAR HISTORIA INFANTIL"
    ):

        if not api_key:

            st.warning(
                "Necesitas introducir nuevamente tu API Key."
            )

        else:

            with st.spinner(
                "📖 Construyendo historia..."
            ):

                try:

                    client = OpenAI(
                        api_key=api_key
                    )

                    story_prompt = f"""

                    Basándote en esta interpretación
                    de un dibujo:

                    {st.session_state.full_response}

                    Crea una historia infantil breve,
                    creativa y entretenida.

                    La historia debe:

                    - Ser apropiada para niños.
                    - Tener un personaje principal.
                    - Tener un pequeño conflicto.
                    - Tener un desarrollo.
                    - Tener un desenlace.
                    - Ser imaginativa.
                    - No mencionar diagnósticos psicológicos.

                    """

                    story_response = (
                        client.chat.completions.create(

                            model="gpt-4o-mini",

                            messages=[
                                {
                                    "role": "user",
                                    "content": story_prompt
                                }
                            ],

                            max_tokens=600
                        )
                    )


                    story = (
                        story_response
                        .choices[0]
                        .message
                        .content
                    )


                    st.markdown(
                        """
                        <div class="analysis">

                        <h3>
                        📖 TU HISTORIA
                        </h3>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(story)


                except Exception as e:

                    st.error(
                        f"❌ Error creando la historia: {e}"
                    )
