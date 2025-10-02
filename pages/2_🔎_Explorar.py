import streamlit as st
import pandas as pd
from utils.data import load_projects, ensure_session_state
from utils.search import filter_and_search
from utils.data import get_project_by_id

ensure_session_state()
projects = load_projects()

st.title("🔎 Explorar proyectos")

# Filtros (facetados)
col1, col2, col3 = st.columns([2,2,1])
with col1:
    q = st.text_input("Buscar (título, resumen, tecnología)", value=st.session_state.get("q", ""))
with col2:
    sel_ind = st.multiselect("Industria", sorted({i for lst in projects['industries'] for i in lst if isinstance(lst, list)}))
with col3:
    trl_opts = ["Idea","Prototipo","Piloto","En producción"]
    sel_trl = st.selectbox("Estado/TRL", ["(Todos)"] + trl_opts)

col4, col5, col6 = st.columns([1,1,2])
with col4:
    has_demo = st.checkbox("Con demo en vivo")
with col5:
    lang = st.selectbox("Idioma", ["(Todos)","ES","EN"])

# Aplicar filtros + búsqueda
res = filter_and_search(projects, query=q, industries=sel_ind, trl=None if sel_trl=="(Todos)" else sel_trl,
                        has_demo=has_demo, language=None if lang=="(Todos)" else lang)

# Mostrar chips de filtros activos
chips = []
if q: chips.append(f"🔎 '{q}'")
if sel_ind: chips.append("🏷️ " + ", ".join(sel_ind))
if sel_trl!="(Todos)": chips.append(f"📈 {sel_trl}")
if has_demo: chips.append("🎥 Demo en vivo")
if lang!="(Todos)": chips.append(f"🌐 {lang}")
if chips:
    st.caption("Filtros activos: " + "  •  ".join(chips))

# Vista de comparación si corresponde
compare_ids = st.session_state["compare"]
if compare_ids:
    st.subheader("Comparar proyectos")
    if len(compare_ids) < 2:
        st.info("Selecciona **al menos 2** proyectos para comparar. Máximo 3.")
    else:
        cols = ["title","one_liner","industries","tech_stack","trl","has_live_demo"]
        comp_df = res[res['id'].isin(compare_ids)][["id"]+cols].copy()
        comp_df["industries"] = comp_df["industries"].apply(lambda x: ", ".join(x))
        comp_df["tech_stack"] = comp_df["tech_stack"].apply(lambda x: ", ".join(x))
        st.dataframe(comp_df.set_index("id"))
        if st.button("Limpiar comparación"):
            st.session_state["compare"] = []

st.subheader(f"Resultados ({len(res)})")
if res.empty:
    st.warning("No hay resultados. Ajusta los filtros o la búsqueda.")
else:
    cols = st.columns(3)
    for i, (_, row) in enumerate(res.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{row['title']}**")
                st.caption(row['one_liner'])
                st.write(", ".join(row['industries']))
                st.write("Stack: " + (", ".join(row['tech_stack']) if row['tech_stack'] else "—"))
                c1, c2, c3 = st.columns(3)
                with c1:
                    fav = row['id'] in st.session_state["favorites"]
                    if st.button("⭐ Guardar" if not fav else "⭐ Quitar", key=f"fav_{row['id']}"):
                        if fav:
                            st.session_state["favorites"].remove(row['id'])
                            st.toast("Quitado de favoritos")
                        else:
                            st.session_state["favorites"].append(row['id'])
                            st.toast("Agregado a favoritos")
                with c2:
                    in_comp = row['id'] in st.session_state["compare"]
                    label = "🧪 Comparar" if not in_comp else "🧪 Quitar"
                    if st.button(label, key=f"cmp_{row['id']}"):
                        if not in_comp and len(st.session_state["compare"]) >= 3:
                            st.warning("Solo puedes comparar hasta 3 proyectos.")
                        else:
                            if in_comp:
                                st.session_state["compare"].remove(row['id'])
                            else:
                                st.session_state["compare"].append(row['id'])
                with c3:
                    if st.button("📄 Ver ficha", key=f"ver_{row['id']}"):
                        st.experimental_set_query_params(project=row['id'])
                        st.experimental_rerun()

# Detalle (ficha) si hay query param
params = st.experimental_get_query_params()
if "project" in params:
    proj_id = params["project"][0]
    proj = get_project_by_id(proj_id)
    if proj is not None:
        st.markdown("---")
        st.header(f"📄 Ficha — {proj['title']}")
        st.caption(proj['one_liner'])
        st.markdown(f"**Industria:** {', '.join(proj['industries']) if proj['industries'] else '—'}")
        st.markdown(f"**Tecnologías:** {', '.join(proj['tech_stack']) if proj['tech_stack'] else '—'}")
        st.markdown(f"**Estado/TRL:** {proj['trl']}  |  **Demo en vivo:** {'Sí' if proj['has_live_demo'] else 'No'}")
        st.subheader("Problema")
        st.write(proj['problem'] or "—")
        st.subheader("Solución e impacto")
        st.write(proj['solution'] or "—")

        c1, c2, c3 = st.columns(3)
        with c1:
            if proj['demo_url']:
                st.link_button("🎥 Ver demo", proj['demo_url'])
        with c2:
            if proj['repo_url']:
                st.link_button("📦 Repositorio", proj['repo_url'])
        with c3:
            if proj['contact_url']:
                st.link_button("✉️ Contactar", proj['contact_url'])

        # Q&A simple (formativo)
        st.subheader("Preguntas y Respuestas (Q&A)")
        with st.form(key=f"qa_{proj_id}"):
            q_txt = st.text_area("Deja una pregunta para el equipo", max_chars=300, height=100)
            submitted = st.form_submit_button("Enviar pregunta")
            if submitted:
                if q_txt.strip():
                    st.session_state["qna"].setdefault(proj_id, []).append({"q": q_txt})
                    st.success("¡Pregunta enviada! (simulado en este MVP)")
                else:
                    st.warning("La pregunta no puede estar vacía.")
    else:
        st.error("Proyecto no encontrado.")
