import requests
import sett
import logging
import time
import re

logger = logging.getLogger(__name__)

# --- Utilidades ---
def normalizar_texto(texto):
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip().lower()

def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    elif s.startswith("549"):
        return "54" + s[3:]
    return s

# --- Funciones WhatsApp ---
def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {whatsapp_token}'
        }
        logger.info(f"Enviando mensaje: {data}")
        response = requests.post(whatsapp_url, headers=headers, json=data)
        logger.info(f"Respuesta WhatsApp: {response.status_code}, {response.text}")
        return response.status_code, response.text
    except Exception as e:
        logger.error(f"Error enviando mensaje: {e}")
        return 403, str(e)

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        return 'mensaje no reconocido'
    t = message['type']
    if t == 'text':
        return message['text']['body']
    elif t == 'button':
        return message['button']['text']
    elif t == 'interactive' and message['interactive']['type'] == 'list_reply':
        return message['interactive']['list_reply']['title']
    elif t == 'interactive' and message['interactive']['type'] == 'button_reply':
        return message['interactive']['button_reply']['title']
    else:
        return 'mensaje no procesado'

# --- Mensajes básicos ---
def text_Message(number, text):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {"body": text}
    }

def replyReaction_Message(number, messageId, emoji):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "reaction",
        "reaction": {"message_id": messageId, "emoji": emoji}
    }

def replyText_Message(number, messageId, text):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "context": {"message_id": messageId},
        "type": "text",
        "text": {"body": text}
    }

def markRead_Message(messageId):
    return {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": messageId
    }

# --- Mensajes interactivos ---
def listReply_Message(number, options, body, footer, sedd):
    rows = [{"id": f"{sedd}_row_{i+1}", "title": opt, "description": ""} for i, opt in enumerate(options)]
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body},
            "footer": {"text": footer},
            "action": {"button": "Ver Opciones", "sections": [{"title": "Secciones", "rows": rows}]}
        }
    }

def buttonReply_Message(number, options, body, footer, sedd):
    buttons = [{"type": "reply", "reply": {"id": f"{sedd}_btn_{i+1}", "title": opt}} for i, opt in enumerate(options)]
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {"type": "button", "body": {"text": body}, "footer": {"text": footer}, "action": {"buttons": buttons}}
    }

# --- Multimedia ---
def image_Message(number, url, caption="Aquí tienes una imagen"):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "image",
        "image": {"link": url, "caption": caption}
    }

def audio_Message(number, url):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "audio",
        "audio": {"link": url}
    }

def document_Message(number, url, caption, filename):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {"link": url, "caption": caption, "filename": filename}
    }

def sticker_Message(number, sticker_id):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "sticker",
        "sticker": {"id": sticker_id}
    }

# --- Chatbot ---
carreras = {
    "Ing Forestal": {
        "misión": "Formar profesionistas con conocimientos técnicos y científicos que contribuyan al manejo sustentable de los ecosistemas forestales en beneficio de la sociedad.",
        "visión": "Consolidarse como un programa educativo líder a nivel nacional en la enseñanza de la ciencia forestal.",
        "objetivo": "Formar profesionistas capaces de manejar los ecosistemas forestales y coadyuvar al desarrollo sustentable del sector forestal."
    },
    "Ambientales": {
        "misión": "Ser una licenciatura de excelencia en el ámbito local y nacional.",
        "visión": "Formar profesionales en el área de Ciencias Ambientales.",
        "objetivo": "Formar profesionales con una visión integral en las Ciencias Ambientales."
    },
    "Software": {
        "misión": "Formar profesionistas altamente competitivos.",
        "visión": "Consolidarse como un programa educativo de vanguardia.",
        "objetivo": "Formar ingenieros en desarrollo de software y sistemas inteligentes."
    },
    "Biología": {
        "misión": "Formar de manera integral profesionales bajo estándares de excelencia en el campo de la biología.",
        "visión": "Posicionarse como un programa educativo reconocido por su excelencia académica.",
        "objetivo": "Formar profesionistas altamente calificados en biología."
    },
    "Turismo": {
        "misión": "Consolidar profesionales de manera integral capaces de incidir en el desarrollo turístico sostenible.",
        "visión": "Ser referente en la excelencia académica y la innovación en la enseñanza.",
        "objetivo": "Formar profesionales que adquieran conocimientos, habilidades, actitudes y valores."
    }
}

carrera_seleccionada = None

def administrar_chatbot(text, number, messageId):
    global carrera_seleccionada
    mainOptions = ["🤔 ¿Qué es la UNSIJ?", "📋 Oferta educativa", "📅 Fechas"]
    text = normalizar_texto(text)
    lista_mensajes = []

    # Marcar mensaje como leído
    lista_mensajes.append(markRead_Message(messageId))
    time.sleep(1)

    # --- Respuestas del menú principal ---
    if text in ["hola", "buenos días", "buenas tardes", "volver al menú principal"]:
        body = "¡Hola! 🤖 Bienvenido a este taller el dia de hoy 10 de julio"
        footer = "Equipo UNSIJ"
        lista_mensajes.append(listReply_Message(number, mainOptions, body, footer, "sed1"))
        lista_mensajes.append(replyReaction_Message(number, messageId, "🫡"))

    elif "qué es la unsij" in text:
        body = "La UNSIJ es un instrumento de desarrollo para la región de la Sierra Norte..."
        body2 = "¿En qué más te podemos ayudar?"
        footer = "Equipo UNSIJ"
        lista_mensajes.append(text_Message(number, body))
        lista_mensajes.append(listReply_Message(number, mainOptions, body2, footer, "sed2"))

    elif "oferta educativa" in text:
        body = "Estas son las carreras disponibles en la UNSIJ. ¿Cuál te interesa?"
        footer = "Equipo UNSIJ"
        options = [f"✅ {carrera}" for carrera in carreras.keys()]
        lista_mensajes.append(listReply_Message(number, options, body, footer, "sed2"))

    elif any(c.lower() in text for c in carreras.keys()):
        carrera_seleccionada = next(c for c in carreras.keys() if c.lower() in text)
        body = f"Has seleccionado la carrera de {carrera_seleccionada}. ¿Qué te gustaría conocer?"
        footer = "Equipo UNSIJ"
        options = ["✅ Misión", "✅ Visión", "📋 Objetivo"]
        lista_mensajes.append(listReply_Message(number, options, body, footer, "sed3"))

    elif carrera_seleccionada and any(k in text for k in ["misión", "visión", "objetivo"]):
        if "misión" in text:
            body = carreras[carrera_seleccionada]["misión"]
        elif "visión" in text:
            body = carreras[carrera_seleccionada]["visión"]
        elif "objetivo" in text:
            body = carreras[carrera_seleccionada]["objetivo"]
        footer = "Equipo UNSIJ"
        options = ["✅ Misión", "✅ Visión", "📋 Objetivo"]
        lista_mensajes.append(listReply_Message(number, options, body, footer, "sed3"))
        carrera_seleccionada = None

    elif "fechas" in text:
        body = "Selecciona un evento para ver las fechas:"
        footer = "Equipo UNSIJ"
        options = ["🗓️ Entrega de fichas", "🗓️ Examen de selección", "🗓️ Inscripciones al CP", "🗓️ Curso propedéutico"]
        lista_mensajes.append(listReply_Message(number, options, body, footer, "sed2"))

    else:
        lista_mensajes.append(text_Message(number, "Lo siento, no entendí lo que dijiste. Prueba con 'hola' para comenzar a chatear 🤑"))

    # --- Enviar todos los mensajes ---
    for msg in lista_mensajes:
        enviar_Mensaje_whatsapp(msg)
