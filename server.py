from flask import Flask, request, jsonify
import os
import sett
import services
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# --- Ruta de prueba ---
@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return 'Hola mundo bigdateros, desde Flask'

# --- Verificación de webhook ---
@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token_request = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token_request == sett.token and challenge is not None:
            logging.info("Webhook verificado correctamente")
            return challenge
        else:
            logging.warning("Token incorrecto en verificación")
            return 'token incorrecto', 403
    except Exception as e:
        logging.error(f"Error al verificar webhook: {e}")
        return str(e), 403

# --- Recepción de mensajes de WhatsApp ---
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()

        # Extraer mensaje
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value.get('messages', [])[0]  # Por si no hay mensaje
        if not message:
            return jsonify({"status": "no hay mensajes"}), 200

        number = services.replace_start(message['from'])
        messageId = message['id']

        contacts = value.get('contacts', [{}])[0]
        name = contacts.get('profile', {}).get('name', 'Usuario')

        text = services.obtener_Mensaje_whatsapp(message)

        # Procesar con chatbot
        services.administrar_chatbot(text, number, messageId)

        logging.info(f"Mensaje recibido y procesado: '{text}' de {number}")
        return jsonify({"status": "enviado"}), 200

    except Exception as e:
        logging.error(f"No se pudo procesar el mensaje: {e}")
        return jsonify({"status": "no enviado", "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)


