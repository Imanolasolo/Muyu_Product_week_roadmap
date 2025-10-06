"""
Módulo para la interfaz de generación y envío de reportes
"""

import streamlit as st
import os
from datetime import datetime
from modules.report_generator import ReportGenerator, generate_weekly_report, generate_full_report, get_report_summary
from modules.email_sender import EmailSender, EMAIL_CONFIGS, get_default_recipients

def show_reports_interface():
    """Muestra la interfaz completa de reportes"""
    st.subheader("📊 Generación de Reportes Automáticos")
    
    # Pestañas para diferentes funciones
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Generar Reporte", "📧 Envío por Email", "⚙️ Configuración", "📋 Vista Previa"])
    
    with tab1:
        show_report_generation()
    
    with tab2:
        show_email_interface()
    
    with tab3:
        show_email_configuration()
    
    with tab4:
        show_report_preview()

def show_report_generation():
    """Interfaz para generar reportes PDF"""
    st.markdown("### 📄 Generar Reporte PDF")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Opciones de reporte
        report_type = st.radio(
            "Tipo de reporte:",
            ["📅 Reporte por semana específica", "🌐 Reporte completo (todas las épicas)"]
        )
        
        week_filter = None
        if report_type.startswith("📅"):
            week_filter = st.selectbox(
                "Selecciona la semana:",
                ["Semana 40 - 2025", "Semana 41 - 2025", "Semana 42 - 2025"]
            )
        
        # Opciones adicionales
        st.markdown("**Opciones del reporte:**")
        include_charts = st.checkbox("📊 Incluir gráficos y análisis visual", value=True)
        include_tasks = st.checkbox("📝 Incluir detalle de tareas por épica", value=True)
        include_recommendations = st.checkbox("💡 Incluir recomendaciones automáticas", value=True)
    
    with col2:
        # Vista previa de métricas
        st.markdown("**📊 Vista Previa de Métricas:**")
        
        if week_filter and report_type.startswith("📅"):
            metrics = get_report_summary(week=week_filter)
            week_display = week_filter
        else:
            metrics = get_report_summary()
            week_display = "Todas las semanas"
        
        st.info(f"**Semana:** {week_display}")
        st.metric("Total Épicas", metrics['total_epics'])
        st.metric("Épicas Completadas", metrics['done'])
        st.metric("Épicas en Progreso", metrics['in_progress'])
        st.metric("Total Tareas", metrics['total_tasks'])
        
        if metrics['total_tasks'] > 0:
            progress_pct = (metrics['completed_tasks'] / metrics['total_tasks']) * 100
            st.metric("Progreso General", f"{progress_pct:.1f}%")
    
    st.divider()
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Actualizar Vista Previa", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📥 Generar y Descargar PDF", use_container_width=True, type="primary"):
            with st.spinner("Generando reporte PDF..."):
                try:
                    generator = ReportGenerator()
                    
                    if report_type.startswith("📅"):
                        pdf_path, report_metrics = generator.generate_report(week_filter=week_filter)
                    else:
                        pdf_path, report_metrics = generator.generate_report()
                    
                    # Mostrar enlace de descarga
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Descargar Reporte PDF",
                            data=pdf_file.read(),
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    st.success(f"✅ Reporte generado exitosamente: {os.path.basename(pdf_path)}")
                    
                    # Guardar información del reporte en session_state para envío por email
                    st.session_state.last_generated_report = {
                        'pdf_path': pdf_path,
                        'metrics': report_metrics,
                        'week': week_filter,
                        'timestamp': datetime.now()
                    }
                    
                except Exception as e:
                    st.error(f"❌ Error generando el reporte: {str(e)}")
    
    with col3:
        if st.button("📧 Generar y Enviar por Email", use_container_width=True):
            if 'email_config' not in st.session_state:
                st.warning("⚠️ Configura primero tu email en la pestaña 'Configuración'")
            else:
                # Generar reporte y preparar para envío
                with st.spinner("Generando reporte para envío..."):
                    try:
                        generator = ReportGenerator()
                        
                        if report_type.startswith("📅"):
                            pdf_path, report_metrics = generator.generate_report(week_filter=week_filter)
                        else:
                            pdf_path, report_metrics = generator.generate_report()
                        
                        st.session_state.last_generated_report = {
                            'pdf_path': pdf_path,
                            'metrics': report_metrics,
                            'week': week_filter,
                            'timestamp': datetime.now()
                        }
                        
                        st.success("✅ Reporte generado. Ve a la pestaña 'Envío por Email' para enviarlo.")
                        
                    except Exception as e:
                        st.error(f"❌ Error generando el reporte: {str(e)}")

