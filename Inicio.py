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
# PALETA
# =========================================================

CREMA = "#F3F0E8"
BLANCO = "#FFFFFF"

AZUL_OSCURO = "#263F4C"
AZUL = "#466778"
AZUL_MEDIO = "#668796"

AZUL_TABLERO = "#B9CBD1"
AZUL_TABLERO_OSCURO = "#A9BEC6"

NEGRO = "#20272B"
GRIS = "#59666C"

BORDE = "#B8C3C7"
BORDE_OSCURO = "#82949C"

# =========================================================
# CSS
# =========================================================

st.markdown(f"""
<style>

    /* =====================================================
       FONDO GENERAL
       ===================================================== */

    .stApp {{
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(255,255,255,0.7),
                transparent 30%
            ),
            {CREMA};

        color: {NEGRO};
    }}

    .main {{
        background-color: transparent;
    }}


    /* =====================================================
       TIPOGRAFÍA
       ===================================================== */

    h1, h2, h3, h4 {{
        color: {AZUL_OSCURO} !important;
    }}

    p, label {{
        color: {NEGRO} !important;
    }}


    /* =====================================================
       ENCABEZADO
       ===================================================== */

    .header-consultorio {{
        background:
            linear-gradient(
                135deg,
                {AZUL_OSCURO},
                {AZUL}
            );

        border-radius: 18px;

        padding: 28px 35px;

        margin-bottom: 28px;

        box-shadow:
            0 8px 25px rgba(38,63,76,0.20);

        position: relative;

        overflow: hidden;

        transition: all 0.3s ease;
    }}

    .header-consultorio:hover {{
        transform: translateY(-2px);

        box-shadow:
            0 12px 30px rgba(38,63,76,0.28);
    }}

    .header-consultorio::after {{
        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        right: -60px;
        top: -80px;

        border: 2px solid rgba(255,255,255,0.15);

        border-radius: 50%;
    }}

    .header-titulo {{
        color: white !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 40px;

        font-weight: bold;

        letter-spacing: 2px;

        margin: 0;
    }}

    .header-subtitulo {{
        color: #DCE7EA !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 16px;

        margin-top: 7px;
    }}

    .header-linea {{
        width: 70px;

        height: 3px;

        background: white;

        margin-top: 18px;

        border-radius: 5px;
    }}


    /* =====================================================
       TARJETAS PRINCIPALES
       ===================================================== */

    .tarjeta {{
        background-color: rgba(255,255,255,0.94);

        border: 1px solid {BORDE};

        border-radius: 16px;

        padding: 23px;

        margin-bottom: 18px;

        box-shadow:
            0 5px 18px rgba(38,63,76,0.09);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }}

    .tarjeta:hover {{
        transform: translateY(-4px);

        border-color: {AZUL_MEDIO};

        box-shadow:
            0 12px 28px rgba(38,63,76,0.16);
    }}

    .tarjeta-titulo {{
        color: {AZUL_OSCURO} !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 21px;

        font-weight: bold;

        margin-bottom: 10px;
    }}

    .tarjeta-texto {{
        color: {GRIS} !important;

        font-size: 14px;

        line-height: 1.65;
    }}


    /* =====================================================
       ETIQUETA VINTAGE
       ===================================================== */

    .etiqueta {{
        display: inline-block;

        background-color: {AZUL_OSCURO};

        color: white !important;

        padding: 5px 11px;

        border-radius: 20px;

        font-size: 11px;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-bottom: 10px;
    }}


    /* =====================================================
       PANEL DERECHO
       ===================================================== */

    .ficha-consultorio {{
        background-color: #E5ECEE;

        border: 1px solid {BORDE};

        border-radius: 16px;

        padding: 23px;

        margin-bottom: 18px;

        box-shadow:
            0 5px 18px rgba(38,63,76,0.10);

        position: relative;

        transition: all 0.25s ease;
    }}

    .ficha-consultorio:hover {{
        transform: translateY(-4px);

        background-color: #E9EFF1;

        box-shadow:
            0 12px 26px rgba(38,63,76,0.15);
    }}

    .ficha-consultorio::before {{
        content: "✦";

        position: absolute;

        top: 13px;
        right: 17px;

        color: {AZUL_MEDIO};

        font-size: 17px;
    }}

    .ficha-titulo {{
        color: {AZUL_OSCURO} !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 21px;

        font-weight: bold;

        margin-bottom: 14px;
    }}

    .ficha-item {{
        background-color: rgba(255,255,255,0.75);

        border-left: 3px solid {AZUL};

        padding: 10px 12px;

        margin-bottom: 9px;

        border-radius: 0 8px 8px 0;

        color: {NEGRO} !important;

        font-size: 13px;

        transition: all 0.2s ease;
    }}

    .ficha-item:hover {{
        transform: translateX(5px);

        border-left-color: {AZUL_OSCURO};

        background-color: white;
    }}


    /* =====================================================
       PANEL REFLEXIVO
       ===================================================== */

    .reflexion {{
        background:
            linear-gradient(
                135deg,
                #D7E3E7,
                #EAF0F1
            );

        border: 1px solid #B8C9CE;

        border-radius: 16px;

        padding: 22px;

        margin-bottom: 18px;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.8),
            0 5px 18px rgba(38,63,76,0.08);

        transition: all 0.25s ease;
    }}

    .reflexion:hover {{
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.9),
            0 10px 25px rgba(38,63,76,0.14);
    }}

    .reflexion-titulo {{
        color: {AZUL_OSCURO} !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-weight: bold;

        font-size: 19px;
    }}

    .reflexion-texto {{
        color: {NEGRO} !important;

        line-height: 1.6;

        font-size: 13px;
    }}


    /* =====================================================
       TABLERO
       ===================================================== */

    .tablero-contenedor {{
        background:
            linear-gradient(
                145deg,
                #AFC3CA,
                #C4D4D8
            );

        border: 1px solid {BORDE_OSCURO};

        border-radius: 18px;

        padding: 14px;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.75),
            0 8px 25px rgba(38,63,76,0.15);

        transition: all 0.3s ease;
    }}

    .tablero-contenedor:hover {{
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.9),
            0 12px 30px rgba(38,63,76,0.20);
    }}


    /* =====================================================
       AVISO
       ===================================================== */

    .aviso {{
        background-color: #E9E5DC;

        border: 1px solid #D1CCC1;

        border-radius: 11px;

        padding: 13px 16px;

        color: {NEGRO} !important;

        font-size: 12px;

        line-height: 1.55;

        margin-top: 12px;
    }}


    /* =====================================================
       BOTONES
       ===================================================== */

    .stButton > button {{
        background:
            linear-gradient(
                135deg,
                {AZUL_OSCURO},
                {AZUL}
            );

        color: white !important;

        border: none;

        border-radius: 10px;

        min-height: 45px;

        font-weight: bold;

        letter-spacing: 0.3px;

        box-shadow:
            0 4px 10px rgba(38,63,76,0.18);

        transition:
            all 0.2s ease;
    }}

    .stButton > button:hover {{
        background:
            linear-gradient(
                135deg,
                {NEGRO},
                {AZUL_OSCURO}
            );

        transform: translateY(-2px);

        box-shadow:
            0 7px 16px rgba(38,63,76,0.25);

        color: white !important;
    }}

    .stButton > button:active {{
        transform: translateY(1px);
    }}


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                #E2E8E9,
                #D7E0E2
            );

        border-right: 1px solid {BORDE};

        box-shadow:
            4px 0 15px rgba(38,63,76,0.06);
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {AZUL_OSCURO} !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif;
    }}

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: {NEGRO} !important;
    }}


    /* =====================================================
       INPUTS
       ===================================================== */

    input {{
        color: {NEGRO} !important;

        background-color:
            white !important;

        border-color:
            {BORDE} !important;
    }}


    /* =====================================================
       DIVISORES
       ===================================================== */

    hr {{
        border-color: {BORDE};
    }}


    /* =====================================================
       RESULTADO
       ===================================================== */

    .resultado-header {{
        background:
            linear-gradient(
                135deg,
                {AZUL_OSCURO},
                {AZUL}
            );

        color: white !important;

        padding: 17px 21px;

        border-radius:
            14px 14px 0 0;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 22px;

        font-weight: bold;

        box-shadow:
            0 4px 12px rgba(38,63,76,0.15);
    }}

    .resultado-cuerpo {{
        background-color: white;

        border:
            1px solid {BORDE};

        border-top: none;

        border-radius:
            0 0 14px 14px;

        padding: 25px;

        color: {NEGRO} !important;

        line-height: 1.7;

        box-shadow:
            0 7px 20px rgba(38,63,76,0.08);
    }}


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {{
        width: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {CREMA};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {AZUL_MEDIO};

        border-radius: 10px;
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
    """
    <div class="header-consultorio">

        <div class="header-titulo">
            🧠 CONSULTORIO DE INTERPRETACIÓN
        </div>

        <div class="header-subtitulo">
            Un espacio para observar, interpretar y reflexionar
            sobre lo que expresamos mediante el dibujo.
        </div>

        <div class="header-linea"></div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧠 Consultorio")

    st.write(
        "Una experiencia de exploración visual mediante "
        "inteligencia artificial."
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
        **ESPACIO DE REFLEXIÓN**

        La interpretación generada es simbólica.
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
# COLUMNAS
# =========================================================

col1, col2 = st.columns(
    [1.65, 1],
    gap="large"
)


# =========================================================
# TABLERO
# =========================================================

with col1:

    st.markdown(
        """
        <div class="tarjeta">

            <span class="etiqueta">
                SESIÓN DE DIBUJO
            </span>

            <div class="tarjeta-titulo">
                🖼️ Expresa lo primero que venga a tu mente
            </div>

            <div class="tarjeta-texto">
                No necesitas crear una obra artística.
                Dibuja libremente y deja que los elementos
                aparezcan de forma espontánea.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # TABLERO
    # -----------------------------------------------------

    st.markdown(
        '<div class="tablero-contenedor">',
        unsafe_allow_html=True
    )

    canvas_result = st_canvas(

        fill_color="rgba(38,63,76,0.08)",

        stroke_width=stroke_width,

        stroke_color="#20272B",

        background_color=AZUL_TABLERO,

        height=420,

        width=650,

        drawing_mode="freedraw",

        key="canvas"

    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="aviso">

        💭 <b>Pequeña indicación:</b>
        no pienses demasiado qué deberías dibujar.
        La idea es trabajar de manera espontánea.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INFORMACIÓN DERECHA
# =========================================================

with col2:

    st.markdown(
        """
        <div class="ficha-consultorio">

            <div class="ficha-titulo">
                🔎 Ficha de observación
            </div>

            <div class="ficha-item">
                <b>01 · Elementos</b><br>
                Objetos, personas, animales y escenarios.
            </div>

            <div class="ficha-item">
                <b>02 · Composición</b><br>
                Distribución, posición y tamaño.
            </div>

            <div class="ficha-item">
                <b>03 · Trazos</b><br>
                Líneas, formas y nivel de detalle.
            </div>

            <div class="ficha-item">
                <b>04 · Color</b><br>
                Tonos y contrastes presentes.
            </div>

            <div class="ficha-item">
                <b>05 · Simbolismo</b><br>
                Posibles asociaciones e interpretaciones.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="reflexion">

            <div class="reflexion-titulo">
                🌿 Mirada reflexiva
            </div>

            <br>

            <div class="reflexion-texto">

            La IA observará el dibujo desde una perspectiva
            simbólica. En lugar de establecer conclusiones
            sobre la persona, propondrá diferentes
            interpretaciones posibles.

            <br><br>

            El significado final siempre depende de la
            historia y contexto de quien realizó el dibujo.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BOTÓN ANALIZAR
# =========================================================

st.markdown("")

analyze_button = st.button(
    "🔎  ANALIZAR MI DIBUJO",
    type="secondary",
    use_container_width=True
)


# =========================================================
# ANÁLISIS
# =========================================================

if (
    canvas_result.image_data is not None
    and api_key
    and analyze_button
):

    with st.spinner(
        "Observando los elementos del dibujo..."
    ):

        try:

            # ---------------------------------------------
            # CONVERTIR CANVAS
            # ---------------------------------------------

            input_numpy_array = np.array(
                canvas_result.image_data
            )

            input_image = Image.fromarray(
                input_numpy_array.astype("uint8")
            ).convert("RGBA")

            input_image.save("img.png")


            # ---------------------------------------------
            # BASE64
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

            Analiza:

            1. Lo que aparece objetivamente.
            2. Elementos principales.
            3. Distribución y uso del espacio.
            4. Tamaño y posición.
            5. Formas y líneas.
            6. Nivel de detalle.
            7. Colores.
            8. Posibles significados simbólicos.
            9. Posibles emociones o temas asociados.

            NO afirmes que un elemento demuestra ansiedad,
            depresión, trauma, trastornos mentales,
            personalidad u otra condición psicológica.

            Utiliza expresiones como:

            "podría representar..."
            "una posible interpretación..."
            "podría estar relacionado con..."
            "también podría tener otros significados..."

            Organiza la respuesta así:

            👁️ LO QUE VEO

            🧩 ELEMENTOS Y SIMBOLISMO

            🌿 POSIBLES EMOCIONES O TEMAS

            💭 PREGUNTAS PARA REFLEXIONAR

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
            🧠 Ficha de interpretación
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

        🌿 <b>Nota:</b>
        esta interpretación es una exploración simbólica
        generada a partir de elementos visuales.
        No constituye una evaluación psicológica,
        diagnóstico ni conclusión clínica.

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
        "📚 Una segunda forma de explorar tu dibujo"
    )

    if st.button(
        "✨ CREAR HISTORIA INFANTIL",
        use_container_width=True
    ):

        with st.spinner(
            "Construyendo la historia..."
        ):

            story_prompt = f"""
            Basándote en esta interpretación del dibujo:

            "{st.session_state.full_response}"

            crea una historia infantil breve,
            creativa y entretenida.

            Convierte los elementos visuales
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
# API WARNING
# =========================================================

if not api_key:

    st.warning(
        "🔐 Ingresa tu API Key en el menú lateral "
        "para comenzar la sesión."
    )
