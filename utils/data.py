
import os
import pandas as pd
import streamlit as st
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@st.cache_data
def load_projects():
    json_path = os.path.join(DATA_DIR, "projects.json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # Parsear listas (separadas por '|')
    for col in ["industries","tech_stack","team","languages","awards"]:
        if col in df.columns:
            df[col] = df[col].fillna("").apply(lambda s: s if isinstance(s, list) else [v.strip() for v in s.split("|") if v.strip()])
    if "has_live_demo" in df.columns:
        df["has_live_demo"] = df["has_live_demo"].fillna(False).astype(bool)
    return df

@st.cache_data
def load_sessions():
    json_path = os.path.join(DATA_DIR, "projects.json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    # Extraer y combinar todos los schedules de todos los proyectos
    sessions = []
    for project in data:
        pid = project.get("id")
        title = project.get("title")
        track = project.get("track")
        speakers = project.get("speakers")
        for sched in project.get("schedules", []):
            session = sched.copy()
            session["project_id"] = pid
            session["project_title"] = title
            session["track"] = track
            session["speakers"] = speakers
            sessions.append(session)
    df = pd.DataFrame(sessions)
    return df

@st.cache_data
def load_taxonomies():
    ind = pd.read_csv(os.path.join(DATA_DIR, "industries.csv"))["industry"].tolist()
    tech = pd.read_csv(os.path.join(DATA_DIR, "tech_stack.csv"))["tech"].tolist()
    return ind, tech

def get_project_by_id(pid: str):
    df = load_projects()
    row = df[df["id"] == pid]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def ensure_session_state():
    st.session_state.setdefault("favorites", [])
    st.session_state.setdefault("compare", [])
    st.session_state.setdefault("agenda", [])
    st.session_state.setdefault("qna", {})
    st.session_state.setdefault("onboarding_filters", {"industries": [], "techs": []})
