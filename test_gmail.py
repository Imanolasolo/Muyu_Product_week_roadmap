"""
Herramienta de diagnóstico específica para Gmail SMTP
Ejecuta este archivo para diagnosticar problemas de conexión Gmail
"""

import smtplib
import ssl
from getpass import getpass

def test_gmail_connection():
    print("🔧 DIAGNÓSTICO GMAIL SMTP")
    print("=" * 40)
    
    # Obtener credenciales
    email = input("📧 Tu email Gmail: ")
    print("\n🔑 Tu App Password de Gmail (16 caracteres):")
    print("   💡 Genera en: https://myaccount.google.com/apppasswords")
    password = getpass("   Password: ")
    
    # Validaciones básicas
    print("\n📋 VALIDACIONES BÁSICAS:")
    
    if not email.endswith('@gmail.com'):
        print("❌ Email debe terminar en @gmail.com")
        return False
    else:
        print("✅ Email válido")
    
    if len(password) != 16:
        print(f"❌ App Password debe tener 16 caracteres (tiene {len(password)})")
        return False
    else:
        print("✅ Longitud de App Password correcta")
    
    if ' ' in password:
        print("❌ App Password no debe tener espacios")
        return False
    else:
        print("✅ App Password sin espacios")
    
    # Pruebas de conexión
    print("\n🔄 PRUEBAS DE CONEXIÓN:")
    
    # Intento 1: TLS puerto 587
    print("1. Probando TLS (puerto 587)...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Mostrar debug
        server.starttls()
        server.login(email, password)
        server.quit()
        print("✅ ¡CONEXIÓN TLS EXITOSA!")
        return True
    except Exception as e:
        print(f"❌ TLS falló: {e}")
    
    # Intento 2: SSL puerto 465
    print("\n2. Probando SSL (puerto 465)...")
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.set_debuglevel(1)  # Mostrar debug
        server.login(email, password)
        server.quit()
        print("✅ ¡CONEXIÓN SSL EXITOSA!")
        return True
    except Exception as e:
        print(f"❌ SSL falló: {e}")
    
    # Si llegamos aquí, ambos métodos fallaron
    print("\n❌ AMBOS MÉTODOS FALLARON")
    print("\n🔧 SOLUCIONES RECOMENDADAS:")
    print("1. Ve a: https://myaccount.google.com/security")
    print("2. Verifica que 'Verificación en 2 pasos' esté ACTIVADA")
    print("3. Ve a: https://myaccount.google.com/apppasswords")
    print("4. ELIMINA cualquier App Password existente para correo")
    print("5. GENERA una nueva App Password específicamente para 'Roadmap App'")
    print("6. COPIA exactamente los 16 caracteres (sin espacios)")
    print("7. Espera 2-3 minutos y vuelve a probar")
    print("\n💡 ALTERNATIVA: Usa Outlook (más fácil, no requiere App Password)")
    
    return False

def test_outlook_connection():
    print("\n🔧 PRUEBA ALTERNATIVA - OUTLOOK")
    print("=" * 40)
    
    email = input("📧 Tu email Outlook/Hotmail: ")
    password = getpass("🔑 Tu contraseña normal de Outlook: ")
    
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(email, password)
        server.quit()
        print("✅ ¡OUTLOOK FUNCIONA! Usa esta configuración:")
        print(f"   📧 Email: {email}")
        print("   🔧 Servidor: smtp-mail.outlook.com")
        print("   🔌 Puerto: 587")
        print("   🔑 Contraseña: Tu contraseña normal")
        return True
    except Exception as e:
        print(f"❌ Outlook también falló: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    
    if not success:
        print("\n" + "="*50)
        retry = input("\n🔄 ¿Quieres probar con Outlook en su lugar? (s/n): ")
        if retry.lower() in ['s', 'si', 'y', 'yes']:
            test_outlook_connection()
        else:
            print("\n💡 Ejecuta este script de nuevo después de seguir las soluciones recomendadas")
    
    input("\nPresiona Enter para salir...")