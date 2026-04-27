# ============================================================
# Bot Bidireccional WhatsApp — Rutina + Proyectos por día
# Fix zona horaria: America/Bogota (UTC-5)
# ============================================================

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import schedule
import time
import threading
import os
import pytz
from datetime import datetime

app = Flask(__name__)

# --- ZONA HORARIA COLOMBIA ---
BOG = pytz.timezone("America/Bogota")
os.environ["TZ"] = "America/Bogota"
try:
    time.tzset()
except AttributeError:
    pass  # Windows no tiene tzset, en Railway (Linux) sí funciona

# --- CREDENCIALES ---
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN",  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
TWILIO_WA   = os.environ.get("TWILIO_FROM",        "whatsapp:+14155238886")
TU_NUMERO   = os.environ.get("MI_NUMERO",           "whatsapp:+57XXXXXXXXXX")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- PROYECTOS ---
PROYECTOS = {
    "1": "SEASHELL 🐚",
    "2": "NOMI 🎯",
    "3": "HON3Y22 🍯"
}

estado = {
    "bloque_manana": "1",
    "bloque_tarde":  "2",
    "bloque_noche":  "3",
}

def nombre_proyecto(num):
    return PROYECTOS.get(str(num), f"Proyecto {num}")

def hora_bogota():
    return datetime.now(BOG).strftime("%H:%M:%S")

def enviar_mensaje(mensaje):
    try:
        client.messages.create(from_=TWILIO_WA, to=TU_NUMERO, body=mensaje)
        print(f"[{hora_bogota()}] Enviado: {mensaje[:60]}...")
    except Exception as e:
        print(f"[{hora_bogota()}] Error: {e}")

def recordatorio_bloque_manana():
    p = nombre_proyecto(estado["bloque_manana"])
    enviar_mensaje(
        f"🧠 BLOQUE 1 — 9:00 a 12:00\n"
        f"Hoy trabajas en: {p}\n\n"
        f"Arranca el Pomodoro y enfocate. 💻\n"
        f"En los descansos: organiza, barre, pendientes rapidos."
    )

def recordatorio_bloque_tarde():
    p = nombre_proyecto(estado["bloque_tarde"])
    enviar_mensaje(
        f"🧠 BLOQUE 2 — 2:45 a 5:00pm\n"
        f"Hoy trabajas en: {p}\n\n"
        f"Pomodoro activado. 💪"
    )

def recordatorio_bloque_noche():
    p = nombre_proyecto(estado["bloque_noche"])
    enviar_mensaje(
        f"🎵 BLOQUE 3 — Sesion de musica\n"
        f"Hoy trabajas en: {p}\n\n"
        f"Fluye. 🎧"
    )

def recordatorio_organizar_dia():
    p1 = nombre_proyecto(estado["bloque_manana"])
    p2 = nombre_proyecto(estado["bloque_tarde"])
    p3 = nombre_proyecto(estado["bloque_noche"])
    enviar_mensaje(
        f"📋 Organiza el dia de manana.\n\n"
        f"Proyectos de hoy:\n"
        f"  Manana → {p1}\n"
        f"  Tarde  → {p2}\n"
        f"  Noche  → {p3}\n\n"
        f"Para cambiar escribeme:\n"
        f"manana: 1 2 3\n"
        f"(1=SEASHELL, 2=NOMI, 3=HON3Y22)"
    )

