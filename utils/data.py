import os
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@st.cache_data
def load_projects():
    df = pd.read_csv(os.path.join(DATA_DIR, "projects.csv"))
    # Parsear listas (separadas por '|')
    for col in ["industries","tech_stack","team","languages","awards"]:
        if col in df.columns:
            df[col] = df[col].fillna("").apply(lambda s: [v.strip() for v in s.split("|") if v.strip()])
    if "has_live_demo" in df.columns:
        df["has_live_demo"] = df["has_live_demo"].fillna(False).astype(bool)
    return df

@st.cache_data
def load_sessions():
    df = pd.read_csv(os.path.join(DATA_DIR, "sessions.csv"))
    df["speakers"] = df["speakers"].fillna("").apply(lambda s: [v.strip() for v in s.split("|") if v.strip()])
    df["project_ids"] = df["project_ids"].fillna("").apply(lambda s: [v.strip() for v in s.split("|") if v.strip()])
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
