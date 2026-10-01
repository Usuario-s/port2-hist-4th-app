import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Consultorio de Interpretación",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

if 'full_response' not in st.session_state:
    st.session_state.full_response = ""

if 'base64_image' not in st.session_state:
    st.session_state.base64_image = ""


# =========================================================
# PALETA VINTAGE
# =========================================================

BLANCO = "#F5F3EE"
BLANCO_PURO = "#FFFFFF"
AZUL = "#294C60"
AZUL_CLARO = "#DCE6EA"
AZUL_MEDIO = "#58798A"
NEGRO = "#1E2529"
GRIS = "#59636A"
BORDE = "#C7D0D3"


# =========================================================
# CSS
# =========================================================

st.markdown(f"""
<style>

    /* =========================================
       FONDO GENERAL
       ========================================= */

    .stApp {{
        background-color: {BLANCO};
        color: {NEGRO};
    }}

    .main {{
        background-color: {BLANCO};
    }}


    /* =========================================
       TEXTO GENERAL
       ========================================= */

    p, label, span, div {{
        color: {NEGRO};
    }}

    h1, h2, h3 {{
        color: {NEGRO} !important;
    }}


    /* =========================================
       ENCABEZADO
       ========================================= */

    .titulo-principal {{
        text-align: center;
        color: {AZUL} !important;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 42px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-top: 5px;
        margin-bottom: 5px;
    }}

    .subtitulo-principal {{
        text-align: center;
        color: {GRIS} !important;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 17px;
        margin-bottom: 28px;
    }}


    /* =========================================
       TARJETAS
       ========================================= */

    .tarjeta {{
        background-color: {BLANCO_PURO};
        border: 1px solid {BORDE};
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0px 3px 10px rgba(30, 37, 41, 0.07);
    }}

    .tarjeta-titulo {{
        color: {AZUL} !important;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 21px;
        font-weight: bold;
        margin-bottom: 8px;
    }}

    .tarjeta-texto {{
        color: {GRIS} !important;
        font-size: 15px;
        line-height: 1.6;
    }}


    /* =========================================
       PANEL DE INFORMACIÓN
       ========================================= */

    .panel-azul {{
        background-color: {AZUL_CLARO};
        border-left: 5px solid {AZUL};
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 18px;
    }}

    .panel-azul-titulo {{
        color: {AZUL} !important;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 8px;
    }}

    .panel-azul-texto {{
        color: {NEGRO} !important;
        font-size: 14px;
        line-height: 1.6;
    }}


    /* =========================================
       AVISO
       ========================================= */

    .aviso {{
        background-color: #E9E6DF;
        border: 1px solid #D0CCC4;
        border-radius: 10px;
        padding: 13px 16px;
        color: {NEGRO} !important;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 12px;
    }}


    /* =========================================
       RESULTADO
       ========================================= */

    .resultado-header {{
        background-color: {AZUL};
        color: white !important;
        padding: 16px 20px;
        border-radius: 10px 10px 0px 0px;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 22px;
        font-weight: bold;
        margin-top: 10px;
    }}

    .resultado-cuerpo {{
        background-color: {BLANCO_PURO};
        border: 1px solid {BORDE};
        border-top: none;
        border-radius: 0px 0px 10px 10px;
        padding: 24px;
        color: {NEGRO} !important;
        line-height: 1.7;
        box-shadow: 0px 3px 10px rgba(30, 37, 41, 0.07);
    }}


    /* =========================================
       BOTONES
       ========================================= */

    .stButton > button {{
        background-color: {AZUL};
        color: #FFFFFF !important;
        border: 1px solid {AZUL};
        border-radius: 8px;
        font-weight: bold;
        min-height: 45px;
        transition: 0.2s;
    }}

    .stButton > button:hover {{
        background-color: {NEGRO};
        color: #FFFFFF !important;
        border-color: {NEGRO};
    }}


    /* =========================================
       SIDEBAR
       ========================================= */

    section[data-testid="stSidebar"] {{
        background-color: #E7E5DF;
        border-right: 1px solid {BORDE};
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {AZUL} !important;
        font-family: Georgia, "Times New Roman", serif;
    }}

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: {NEGRO} !important;
    }}


    /* =========================================
       INPUTS
       ========================================= */

    input {{
        color: {NEGRO} !important;
        background-color: {BLANCO_PURO} !important;
    }}


    /* =========================================
       SEPARADORES
       ========================================= */

    hr {{
        border-color: {BORDE};
    }}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCIÓN BASE64
# =========================================================

def encode_image_to_base64(image_path):

    try:

        with open(image_path, "rb") as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

            return encoded_image

    except FileNotFoundError:

        return "Error: La imagen no se encontró."


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    '<div class="titulo-principal">'
    'CONSULTORIO DE INTERPRETACIÓN'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo-principal">'
    'Explora los posibles significados detrás de tu dibujo'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧠 Espacio de reflexión")

    st.write(
        "Esta aplicación utiliza inteligencia artificial "
        "para observar e interpretar simbólicamente "
        "los elementos presentes en un dibujo."
    )

    st.divider()

    st.subheader("🖌️ Herramientas")

    stroke_width = st.slider(
        "Ancho del lápiz",
        1,
        30,
        5
    )

    st.divider()

    st.subheader("🔐 Conexión")

    ke = st.text_input(
        "Ingresa tu API Key",
        type="password"
    )

    st.divider()

    st.markdown(
        """
        **Nota importante**

        La interpretación es simbólica y reflexiva.
        No constituye un diagnóstico psicológico
        ni reemplaza la evaluación de un profesional.
        """
    )


# =========================================================
# API
# =========================================================

os.environ["OPENAI_API_KEY"] = ke

api_key = os.environ.get(
    "OPENAI_API_KEY",
    ""
)

if api_key:

    client = OpenAI(
        api_key=api_key
    )


# =========================================================
# ÁREA PRINCIPAL
# =========================================================

col1, col2 = st.columns(
    [1.6, 1],
    gap="large"
)


# =========================================================
# COLUMNA IZQUIERDA
# =========================================================

with col1:

    st.markdown(
        """
        <div class="tarjeta">

        <div class="tarjeta-titulo">
        🖼️ Área de dibujo
        </div>

        <div class="tarjeta-texto">
        Dibuja libremente. No necesitas realizar una obra
        artística ni seguir instrucciones específicas.
        Puedes representar una persona, objeto, lugar,
        recuerdo o simplemente dibujar lo primero que
        aparezca en tu mente.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # CANVAS

    canvas_result = st_canvas(

        fill_color="rgba(41, 76, 96, 0.10)",

        stroke_width=stroke_width,

        stroke_color=NEGRO,

        background_color="#FFFFFF",

        height=420,

        width=650,

        drawing_mode="freedraw",

        key="canvas"

    )


    st.markdown(
        """
        <div class="aviso">
        💭 <b>Recuerda:</b> intenta dibujar de manera
        espontánea. No existe una forma correcta o incorrecta
        de realizar el dibujo.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# COLUMNA DERECHA
# =========================================================

with col2:

    st.markdown(
        """
        <div class="tarjeta">

        <div class="tarjeta-titulo">
        🔎 ¿Qué observaremos?
        </div>

        <div class="tarjeta-texto">

        <b>Elementos visuales</b><br>
        Objetos, personas, animales y escenarios.

        <br><br>

        <b>Composición</b><br>
        Posición, tamaño y distribución de los elementos.

        <br><br>

        <b>Características gráficas</b><br>
        Líneas, formas, detalles y colores.

        <br><br>

        <b>Simbolismo</b><br>
        Posibles asociaciones o significados.

        <br><br>

        <b>Reflexión</b><br>
        Posibles emociones o temas relacionados.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="panel-azul">

        <div class="panel-azul-titulo">
        🌿 Interpretación reflexiva
        </div>

        <div class="panel-azul-texto">

        La IA no intentará determinar cómo es
        psicológicamente una persona.

        En cambio, buscará posibles significados
        simbólicos y planteará preguntas que permitan
        reflexionar sobre el dibujo.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BOTÓN
# =========================================================

st.markdown("")

analyze_button = st.button(
    "🔎 Analizar mi dibujo",
    type="secondary",
    use_container_width=True
)


# =========================================================
# ANÁLISIS DEL DIBUJO
# =========================================================

if (
    canvas_result.image_data is not None
    and api_key
    and analyze_button
):

    with st.spinner(
        "Analizando los elementos del dibujo..."
    ):

        try:

            # ---------------------------------------------
            # Convertir canvas en imagen
            # ---------------------------------------------

            input_numpy_array = np.array(
                canvas_result.image_data
            )

            input_image = Image.fromarray(
                input_numpy_array.astype("uint8")
            ).convert("RGBA")

            input_image.save("img.png")


            # ---------------------------------------------
            # Base64
            # ---------------------------------------------

            base64_image = encode_image_to_base64(
                "img.png"
            )

            st.session_state.base64_image = base64_image


            # ---------------------------------------------
            # PROMPT
            # ---------------------------------------------

            prompt_text = """
            Analiza cuidadosamente el dibujo proporcionado.

            Realiza una interpretación simbólica y reflexiva.
            NO realices un diagnóstico psicológico.

            Analiza los siguientes aspectos:

            1. Lo que aparece objetivamente en la imagen.
            2. Elementos principales.
            3. Distribución y uso del espacio.
            4. Tamaño y posición de los elementos.
            5. Formas, líneas y nivel de detalle.
            6. Colores utilizados.
            7. Posibles significados simbólicos.
            8. Posibles emociones o temas asociados.

            Es fundamental no afirmar que un elemento demuestra
            ansiedad, depresión, trauma, trastornos mentales,
            personalidad u otra condición psicológica.

            Utiliza expresiones como:

            "podría representar..."
            "una posible interpretación..."
            "podría estar relacionado con..."
            "también podría tener otros significados..."

            Organiza la respuesta así:

            👁️ LO QUE VEO

            Describe objetivamente el dibujo.

            🧩 ELEMENTOS Y SIMBOLISMO

            Explica posibles significados simbólicos.

            🌿 POSIBLES EMOCIONES O TEMAS

            Presenta posibilidades, no conclusiones.

            💭 PREGUNTAS PARA REFLEXIONAR

            Formula preguntas que ayuden a la persona
            a interpretar su propio dibujo.

            Finaliza indicando que el significado real depende
            del contexto personal de quien realizó el dibujo.
            """


            # ---------------------------------------------
            # OPENAI
            # ---------------------------------------------

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

                                    "url":
                                    f"data:image/png;base64,{base64_image}"

                                }

                            }

                        ]

                    }

                ],

                max_tokens=800
            )


            # ---------------------------------------------
            # RESPUESTA
            # ---------------------------------------------

            full_response = ""

            if response.choices[0].message.content:

                full_response = (
                    response
                    .choices[0]
                    .message
                    .content
                )


            st.session_state.full_response = (
                full_response
            )

            st.session_state.analysis_done = True


        except Exception as e:

            st.error(
                f"Ocurrió un error al analizar el dibujo: {e}"
            )


