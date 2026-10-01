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
# ESTILOS
# =========================================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #F3EFE7;
    }

    /* Contenedor principal */
    .main {
        background-color: #F3EFE7;
    }

    /* Título */
    .titulo {
        text-align: center;
        color: #3F5145;
        font-family: Georgia, serif;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitulo {
        text-align: center;
        color: #6B756B;
        font-family: Arial, sans-serif;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Tarjetas */
    .tarjeta {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #D9D4C8;
        box-shadow: 0px 4px 15px rgba(70, 70, 60, 0.08);
        margin-bottom: 20px;
    }

    .tarjeta-titulo {
        color: #3F5145;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Texto de información */
    .info {
        color: #687168;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Resultado */
    .resultado {
        background-color: #FAF9F5;
        padding: 25px;
        border-radius: 18px;
        border-left: 6px solid #819581;
        box-shadow: 0px 3px 12px rgba(50, 50, 40, 0.06);
    }

    /* Disclaimer */
    .aviso {
        background-color: #ECE8DE;
        padding: 15px;
        border-radius: 12px;
        color: #66645D;
        font-size: 13px;
        margin-top: 15px;
    }

    /* Botón */
    .stButton > button {
        background-color: #657B69;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 25px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #526557;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E5E0D5;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #3F5145;
    }

    /* Separadores */
    hr {
        border-color: #D6D0C3;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIÓN PARA CODIFICAR IMAGEN
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
    '<div class="titulo">🧠 Consultorio de Interpretación</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Un espacio para explorar los posibles significados de tu dibujo'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🌿 Espacio de reflexión")

    st.markdown("""
    Este espacio utiliza inteligencia artificial para observar
    los elementos visuales de un dibujo y generar una interpretación
    simbólica y reflexiva.
    """)

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

    st.markdown("""
    **Importante**

    La interpretación generada no es un diagnóstico psicológico
    ni reemplaza la evaluación de un profesional de la salud mental.
    """)


# =========================================================
# ÁREA PRINCIPAL
# =========================================================

col1, col2 = st.columns([1.5, 1])

# =========================================================
# COLUMNA DEL DIBUJO
# =========================================================

with col1:

    st.markdown("""
    <div class="tarjeta">
        <div class="tarjeta-titulo">🖼️ Tu dibujo</div>
        <div class="info">
        Dibuja libremente en el espacio. No existe una forma correcta
        de hacerlo. Puedes representar una persona, un objeto,
        un paisaje, un recuerdo o simplemente dibujar lo primero
        que se te ocurra.
        </div>
    </div>
    """, unsafe_allow_html=True)

    canvas_result = st_canvas(
        fill_color="rgba(129, 149, 129, 0.15)",
        stroke_width=stroke_width,
        stroke_color="#3F5145",
        background_color="#FFFDF8",
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas"
    )

    st.markdown("""
    <div class="aviso">
    💭 <b>Consejo:</b> intenta dibujar de manera espontánea.
    No necesitas crear una obra artística.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# COLUMNA DE INFORMACIÓN
# =========================================================

with col2:

    st.markdown("""
    <div class="tarjeta">
        <div class="tarjeta-titulo">🔎 ¿Qué analizaremos?</div>

        <div class="info">

        La inteligencia artificial observará aspectos como:

        <br><br>

        • Elementos presentes en el dibujo<br>
        • Composición y distribución<br>
        • Uso del espacio<br>
        • Formas y objetos representados<br>
        • Colores utilizados<br>
        • Tamaño relativo de los elementos<br>
        • Posibles asociaciones simbólicas<br>
        • Temas o emociones que podrían relacionarse
        con la representación

        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tarjeta">

    <div class="tarjeta-titulo">
    🌱 Interpretación reflexiva
    </div>

    <div class="info">

    El objetivo no es determinar "qué le ocurre" a una persona,
    sino generar preguntas y posibles interpretaciones que puedan
    ayudar a reflexionar sobre el dibujo.

    </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# API
# =========================================================

os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ.get('OPENAI_API_KEY', '')

if api_key:
    client = OpenAI(api_key=api_key)


# =========================================================
# BOTÓN ANALIZAR
# =========================================================

st.markdown("###")

analyze_button = st.button(
    "🔎 Analizar mi dibujo",
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

    with st.spinner("Observando el dibujo..."):

        try:

            # Convertir canvas a imagen
            input_numpy_array = np.array(
                canvas_result.image_data
            )

            input_image = Image.fromarray(
                input_numpy_array.astype('uint8')
            ).convert('RGBA')

            input_image.save('img.png')

            # Base64
            base64_image = encode_image_to_base64(
                "img.png"
            )

            st.session_state.base64_image = base64_image

            # =================================================
            # PROMPT DE INTERPRETACIÓN
            # =================================================

            prompt_text = """
            Analiza cuidadosamente el dibujo proporcionado.

            Quiero una interpretación simbólica y reflexiva del dibujo,
            NO un diagnóstico psicológico.

            Describe primero objetivamente lo que aparece en la imagen.

            Después analiza:

            1. Elementos principales del dibujo.
            2. Distribución y uso del espacio.
            3. Tamaño y posición de los elementos.
            4. Formas, líneas y nivel de detalle.
            5. Colores utilizados, si los hay.
            6. Posibles significados simbólicos de esos elementos.
            7. Posibles emociones o temas que podrían asociarse
               con el dibujo, dejando claro que son posibilidades
               y no conclusiones.
            8. Preguntas de reflexión que podrían ayudar a la persona
               a explicar qué significa el dibujo para ella.

            Es muy importante NO afirmar que determinados elementos
            demuestran ansiedad, depresión, trauma, personalidad,
            trastornos mentales o cualquier otra condición psicológica.

            No hagas diagnósticos.

            Utiliza expresiones como:
            "podría representar",
            "una posible interpretación es",
            "podría estar relacionado con",
            "esto también podría entenderse de otra manera".

            La respuesta debe ser clara, humana y comprensible.

            Organiza la respuesta con estos apartados:

            👁️ Lo que veo
            🧩 Elementos y simbolismo
            🌿 Posibles emociones o temas
            💭 Preguntas para reflexionar

            Termina indicando que la interpretación depende del contexto
            personal de quien realizó el dibujo.
            """

            # =================================================
            # OPENAI
            # =================================================

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

            # =================================================
            # RESULTADO
            # =================================================

            full_response = ""

            if response.choices[0].message.content is not None:

                full_response = (
                    response.choices[0]
                    .message
                    .content
                )

            st.session_state.full_response = full_response
            st.session_state.analysis_done = True

        except Exception as e:

            st.error(
                f"Ocurrió un error al analizar el dibujo: {e}"
            )


# =========================================================
# MOSTRAR RESULTADO
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown("""
    <div class="resultado">
        <div class="tarjeta-titulo">
            🧠 Interpretación de tu dibujo
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        st.session_state.full_response
    )

    st.markdown("""
    <div class="aviso">
    🌿 <b>Nota:</b> esta interpretación es una exploración
    simbólica generada a partir de elementos visuales.
    No constituye una evaluación psicológica, diagnóstico
    ni interpretación clínica. El significado real del dibujo
    depende del contexto y de la experiencia de quien lo realizó.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# CREAR HISTORIA
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.subheader("📚 También puedes convertir tu dibujo en una historia")

    if st.button(
        "✨ Crear historia infantil",
        use_container_width=True
    ):

        with st.spinner("Creando historia..."):

            story_prompt = f"""
            Basándote en la descripción del dibujo:

            "{st.session_state.full_response}"

            crea una historia infantil breve, creativa,
            entretenida y apropiada para niños.

            No presentes la interpretación psicológica
            como un hecho. Convierte los elementos del dibujo
            en personajes, lugares o situaciones imaginativas.
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

            st.markdown("### 📖 Tu historia")

            st.write(
                story_response
                .choices[0]
                .message
                .content
            )


# =========================================================
# ADVERTENCIA API
# =========================================================

if not api_key:

    st.warning(
        "🔐 Ingresa tu API Key en el menú lateral "
        "para poder analizar el dibujo."
    )
