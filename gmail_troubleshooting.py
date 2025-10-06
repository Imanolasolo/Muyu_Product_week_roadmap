"""
Guía de solución de problemas para Gmail SMTP
Soluciona errores de autenticación con Gmail
"""

import streamlit as st

def show_gmail_troubleshooting():
    """Muestra guía detallada para solucionar problemas con Gmail"""
    
    st.markdown("## 🔧 Solución de Problemas - Gmail SMTP")
    
    st.error("**Error 535**: Username and Password not accepted")
    
    st.markdown("### 📋 Lista de Verificación")
    
    # Checklist interactivo
    st.markdown("**✅ Verifica cada punto:**")
    
    with st.expander("1. 🔐 Verificación de 2FA y App Password", expanded=True):
        st.markdown("""
        **Pasos obligatorios:**
        
        1. **Verificación en 2 pasos ACTIVADA**
           - Ve a: https://myaccount.google.com/security
           - Busca "Verificación en 2 pasos"
           - DEBE estar activada (azul)
        
        2. **Generar App Password correcta**
           - Ve a: https://myaccount.google.com/apppasswords
           - Selecciona "Correo" y "Otro (nombre personalizado)"
           - Escribe: "Roadmap App"
           - Copia la contraseña de 16 caracteres (sin espacios)
        
        3. **Formato correcto**
           - ✅ Usa: `abcdabcdabcdabcd` (16 caracteres)
           - ❌ NO uses: `abcd abcd abcd abcd` (con espacios)
           - ❌ NO uses tu contraseña normal de Gmail
        """)
        
        # Test input
        test_email = st.text_input("🧪 Tu email de Gmail:", placeholder="ejemplo@gmail.com")
        test_password = st.text_input("🔑 Tu App Password (16 caracteres):", type="password", placeholder="abcdabcdabcdabcd")
        
        if test_email and test_password:
            if len(test_password) == 16 and ' ' not in test_password:
                st.success("✅ Formato de App Password correcto")
            else:
                st.error("❌ App Password debe ser exactamente 16 caracteres sin espacios")
    
    with st.expander("2. 🔍 Diagnóstico Avanzado"):
        st.markdown("""
        **Si aún no funciona, verifica:**
        
        **A. Configuración de cuenta:**
        - Acceso de aplicaciones menos seguras: DESACTIVADO (ya no se usa)
        - Verificación en 2 pasos: ACTIVADA
        - App Passwords: GENERADA recientemente
        
        **B. Configuración SMTP correcta:**
        - Servidor: `smtp.gmail.com`
        - Puerto: `587` (TLS) o `465` (SSL)
        - Encriptación: TLS/STARTTLS
        
        **C. Restricciones de cuenta:**
        - Cuenta no suspendida
        - No hay actividad sospechosa reciente
        - No hay límites de envío activos
        """)
        
        if st.button("🧪 Probar conexión con diagnóstico avanzado"):
            if test_email and test_password:
                try:
                    import smtplib
                    import ssl
                    
                    with st.spinner("Probando conexión..."):
                        # Intento 1: TLS en puerto 587
                        try:
                            st.info("🔄 Intentando conexión TLS (puerto 587)...")
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(test_email, test_password)
                            server.quit()
                            st.success("✅ ¡Conexión exitosa con TLS!")
                            return
                        except Exception as e1:
                            st.warning(f"❌ TLS falló: {str(e1)}")
                        
                        # Intento 2: SSL en puerto 465
                        try:
                            st.info("🔄 Intentando conexión SSL (puerto 465)...")
                            context = ssl.create_default_context()
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
                            server.login(test_email, test_password)
                            server.quit()
                            st.success("✅ ¡Conexión exitosa con SSL!")
                            return
                        except Exception as e2:
                            st.error(f"❌ SSL también falló: {str(e2)}")
                        
                        st.error("❌ Ambos métodos fallaron. Revisa la configuración.")
                
                except ImportError:
                    st.error("❌ Error importando librerías. Instala las dependencias.")
            else:
                st.warning("⚠️ Ingresa email y contraseña para probar")
    
    with st.expander("3. 🔄 Alternativas si Gmail no funciona"):
        st.markdown("""
        **Opciones alternativas:**
        
        **A. Outlook/Hotmail (más fácil):**
        - Servidor: `smtp-mail.outlook.com`
        - Puerto: `587`
        - Usa tu email y contraseña normal
        - No requiere App Password
        
        **B. Yahoo Mail:**
        - Servidor: `smtp.mail.yahoo.com`
        - Puerto: `587`
        - Requiere App Password similar a Gmail
        
        **C. Email corporativo:**
        - Consulta con tu administrador IT
        - Configuración específica de tu empresa
        """)
        
        # Selector de alternativa
        alternative = st.selectbox("Selecciona alternativa:", 
                                 ["Gmail", "Outlook", "Yahoo", "Otro"])
        
        if alternative == "Outlook":
            st.info("""
            **Configuración Outlook:**
            - Servidor SMTP: smtp-mail.outlook.com
            - Puerto: 587
            - Email: tu-email@outlook.com (o @hotmail.com)
            - Contraseña: Tu contraseña normal de Outlook
            """)
        elif alternative == "Yahoo":
            st.info("""
            **Configuración Yahoo:**
            - Servidor SMTP: smtp.mail.yahoo.com
            - Puerto: 587
            - Email: tu-email@yahoo.com
            - Contraseña: App Password (similar a Gmail)
            """)
    
    with st.expander("4. 🆘 Solución Rápida - Regenerar Todo"):
        st.markdown("""
        **Si nada funciona, hazlo desde cero:**
        
        1. **Eliminar App Password actual:**
           - Ve a: https://myaccount.google.com/apppasswords
           - Elimina cualquier App Password existente para correo
        
        2. **Crear nueva App Password:**
           - Genera una nueva específicamente para "Roadmap App"
           - Copia exactamente los 16 caracteres
        
        3. **Verificar configuración:**
           - Email: tu-email@gmail.com (sin espacios)
           - Password: nuevaapppassword16chars (sin espacios)
           - Servidor: smtp.gmail.com
           - Puerto: 587
        
        4. **Probar inmediatamente:**
           - No esperes, prueba la conexión de inmediato
           - Gmail a veces demora unos minutos en activar nuevas App Passwords
        """)
        
        if st.button("🔄 Regenerar configuración completa", type="primary"):
            st.info("📋 Sigue estos pasos en orden:")
            st.markdown("""
            1. Abre: https://myaccount.google.com/apppasswords
            2. Elimina app passwords existentes
            3. Crea nueva: "Roadmap-App"
            4. Copia la nueva contraseña de 16 caracteres
            5. Pégala en la configuración (sin espacios)
            6. Prueba la conexión
            """)

if __name__ == "__main__":
    show_gmail_troubleshooting()