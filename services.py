import requests
import sett
import json
import time

import re

def normalizar_texto(texto):
    # Eliminar emojis y caracteres especiales
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip().lower()


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def text_Message_2(number,body, footer):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": message_body
                }
            }
    )
    return data

  
def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data
  
def audio_Message(number, url):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "audio",
            "audio": {
                "link": url  # URL del audio
            }
        }
    )
    return data


def image_Message(number, url, caption="Aquí tienes una imagen"):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "image",
            "image": {
                "link": url,  # URL de la imagen
                "caption": caption
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data
  
  
carreras = {
    "Ing Forestal": {
        "misión": "Formar profesionistas con conocimientos técnicos y científicos que contribuyan al manejo sustentable de los ecosistemas forestales en beneficio de la sociedad, mediante una educación de calidad con base en principios éticos.",
        "visión": "Consolidarse como un programa educativo líder a nivel nacional en la enseñanza de la ciencia forestal y en la formación de profesionales en el manejo sustentable de los ecosistemas forestales.",
        "objetivo": "Formar profesionistas con conocimientos, habilidades, valores y aptitudes capaces de manejar los ecosistemas forestales y coadyuvar al desarrollo sustentable del sector forestal."
    },
    "Ambientales": {
        "misión": "Ser una licenciatura de excelencia en el ámbito local y nacional, a partir de un plan de estudios integral e intercultural...",
        "visión": "Formar profesionales en el área de Ciencias Ambientales...",
        "objetivo": "Formar profesionales con una visión integral en las Ciencias Ambientales..."
    },
    "Software": {
        "misión": "Formar profesionistas altamente competitivos.",
        "visión": "Consolidarse como un programa educativo de vanguardia...",
        "objetivo": "Formar ingenieros en desarrollo de software y sistemas inteligentes..."
    },
    "Biología": {  # Corregido de "Biolígia"
        "misión": "Formar de manera integral profesionales bajo estándares de excelencia en el campo de la biología...",
        "visión": "Posicionarse como un programa educativo reconocido por su excelencia académica...",
        "objetivo": "La Licenciatura en Biología tiene como objetivo fundamental formar profesionistas altamente calificados..."
    },
    "Turismo": {
        "misión": "Consolidar profesionales de manera integral capaces de incidir en el desarrollo turístico sostenible...",
        "visión": "Ser referente en la excelencia académica, la innovación en la enseñanza...",
        "objetivo": "Formar profesionales que adquieran conocimientos, habilidades, actitudes y valores..."
    }
}

# Variables globales
carrera_seleccionada = None
fecha_seleccionada = None

def administrar_chatbot(text, number, messageId, name):
    global carrera_seleccionada
    global fecha_seleccionada

    mainOptions = ["🤔 ¿Qué es la UNSIJ?", "📋 Oferta educativa", "📅 Fechas"]
    text = text.lower().strip()
    list = []
    
    print("Mensaje del usuario:", text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if text in ["hola", "buenos días", "buenas tardes", "volver al menú principal"]:
        body = "¡Hola! 🤖 Bienvenido al chatbot de la Universidad de la Sierra Juárez. ¿En qué te podemos ayudar?"
        footer = "Equipo UNSIJ"
        replyButtonData = listReply_Message(number, mainOptions, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.extend([replyReaction, replyButtonData])

    elif "¿qué es la unsij?" in text:
        body = "La UNSIJ es un instrumento de desarrollo para la región de la Sierra Norte..."
        body2 = "¿En qué más te podemos ayudar?"
        footer = "Equipo UNSIJ"
        replyMsg = text_Message(number, body)
        replyButtonData = listReply_Message(number, mainOptions, body2, footer, "sed2", messageId)
        list.extend([replyMsg, replyButtonData])

    elif "oferta educativa" in text:
        body = "Estas son las carreras disponibles en la UNSIJ. ¿Cuál te interesa?"
        footer = "Equipo UNSIJ"
        options = [f"✅ {carrera}" for carrera in carreras.keys()]
        replyButtonData = listReply_Message(number, options, body, footer, "sed2", messageId)
        list.append(replyButtonData)

    elif any(carrera.lower() in text for carrera in carreras.keys()):
        carrera_seleccionada = next(carrera for carrera in carreras.keys() if carrera.lower() in text)
        body = f"Has seleccionado la carrera de {carrera_seleccionada}. ¿Qué te gustaría conocer?"
        footer = "Equipo UNSIJ"
        options = ["✅ Misión", "✅ Visión", "📋 Objetivo"]

        replyButtonData = listReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)
        
        
    elif carrera_seleccionada:  # Si hay una carrera seleccionada y el usuario pregunta por misión, visión o plan de estudio
        print(carrera_seleccionada)
        print("misión" in text)
        if "misión" in text:
            body = carreras[carrera_seleccionada]["misión"]
        elif "visión" in text:
            body = carreras[carrera_seleccionada]["visión"]
        elif "objetivo" in text:
            body = carreras[carrera_seleccionada]["objetivo"]
        carrera_seleccionada = None
        footer = "Equipo UNSIJ"
        options = ["✅ Misión", "✅ Visión", "📋 Objetivo"]  # Asegúrate de definir las opciones aquí
        replyButtonData = listReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)

    elif "fechas" in text:
        body = "Selecciona un evento para ver las fechas:"
        footer = "Equipo UNSIJ"
        options = ["🗓️ Entrega de fichas", "🗓️ Examen de selección", "🗓️ Inscripciones al CP", "🗓️ Curso propedéutico"]
        replyButtonData = listReply_Message(number, options, body, footer, "sed2", messageId)
        list.append(replyButtonData)

    elif "entrega de fichas" in text:
        body = "La entrega de fichas será del 16 de febrero al 26 de junio de 2024"
        footer = "Equipo UNSIJ"
        options = ["Volver al menú de fechas", "Volver al menú principal"]
        replyButtonData = listReply_Message(number, options, body, footer, "fecha_entrega_fichas", messageId)
        list.append(replyButtonData)

    elif "examen de selección" in text:
        body = "El examen de selección será el 25 de mayo y 01 de julio de 2024"
        footer = "Equipo UNSIJ"
        options = ["Volver al menú de fechas", "Volver al menú principal"]
        replyButtonData = listReply_Message(number, options, body, footer, "fecha_examen_seleccion", messageId)
        list.append(replyButtonData)

    elif "inscripciones al cp" in text:
        body = "Las inscripciones al curso propedéutico son del 15 al 26 de julio de 2024"
        footer = "Equipo UNSIJ"
        options = ["Volver al menú de fechas", "Volver al menú principal"]
        replyButtonData = listReply_Message(number, options, body, footer, "fecha_inscripciones_cp", messageId)
        list.append(replyButtonData)

    elif "curso propedéutico" in text:
        body = "El curso propedéutico será del 29 de julio al 20 de septiembre de 2024"
        footer = "Equipo UNSIJ"
        options = ["Volver al menú de fechas", "Volver al menú principal"]
        replyButtonData = listReply_Message(number, options, body, footer, "fecha_curso_propedeutico", messageId)
        list.append(replyButtonData)
    elif "escuchar audio" in text:
        audio_url = "https://cdn.freesound.org/previews/165/165879_2453745-lq.mp3"  # Reemplaza con la URL de tu audio
        audioMsg = audio_Message(number, audio_url)
        list.append(audioMsg)

    elif "ver imagen" in text:
        image_url = "https://cdn.glitch.global/2f982c3f-3080-4974-a218-6a1285c0b62c/c3194dd8-bab5-48c8-8f40-6510790df95b.image.png?v=1743619814387"  # Reemplaza con la URL de tu imagen
        imageMsg = image_Message(number, image_url, "Aquí tienes una imagen")
        list.append(imageMsg)

    else:
        body = "Lo siento, no entendí lo que dijiste. Prueba con 'hola' para comenzar a chatear 🤑"
        list.append(text_Message(number, body))

    for item in list:
        enviar_Mensaje_whatsapp(item)




#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
        
