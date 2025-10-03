import streamlit as st
import pandas as pd
from utils.data import load_sessions, ensure_session_state

ensure_session_state()
sessions = load_sessions()

st.title("🗓️ Programa")

print(sessions.columns)
# Extraer días y tracks correctamente usando el campo 'date' de cada sesión
sessions['date'] = pd.to_datetime(sessions['date']).dt.date
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
                # Asegurar que speakers sea lista
                speakers = row['speakers']
                if isinstance(speakers, str):
                    speakers = [v.strip() for v in speakers.split('|') if v.strip()]
                elif not isinstance(speakers, list) or pd.isna(speakers):
                    speakers = []
                st.markdown(f"**{row['project_title']}**  \n"
                            f"🕒 {row['start']} — {row['end']}  \n"
                            f"🎤 {', '.join(speakers) if speakers else '—'}  \n"
                            f"🎯 Área: {row['track'] or '—'}")
                c1, c2 = st.columns(2)
                with c1:
                    if row['sub_id']:
                        st.link_button("▶️ Ver transmisión en sala " + str(row['room']), row['sub_id'])
                with c2:
                    add = st.button("➕ Añadir a mi agenda", key=f"agenda_{row['sub_id']}")
                    if add:
                        if row['sub_id'] not in st.session_state["agenda"]:
                            st.session_state["agenda"].append(row['sub_id'])
                            st.toast("Sesión añadida a tu agenda")
                        else:
                            st.warning("Esta sesión ya está en tu agenda")
else:
    st.info("Aún no hay sesiones cargadas.")
