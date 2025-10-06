# 🚀 Roadmap Semanal - Reunión de Lunes

Sistema de gestión de épicas y tareas para reuniones semanales de producto.

## ✨ Características

- 📋 **Tablero Kanban** con estados: Pendiente, En progreso, Hecho
- ✅ **Checklist de tareas** para cada épica
- 🔄 **Auto-completación** de épicas cuando todas las tareas están hechas
- 📊 **Barra de progreso** visual por épica
- 🎯 **Priorización** de tareas (Alta, Media, Baja)
- 👥 **Asignación** de responsables
- 📅 **Gestión por semanas**
- 📄 **Reportes PDF automáticos** con gráficos y métricas
- 📧 **Envío automático por email** a stakeholders
- 📈 **Análisis visual** con gráficos de progreso
- 💡 **Recomendaciones automáticas** basadas en datos

## 🛠️ Instalación

### Opción 1: Instalación mínima
```bash
pip install -r requirements-minimal.txt
```

### Opción 2: Instalación completa (con herramientas adicionales)
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar la aplicación
```bash
streamlit run app.py
```

### Crear datos de prueba
```bash
python create_sample_data.py
```

### Generar reportes de demostración
```bash
python demo_reports.py
```

## 📁 Estructura del Proyecto

```
📦 Muyu_Product_week_roadmap/
├── 📄 app.py                    # Aplicación principal
├── 📄 requirements.txt          # Dependencias completas
├── 📄 requirements-minimal.txt  # Dependencias mínimas
├── 📄 create_sample_data.py     # Script para datos de prueba
├── 📁 db/
│   ├── 📄 db_setup.py          # Configuración de base de datos
│   └── 📄 db_manager.py        # Gestión de datos
├── 📁 modules/
│   ├── 📄 epic_form.py         # Formulario de épicas
│   └── 📄 epic_board.py        # Tablero principal
└── 📄 roadmap.db               # Base de datos SQLite (se crea automáticamente)
```

## 💡 Cómo usar

1. **Crear épicas**: Ve a la pestaña "➕ Nueva épica"
2. **Agregar tareas**: En épicas "En progreso", usa el checklist
3. **Completar tareas**: Marca los checkboxes para completar
4. **Auto-completación**: Las épicas pasan automáticamente a "Hecho"
5. **Generar reportes**: Ve a la pestaña "📊 Reportes" para crear PDFs
6. **Enviar por email**: Configura tu email y envía automáticamente a stakeholders

## 🔧 Funcionalidades

### Tablero Principal
- Vista por columnas (Pendiente | En progreso | Hecho)
- Contador de épicas por estado
- Botón de actualización manual

### Gestión de Épicas
- Crear, editar y eliminar épicas
- Mover entre estados
- Barra de progreso visual

### Sistema de Tareas
- Checklist interactivo
- Priorización con emojis (🔴🟡🟢)
- Asignación de responsables
- Eliminación individual

### Sistema de Reportes
- Generación automática de PDFs profesionales
- Gráficos de progreso y métricas visuales
- Reportes por semana específica o completos
- Análisis automático de progreso

### Envío por Email
- Plantillas personalizadas por tipo de destinatario
- Soporte para Gmail, Outlook, Office 365
- Envío automático a CEOs, CTOs, stakeholders
- Configuración de destinatarios por defecto

## 🎯 Casos de Uso

- **Reuniones de lunes**: Planificación semanal
- **Seguimiento de sprints**: Control de progreso
- **Gestión de producto**: Roadmap visual
- **Coordinación de equipos**: Asignación clara

## 🐛 Troubleshooting

### La épica no aparece en el tablero
1. Revisa el panel de debug (🔍)
2. Verifica que la semana coincida
3. Usa el botón "🔄 Actualizar tablero"

### Las tareas no se guardan
1. Asegúrate de que el título no esté vacío
2. Verifica permisos de escritura en la carpeta
3. Reinicia la aplicación

## 📝 Roadmap Futuro

- [ ] Exportar a Excel/CSV
- [ ] Notificaciones por email
- [ ] Integración con calendarios
- [ ] Métricas y reportes
- [ ] Plantillas de épicas
- [ ] Historial de cambios

---

Desarrollado con ❤️ usando Streamlit