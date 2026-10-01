import streamlit as st
import base64
from io import BytesIO
from openai import OpenAI
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Tablero Inteligente",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTADO DE LA APLICACIÓN
# ============================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "full_response" not in st.session_state:
    st.session_state.full_response = ""

if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# ============================================================
# DISEÑO
# ============================================================

st.markdown(
    """
    <style>

    /* ==============================
       FONDO
       ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 110, 255, 0.20),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 90%,
                rgba(0, 180, 255, 0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020409 0%,
                #06101e 50%,
                #020409 100%
            );
    }


    /* ==============================
       CONTENEDOR
       ============================== */

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
    }


    /* ==============================
       TITULOS
       ============================== */

    h1 {
        color: white !important;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: 4px;

        text-shadow:
            0 0 8px rgba(0, 153, 255, 0.9),
            0 0 25px rgba(0, 100, 255, 0.5);
    }

    h2,
    h3 {
        color: #5bc7ff !important;
    }


    /* ==============================
       TEXTO
       ============================== */

    p {
        color: #c9dced;
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #02050b,
                #061426,
                #02050b
            );

        border-right: 1px solid #087cff;
    }


    /* ==============================
       TARJETAS
       ============================== */

    .panel {
        background: rgba(3, 14, 28, 0.90);

        border: 1px solid rgba(0, 140, 255, 0.45);

        border-radius: 12px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow:
            0 0 20px rgba(0, 100, 255, 0.12);
    }


    /* ==============================
       TABLERO
       ============================== */

    .board-title {
        text-align: center;

        color: #53c7ff;

        font-size: 0.85rem;

        letter-spacing: 3px;

        margin-bottom: 8px;
    }


    /* ==============================
       BOTONES
       ============================== */

    .stButton > button {
        width: 100%;

        background:
            linear-gradient(
                135deg,
                #0055d9,
                #009cff
            );

        color: white;

        border: 1px solid #4ac9ff;

        border-radius: 8px;

        font-weight: bold;

        letter-spacing: 1px;

        padding: 0.65rem;

        box-shadow:
            0 0 12px rgba(0, 140, 255, 0.30);

        transition: 0.2s;
    }


    .stButton > button:hover {
        box-shadow:
            0 0 22px rgba(0, 170, 255, 0.60);

        transform: translateY(-2px);
    }


    /* ==============================
       INPUT
       ============================== */

    .stTextInput input {
        background-color: #030914 !important;

        color: white !important;

        border: 1px solid #087cff !important;

        border-radius: 7px !important;
    }


    /* ==============================
       RESULTADO IA
       ============================== */

    .result-box {
        background:
            linear-gradient(
                145deg,
                rgba(3, 17, 34, 0.98),
                rgba(1, 6, 14, 0.98)
            );

        border-left: 4px solid #00aaff;

        border-radius: 10px;

        padding: 20px;

        margin-top: 15px;

        box-shadow:
            0 0 25px rgba(0, 130, 255, 0.15);
    }


    /* ==============================
       DIVISOR
       ============================== */

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

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧠 SISTEMA")

    st.markdown(
        """
        <div class="panel">

        <h3>Tablero Inteligente</h3>

        <p>
        Realiza un dibujo y utiliza inteligencia artificial
        para obtener una interpretación visual y psicológica
        orientativa.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Propiedades del tablero")

    stroke_width = st.slider(
        "Grosor del lápiz",
        min_value=1,
        max_value=30,
        value=5
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="panel">

        <b>PROTOCOLO</b>

        <br><br>

        01 · Dibujar<br>
        02 · Introducir API Key<br>
        03 · Analizar<br>
        04 · Interpretar<br>
        05 · Crear historia

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    "<p style='text-align:center; color:#52c7ff; "
    "letter-spacing:3px;'>"
    "ARTIFICIAL INTELLIGENCE / VISUAL ANALYSIS"
    "</p>",
    unsafe_allow_html=True
)

st.title("◈ TABLERO INTELIGENTE ◈")

st.markdown(
    "<p style='text-align:center; font-size:1.1rem;'>"
    "DIBUJA · ANALIZA · INTERPRETA · CREA"
    "</p>",
    unsafe_allow_html=True
)


# ============================================================
# INSTRUCCIONES
# ============================================================

st.markdown(
    """
    <div class="panel">

    <h3>✦ Área de dibujo</h3>

    <p>
    Realiza libremente el dibujo que deseas analizar.
    Puedes utilizar todo el tablero.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABLERO
# ============================================================

st.markdown(
    "<div class='board-title'>"
    "◈ DRAWING INTERFACE ◈"
    "</div>",
    unsafe_allow_html=True
)


canvas_result = st_canvas(

    fill_color="rgba(0, 0, 0, 0)",

    stroke_width=stroke_width,

    stroke_color="#000000",

    background_color="#FFFFFF",

    height=400,

    width=700,

    drawing_mode="freedraw",

    key="drawing_canvas"
)


# ============================================================
# API KEY
# ============================================================

st.markdown("### 🔐 CONEXIÓN CON IA")

api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

# Guardar la clave durante la sesión
if api_key:
    st.session_state.api_key = api_key

api_key = st.session_state.api_key


# ============================================================
# BOTÓN ANALIZAR
# ============================================================

analyze_button = st.button(
    "◈ ANALIZAR DIBUJO"
)


# ============================================================
# PROCESAR DIBUJO
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # COMPROBAR API KEY
    # --------------------------------------------------------

    if not api_key:

        st.error(
            "❌ Debes ingresar una API Key."
        )

        st.stop()


    # --------------------------------------------------------
    # COMPROBAR TABLERO
    # --------------------------------------------------------

    if canvas_result.image_data is None:

        st.error(
            "❌ No se pudo obtener el dibujo del tablero."
        )

        st.stop()


    try:

        with st.spinner(
            "🧠 La inteligencia artificial está analizando el dibujo..."
        ):

            # =================================================
            # OBTENER IMAGEN DEL CANVAS
            # =================================================

            canvas_array = np.array(
                canvas_result.image_data
            )

            # Convertir a uint8
            canvas_array = canvas_array.astype(
                np.uint8
            )

            # Crear imagen
            image = Image.fromarray(
                canvas_array
            )


            # =================================================
            # CONVERTIR A PNG EN MEMORIA
            # =================================================

            image_buffer = BytesIO()

            image.save(
                image_buffer,
                format="PNG"
            )

            image_buffer.seek(0)


            # =================================================
            # BASE64
            # =================================================

            encoded_image = base64.b64encode(
                image_buffer.read()
            ).decode("utf-8")


            # =================================================
            # CLIENTE OPENAI
            # =================================================

            client = OpenAI(
                api_key=api_key
            )


            # =================================================
            # PROMPT
            # =================================================

            prompt = """
            Analiza el dibujo que aparece en la imagen.

            Quiero una interpretación psicológica ORIENTATIVA
            basada únicamente en los elementos visuales
            presentes en el dibujo.

            IMPORTANTE:

            No realices un diagnóstico psicológico o psiquiátrico.

            No afirmes que la persona tiene una enfermedad,
            trastorno o condición mental.

            Diferencia claramente entre:

            1. OBSERVACIONES:
            Lo que realmente se puede observar en el dibujo.

            2. POSIBLES INTERPRETACIONES:
            Asociaciones psicológicas hipotéticas que podrían
            relacionarse con esos elementos.

            Analiza:

            • Composición.
            • Distribución de los elementos.
            • Uso del espacio.
            • Tamaño de las figuras.
            • Posición de los elementos.
            • Intensidad aparente del trazo.
            • Repetición de líneas.
            • Formas.
            • Simetría.
            • Cantidad de detalles.
            • Elementos principales y secundarios.
            • Uso del color si existe.
            • Elementos que llamen especialmente la atención.

            Después explica posibles asociaciones psicológicas
            utilizando lenguaje prudente:

            "podría estar relacionado con..."
            "podría asociarse con..."
            "una posible interpretación sería..."

            No presentes estas interpretaciones como hechos.

            Termina con una síntesis general.

            Responde en español.
            Sé claro y estructurado.
            """


            # =================================================
            # LLAMADA A OPENAI
            # =================================================

            response = client.chat.completions.create(

                model="gpt-4o-mini",

                messages=[
                    {
                        "role": "user",

                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },

                            {
                                "type": "image_url",

                                "image_url": {
                                    "url":
                                    "data:image/png;base64,"
                                    + encoded_image
                                }
                            }
                        ]
                    }
                ],

                max_tokens=900
            )


            # =================================================
            # OBTENER RESPUESTA
            # =================================================

            result = (
                response
                .choices[0]
                .message
                .content
            )


            if not result:

                raise Exception(
                    "La IA no devolvió ninguna respuesta."
                )


            # Guardar resultado
            st.session_state.full_response = result

            st.session_state.analysis_done = True


            # =================================================
            # MOSTRAR RESULTADO
            # =================================================

            st.markdown(
                """
                <div class="result-box">

                <h3>
                🧠 INTERPRETACIÓN DEL DIBUJO
                </h3>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(result)


    except Exception as error:

        st.error(
            "❌ Error durante el análisis:"
        )

        st.code(
            str(error)
        )


# ============================================================
# HISTORIA
# ============================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(
        """
        <div class="panel">

        <h3>📚 MÓDULO NARRATIVO</h3>

        <p>
        Puedes transformar el análisis del dibujo en una
        historia infantil.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    create_story = st.button(
        "✦ CREAR HISTORIA INFANTIL"
    )


    if create_story:

        if not api_key:

            st.error(
                "❌ Debes ingresar tu API Key."
            )

        else:

            try:

                with st.spinner(
                    "📖 Creando historia..."
                ):

                    client = OpenAI(
                        api_key=api_key
                    )


                    story_prompt = f"""
                    Crea una historia infantil breve y creativa
                    utilizando como inspiración esta interpretación
                    de un dibujo:

                    {st.session_state.full_response}

                    La historia debe:

                    - Ser apropiada para niños.
                    - Tener un protagonista.
                    - Tener un pequeño conflicto.
                    - Tener un desarrollo.
                    - Tener un final.
                    - Ser imaginativa.
                    - No mencionar diagnósticos psicológicos.

                    Escribe la historia en español.
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

                            max_tokens=700
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
                        <div class="result-box">

                        <h3>
                        📖 TU HISTORIA
                        </h3>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(story)


            except Exception as error:

                st.error(
                    "❌ Error creando la historia:"
                )

                st.code(
                    str(error)
                )
