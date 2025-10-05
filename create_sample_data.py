#!/usr/bin/env python3
"""
Script para crear datos de prueba para el sistema de roadmap
"""

from db.db_setup import init_db
from db.db_manager import create_epic, create_task

def create_sample_data():
    print("🚀 Creando datos de prueba...")
    
    # Inicializar base de datos
    init_db()
    
    # Crear épicas de ejemplo
    epic_examples = [
        {
            "name": "Implementar autenticación de usuarios",
            "description": "Sistema completo de login y registro de usuarios",
            "week": "Semana 40 - 2025",
            "status": "En progreso",
            "tasks": [
                {"title": "Diseñar esquema de base de datos", "priority": "Alta", "owner": "Backend Dev"},
                {"title": "Implementar endpoints de API", "priority": "Alta", "owner": "Backend Dev"},
                {"title": "Crear formularios de login/registro", "priority": "Media", "owner": "Frontend Dev"},
                {"title": "Agregar validaciones", "priority": "Media", "owner": "Frontend Dev"},
                {"title": "Pruebas de seguridad", "priority": "Alta", "owner": "QA"},
            ]
        },
        {
            "name": "Optimizar rendimiento de la aplicación",
            "description": "Mejorar tiempos de carga y responsividad",
            "week": "Semana 41 - 2025",
            "status": "Pendiente",
            "tasks": [
                {"title": "Análisis de performance actual", "priority": "Alta", "owner": "Tech Lead"},
                {"title": "Optimizar consultas de base de datos", "priority": "Alta", "owner": "Backend Dev"},
                {"title": "Implementar caché", "priority": "Media", "owner": "Backend Dev"},
                {"title": "Comprimir assets estáticos", "priority": "Baja", "owner": "Frontend Dev"},
            ]
        },
        {
            "name": "Dashboard de métricas",
            "description": "Panel para visualizar KPIs y métricas del negocio",
            "week": "Semana 42 - 2025",
            "status": "Pendiente",
            "tasks": [
                {"title": "Definir métricas a mostrar", "priority": "Alta", "owner": "Product Manager"},
                {"title": "Diseñar mockups del dashboard", "priority": "Alta", "owner": "UX Designer"},
                {"title": "Implementar gráficos interactivos", "priority": "Media", "owner": "Frontend Dev"},
                {"title": "Conectar con APIs de datos", "priority": "Media", "owner": "Backend Dev"},
            ]
        }
    ]
    
    for epic_data in epic_examples:
        # Crear épica
        create_epic(
            epic_data["name"],
            epic_data["description"],
            epic_data["week"],
            epic_data["status"]
        )
        
        # Obtener ID de la épica recién creada (asumiendo que es la última)
        from db.db_manager import get_all_epics
        all_epics = get_all_epics()
        epic_id = all_epics[0][0] if all_epics else None
        
        # Crear tareas para esta épica
        if epic_id:
            for task_data in epic_data["tasks"]:
                create_task(
                    task_data["title"],
                    "",  # descripción vacía
                    epic_id,
                    task_data["owner"],
                    task_data["priority"]
                )
        
        print(f"✅ Épica creada: {epic_data['name']} con {len(epic_data['tasks'])} tareas")
    
    print("🎉 ¡Datos de prueba creados exitosamente!")
    print("Ejecuta 'streamlit run app.py' para ver el resultado")

if __name__ == "__main__":
    create_sample_data()