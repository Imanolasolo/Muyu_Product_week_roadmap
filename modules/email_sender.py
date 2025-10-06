"""
Módulo para envío automático de reportes por email
Incluye configuración SMTP y plantillas de email
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
import streamlit as st

class EmailSender:
    def __init__(self, smtp_server=None, smtp_port=587, email=None, password=None):
        """
        Inicializa el enviador de emails
        
        Args:
            smtp_server: Servidor SMTP (ej: smtp.gmail.com)
            smtp_port: Puerto SMTP (587 para TLS, 465 para SSL)
            email: Email del remitente
            password: Contraseña o app password del remitente
        """
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
        self.email = email or os.getenv('SENDER_EMAIL')
        self.password = password or os.getenv('SENDER_PASSWORD')
        
    def create_email_template(self, recipient_type, metrics, week=None):
        """
        Crea plantilla de email según el tipo de destinatario
        
        Args:
            recipient_type: 'ceo', 'cto', 'stakeholder', 'team'
            metrics: Métricas del reporte
            week: Semana específica (opcional)
        """
        templates = {
            'ceo': {
                'subject': f'📊 Reporte Ejecutivo - Roadmap Semanal {week or "Completo"}',
                'greeting': 'Estimado/a CEO,',
                'focus': 'resumen ejecutivo y métricas clave',
                'content': f"""
                <h2>Resumen Ejecutivo del Roadmap</h2>
                <p>Me complace presentar el reporte semanal de nuestro roadmap de producto:</p>
                
                <div style="background-color: #f0f8ff; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3>🎯 Métricas Clave</h3>
                    <ul>
                        <li><strong>Épicas Completadas:</strong> {metrics['done']} de {metrics['total_epics']} ({metrics['done']/metrics['total_epics']*100:.1f}%)</li>
                        <li><strong>Progreso de Tareas:</strong> {metrics['completed_tasks']} de {metrics['total_tasks']} ({metrics['completed_tasks']/metrics['total_tasks']*100 if metrics['total_tasks'] > 0 else 0:.1f}%)</li>
                        <li><strong>Épicas en Progreso:</strong> {metrics['in_progress']}</li>
                    </ul>
                </div>
                
                <h3>📈 Estado General</h3>
                <p>El equipo está ejecutando {metrics['in_progress']} épicas activamente, con un progreso general del 
                {metrics['completed_tasks']/metrics['total_tasks']*100 if metrics['total_tasks'] > 0 else 0:.1f}% en tareas completadas.</p>
                """
            },
            
            'cto': {
                'subject': f'🔧 Reporte Técnico - Roadmap Semanal {week or "Completo"}',
                'greeting': 'Estimado/a CTO,',
                'focus': 'detalles técnicos y progreso de desarrollo',
                'content': f"""
                <h2>Reporte Técnico del Roadmap</h2>
                <p>Adjunto encontrarás el análisis detallado del progreso técnico:</p>
                
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3>⚙️ Métricas de Desarrollo</h3>
                    <ul>
                        <li><strong>Total de Épicas:</strong> {metrics['total_epics']}</li>
                        <li><strong>Completadas:</strong> {metrics['done']} ✅</li>
                        <li><strong>En Desarrollo:</strong> {metrics['in_progress']} 🔧</li>
                        <li><strong>Pendientes:</strong> {metrics['pending']} ⏳</li>
                        <li><strong>Tareas Técnicas:</strong> {metrics['completed_tasks']}/{metrics['total_tasks']}</li>
                    </ul>
                </div>
                
                <h3>🚀 Recomendaciones Técnicas</h3>
                <p>El reporte PDF adjunto incluye análisis detallado de cada épica, 
                progreso de tareas técnicas y recomendaciones específicas para optimizar el desarrollo.</p>
                """
            },
            
            'stakeholder': {
                'subject': f'📋 Update del Roadmap - {week or "Reporte Completo"}',
                'greeting': 'Estimado Stakeholder,',
                'focus': 'progreso del producto y impacto en el negocio',
                'content': f"""
                <h2>Update del Roadmap de Producto</h2>
                <p>Te compartimos el progreso actual de nuestras iniciativas de producto:</p>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3>📊 Progreso General</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iniciativas Totales</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{metrics['total_epics']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Completadas</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{metrics['done']} ✅</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>En Ejecución</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{metrics['in_progress']} 🚀</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Planificadas</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{metrics['pending']} 📋</td>
                        </tr>
                    </table>
                </div>
                
                <p>El reporte detallado se encuentra adjunto con análisis completo y próximos pasos.</p>
                """
            },
            
            'team': {
                'subject': f'👥 Reporte del Equipo - Roadmap {week or "Completo"}',
                'greeting': 'Hola Equipo,',
                'focus': 'progreso colaborativo y próximas tareas',
                'content': f"""
                <h2>Reporte de Progreso del Equipo</h2>
                <p>¡Excelente trabajo! Aquí está nuestro progreso actualizado:</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3>🎉 Logros del Equipo</h3>
                    <ul>
                        <li><strong>Épicas Completadas:</strong> {metrics['done']} 🎯</li>
                        <li><strong>Tareas Finalizadas:</strong> {metrics['completed_tasks']} ✅</li>
                        <li><strong>Épicas Activas:</strong> {metrics['in_progress']} 🔧</li>
                        <li><strong>Progreso General:</strong> {metrics['completed_tasks']/metrics['total_tasks']*100 if metrics['total_tasks'] > 0 else 0:.1f}% 📈</li>
                    </ul>
                </div>
                
                <h3>🚀 Próximos Pasos</h3>
                <p>Continuemos con el excelente momentum. El reporte detallado incluye el breakdown 
                completo de tareas por épica y asignaciones del equipo.</p>
                """
            }
        }
        
        return templates.get(recipient_type, templates['stakeholder'])
    
    def send_report(self, pdf_path, recipients, recipient_type='stakeholder', metrics=None, week=None):
        """
        Envía el reporte por email
        
        Args:
            pdf_path: Ruta al archivo PDF del reporte
            recipients: Lista de emails destinatarios
            recipient_type: Tipo de destinatario para personalizar el mensaje
            metrics: Métricas del reporte
            week: Semana específica (opcional)
        """
        if not all([self.smtp_server, self.email, self.password]):
            raise ValueError("Configuración SMTP incompleta. Verifica las variables de entorno.")
        
        # Crear plantilla de email
        template = self.create_email_template(recipient_type, metrics, week)
        
        try:
            # Configurar servidor SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            for recipient in recipients:
                # Crear mensaje
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = recipient
                msg['Subject'] = template['subject']
                msg['Date'] = formatdate(localtime=True)
                
                # Cuerpo del email
                body = f"""
                <html>
                <head></head>
                <body>
                    <p>{template['greeting']}</p>
                    
                    {template['content']}
                    
                    <hr style="margin: 30px 0;">
                    
                    <p><strong>📎 Archivo Adjunto:</strong> Reporte detallado en PDF con gráficos y análisis completo.</p>
                    
                    <p>Saludos cordiales,<br>
                    <strong>Sistema de Roadmap Semanal</strong></p>
                    
                    <footer style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
                        <p>Este reporte fue generado automáticamente el {formatdate(localtime=True)}</p>
                        <p>Para más información, contacta al equipo de producto.</p>
                    </footer>
                </body>
                </html>
                """
                
                msg.attach(MIMEText(body, 'html'))
                
                # Adjuntar PDF
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(pdf_path)}'
                    )
                    msg.attach(part)
                
                # Enviar email
                server.send_message(msg)
                print(f"✅ Reporte enviado exitosamente a {recipient}")
            
            server.quit()
            return True, "Reportes enviados exitosamente"
            
        except Exception as e:
            return False, f"Error enviando emails: {str(e)}"

# Configuraciones predefinidas para diferentes organizaciones
EMAIL_CONFIGS = {
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'instructions': '⚠️ Gmail requiere: 1) Verificación 2FA activada, 2) App Password de 16 caracteres (NO tu contraseña normal)',
        'setup_url': 'https://myaccount.google.com/apppasswords',
        'difficulty': 'Avanzado',
        'common_errors': ['535 Username and Password not accepted', 'App Password requerida']
    },
    'outlook': {
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587,
        'instructions': '✅ Outlook es más fácil: usa tu email y contraseña normal. No requiere configuración especial.',
        'setup_url': None,
        'difficulty': 'Fácil',
        'common_errors': []
    },
    'office365': {
        'smtp_server': 'smtp.office365.com',
        'smtp_port': 587,
        'instructions': 'Para Office 365 corporativo: usa tu email de empresa y contraseña. Consulta con IT si tienes problemas.',
        'setup_url': None,
        'difficulty': 'Medio',
        'common_errors': ['Puede requerir configuración corporativa']
    }
}

def get_default_recipients():
    """Obtiene lista de destinatarios por defecto desde variables de entorno"""
    return {
        'ceo': os.getenv('CEO_EMAIL', '').split(',') if os.getenv('CEO_EMAIL') else [],
        'cto': os.getenv('CTO_EMAIL', '').split(',') if os.getenv('CTO_EMAIL') else [],
        'stakeholders': os.getenv('STAKEHOLDER_EMAILS', '').split(',') if os.getenv('STAKEHOLDER_EMAILS') else [],
        'team': os.getenv('TEAM_EMAILS', '').split(',') if os.getenv('TEAM_EMAILS') else []
    }