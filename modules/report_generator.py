"""
Módulo para generar reportes automáticos en PDF
Incluye métricas, gráficos y análisis de progreso
"""

import os
import datetime
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor

from db.db_manager import (
    get_all_epics, get_tasks_by_epic, get_task_completion_status,
    get_epic_count_by_week
)

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configura estilos personalizados para el reporte"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2E86AB'),
            alignment=1  # Centrado
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#A23B72'),
        ))
        
        # Estilo para métricas destacadas
        self.styles.add(ParagraphStyle(
            name='MetricStyle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#F18F01'),
            alignment=1
        ))

    def get_epic_metrics(self):
        """Obtiene métricas generales de las épicas"""
        all_epics = get_all_epics()
        
        metrics = {
            'total_epics': len(all_epics),
            'pending': 0,
            'in_progress': 0,
            'done': 0,
            'total_tasks': 0,
            'completed_tasks': 0,
            'epic_details': []
        }
        
        for epic in all_epics:
            epic_id, name, description, week, status = epic
            completed, total, percentage = get_task_completion_status(epic_id)
            
            # Contar épicas por estado
            if status == 'Pendiente':
                metrics['pending'] += 1
            elif status == 'En progreso':
                metrics['in_progress'] += 1
            elif status == 'Hecho':
                metrics['done'] += 1
            
            # Contar tareas
            metrics['total_tasks'] += total
            metrics['completed_tasks'] += completed
            
            # Detalles de épica
            metrics['epic_details'].append({
                'id': epic_id,
                'name': name,
                'description': description,
                'week': week,
                'status': status,
                'tasks_completed': completed,
                'tasks_total': total,
                'progress_percentage': percentage
            })
        
        return metrics

    def create_metrics_chart(self, metrics):
        """Crea gráfico de métricas de épicas"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de torta - Estados de épicas
        states = ['Pendiente', 'En progreso', 'Hecho']
        values = [metrics['pending'], metrics['in_progress'], metrics['done']]
        colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        ax1.pie(values, labels=states, colors=colors_pie, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribución de Épicas por Estado', fontsize=14, fontweight='bold')
        
        # Gráfico de barras - Progreso de tareas
        weeks = list(set([epic['week'] for epic in metrics['epic_details']]))
        week_progress = {}
        
        for week in weeks:
            week_epics = [e for e in metrics['epic_details'] if e['week'] == week]
            total_tasks = sum([e['tasks_total'] for e in week_epics])
            completed_tasks = sum([e['tasks_completed'] for e in week_epics])
            week_progress[week] = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        ax2.bar(range(len(weeks)), list(week_progress.values()), color='#45B7D1')
        ax2.set_xlabel('Semanas')
        ax2.set_ylabel('% Progreso')
        ax2.set_title('Progreso de Tareas por Semana', fontsize=14, fontweight='bold')
        ax2.set_xticks(range(len(weeks)))
        ax2.set_xticklabels([w.replace(' - 2025', '') for w in weeks], rotation=45)
        
        plt.tight_layout()
        
        # Guardar en memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer

    def create_epic_progress_chart(self, metrics):
        """Crea gráfico de progreso individual de épicas"""
        epic_names = [e['name'][:30] + '...' if len(e['name']) > 30 else e['name'] 
                     for e in metrics['epic_details']]
        progress_values = [e['progress_percentage'] for e in metrics['epic_details']]
        
        fig, ax = plt.subplots(figsize=(12, len(epic_names) * 0.5 + 2))
        
        # Colores basados en progreso
        colors_bar = ['#FF6B6B' if p < 30 else '#4ECDC4' if p < 80 else '#45B7D1' 
                      for p in progress_values]
        
        bars = ax.barh(epic_names, progress_values, color=colors_bar)
        ax.set_xlabel('Progreso (%)')
        ax.set_title('Progreso Individual de Épicas', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        # Agregar etiquetas de porcentaje
        for i, (bar, progress) in enumerate(zip(bars, progress_values)):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                   f'{progress:.1f}%', va='center', fontsize=10)
        
        plt.tight_layout()
        
        # Guardar en memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer

    def generate_report(self, week_filter=None, output_path=None):
        """Genera el reporte completo en PDF"""
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"reports/roadmap_report_{timestamp}.pdf"
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Obtener métricas
        metrics = self.get_epic_metrics()
        
        # Filtrar por semana si se especifica
        if week_filter:
            metrics['epic_details'] = [e for e in metrics['epic_details'] 
                                     if e['week'] == week_filter]
        
        # TÍTULO Y FECHA
        story.append(Paragraph("🚀 REPORTE DE ROADMAP SEMANAL", self.styles['CustomTitle']))
        story.append(Paragraph(f"Generado el: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                              self.styles['Normal']))
        if week_filter:
            story.append(Paragraph(f"Filtrado por: {week_filter}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # RESUMEN EJECUTIVO
        story.append(Paragraph("📊 RESUMEN EJECUTIVO", self.styles['CustomHeading']))
        
        total_progress = (metrics['completed_tasks'] / metrics['total_tasks'] * 100) if metrics['total_tasks'] > 0 else 0
        
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de Épicas', str(metrics['total_epics'])],
            ['Épicas Completadas', str(metrics['done'])],
            ['Épicas en Progreso', str(metrics['in_progress'])],
            ['Épicas Pendientes', str(metrics['pending'])],
            ['Total de Tareas', str(metrics['total_tasks'])],
            ['Tareas Completadas', str(metrics['completed_tasks'])],
            ['Progreso General', f"{total_progress:.1f}%"]
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # GRÁFICOS
        story.append(Paragraph("📈 ANÁLISIS VISUAL", self.styles['CustomHeading']))
        
        # Gráfico de métricas
        chart_buffer = self.create_metrics_chart(metrics)
        chart_img = Image(chart_buffer, width=7*inch, height=3*inch)
        story.append(chart_img)
        story.append(Spacer(1, 20))
        
        # Gráfico de progreso individual
        if metrics['epic_details']:
            progress_buffer = self.create_epic_progress_chart(metrics)
            progress_img = Image(progress_buffer, width=7*inch, height=len(metrics['epic_details'])*0.3*inch + 2*inch)
            story.append(progress_img)
            story.append(Spacer(1, 20))
        
        # DETALLE DE ÉPICAS
        story.append(Paragraph("📋 DETALLE DE ÉPICAS", self.styles['CustomHeading']))
        
        for epic in metrics['epic_details']:
            # Título de épica
            epic_title = f"📌 {epic['name']} ({epic['status']})"
            story.append(Paragraph(epic_title, self.styles['Heading3']))
            
            # Información de la épica
            epic_info = [
                ['Campo', 'Valor'],
                ['Semana', epic['week']],
                ['Estado', epic['status']],
                ['Descripción', epic['description'] or 'Sin descripción'],
                ['Progreso de Tareas', f"{epic['tasks_completed']}/{epic['tasks_total']} ({epic['progress_percentage']:.1f}%)"]
            ]
            
            epic_table = Table(epic_info, colWidths=[2*inch, 4*inch])
            epic_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A23B72')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(epic_table)
            
            # Tareas de la épica
            tasks = get_tasks_by_epic(epic['id'])
            if tasks:
                story.append(Paragraph("Tareas:", self.styles['Heading4']))
                task_data = [['Tarea', 'Responsable', 'Prioridad', 'Estado']]
                for task in tasks:
                    task_id, title, desc, _, owner, priority, status = task
                    task_data.append([
                        title[:40] + '...' if len(title) > 40 else title,
                        owner or 'Sin asignar',
                        priority,
                        '✅' if status == 'Completado' else '⏳'
                    ])
                
                task_table = Table(task_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 0.8*inch])
                task_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4ECDC4')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(task_table)
            
            story.append(Spacer(1, 15))
        
        # RECOMENDACIONES
        story.append(Paragraph("💡 RECOMENDACIONES", self.styles['CustomHeading']))
        
        recommendations = []
        
        if metrics['pending'] > metrics['in_progress']:
            recommendations.append("• Considerar mover más épicas a 'En progreso' para acelerar el desarrollo")
        
        if total_progress < 50:
            recommendations.append("• El progreso general está por debajo del 50%. Revisar recursos y prioridades")
        
        blocked_epics = [e for e in metrics['epic_details'] 
                        if e['status'] == 'En progreso' and e['progress_percentage'] == 0]
        if blocked_epics:
            recommendations.append(f"• {len(blocked_epics)} épicas en progreso sin tareas completadas. Revisar posibles bloqueos")
        
        if not recommendations:
            recommendations.append("• El proyecto está progresando adecuadamente. Continuar con el plan actual")
        
        for rec in recommendations:
            story.append(Paragraph(rec, self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # PIE DE PÁGINA
        story.append(Paragraph("---", self.styles['Normal']))
        story.append(Paragraph("📧 Reporte generado automáticamente por el Sistema de Roadmap Semanal", 
                              self.styles['Normal']))
        
        # Generar PDF
        doc.build(story)
        
        return output_path, metrics

# Funciones utilitarias
def generate_weekly_report(week):
    """Genera reporte para una semana específica"""
    generator = ReportGenerator()
    return generator.generate_report(week_filter=week)

def generate_full_report():
    """Genera reporte completo de todas las épicas"""
    generator = ReportGenerator()
    return generator.generate_report()

def get_report_summary(week=None):
    """Obtiene resumen rápido para mostrar en la interfaz"""
    generator = ReportGenerator()
    metrics = generator.get_epic_metrics()
    
    if week:
        metrics['epic_details'] = [e for e in metrics['epic_details'] if e['week'] == week]
        # Recalcular métricas filtradas
        metrics['total_epics'] = len(metrics['epic_details'])
        metrics['pending'] = len([e for e in metrics['epic_details'] if e['status'] == 'Pendiente'])
        metrics['in_progress'] = len([e for e in metrics['epic_details'] if e['status'] == 'En progreso'])
        metrics['done'] = len([e for e in metrics['epic_details'] if e['status'] == 'Hecho'])
        metrics['total_tasks'] = sum([e['tasks_total'] for e in metrics['epic_details']])
        metrics['completed_tasks'] = sum([e['tasks_completed'] for e in metrics['epic_details']])
    
    return metrics