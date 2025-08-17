from flask import Flask, request, jsonify
import os
import sett
import services
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return 'Hola mundo bigdateros, desde Flask'

# Verificación de webhook
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

# Recepción de mensajes de WhatsApp
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
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
        logging.info(f"Mensaje recibido y enviado: {text} de {number}")
        return jsonify({"status": "enviado"}), 200

    except Exception as e:
        logging.error(f"No se pudo procesar el mensaje: {e}")
        return jsonify({"status": "no enviado", "error": str(e)}), 500

if __name__ == '__main__':
    # Solo para pruebas locales
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)


