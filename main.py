import os
import time
import subprocess
from twilio.rest import Client

# --- Configuración de Twilio ---
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = "whatsapp:+14155238886"  # Número del Sandbox de Twilio
TO_WHATSAPP = os.getenv("TO_WHATSAPP")   # Tu número en formato WhatsApp: whatsapp:+521XXXXXXXXXX

# --- Configuración de IPs ---
IPS = [
    "200.94.125.2",
    "189.206.125.61"
]

# --- Inicializar cliente Twilio ---
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- Estado previo de cada IP ---
estado_anterior = {ip: True for ip in IPS}


def ping(ip):
    """Devuelve True si la IP responde al ping, False si no."""
    try:
        output = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
        return output.returncode == 0
    except Exception:
        return False


def enviar_mensaje(mensaje):
    """Envía un mensaje de WhatsApp por Twilio."""
    try:
        client.messages.create(
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP,
            body=mensaje
        )
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")


while True:
    for ip in IPS:
        activo = ping(ip)

        # Si cambia de estado (de activo a caído o viceversa)
        if activo != estado_anterior[ip]:
            if not activo:
                enviar_mensaje(f"⚠️ Enlace {ip} está CAÍDO")
            else:
                enviar_mensaje(f"✅ Enlace {ip} se RECUPERÓ")

            estado_anterior[ip] = activo

    time.sleep(30)