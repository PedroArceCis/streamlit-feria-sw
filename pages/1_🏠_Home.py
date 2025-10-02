import streamlit as st
from utils.data import load_projects, load_taxonomies, ensure_session_state

ensure_session_state()
projects = load_projects()
industries, techs = load_taxonomies()

st.title("🏠 Home — Onboarding por intereses")
st.write("Selecciona tus **intereses** para arrancar con un set de proyectos recomendado. Luego visita **Explorar** para refinar.")

col1, col2 = st.columns(2)
with col1:
    sel_industries = st.multiselect("Industrias de interés", industries, default=industries[:2])
with col2:
    sel_techs = st.multiselect("Tecnologías de interés", techs, default=techs[:3])

st.session_state["onboarding_filters"] = {"industries": sel_industries, "techs": sel_techs}

# Recomendados simples (coincidencia por intersección)
mask = projects['industries'].apply(lambda lst: any(i in lst for i in sel_industries) if lst else False) | \
       projects['tech_stack'].apply(lambda lst: any(t in lst for t in sel_techs) if lst else False)
recs = projects[mask].head(6)

st.subheader("Proyectos recomendados")
if recs.empty:
    st.info("No hay coincidencias con tus intereses. Ajusta la selección para ver recomendaciones.")
else:
    cols = st.columns(3)
    for i, (_, row) in enumerate(recs.iterrows()):
        with cols[i % 3]:
            st.markdown(f"**{row['title']}**")
            st.caption(row['one_liner'])
            st.write(", ".join(row['industries']))
            btn = st.button("⭐ Guardar", key=f"home_fav_{row['id']}")
            if btn:
                favs = st.session_state["favorites"]
                if row['id'] not in favs:
                    favs.append(row['id'])
                    st.success("Agregado a favoritos")
                else:
                    favs.remove(row['id'])
                    st.warning("Quitado de favoritos")

st.info("Ahora ve a **Explorar** para ver el listado completo con filtros facetados o al **Programa** para armar tu agenda.")
