from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTIONS
import datetime
from tkinter import messagebox

# Variáveis globais para as coleções
lembretes = None
preferencias = None
tarefas = None

def conectar_mongodb():
    """Conecta ao MongoDB e inicializa as coleções"""
    global lembretes, preferencias, tarefas
    
    try:
        # Tentar conectar ao MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Verificar se o servidor está respondendo
        client.server_info()
        
        print("✅ Conectado ao MongoDB com sucesso!")
        
        # Selecionar o banco de dados
        db = client[MONGO_DB]
        
        # Inicializar as coleções
        lembretes = db[MONGO_COLLECTIONS['lembretes']]
        preferencias = db[MONGO_COLLECTIONS['preferencias']]
        tarefas = db[MONGO_COLLECTIONS['tarefas']]
        
        return True
        
    except Exception as e:
        erro = str(e)
        
        if "ServerSelectionTimeoutError" in erro:
            messagebox.showerror("Erro de Conexão", 
                "Não foi possível conectar ao MongoDB!\n\n"
                "Verifique se:\n"
                "1. O MongoDB está instalado\n"
                "2. O serviço do MongoDB está rodando\n\n"
                "Para resolver:\n"
                "1. Abra o Gerenciador de Serviços do Windows\n"
                "2. Procure por 'MongoDB Server'\n"
                "3. Clique com botão direito e selecione 'Iniciar'")
        else:
            messagebox.showerror("Erro", 
                f"Erro ao conectar ao MongoDB:\n{erro}\n\n"
                "Se precisar de ajuda, mostre esta mensagem de erro.")
        
        return False

def salvar_documento(colecao, documento):
    """Função genérica para salvar documentos no MongoDB"""
    try:
        resultado = colecao.insert_one(documento)
        return resultado.inserted_id
    except Exception as e:
        print(f"Erro ao salvar documento: {str(e)}")
        return None

def buscar_documentos(colecao, filtro=None):
    """Função genérica para buscar documentos no MongoDB"""
    try:
        if filtro is None:
            filtro = {}
        return list(colecao.find(filtro))
    except Exception as e:
        print(f"Erro ao buscar documentos: {str(e)}")
        return []

def atualizar_documento(colecao, filtro, atualizacao):
    """Função genérica para atualizar documentos no MongoDB"""
    try:
        resultado = colecao.update_one(filtro, {'$set': atualizacao})
        return resultado.modified_count > 0
    except Exception as e:
        print(f"Erro ao atualizar documento: {str(e)}")
        return False

def salvar_preferencia(chave, valor):
    """Salva uma preferência do usuário"""
    try:
        preferencias.update_one(
            {'chave': chave},
            {'$set': {'valor': valor}},
            upsert=True
        )
    except Exception as e:
        print(f"Erro ao salvar preferência: {str(e)}")

def obter_preferencia(chave, padrao=None):
    """Obtém uma preferência do usuário"""
    try:
        pref = preferencias.find_one({'chave': chave})
        return pref['valor'] if pref else padrao
    except Exception as e:
        print(f"Erro ao obter preferência: {str(e)}")
        return padrao 