def programar_tareas():
    tareas = [
        ("04:30", lambda: enviar_mensaje(
            "🙏 Buenos dias. Antes de todo — gracias a Dios Todopoderoso "
            "por permitirte estar un dia mas con vida. Respira, siente ese "
            "privilegio y arranca con gratitud.\n\n"
            "15 minutos sin celular — aclara la mente y ordena tus pensamientos."
        )),
        ("04:45", lambda: enviar_mensaje("🚿 Hora de banarte y alistarte. Tienes 15 minutos para salir fresco.")),
        ("05:00", lambda: enviar_mensaje("💊 Toma la creatina y suplementos. Agarra el batido y sal al gym!")),
        ("07:00", lambda: enviar_mensaje("💪 Fin del entrenamiento. Buen trabajo. Descansa 15 minutos.")),
        ("07:15", lambda: enviar_mensaje("📱 15 minutos de redes sociales — pon el timer ya.")),
        ("07:30", lambda: enviar_mensaje("🍳 A cocinar el desayuno.")),
        ("08:00", lambda: enviar_mensaje("🍽️ Hora de comer. Desayuno tranquilo.")),
        ("09:00", recordatorio_bloque_manana),
        ("10:00", lambda: enviar_mensaje("⏱️ Check-in Pomodoro — como vas? Toma agua.")),
        ("11:00", lambda: enviar_mensaje("⏱️ Ultima hora del bloque manana. Termina fuerte.")),
        ("12:00", lambda: enviar_mensaje("✅ Fin bloque manana. 30 min de descanso — siesta si puedes.")),
        ("12:30", lambda: enviar_mensaje("🍚 Prepara el almuerzo — descongela proteina o pon arroz.")),
        ("12:45", lambda: enviar_mensaje("📖 Lectura hasta la 1:30. Apaga notificaciones.")),
        ("13:30", lambda: enviar_mensaje("👨‍🍳 Termina de preparar el almuerzo.")),
        ("14:00", lambda: enviar_mensaje("🍽️ A comer. Almuerzo tranquilo.")),
        ("14:30", lambda: enviar_mensaje("📱 30 minutos de redes — pon el timer.")),
        ("14:45", recordatorio_bloque_tarde),
        ("16:00", lambda: enviar_mensaje("⏱️ Check-in tarde — queda 1 hora. Como vas?")),
        ("17:00", lambda: enviar_mensaje("🌇 Fin bloque tarde. Descanso real — camina, echa porro, ve serie.")),
        ("18:00", recordatorio_bloque_noche),
        ("19:30", lambda: enviar_mensaje("🍽️ Ve pensando que comer esta noche.")),
        ("20:00", lambda: enviar_mensaje("🍽️ Hora de cenar.")),
        ("20:30", lambda: enviar_mensaje("🎵 Fin de sesion de musica. Guarda el trabajo.")),
        ("21:00", recordatorio_organizar_dia),
        ("21:30", lambda: enviar_mensaje("🌙 Empieza a bajar el ritmo. Nada de pantallas intensas.")),
        ("21:45", lambda: enviar_mensaje("🪥 Lava los dientes. Modo sueno activado.")),
        ("22:00", lambda: enviar_mensaje(
            "🙏 Antes de cerrar los ojos — gracias a Dios Todopoderoso por este dia. "
            "Por la salud, la energia, los proyectos, el gym y cada momento vivido hoy. "
            "Duerme en paz, manana es otro dia para crecer. 🔥\n\n😴 Buenas noches."
        )),
    ]
    for hora, fn in tareas:
        schedule.every().day.at(hora).do(fn)
        print(f"  {hora} programado")
    print(f"\n{len(tareas)} recordatorios activos.")

@app.route("/webhook", methods=["POST"])
def webhook():
    mensaje = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if any(mensaje.startswith(p) for p in ["manana:", "mañana:", "hoy:"]):
        try:
            partes = mensaje.split(":")[1].strip().split()
            if len(partes) == 3 and all(p in ["1","2","3"] for p in partes):
                estado["bloque_manana"] = partes[0]
                estado["bloque_tarde"]  = partes[1]
                estado["bloque_noche"]  = partes[2]
                p1 = nombre_proyecto(partes[0])
                p2 = nombre_proyecto(partes[1])
                p3 = nombre_proyecto(partes[2])
                msg.body(
                    f"✅ Proyectos actualizados:\n\n"
                    f"🌅 Manana (9-12)   → {p1}\n"
                    f"☀️ Tarde (2:45-5)  → {p2}\n"
                    f"🎵 Noche (6-8:30)  → {p3}\n\n"
                    f"Listo, manana el bot ya sabe que recordarte! 💪"
                )
            else:
                msg.body("Formato incorrecto. Usa:\nmanana: 1 2 3\n(1=SEASHELL, 2=NOMI, 3=HON3Y22)")
        except:
            msg.body("No entendi. Ejemplo:\nmanana: 1 2 3")

    elif "proyectos" in mensaje:
        p1 = nombre_proyecto(estado["bloque_manana"])
        p2 = nombre_proyecto(estado["bloque_tarde"])
        p3 = nombre_proyecto(estado["bloque_noche"])
        msg.body(
            f"📋 Proyectos de hoy:\n\n"
            f"🌅 Manana (9-12)   → {p1}\n"
            f"☀️ Tarde (2:45-5)  → {p2}\n"
            f"🎵 Noche (6-8:30)  → {p3}"
        )

    elif "ayuda" in mensaje:
        msg.body(
            "🤖 Comandos:\n\n"
            "manana: 1 2 3 → asigna proyectos del dia\n"
            "hoy: 1 2 3    → cambia proyectos ahora\n"
            "proyectos     → ver que tienes hoy\n"
            "ayuda         → ver esta lista\n\n"
            "1 = SEASHELL 🐚\n"
            "2 = NOMI 🎯\n"
            "3 = HON3Y22 🍯"
        )
    else:
        msg.body("No entendi. Escribe ayuda para ver que puedo hacer. 🤖")

    return str(resp)

def correr_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    print(f"Bot iniciado: {datetime.now(BOG).strftime('%d/%m/%Y %H:%M:%S')} (Bogota)")
    programar_tareas()
    hilo = threading.Thread(target=correr_scheduler, daemon=True)
    hilo.start()
    port = int(os.environ.get("PORT", 5000))
    print(f"Webhook activo en puerto {port}")
    app.run(host="0.0.0.0", port=port)
