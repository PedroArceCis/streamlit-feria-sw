
import streamlit as st
from utils.data import ensure_session_state

# Función para cargar CSS desde archivo externo
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llamar la función al inicio de tu app
load_css("app.css")

# CSS GLOBAL: gradiente de fondo
st.markdown("""
<style>
.stApp {
	background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
	min-height: 100vh;
	padding-top: 80px !important;
    font-family: CTAMonumentGrotesk, "Monument Grotesk", helvetica, Cantarell, Ubuntu, roboto, noto, arial, sans-serif;
}
.header-fixed {
	position: fixed;
	top: 8%;
	left: 0;
	width: 100vw;
	z-index: 9999;
}
/* Typewriter animation only */
.typewriter-animation {
	animation:
		typewriter 1.5s steps(25) 1s 1 normal both,
		blinkingCursor 500ms steps(20) infinite normal;
	border-right: 2px solid rgba(255,255,255,.75);
	white-space: nowrap;
	overflow: hidden;
}
@keyframes typewriter {
	from { width: 0; }
	to { width: 60%; }
}
@keyframes blinkingCursor{
	from { border-right-color: rgba(255,255,255,.75); }
	to { border-right-color: transparent; }
}
</style>
""", unsafe_allow_html=True)

# HEADER/BARRA SUPERIOR CON LOGOS Y GRADIENTE
st.markdown("""
<div class='header-fixed' style='display:flex; justify-content:space-between; align-items:center; opacity: 100% ; padding:12px 0px 10px 0px; border-bottom:1px;'>
	<img src='https://www.feriadesoftware.cl/wp-content/uploads/2025/09/di-usm.png' alt='Logo UTFSM' style='height:48px; margin-left:32px;'>
	<img src='https://static.younoodle.com/pictures/38/49/41/5a8dac8eec2968_49384881.png' alt='Logo Feria' style='height:48px; margin-right:32px;'>
</div>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Feria de Software en línea",
                   page_icon="🤓", layout="wide")
ensure_session_state()


# HERO SECTION centrado
st.markdown("""
<div style='display: flex; flex-direction: column; justify-content: center; align-items: center; margin-top: 0px; margin-bottom: 0px;'>
	<div style='max-width:600px; max-height:600px; width:100%; height:100%; display:grid; grid-template-columns: 1fr 8fr 1fr; grid-template-rows: repeat(4, auto); align-items:center; justify-items:center; padding:48px 24px;'>
		<!-- Llave de apertura más arriba -->
		<span style="grid-column:1; grid-row:1/4; font-size:140px; font-weight:bold; background: linear-gradient(120deg, #fd1d1d 0%, #E1F5C4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; justify-self:end; align-self:start; margin-right:12px; position:relative; top:-60px;">&#123;</span>
		<!-- Feria de -->
		<span style="grid-column:2; grid-row:1; font-size:120px; color:#f5f5f5; text-align:center; line-height:1;">Feria de</span>
		<!-- Software -->
		<span style="grid-column:2; grid-row:2; font-size:120px;  color:#f5f5f5; text-align:center; line-height:1;">Software</span>
		<!-- USM -->
		<span class="typewriter-animation" style="grid-column:2; grid-row:3; font-size:120px; font-weight:bold; background: linear-gradient(90deg, #b92b27 0%, #1565c0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; text-align:center; line-height:1;">USM</span>
		<!-- Llave de cierre más abajo -->
		<span style="grid-column:3; grid-row:1/4; font-size:140px; font-weight:bold; background: linear-gradient(120deg, #fd1d1d 0%, #E1F5C4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; justify-self:start; align-self:end; margin-left:12px; position:relative; top:50px;">&#125;</span>
		<span style='font-weight:bold ;grid-column:1/4; grid-row:4; font-size:24px; white-space: nowrap; background: #f5f5f5; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent; margin-top:20px; text-align:center;'>Donde las ideas se transforman en software que impacta  |  FESW</span>
	</div>

</div>
""", unsafe_allow_html=True)

# Botón centrado con st.button() nativo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
	if st.button("EXPLORAR AHORA →", use_container_width=True):
		st.switch_page("pages/2_🔎_Explorar.py")

# FOOTER centrado
st.markdown("""
<div style='text-align:center; margin-top: 80px; color: #888; font-size: 16px;'>
	© 2025 Feria de Software — MVP Docencia
</div>
""", unsafe_allow_html=True)
