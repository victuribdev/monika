from flask import Flask, request, jsonify
from flask_cors import CORS
from weather import WeatherAPI
import datetime
from pymongo import MongoClient
import threading
import time
import random
import requests
import json

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

# Inicializar APIs
weather_api = WeatherAPI()

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['aliem']
lembretes = db['lembretes']
aprendizado = db['aprendizado']
configuracoes = db['configuracoes']

# Inicializar configurações padrão
if configuracoes.count_documents({}) == 0:
    configuracoes.insert_one({
        'nome': 'ALIEM',
        'personalidade': 'neutra',
        'preferencias': {}
    })

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.json
    message = data.get('message', '').lower()
    
    response = {
        'text': "Não entendi. Pode reformular?",
        'isMonika': True
    }
    
    # Sistema de aprendizado
    if message.startswith('aprenda que'):
        try:
            pergunta, resposta = message.split('aprenda que')[1].split('é')
            aprendizado.insert_one({
                'pergunta': pergunta.strip(),
                'resposta': resposta.strip(),
                'data': datetime.datetime.now()
            })
            response['text'] = "Aprendido! Posso usar isso no futuro."
        except:
            response['text'] = "Formato inválido. Use: aprenda que [pergunta] é [resposta]"
    
    # Consulta ao aprendizado
    elif aprendizado.count_documents({'pergunta': message}) > 0:
        resposta = aprendizado.find_one({'pergunta': message})
        response['text'] = resposta['resposta']
    
    # Clima
    elif 'clima' in message or 'tempo' in message:
        cidade = message.split('em ')[1] if 'em ' in message else 'São Paulo'
        clima = weather_api.obter_clima(cidade)
        if clima:
            response['text'] = f"Em {clima['cidade']} está fazendo {clima['temperatura']}°C\n"
            response['text'] += f"Sensação térmica: {clima['sensacao']}°C\n"
            response['text'] += f"Umidade: {clima['umidade']}%\n"
            response['text'] += f"Condição: {clima['descricao']}"
        else:
            response['text'] = "Não consegui obter o clima para esta cidade."
    
    # Lembretes
    elif 'lembrete' in message or 'lembra' in message:
        texto = message.split('de ')[1] if 'de ' in message else message
        doc = {
            'texto': texto,
            'data': datetime.datetime.now()
        }
        lembretes.insert_one(doc)
        response['text'] = f"Lembrete criado: {texto}"
    
    # Notícias
    elif 'notícias' in message or 'noticias' in message:
        try:
            api_key = "8ee464988aa04542a746033215b524f3"
            url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={api_key}"
            
            response_news = requests.get(url)
            noticias = response_news.json()
            
            if noticias['status'] == 'ok' and noticias['articles']:
                noticias_formatadas = []
                for article in noticias['articles'][:3]:
                    titulo = article.get('title', 'Sem título')
                    fonte = article.get('source', {}).get('name', 'Fonte desconhecida')
                    noticias_formatadas.append(f"📰 {titulo} ({fonte})")
                
                response['text'] = "Principais notícias do Brasil:\n\n" + "\n\n".join(noticias_formatadas)
            else:
                response['text'] = "Não encontrei notícias no momento."
        except Exception as e:
            print(f"Erro ao buscar notícias: {str(e)}")
            response['text'] = "Erro ao buscar notícias. Tente novamente mais tarde."
    
    # Calculadora
    elif any(op in message for op in ['+', '-', '*', '/']):
        try:
            resultado = eval(message)
            response['text'] = f"Resultado: {resultado}"
        except:
            response['text'] = "Não consegui calcular."
    
    # Configurações
    elif 'mude seu nome para' in message:
        novo_nome = message.split('mude seu nome para')[1].strip()
        configuracoes.update_one({}, {'$set': {'nome': novo_nome}})
        response['text'] = f"Meu nome foi alterado para {novo_nome}"
    
    return jsonify(response)

def verificar_notificacoes():
    while True:
        try:
            agora = datetime.datetime.now()
            lembretes_atrasados = list(lembretes.find({
                'data': {'$lte': agora}
            }))
            
            for lembrete in lembretes_atrasados:
                print(f"Lembrete: {lembrete['texto']}")
                lembretes.delete_one({'_id': lembrete['_id']})
            
            time.sleep(300)  # Verificar a cada 5 minutos
        except Exception as e:
            print(f"Erro na thread de notificações: {str(e)}")
            time.sleep(60)

if __name__ == '__main__':
    # Iniciar thread de notificações
    thread = threading.Thread(target=verificar_notificacoes, daemon=True)
    thread.start()
    
    # Iniciar servidor Flask
    app.run(port=5000, debug=True) 