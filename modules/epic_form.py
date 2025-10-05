import streamlit as st
from db.db_manager import create_epic, create_task, get_all_epics

def show_epic_form():
    st.subheader("➕ Crear nueva épica")

    with st.form("epic_form"):
        name = st.text_input("Nombre de la épica")
        description = st.text_area("Descripción")
        week = st.selectbox("Semana", ["Semana 40 - 2025", "Semana 41 - 2025", "Semana 42 - 2025"], index=0)
        status = st.selectbox("Estado inicial", ["Pendiente", "En progreso", "Hecho"], index=0)
        
        # Sección para agregar tareas iniciales
        st.markdown("### 📝 Tareas iniciales (opcional)")
        st.caption("Puedes agregar tareas que se necesiten completar para esta épica")
        
        # Permitir hasta 5 tareas iniciales
        initial_tasks = []
        for i in range(3):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                task_title = st.text_input(f"Tarea {i+1}", key=f"task_title_{i}")
            with col2:
                task_owner = st.text_input(f"Responsable", key=f"task_owner_{i}")
            with col3:
                task_priority = st.selectbox(f"Prioridad", ["Alta", "Media", "Baja"], key=f"task_priority_{i}", index=1)
            
            if task_title:
                initial_tasks.append({
                    "title": task_title,
                    "owner": task_owner,
                    "priority": task_priority
                })
        
        submitted = st.form_submit_button("Crear épica")

        if submitted:
            if name:
                # Crear la épica
                create_epic(name, description, week, status)
                
                # Obtener el ID de la épica recién creada
                all_epics = get_all_epics()
                new_epic_id = all_epics[0][0] if all_epics else None
                
                # Crear tareas iniciales si las hay
                if new_epic_id and initial_tasks:
                    for task in initial_tasks:
                        create_task(task["title"], "", new_epic_id, task["owner"], task["priority"])
                
                task_count = len(initial_tasks)
                success_msg = f"✅ Épica '{name}' creada para {week} con estado '{status}'"
                if task_count > 0:
                    success_msg += f" y {task_count} tarea{'s' if task_count > 1 else ''}"
                
                st.success(success_msg)
                st.info("💡 Ve al tablero para ver tu nueva épica y sus tareas")
                
                # Limpiar el formulario
                st.session_state.clear()
            else:
                st.warning("⚠️ El nombre es obligatorio.")
