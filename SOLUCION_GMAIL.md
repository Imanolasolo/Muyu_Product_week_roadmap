# 🔧 SOLUCIÓN ESPECÍFICA PARA TU ERROR GMAIL

## ❌ Error actual:
```
535 Username and Password not accepted
BadCredentials a1e0cc1a2514c-92eb4da2028sm2987750241.6 - gsmtp
```

## 🚀 SOLUCIÓN PASO A PASO:

### 1. ✅ **VERIFICAR 2FA (MUY IMPORTANTE)**
- Ve a: https://myaccount.google.com/security
- Busca "Verificación en 2 pasos"
- **DEBE estar ACTIVADA** (color azul)
- Si no está activada, actívala primero

### 2. 🔑 **REGENERAR APP PASSWORD**
- Ve a: https://myaccount.google.com/apppasswords
- **ELIMINA** cualquier App Password existente para correo
- Haz clic en "Generar contraseña de aplicación"
- Selecciona: **"Correo"** y **"Otro (nombre personalizado)"**
- Escribe: **"Roadmap-App-2025"**
- **COPIA exactamente los 16 caracteres** que aparecen

### 3. 📋 **FORMATO CORRECTO**
**✅ CORRECTO:**
```
Email: tu-email@gmail.com
Password: abcdabcdabcdabcd (exactamente 16 caracteres)
```

**❌ INCORRECTO:**
```
Password: abcd abcd abcd abcd (con espacios)
Password: tu-contraseña-normal-gmail
Password: abcdabcdabcdabcd1 (17 caracteres)
```

### 4. ⏰ **TIMING IMPORTANTE**
- Después de generar la App Password, **espera 2-3 minutos**
- Gmail a veces demora en activar nuevas credenciales
- **NO uses** la App Password inmediatamente

### 5. 🧪 **PROBAR CON SCRIPT**
Ejecuta este comando para probar tu configuración:
```bash
cd "f:\CODECODIX\Muyu projects\Muyu_Product_week_roadmap"
python test_gmail.py
```

### 6. 🔄 **ALTERNATIVA FÁCIL - OUTLOOK**
Si Gmail sigue fallando, cambia a Outlook (mucho más fácil):

**Configuración Outlook:**
- Email: tu-email@outlook.com (o @hotmail.com)
- Contraseña: Tu contraseña normal de Outlook
- Servidor: smtp-mail.outlook.com
- Puerto: 587
- **NO requiere App Password**

## 🎯 **ACCIÓN INMEDIATA:**

1. **Abre:** https://myaccount.google.com/apppasswords
2. **Elimina** App Passwords existentes
3. **Genera nueva** App Password para "Roadmap-App"
4. **Copia** exactamente los 16 caracteres
5. **Espera** 3 minutos
6. **Prueba** en la aplicación

## 📞 **SI NADA FUNCIONA:**

**Opción A: Usa Outlook (recomendado)**
- Más fácil de configurar
- No requiere App Passwords
- Funciona con contraseña normal

**Opción B: Verifica cuenta Gmail**
- Asegúrate que no esté suspendida
- Verifica que no haya actividad sospechosa
- Prueba desde otro dispositivo/navegador

---

**💡 TIP:** El 90% de problemas Gmail se solucionan regenerando la App Password y esperando unos minutos antes de probar.