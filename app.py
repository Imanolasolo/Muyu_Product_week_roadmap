import streamlit as st
from db.db_setup import init_db
from modules.epic_form import show_epic_form
from modules.epic_board import show_epic_board
from db.db_manager import get_all_epics, get_epic_count_by_week

st.set_page_config(page_title="Roadmap Semanal", layout="wide")

# Inicializar DB
init_db()

st.title("🚀 Roadmap Semanal - Reunión de Lunes")

# Seleccionar semana
week = st.selectbox("Selecciona la semana", ["Semana 40 - 2025", "Semana 41 - 2025", "Semana 42 - 2025"])

# Agregar panel de debug expandible
with st.expander("🔍 Panel de Debug - Ver todas las épicas"):
    all_epics = get_all_epics()
    st.write(f"**Total de épicas en la base de datos:** {len(all_epics)}")
    
    if all_epics:
        st.write("**Todas las épicas:**")
        for epic in all_epics:
            st.write(f"- ID: {epic[0]} | Nombre: {epic[1]} | Semana: {epic[3]} | Estado: {epic[4]}")
    else:
        st.warning("⚠️ No hay épicas en la base de datos")
    
    # Contador por semana
    week_counts = get_epic_count_by_week()
    if week_counts:
        st.write("**Épicas por semana:**")
        for week_data in week_counts:
            st.write(f"- {week_data[0]}: {week_data[1]} épicas")

tab1, tab2 = st.tabs(["📋 Tablero", "➕ Nueva épica"])

with tab1:
    show_epic_board(week)

with tab2:
    show_epic_form()
