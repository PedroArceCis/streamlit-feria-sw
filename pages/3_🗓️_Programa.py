import streamlit as st
import pandas as pd
from utils.data import load_sessions, ensure_session_state

ensure_session_state()
sessions = load_sessions()

st.title("🗓️ Programa")

# Extraer días y tracks
sessions['date'] = pd.to_datetime(sessions['start']).dt.date
days = sorted(sessions['date'].unique())
tracks = sorted([t for t in sessions['track'].dropna().unique()])

col1, col2 = st.columns(2)
with col1:
    sel_day = st.selectbox("Día", days if days else ["—"])
with col2:
    sel_track = st.selectbox("Track", ["(Todos)"] + tracks)

if days:
    mask = sessions['date'] == sel_day
    if sel_track != "(Todos)":
        mask = mask & (sessions['track'] == sel_track)
    subset = sessions[mask].sort_values("start")

    st.subheader(f"Sesiones para {sel_day}{'' if sel_track=='(Todos)' else f' — {sel_track}'}")
    if subset.empty:
        st.info("No hay sesiones para el filtro seleccionado.")
    else:
        for _, row in subset.iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['title']}**  \n"
                            f"🕒 {row['start']} — {row['end']}  \n"
                            f"🎤 {', '.join(row['speakers']) if row['speakers'] else '—'}  \n"
                            f"🎯 Track: {row['track'] or '—'}")
                c1, c2 = st.columns(2)
                with c1:
                    if row['streaming_url']:
                        st.link_button("▶️ Ver transmisión", row['streaming_url'])
                with c2:
                    add = st.button("➕ Añadir a mi agenda", key=f"agenda_{row['id']}")
                    if add:
                        if row['id'] not in st.session_state["agenda"]:
                            st.session_state["agenda"].append(row['id'])
                            st.toast("Sesión añadida a tu agenda")
                        else:
                            st.warning("Esta sesión ya está en tu agenda")
else:
    st.info("Aún no hay sesiones cargadas.")
