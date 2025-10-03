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
print("\n\n",fav_ids)
if not fav_ids:
    st.info("Aún no tienes favoritos. En **Explorar** puedes marcar ⭐ proyectos para guardarlos aquí.")
else:
    print(projects.columns)
    fav_df = projects[projects['id'].isin(fav_ids)][["id","title","one_liner","industries"]]
    fav_df["industries"] = fav_df["industries"].apply(lambda x: ", ".join(x))
    st.dataframe(fav_df.set_index("id"))
    for _, row in fav_df.iterrows():
        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"**{row['title']}**  \n{row['one_liner']}  \n_{row['industries']}_")
        with c2:
            if st.button("❌ Eliminar", key=f"del_fav_{row['id']}"):
                st.session_state["favorites"].remove(row['id'])
                st.rerun()

# Comparación
st.subheader("Comparación (hasta 3)")
cmp_ids = st.session_state["compare"]
if len(cmp_ids) < 2:
    st.info("Selecciona **al menos 2** proyectos en **Explorar** para comparar. Máximo 3.")
else:
    cols = ["title","one_liner","industries","tech_stack","trl","has_live_demo"]
    comp_df = projects[projects['sub_id'].isin(cmp_ids)][["sub_id"]+cols].copy()
    comp_df["industries"] = comp_df["industries"].apply(lambda x: ", ".join(x))
    comp_df["tech_stack"] = comp_df["tech_stack"].apply(lambda x: ", ".join(x))
    st.dataframe(comp_df.set_index("sub_id"))
    if st.button("Limpiar comparación"):
        st.session_state["compare"] = []

# Agenda
st.subheader("Mi agenda")
ag_ids = st.session_state["agenda"]
if not ag_ids:
    st.info("Tu agenda está vacía. En **Programa** añade sesiones.")
else:
    ag_df = sessions[sessions['sub_id'].isin(ag_ids)][["sub_id","date","project_title","start","end","track"]]
    st.table(ag_df.set_index("sub_id"))
    for _, row in ag_df.iterrows():
        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"**{row['project_title']}**  \n{row['date']} {row['start']}–{row['end']}  \n_{row['track']}_")
        with c2:
            if st.button("❌ Eliminar", key=f"del_ag_{row['sub_id']}"):
                st.session_state["agenda"].remove(row['sub_id'])
                st.rerun()
    ics_str = build_ics(ag_df)
    st.download_button("⬇️ Descargar .ics", data=ics_str, file_name="mi_agenda.ics", mime="text/calendar")

st.caption("Recuerda: puedes quitar favoritos o limpiar comparación cuando quieras (control y libertad del usuario).")
