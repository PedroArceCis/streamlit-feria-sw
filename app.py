import streamlit as st
from utils.data import load_projects, load_sessions, load_taxonomies, ensure_session_state

st.set_page_config(page_title="Feria de Software en línea", page_icon="🤓", layout="wide")

# Inicializar estado global
ensure_session_state()

# Cargar datos (cacheados)
projects = load_projects()
sessions = load_sessions()

st.title("Feria de Software en línea — MVP")
st.write(
    "Bienvenid@. Usa la navegación de la izquierda para visitar **Home**, **Explorar**, **Programa** y **Mi Feria**. "
    "Este prototipo aplica principios de **usabilidad**, **modelo conceptual**, **visibilidad**, **mapeo**, "
    "**retroalimentación**, y ciclo **Lean UX** a través de un flujo simple: descubrir → comprender → comparar/accionar."
)

st.subheader("Atajos útiles")
st.markdown("- **Explorar**: Búsqueda + filtros facetados para encontrar proyectos relevantes.")
st.markdown("- **Programa**: Seminarios y paneles por track; añade sesiones a tu agenda personal.")
st.markdown("- **Mi Feria**: Favoritos, Comparar (hasta 3) y descargar tu agenda en **.ics**.")

with st.expander("¿Qué incluye este MVP? (criterios de diseño)"):
    st.markdown("""
- **Modelo de contenido estandarizado** (fichas) para reducir ambigüedad.
- **Visibilidad del estado**: etiquetas, chips de filtros activos, favoritos y comparaciones en sesión.
- **Mapeo y feedback inmediato**: resultados se actualizan al instante; límites (p. ej., comparar ≤ 3) con mensajes claros.
- **Manipulación directa**: agregar/quitar favoritos/comparación con toggles; arrastrar no se incluye, pero el patrón de reversibilidad sí.
- **Pruebas formativas**: tareas críticas medibles (descubrimiento, comprensión, acción) listas para instrumentar.
""")
st.info("Sugerencia: ve a **Home** para un onboarding por intereses y arranca desde ahí.")

st.caption("Versión MVP para docencia — Streamlit")