# =========================================================
# RESULTADO
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(
        """
        <div class="resultado-header">
        🧠 Interpretación de tu dibujo
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="resultado-cuerpo">

        {st.session_state.full_response}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="aviso">

        🌿 <b>Importante:</b>
        esta interpretación es una exploración simbólica
        generada a partir de elementos visuales.
        No constituye una evaluación psicológica ni un diagnóstico.
        El significado del dibujo depende principalmente
        del contexto y experiencia de quien lo realizó.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HISTORIA
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.subheader(
        "📚 Convierte tu dibujo en una historia"
    )

    if st.button(
        "✨ Crear historia infantil",
        use_container_width=True
    ):

        with st.spinner(
            "Creando historia..."
        ):

            story_prompt = f"""
            Basándote en la descripción del dibujo:

            "{st.session_state.full_response}"

            crea una historia infantil breve,
            creativa y entretenida.

            Convierte los elementos del dibujo
            en personajes, lugares o situaciones
            imaginativas.

            No presentes las interpretaciones psicológicas
            como hechos.
            """

            story_response = (
                openai.chat.completions.create(

                    model="gpt-4o-mini",

                    messages=[

                        {
                            "role": "user",
                            "content": story_prompt
                        }

                    ],

                    max_tokens=500
                )
            )

            st.markdown(
                "### 📖 Tu historia"
            )

            st.write(
                story_response
                .choices[0]
                .message
                .content
            )


# =========================================================
# WARNING API
# =========================================================

if not api_key:

    st.warning(
        "🔐 Ingresa tu API Key en el menú lateral "
        "para comenzar."
    )
