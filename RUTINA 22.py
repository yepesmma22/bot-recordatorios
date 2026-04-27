# ============================================================
# Bot de Recordatorios WhatsApp — Rutina Personalizada
# ============================================================

import schedule
import time
from datetime import datetime
from twilio.rest import Client
import os

# --- CREDENCIALES ---
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN",  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
TWILIO_WA   = os.environ.get("TWILIO_FROM",        "whatsapp:+14155238886")
TU_NUMERO   = os.environ.get("MI_NUMERO",           "whatsapp:+57XXXXXXXXXX")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- RUTINA DEL DIA ---
tareas = [

    # 🙏 GRATITUD INICIO
    {"hora": "04:30", "mensaje": "🙏 Buenos días. Antes de todo — gracias a Dios Todopoderoso por permitirte estar un día más con vida. Respira, siente ese privilegio y arranca con gratitud.\n\n15 minutos sin celular — aclara la mente y ordena tus pensamientos."},
    {"hora": "04:45", "mensaje": "🚿 Hora de bañarte y alistarte. Tienes 15 minutos para salir fresco."},
    {"hora": "05:00", "mensaje": "💊 Toma la creatina y suplementos. Agarra el batido o carbohidrato y sal al gym. ¡A entrenar!"},
    {"hora": "07:00", "mensaje": "💪 Fin del entrenamiento. Buen trabajo. Descansa 15 minutos."},
    {"hora": "07:15", "mensaje": "📱 15 minutos de redes sociales — pon el timer ya."},
    {"hora": "07:30", "mensaje": "🍳 A cocinar el desayuno."},
    {"hora": "08:00", "mensaje": "🍽️ Hora de comer. Desayuno tranquilo, sin pantallas si puedes."},

    # 💼 BLOQUE 1 — TRABAJO/ESTUDIO MAÑANA
    {"hora": "09:00", "mensaje": "🧠 BLOQUE 1 — 9:00 a 12:00\n¿Cuál proyecto arrancas hoy?\n\n1️⃣ SEASHELL\n2️⃣ NOMI\n3️⃣ HON3Y22\n\nArranca el Pomodoro y enfócate. 💻"},
    {"hora": "10:00", "mensaje": "⏱️ Check-in Pomodoro — ¿Cómo vas? Recuerda tomar agua entre bloques."},
    {"hora": "11:00", "mensaje": "⏱️ Última hora del bloque mañana. Termina fuerte lo que empezaste."},

    # 😴 DESCANSO MEDIODÍA
    {"hora": "12:00", "mensaje": "✅ Fin del bloque mañana. 30 minutos de descanso — siesta si puedes, desconéctate del proyecto."},
    {"hora": "12:30", "mensaje": "🍚 Prepara el almuerzo — descongela proteína o pon a hervir el arroz."},
    {"hora": "12:45", "mensaje": "📖 Lectura hasta la 1:30. Apaga notificaciones y disfruta el libro."},
    {"hora": "13:30", "mensaje": "👨‍🍳 Termina de preparar el almuerzo."},
    {"hora": "14:00", "mensaje": "🍽️ A comer. Almuerzo sin pantallas si puedes."},
    {"hora": "14:30", "mensaje": "📱 30 minutos de redes sociales — pon el timer."},

    # 💼 BLOQUE 2 — TRABAJO/ESTUDIO TARDE
    {"hora": "14:45", "mensaje": "🧠 BLOQUE 2 — 2:45 a 5:00pm\n¿Cuál proyecto arrancas?\n\n1️⃣ SEASHELL\n2️⃣ NOMI\n3️⃣ HON3Y22\n\nPomodoro activado. En los descansos: organiza, barre, pendientes rápidos. 💪"},
    {"hora": "16:00", "mensaje": "⏱️ Check-in tarde — queda 1 hora. ¿Cómo vas con el Pomodoro?"},

    # 🌇 DESCANSO TARDE
    {"hora": "17:00", "mensaje": "🌇 Fin del bloque tarde. Hora de descanso real — sal a caminar, echa porro, ve una serie. Desconéctate."},

    # 🎵 BLOQUE 3 — MÚSICA / PROYECTO NOCHE
    {"hora": "18:00", "mensaje": "🎵 BLOQUE 3 — Hora de música\n¿Cuál proyecto trabajas hoy en el bloque musical?\n\n1️⃣ SEASHELL\n2️⃣ NOMI\n3️⃣ HON3Y22\n\nFluye. 🎧"},
    {"hora": "19:30", "mensaje": "🍽️ Ve pensando qué comer esta noche."},
    {"hora": "20:00", "mensaje": "🍽️ Hora de cenar."},
    {"hora": "20:30", "mensaje": "🎵 Fin de sesión de música. Guarda el trabajo, exporta si hay algo pendiente."},

    # 🌙 CIERRE DEL DÍA
    {"hora": "21:00", "mensaje": "📋 Organiza el día de mañana — anota las 3 cosas más importantes que tienes que hacer y decide qué proyecto arrancas."},
    {"hora": "21:30", "mensaje": "🌙 Empieza a bajar el ritmo. Nada de pantallas intensas."},
    {"hora": "21:45", "mensaje": "🪥 Lava los dientes y empieza a desconectarte. Modo sueño activado."},
    {"hora": "22:00", "mensaje": "🙏 Antes de cerrar los ojos — gracias a Dios Todopoderoso por este día. Por la salud, la energía, los proyectos, el gym, la música y cada momento vivido hoy. Duerme en paz, que mañana es otro día para crecer. 🔥\n\n😴 Buenas noches."},
]

def enviar_mensaje(mensaje):
    try:
        client.messages.create(from_=TWILIO_WA, to=TU_NUMERO, body=mensaje)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Enviado: {mensaje[:50]}...")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {e}")

def programar_tareas():
    for tarea in tareas:
        schedule.every().day.at(tarea["hora"]).do(enviar_mensaje, tarea["mensaje"])
        print(f"  ⏰ {tarea['hora']} → {tarea['mensaje'][:50]}...")

if __name__ == "__main__":
    print("=" * 55)
    print("  Bot de Recordatorios — Rutina Personalizada")
    print(f"  Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  Total recordatorios: {len(tareas)}")
    print("=" * 55)
    programar_tareas()
    print(f"\n✅ {len(tareas)} recordatorios activos. Bot escuchando...\n")
    while True:
        schedule.run_pending()
        time.sleep(30)
