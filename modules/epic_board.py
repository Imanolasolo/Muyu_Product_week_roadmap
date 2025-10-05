import streamlit as st
from db.db_manager import (
    get_epics_by_week, update_epic_status, delete_epic,
    get_tasks_by_epic, create_task, update_task_status, delete_task,
    get_task_completion_status, auto_complete_epic_if_tasks_done
)

def show_epic_board(week):
    st.subheader(f"📅 Roadmap de {week}")
    
    # Botón para refrescar manualmente
    if st.button("🔄 Actualizar tablero"):
        st.rerun()

    epics = get_epics_by_week(week)
    
    # Mostrar contador de épicas
    st.info(f"📊 Total de épicas en {week}: {len(epics)}")
    
    columns = st.columns(3)
    states = ["Pendiente", "En progreso", "Hecho"]

    for i, state in enumerate(states):
        with columns[i]:
            filtered_epics = [e for e in epics if e[4] == state]
            st.markdown(f"### {state} ({len(filtered_epics)})")
            
            if len(filtered_epics) == 0:
                st.info(f"No hay épicas en estado '{state}'")
            
            for epic in filtered_epics:
                epic_id = epic[0]
                epic_name = epic[1]
                epic_description = epic[2]
                epic_week = epic[3]
                epic_status = epic[4]
                
                # Obtener estadísticas de tareas
                completed, total, percentage = get_task_completion_status(epic_id)
                tasks = get_tasks_by_epic(epic_id)
                
                with st.container():
                    # Crear una tarjeta visual más atractiva con barra de progreso
                    progress_color = "#28a745" if percentage == 100 else "#ffc107" if percentage > 0 else "#6c757d"
                    
                    st.markdown(f"""
                    <div style="
                        border: 1px solid #ddd; 
                        border-radius: 8px; 
                        padding: 15px; 
                        margin: 10px 0; 
                        background-color: #f9f9f9;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    ">
                        <h4 style="margin: 0 0 5px 0; color: #333;">📋 {epic_name}</h4>
                        <p style="margin: 0 0 10px 0; color: #666; font-size: 0.9em;">{epic_description or 'Sin descripción'}</p>
                        <div style="background-color: #e9ecef; border-radius: 10px; height: 8px; margin: 10px 0;">
                            <div style="background-color: {progress_color}; height: 8px; border-radius: 10px; width: {percentage}%;"></div>
                        </div>
                        <small style="color: #999;">Progreso: {completed}/{total} tareas ({percentage:.0f}%) | ID: {epic_id}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Checklist de tareas (solo para épicas "En progreso")
                    if epic_status == "En progreso":
                        st.markdown("**📝 Checklist de Tareas:**")
                        
                        # Mostrar tareas existentes
                        task_updated = False
                        for task in tasks:
                            task_id, task_title, task_desc, _, task_owner, task_priority, task_status = task
                            task_key = f"task_{task_id}_{epic_id}"
                            
                            col_check, col_task, col_del = st.columns([1, 6, 1])
                            
                            with col_check:
                                task_completed = st.checkbox(
                                    "", 
                                    value=(task_status == "Completado"),
                                    key=task_key
                                )
                                if task_completed != (task_status == "Completado"):
                                    new_task_status = "Completado" if task_completed else "Pendiente"
                                    update_task_status(task_id, new_task_status)
                                    task_updated = True
                            
                            with col_task:
                                priority_emoji = "🔴" if task_priority == "Alta" else "🟡" if task_priority == "Media" else "🟢"
                                task_style = "text-decoration: line-through; color: #6c757d;" if task_completed else ""
                                st.markdown(f'<span style="{task_style}">{priority_emoji} {task_title}</span>', unsafe_allow_html=True)
                                if task_desc:
                                    st.caption(task_desc)
                            
                            with col_del:
                                if st.button("❌", key=f"del_task_{task_id}", help="Eliminar tarea"):
                                    delete_task(task_id)
                                    st.rerun()
                        
                        # Verificar si se completó automáticamente
                        if task_updated:
                            if auto_complete_epic_if_tasks_done(epic_id):
                                st.success("🎉 ¡Todas las tareas completadas! Épica movida a 'Hecho'")
                                st.rerun()
                            else:
                                st.rerun()
                        
                        # Formulario para agregar nueva tarea
                        with st.expander("➕ Agregar nueva tarea"):
                            with st.form(f"task_form_{epic_id}"):
                                new_task_title = st.text_input("Título de la tarea")
                                new_task_desc = st.text_input("Descripción (opcional)")
                                task_cols = st.columns(2)
                                with task_cols[0]:
                                    new_task_owner = st.text_input("Responsable (opcional)")
                                with task_cols[1]:
                                    new_task_priority = st.selectbox("Prioridad", ["Alta", "Media", "Baja"], index=1)
                                
                                if st.form_submit_button("Agregar tarea"):
                                    if new_task_title:
                                        create_task(new_task_title, new_task_desc, epic_id, new_task_owner, new_task_priority)
                                        st.success(f"✅ Tarea '{new_task_title}' agregada")
                                        st.rerun()
                                    else:
                                        st.warning("El título es obligatorio")
                    
                    # Controles principales en columnas
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        new_status = st.selectbox(
                            "Mover a:", states, index=states.index(state),
                            key=f"move_{epic_id}"
                        )
                        if new_status != state:
                            update_epic_status(epic_id, new_status)
                            st.success(f"✅ Épica movida a '{new_status}'")
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️", key=f"del_{epic_id}", help="Eliminar épica"):
                            if st.session_state.get(f"confirm_del_{epic_id}", False):
                                delete_epic(epic_id)
                                st.success("🗑️ Épica eliminada")
                                st.rerun()
                            else:
                                st.session_state[f"confirm_del_{epic_id}"] = True
                                st.warning("⚠️ Haz clic de nuevo para confirmar eliminación")
                    
                    st.divider()
