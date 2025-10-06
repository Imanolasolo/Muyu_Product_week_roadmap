#!/usr/bin/env python3
"""
Script de demostración para generar reportes PDF de ejemplo
Útil para probar el sistema sin configurar email
"""

import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.report_generator import ReportGenerator, generate_weekly_report, generate_full_report
from db.db_setup import init_db

def demo_report_generation():
    print("🚀 Demo de Generación de Reportes PDF")
    print("=" * 50)
    
    # Inicializar DB
    init_db()
    
    try:
        # Crear generador
        generator = ReportGenerator()
        
        print("1. 📊 Generando reporte completo...")
        full_report_path, full_metrics = generator.generate_report()
        print(f"   ✅ Reporte completo generado: {full_report_path}")
        print(f"   📈 Métricas: {full_metrics['total_epics']} épicas, {full_metrics['total_tasks']} tareas")
        
        print("\n2. 📅 Generando reporte semanal...")
        week_report_path, week_metrics = generator.generate_report(week_filter="Semana 40 - 2025")
        print(f"   ✅ Reporte semanal generado: {week_report_path}")
        print(f"   📈 Métricas semana 40: {week_metrics['total_epics']} épicas")
        
        print("\n3. 📋 Resumen de archivos generados:")
        reports_dir = "reports"
        if os.path.exists(reports_dir):
            report_files = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]
            print(f"   📁 Directorio: {os.path.abspath(reports_dir)}")
            print(f"   📄 Archivos PDF: {len(report_files)}")
            
            for i, file in enumerate(report_files[-5:], 1):  # Mostrar últimos 5
                file_path = os.path.join(reports_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"      {i}. {file} ({file_size:.1f} KB)")
        
        print("\n🎉 Demo completada exitosamente!")
        print("\n💡 Próximos pasos:")
        print("   1. Abre los archivos PDF generados para revisarlos")
        print("   2. Configura tu email en la aplicación para envío automático")
        print("   3. Ejecuta 'streamlit run app.py' para usar la interfaz completa")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la demo: {str(e)}")
        return False

def create_sample_reports():
    """Crea reportes de ejemplo con diferentes configuraciones"""
    print("\n🎨 Creando reportes de ejemplo adicionales...")
    
    try:
        generator = ReportGenerator()
        
        # Reportes por cada semana
        weeks = ["Semana 40 - 2025", "Semana 41 - 2025", "Semana 42 - 2025"]
        
        for week in weeks:
            try:
                path, metrics = generator.generate_report(week_filter=week)
                if metrics['total_epics'] > 0:
                    print(f"   ✅ Reporte {week}: {metrics['total_epics']} épicas")
                else:
                    print(f"   ⚠️ Reporte {week}: Sin épicas")
            except Exception as e:
                print(f"   ❌ Error en {week}: {str(e)}")
        
        print("   🎉 Reportes de ejemplo creados")
        
    except Exception as e:
        print(f"❌ Error creando reportes de ejemplo: {str(e)}")

def show_report_stats():
    """Muestra estadísticas de los reportes generados"""
    print("\n📊 Estadísticas de Reportes:")
    
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        print("   📁 No existe directorio de reportes")
        return
    
    report_files = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]
    
    if not report_files:
        print("   📄 No hay reportes PDF generados")
        return
    
    total_size = 0
    for file in report_files:
        file_path = os.path.join(reports_dir, file)
        total_size += os.path.getsize(file_path)
    
    print(f"   📄 Total archivos: {len(report_files)}")
    print(f"   💾 Tamaño total: {total_size / 1024:.1f} KB")
    print(f"   📈 Tamaño promedio: {total_size / len(report_files) / 1024:.1f} KB")
    
    # Mostrar archivos más recientes
    recent_files = sorted(
        [(f, os.path.getmtime(os.path.join(reports_dir, f))) for f in report_files],
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    print("   🕒 Archivos más recientes:")
    for file, mtime in recent_files:
        date_str = datetime.fromtimestamp(mtime).strftime('%d/%m/%Y %H:%M')
        print(f"      • {file} ({date_str})")

if __name__ == "__main__":
    print("🚀 DEMO DE SISTEMA DE REPORTES")
    print("Roadmap Semanal - Generación Automática de PDFs")
    print("=" * 60)
    
    # Verificar si hay datos
    from db.db_manager import get_all_epics
    epics = get_all_epics()
    
    if not epics:
        print("⚠️ No hay épicas en la base de datos.")
        print("💡 Ejecuta primero: python create_sample_data.py")
        print("   Luego vuelve a ejecutar este script.")
        sys.exit(1)
    
    print(f"📊 Base de datos: {len(epics)} épicas encontradas")
    
    # Ejecutar demo principal
    success = demo_report_generation()
    
    if success:
        # Crear reportes adicionales
        create_sample_reports()
        
        # Mostrar estadísticas
        show_report_stats()
        
        print("\n" + "=" * 60)
        print("✨ DEMO COMPLETADA - ¡Revisa los reportes generados!")
    else:
        print("\n❌ Demo falló. Revisa los errores anteriores.")
        sys.exit(1)