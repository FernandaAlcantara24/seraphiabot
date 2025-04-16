from flask import Flask, request
from send_message import send_whatsapp_message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.json
        print("Mensagem recebida:", data)

        try:
            messages = data['entry'][0]['changes'][0]['value']['messages']
            if messages:
                message = messages[0]
                sender = message['from']
                text = message['text']['body']
                print(f'Mensagem de {sender}: {text}')
                # Resposta automática
                send_whatsapp_message(sender, f"Você disse: {text}")
        except:
            pass

        return 'OK', 200

if __name__ == '__main__':
    send_whatsapp_message("numero", "Olá! Eu sou a Lux, assistente virtual da Seraphia Aromas. Em que posso te ajudar hoje? 😄")
