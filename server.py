import os
import logging
from flask import Flask, request
import sett
import services

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return 'Hola mundo bigdateros, desde Flask'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge is not None:
            logging.info("Webhook verificado correctamente")
            return challenge
        else:
            logging.warning("Token incorrecto al verificar webhook")
            return 'token incorrecto', 403
    except Exception as e:
        logging.error(f"Error en la verificación del webhook: {e}")
        return str(e), 500

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    """
    try:
        body = request.get_json()
        logging.info(f"Mensaje recibido: {body}")

        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number, messageId, name)
        logging.info(f"Mensaje procesado correctamente de {number}")

        # Responder 200 a WhatsApp
        return 'enviado', 200

    except Exception as e:
        logging.error(f"Error al procesar mensaje: {e}")
        # Responder 500 para que WhatsApp sepa que hubo error
        return 'no enviado', 500
        """
    try:
        body = request.get_json()
        logging.info(f"Mensaje recibido: {body}")
        return 'ok', 200
    except Exception as e:
        logging.error(f"Error al procesar mensaje: {e}")
        return 'error', 500

# Nota: app.run() se elimina, Gunicorn lo manejará


