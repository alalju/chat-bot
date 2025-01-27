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
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                        "text": body
                    },
                    "footer": {
                        "text": footer
                    }
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
    "Ciencias Ambientales": {
        "misión": "Ser una licenciatura de excelencia en el ámbito local y nacional, a partir de un plan de estudios integral e intercultural de acuerdo a las necesidades actuales integrando contenidos éticos, democráticos y humanísticos. Contando con una planta académica de calidad, que permita la formación de estudiantes aptos para favorecer el desarrollo sostenible en sus entornos de vida y de influencia, a través de líneas de investigación que aborden los problemas socioambientales y fomenten el Desarrollo Comunitario.",
        "visión": "Formar profesionales en el área de Ciencias Ambientales, a través de los procesos integrales desarrollados en el currículo que se fundamenta en los ejes de docencia, investigación, promoción al desarrollo y difusión de la cultura, con un enfoque intercultural; promoviendo la adquisición de conocimientos, actitudes, habilidades y destrezas con un alto nivel de responsabilidad y de excelencia, que permita a los egresados trabajar en equipos transdisciplinarios y multidisciplinarios, en un contexto ético, democrático y humanista para la prevención, análisis, evaluación e implementación de soluciones creativas e innovadoras a los problemas socioambientales, con el propósito de lograr el desarrollo sostenible local y nacional.",
        "objetivo": "El plan de estudios incluye los siguientes módulos..."
    },
    "Derecho": {
        "misión": "La misión de la carrera de Derecho es...",
        "visión": "La visión de la carrera de Derecho es...",
        "objetivo": "El plan de estudios incluye los siguientes módulos..."
    },
    "Medicina": {
        "misión": "La misión de la carrera de Medicina es...",
        "visión": "La visión de la carrera de Medicina es...",
        "objetivo": "El plan de estudios incluye los siguientes módulos..."
    }
}



# Variable global para rastrear la carrera seleccionada
carrera_seleccionada = None
fecha_seleccionada = None

def administrar_chatbot(text, number, messageId, name):
    global carrera_seleccionada  # Usamos la variable global para almacenar la carrera seleccionada
    global fecha_seleccionada  # Usamos la variable global para almacenar la fecha seleccionada
    mainOptions = ["🤔 ¿Qué es la UNSIJ?", "📋 Oferta educativa", "✅ Misión y Visión", "📅 Fechas"]

    text = text.lower()  # Mensaje que envió el usuario
    list = []
    print("mensaje del usuario: ", text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "hola" in text:
        body = "¡Hola! 🤖 Bienvenido al chatbot de la Universidad de la Sierra Juárez. ¿En qué te podemos ayudar?"
        footer = "Equipo UNSIJ"

        replyButtonData = listReply_Message(number, mainOptions, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "¿qué es la unsij?" in text:
        body = "La UNSIJ es un instrumento de desarrollo para la región de la Sierra Norte, como Centro de Educación Superior e Investigación Científica..."
        body2 = "¿En qué más te podemos ayudar?"
        footer = "Equipo UNSIJ"
        replyMsg = text_Message(number, body)
        replyButtonData = listReply_Message(number, mainOptions, body2, footer, "sed2", messageId)
        list.append(replyMsg)
        list.append(replyButtonData)
        
    elif "oferta educativa" in text:
        body = "Estas son las carreras disponibles en la UNSIJ. ¿Cuál te interesa?"
        footer = "Equipo UNSIJ"
        options = ["✅ Ing Forestal", "✅ Lic en Administracion", "✅ Derecho", "✅ Medicina"]

        replyButtonData = listReply_Message(number, options, body, footer, "sed2", messageId)
        list.append(replyButtonData)
        
    elif any(carrera.lower() in text for carrera in carreras.keys()):
        carrera_seleccionada = next(carrera for carrera in carreras.keys() if carrera.lower() in text)
        body = f"Has seleccionado la carrera de {carrera_seleccionada}. ¿Qué te gustaría conocer?"
        footer = "Equipo UNSIJ"
        options = ["✅ Misión", "✅ Visión", "📋 Plan de estudio"]

        replyButtonData = listReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)

    elif carrera_seleccionada:  # Si hay una carrera seleccionada y el usuario pregunta por misión, visión o plan de estudio
        if "misión" in text:
            body = carreras[carrera_seleccionada]["misión"]
        elif "visión" in text:
            body = carreras[carrera_seleccionada]["visión"]
        elif "plan de estudio" in text:
            body = carreras[carrera_seleccionada]["plan_estudio"]
        footer = "Equipo UNSIJ"
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
        body = "El examen de selección será del 25 de mayo y 01 de julio de 2024"
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
    elif "curso propedeutico" in text:
        body = "El curso propedéutico será del 29 de julio al 20 de septiembre de 2024"
        footer = "Equipo UNSIJ"
        options = ["Volver al menú de fechas", "Volver al menú principal"]

        replyButtonData = listReply_Message(number, options, body, footer, "fecha_curso_propedeutico", messageId)
        list.append(replyButtonData)

    else:
        data = text_Message(number, "Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

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
        
