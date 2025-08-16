import os

# Token para verificar webhook de WhatsApp
token = os.getenv("MY_APP_TOKEN", "appPrueba")  # valor por defecto solo para pruebas locales

# Token de la API de WhatsApp
whatsapp_token = os.getenv("WHATSAPP_TOKEN")

# URL de la API de WhatsApp
whatsapp_url = os.getenv("WHATSAPP_URL", "https://graph.facebook.com/v21.0/492826513925103/messages")

# Stickers del chatbot
stickers = {
    "poyo_feliz": 984778742532668,
    "perro_traje": 1009219236749949,
    "perro_triste": 982264672785815,
    "pedro_pascal_love": 801721017874258,
    "pelfet": 3127736384038169,
    "anotado": 24039533498978939,
    "gato_festejando": 1736736493414401,
    "okis": 268811655677102,
    "cachetada": 275511571531644,
    "gato_juzgando": 107235069063072,
    "chicorita": 3431648470417135,
    "gato_triste": 210492141865964,
    "gato_cansado": 1021308728970759
}

# Documento de ejemplo
document_url = "https://www.africau.edu/images/default/sample.pdf"
