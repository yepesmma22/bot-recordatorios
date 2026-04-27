# ============================================================
# Bot de Recordatorios WhatsApp — Version Railway
# ============================================================
# Corre 24/7 en Railway, envia recordatorios por WhatsApp
# usando Twilio. Edita la seccion TAREAS DEL DIA con las tuyas.
# ============================================================

import schedule
import time
from datetime import datetime
from twilio.rest import Client
import os

# --- CREDENCIALES (se leen desde variables de entorno en Railway) ---
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN",  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
TWILIO_WA   = os.environ.get("TWILIO_FROM",        "whatsapp:+14155238886")
TU_NUMERO   = os.environ.get("MI_NUMERO",           "whatsapp:+57XXXXXXXXXX")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- TAREAS DEL DIA ---
# Edita esta lista con tus horarios y mensajes personales
tareas = [
    {"hora": "07:00", "mensaje": "🌅 Buenos dias! Hora de levantarse y tomar agua."},
    {"hora": "08:00", "mensaje": "💊 Recuerda tomar tus vitaminas con el desayuno."},
    {"hora": "09:00", "mensaje": "💼 Empieza tu bloque principal de trabajo."},
    {"hora": "13:00", "mensaje": "🍽️ Hora del almuerzo! Descansa 30 minutos."},
    {"hora": "15:00", "mensaje": "☕ Pausa de la tarde - estira las piernas."},
    {"hora": "18:00", "mensaje": "🏃 Hora del ejercicio!"},
    {"hora": "21:00", "mensaje": "📵 Empieza a desconectarte. Modo descanso."},
    {"hora": "22:30", "mensaje": "😴 Hora de dormir. Buenas noches!"},
]

def enviar_mensaje(mensaje):
    try:
        client.messages.create(from_=TWILIO_WA, to=TU_NUMERO, body=mensaje)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Enviado: {mensaje}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {e}")

def programar_tareas():
    for tarea in tareas:
        schedule.every().day.at(tarea["hora"]).do(enviar_mensaje, tarea["mensaje"])
        print(f"  ⏰ Programado: {tarea['hora']} → {tarea['mensaje']}")

if __name__ == "__main__":
    print("=" * 50)
    print("  Bot de Recordatorios WhatsApp - Railway")
    print(f"  Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)
    programar_tareas()
    print("\n✅ Bot activo. Esperando horarios...\n")
    while True:
        schedule.run_pending()
        time.sleep(30)
