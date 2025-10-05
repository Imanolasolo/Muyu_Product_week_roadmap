#!/usr/bin/env python3
"""
Script de configuración rápida para el Roadmap Semanal
Ejecuta este script para configurar todo automáticamente
"""

import subprocess
import sys
import os

def run_command(command):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    print("🚀 Configuración rápida del Roadmap Semanal")
    print("=" * 50)
    
    # Verificar si Python está instalado
    print("1. Verificando Python...")
    success, output = run_command("python --version")
    if success:
        print(f"   ✅ {output.strip()}")
    else:
        print("   ❌ Python no encontrado. Instala Python 3.8+ primero.")
        return
    
    # Verificar si pip está disponible
    print("2. Verificando pip...")
    success, output = run_command("pip --version")
    if success:
        print(f"   ✅ pip disponible")
    else:
        print("   ❌ pip no encontrado.")
        return
    
    # Instalar dependencias
    print("3. Instalando dependencias...")
    success, output = run_command("pip install -r requirements-minimal.txt")
    if success:
        print("   ✅ Dependencias instaladas correctamente")
    else:
        print(f"   ❌ Error instalando dependencias: {output}")
        return
    
    # Inicializar base de datos
    print("4. Inicializando base de datos...")
    try:
        from db.db_setup import init_db
        init_db()
        print("   ✅ Base de datos inicializada")
    except Exception as e:
        print(f"   ❌ Error inicializando base de datos: {e}")
        return
    
    # Crear datos de prueba (opcional)
    print("5. ¿Quieres crear datos de prueba? (y/n): ", end="")
    response = input().lower()
    if response in ['y', 'yes', 'sí', 's']:
        try:
            exec(open('create_sample_data.py').read())
            print("   ✅ Datos de prueba creados")
        except Exception as e:
            print(f"   ❌ Error creando datos de prueba: {e}")
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("   1. Ejecuta: streamlit run app.py")
    print("   2. Abre tu navegador en: http://localhost:8501")
    print("   3. ¡Empieza a crear épicas y tareas!")
    
    print("\n💡 Comandos útiles:")
    print("   - Ejecutar app: streamlit run app.py")
    print("   - Crear datos prueba: python create_sample_data.py")
    print("   - Ver ayuda: python setup.py --help")

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("🚀 Script de configuración del Roadmap Semanal")
        print("\nUso:")
        print("  python setup.py          # Configuración completa")
        print("  python setup.py --help   # Mostrar esta ayuda")
        print("\nEste script:")
        print("  1. Verifica Python y pip")
        print("  2. Instala dependencias")
        print("  3. Inicializa la base de datos")
        print("  4. Opcionalmente crea datos de prueba")
    else:
        main()