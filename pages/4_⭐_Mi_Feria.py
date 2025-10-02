import streamlit as st
import pandas as pd
from utils.data import load_projects, load_sessions, ensure_session_state
from utils.ics import build_ics

ensure_session_state()
projects = load_projects()
sessions = load_sessions()

st.title("⭐ Mi Feria")

# Favoritos
st.subheader("Favoritos")
fav_ids = st.session_state["favorites"]
if not fav_ids:
    st.info("Aún no tienes favoritos. En **Explorar** puedes marcar ⭐ proyectos para guardarlos aquí.")
else:
    fav_df = projects[projects['id'].isin(fav_ids)][["id","title","one_liner","industries"]]
    fav_df["industries"] = fav_df["industries"].apply(lambda x: ", ".join(x))
    st.dataframe(fav_df.set_index("id"))

# Comparación
st.subheader("Comparación (hasta 3)")
cmp_ids = st.session_state["compare"]
if len(cmp_ids) < 2:
    st.info("Selecciona **al menos 2** proyectos en **Explorar** para comparar. Máximo 3.")
else:
    cols = ["title","one_liner","industries","tech_stack","trl","has_live_demo"]
    comp_df = projects[projects['id'].isin(cmp_ids)][["id"]+cols].copy()
    comp_df["industries"] = comp_df["industries"].apply(lambda x: ", ".join(x))
    comp_df["tech_stack"] = comp_df["tech_stack"].apply(lambda x: ", ".join(x))
    st.dataframe(comp_df.set_index("id"))
    if st.button("Limpiar comparación"):
        st.session_state["compare"] = []

# Agenda
st.subheader("Mi agenda")
ag_ids = st.session_state["agenda"]
if not ag_ids:
    st.info("Tu agenda está vacía. En **Programa** añade sesiones.")
else:
    ag_df = sessions[sessions['id'].isin(ag_ids)][["id","title","start","end","track"]]
    st.table(ag_df.set_index("id"))
    ics_str = build_ics(ag_df)
    st.download_button("⬇️ Descargar .ics", data=ics_str, file_name="mi_agenda.ics", mime="text/calendar")

st.caption("Recuerda: puedes quitar favoritos o limpiar comparación cuando quieras (control y libertad del usuario).")