def show_email_interface():
    """Interfaz para envío de reportes por email"""
    st.markdown("### 📧 Envío Automático por Email")
    
    # Verificar si hay un reporte generado
    if 'last_generated_report' not in st.session_state:
        st.info("💡 Primero genera un reporte en la pestaña 'Generar Reporte'")
        return
    
    # Verificar configuración de email
    if 'email_config' not in st.session_state:
        st.warning("⚠️ Configura tu email en la pestaña 'Configuración' antes de enviar reportes")
        return
    
    report_info = st.session_state.last_generated_report
    
    # Información del reporte a enviar
    st.markdown("**📄 Reporte a Enviar:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Archivo:** {os.path.basename(report_info['pdf_path'])}")
    with col2:
        st.info(f"**Semana:** {report_info['week'] or 'Todas'}")
    with col3:
        st.info(f"**Generado:** {report_info['timestamp'].strftime('%H:%M')}")
    
    st.divider()
    
    # Configuración de envío
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**🎯 Tipo de Destinatarios:**")
        recipient_type = st.selectbox(
            "Selecciona el tipo:",
            ["stakeholder", "ceo", "cto", "team"],
            format_func=lambda x: {
                "stakeholder": "📊 Stakeholders (General)",
                "ceo": "👔 CEO (Ejecutivo)",
                "cto": "🔧 CTO (Técnico)",
                "team": "👥 Equipo (Interno)"
            }[x]
        )
        
        # Explicación del tipo seleccionado
        type_descriptions = {
            "stakeholder": "Reporte general con métricas de progreso y estado del roadmap",
            "ceo": "Resumen ejecutivo enfocado en resultados de alto nivel",
            "cto": "Reporte técnico con detalles de desarrollo y métricas técnicas",
            "team": "Reporte interno para el equipo con progreso colaborativo"
        }
        st.caption(type_descriptions[recipient_type])
    
    with col2:
        st.markdown("**📮 Lista de Destinatarios:**")
        
        # Obtener destinatarios por defecto
        default_recipients = get_default_recipients()
        
        # Permitir editar la lista
        email_list = st.text_area(
            "Emails (uno por línea):",
            value="\n".join(default_recipients.get(recipient_type, [])),
            height=100,
            help="Ingresa un email por línea"
        )
        
        # Parsear emails
        recipients = [email.strip() for email in email_list.split('\n') if email.strip()]
        
        if recipients:
            st.success(f"✅ {len(recipients)} destinatario(s) configurado(s)")
        else:
            st.warning("⚠️ Agrega al menos un email destinatario")
    
    # Opciones adicionales
    st.markdown("**⚙️ Opciones de Envío:**")
    col1, col2 = st.columns(2)
    
    with col1:
        send_to_self = st.checkbox("📧 Enviarme una copia", value=True)
        schedule_send = st.checkbox("⏰ Programar envío automático", value=False)
    
    with col2:
        priority = st.selectbox("Prioridad:", ["Normal", "Alta", "Baja"])
        include_summary = st.checkbox("📋 Incluir resumen en el email", value=True)
    
    if schedule_send:
        st.info("🚧 Función de programación en desarrollo. Por ahora el envío es inmediato.")
    
    st.divider()
    
    # Botón de envío
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("📧 Enviar Reporte por Email", use_container_width=True, type="primary"):
            if not recipients:
                st.error("❌ Agrega al menos un destinatario")
                return
            
            # Agregar remitente a la lista si se solicita
            final_recipients = recipients.copy()
            if send_to_self and st.session_state.email_config['email'] not in final_recipients:
                final_recipients.append(st.session_state.email_config['email'])
            
            with st.spinner(f"Enviando reporte a {len(final_recipients)} destinatario(s)..."):
                try:
                    # Crear sender con la configuración guardada
                    sender = EmailSender(
                        smtp_server=st.session_state.email_config['smtp_server'],
                        smtp_port=st.session_state.email_config['smtp_port'],
                        email=st.session_state.email_config['email'],
                        password=st.session_state.email_config['password']
                    )
                    
                    # Enviar reporte
                    success, message = sender.send_report(
                        pdf_path=report_info['pdf_path'],
                        recipients=final_recipients,
                        recipient_type=recipient_type,
                        metrics=report_info['metrics'],
                        week=report_info['week']
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        
                        # Mostrar resumen del envío
                        st.markdown("**📊 Resumen del Envío:**")
                        st.info(f"• **Destinatarios:** {len(final_recipients)}\n• **Tipo:** {recipient_type.title()}\n• **Archivo:** {os.path.basename(report_info['pdf_path'])}")
                        
                    else:
                        st.error(f"❌ {message}")
                        
                except Exception as e:
                    st.error(f"❌ Error enviando el reporte: {str(e)}")

def show_email_configuration():
    """Interfaz para configurar el email"""
    st.markdown("### ⚙️ Configuración de Email")
    
    # Selección de proveedor
    st.markdown("**📮 Proveedor de Email:**")
    provider = st.selectbox(
        "Selecciona tu proveedor:",
        list(EMAIL_CONFIGS.keys()),
        format_func=lambda x: x.title()
    )
    
    config = EMAIL_CONFIGS[provider]
    st.info(f"ℹ️ {config['instructions']}")
    
    # Alerta especial para Gmail
    if provider == 'gmail':
        st.warning("""
        ⚠️ **Gmail requiere configuración especial:**
        1. Activar verificación en 2 pasos
        2. Generar App Password de 16 caracteres
        3. NO usar contraseña normal
        """)
        
        col_warn1, col_warn2 = st.columns(2)
        with col_warn1:
            if st.button("🔗 Configurar Gmail", key="config_gmail"):
                st.markdown("""
                **Enlaces directos:**
                - [🔐 App Passwords](https://myaccount.google.com/apppasswords)
                - [🛡️ Seguridad](https://myaccount.google.com/security)
                """)
        
        with col_warn2:
            if st.button("🔄 Cambiar a Outlook (más fácil)", key="switch_outlook"):
                st.session_state.email_provider_switch = 'outlook'
                st.rerun()
    
    # Auto-switch a Outlook si se solicitó
    if st.session_state.get('email_provider_switch') == 'outlook':
        provider = 'outlook'
        config = EMAIL_CONFIGS[provider]
        st.success("✅ Cambiado a Outlook - configuración más simple")
        st.session_state.email_provider_switch = None
    
    # Configuración manual
    use_advanced = st.checkbox("🔧 Configuración Avanzada", value=False)
    
    if use_advanced:
        custom_smtp = st.text_input("Servidor SMTP personalizado:", value=config['smtp_server'])
        custom_port = st.number_input("Puerto SMTP:", value=config['smtp_port'], min_value=1, max_value=65535)
    else:
        custom_smtp = config['smtp_server']
        custom_port = config['smtp_port']
    
    # Credenciales
    st.markdown("**🔐 Credenciales:**")
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("Tu email:", placeholder="ejemplo@gmail.com")
    
    with col2:
        sender_password = st.text_input("Contraseña/App Password:", type="password")
    
    # Configuración de destinatarios por defecto
    st.markdown("**👥 Destinatarios por Defecto:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ceo_emails = st.text_area("📊 CEO/Ejecutivos:", placeholder="ceo@empresa.com")
        stakeholder_emails = st.text_area("👔 Stakeholders:", placeholder="stakeholder1@empresa.com\nstakeholder2@empresa.com")
    
    with col2:
        cto_emails = st.text_area("🔧 CTO/Técnicos:", placeholder="cto@empresa.com")
        team_emails = st.text_area("👥 Equipo:", placeholder="dev1@empresa.com\ndev2@empresa.com")
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🧪 Probar Conexión", use_container_width=True):
            if sender_email and sender_password:
                with st.spinner("Probando conexión SMTP..."):
                    try:
                        import smtplib
                        import ssl
                        
                        # Diagnóstico mejorado para Gmail
                        if 'gmail.com' in custom_smtp:
                            # Verificar formato App Password para Gmail
                            if len(sender_password) != 16 or ' ' in sender_password:
                                st.error("❌ Gmail requiere App Password de exactamente 16 caracteres sin espacios")
                                st.info("💡 Ve a https://myaccount.google.com/apppasswords para generar una nueva")
                                return
                        
                        # Intentar conexión TLS (puerto 587)
                        if custom_port == 587:
                            server = smtplib.SMTP(custom_smtp, custom_port)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.quit()
                            st.success("✅ Conexión TLS exitosa!")
                        
                        # Intentar conexión SSL (puerto 465)
                        elif custom_port == 465:
                            context = ssl.create_default_context()
                            server = smtplib.SMTP_SSL(custom_smtp, custom_port, context=context)
                            server.login(sender_email, sender_password)
                            server.quit()
                            st.success("✅ Conexión SSL exitosa!")
                        
                        else:
                            # Puerto personalizado
                            server = smtplib.SMTP(custom_smtp, custom_port)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.quit()
                            st.success("✅ Conexión exitosa!")
                            
                    except Exception as e:
                        error_msg = str(e)
                        st.error(f"❌ Error de conexión: {error_msg}")
                        
                        # Diagnóstico específico para errores comunes
                        if "535" in error_msg and "gmail" in sender_email.lower():
                            st.warning("🔧 Error de autenticación Gmail detectado")
                            with st.expander("📋 Guía de Solución Gmail", expanded=True):
                                st.markdown("""
                                **Soluciones paso a paso:**
                                
                                1. **Verifica 2FA activada**: https://myaccount.google.com/security
                                2. **Genera nueva App Password**: https://myaccount.google.com/apppasswords
                                3. **Formato correcto**: 16 caracteres sin espacios (ej: `abcdabcdabcdabcd`)
                                4. **NO uses**: Tu contraseña normal de Gmail
                                
                                **Si sigue fallando:**
                                - Elimina App Passwords existentes
                                - Genera una nueva específicamente para "Roadmap App"
                                - Espera 2-3 minutos antes de probar
                                """)
                                
                                if st.button("🔗 Abrir configuración Gmail", key="gmail_config"):
                                    st.markdown("[🔐 App Passwords](https://myaccount.google.com/apppasswords)")
                        
                        elif "534" in error_msg:
                            st.info("💡 Código 534: Prueba con Outlook como alternativa más fácil")
                        
                        elif "timeout" in error_msg.lower():
                            st.info("💡 Timeout: Verifica tu conexión a internet y firewall")
            else:
                st.warning("⚠️ Ingresa email y contraseña")
    
    with col2:
        if st.button("💾 Guardar Configuración", use_container_width=True, type="primary"):
            if sender_email and sender_password:
                # Guardar en session_state
                st.session_state.email_config = {
                    'smtp_server': custom_smtp,
                    'smtp_port': custom_port,
                    'email': sender_email,
                    'password': sender_password,
                    'provider': provider
                }
                
                # Guardar destinatarios por defecto
                st.session_state.default_recipients = {
                    'ceo': [email.strip() for email in ceo_emails.split('\n') if email.strip()],
                    'cto': [email.strip() for email in cto_emails.split('\n') if email.strip()],
                    'stakeholders': [email.strip() for email in stakeholder_emails.split('\n') if email.strip()],
                    'team': [email.strip() for email in team_emails.split('\n') if email.strip()]
                }
                
                st.success("✅ Configuración guardada correctamente")
            else:
                st.warning("⚠️ Email y contraseña son obligatorios")
    
    with col3:
        if st.button("🗑️ Limpiar Config", use_container_width=True):
            if 'email_config' in st.session_state:
                del st.session_state.email_config
            if 'default_recipients' in st.session_state:
                del st.session_state.default_recipients
            st.success("✅ Configuración eliminada")
            st.rerun()
    
    # Mostrar configuración actual
    if 'email_config' in st.session_state:
        st.divider()
        st.markdown("**📋 Configuración Actual:**")
        config = st.session_state.email_config
        st.info(f"**Email:** {config['email']}\n**Servidor:** {config['smtp_server']}:{config['smtp_port']}\n**Proveedor:** {config['provider'].title()}")

def show_report_preview():
    """Vista previa del contenido del reporte"""
    st.markdown("### 📋 Vista Previa del Reporte")
    
    # Selector de semana para preview
    preview_week = st.selectbox(
        "Selecciona semana para vista previa:",
        [None] + ["Semana 40 - 2025", "Semana 41 - 2025", "Semana 42 - 2025"],
        format_func=lambda x: "Todas las semanas" if x is None else x
    )
    
    # Obtener métricas
    metrics = get_report_summary(week=preview_week)
    
    if metrics['total_epics'] == 0:
        st.warning("⚠️ No hay épicas para mostrar. Crea algunas épicas primero.")
        return
    
    # Mostrar vista previa del contenido
    st.markdown("#### 📊 Resumen Ejecutivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Épicas", metrics['total_epics'])
    with col2:
        st.metric("Completadas", metrics['done'], 
                 delta=f"{metrics['done']/metrics['total_epics']*100:.1f}%")
    with col3:
        st.metric("En Progreso", metrics['in_progress'])
    with col4:
        st.metric("Pendientes", metrics['pending'])
    
    # Progreso de tareas
    if metrics['total_tasks'] > 0:
        progress = metrics['completed_tasks'] / metrics['total_tasks']
        st.progress(progress)
        st.caption(f"Progreso de tareas: {metrics['completed_tasks']}/{metrics['total_tasks']} ({progress*100:.1f}%)")
    
    # Detalle de épicas
    st.markdown("#### 📋 Detalle de Épicas")
    
    for epic in metrics['epic_details']:
        with st.expander(f"📌 {epic['name']} ({epic['status']})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Descripción:** {epic['description'] or 'Sin descripción'}")
                st.write(f"**Semana:** {epic['week']}")
                
                if epic['tasks_total'] > 0:
                    st.progress(epic['progress_percentage'] / 100)
                    st.caption(f"Progreso: {epic['tasks_completed']}/{epic['tasks_total']} tareas")
            
            with col2:
                # Indicador de estado
                status_colors = {
                    'Pendiente': '🔴',
                    'En progreso': '🟡',
                    'Hecho': '🟢'
                }
                st.markdown(f"### {status_colors.get(epic['status'], '⚪')} {epic['status']}")
    
    # Recomendaciones automáticas
    st.markdown("#### 💡 Recomendaciones")
    
    recommendations = []
    
    if metrics['pending'] > metrics['in_progress']:
        recommendations.append("• Considerar mover más épicas a 'En progreso'")
    
    total_progress = (metrics['completed_tasks'] / metrics['total_tasks'] * 100) if metrics['total_tasks'] > 0 else 0
    if total_progress < 50:
        recommendations.append("• El progreso general está por debajo del 50%")
    
    if not recommendations:
        recommendations.append("• El proyecto está progresando adecuadamente")
    
    for rec in recommendations:
        st.write(rec)
    
    st.divider()
    st.info("💡 Esta es una vista previa del contenido que se incluirá en el reporte PDF")