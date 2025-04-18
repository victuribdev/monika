import requests
import json
from datetime import datetime, timedelta
from tkinter import messagebox

class WeatherAPI:
    def __init__(self):
        self.api_key = "d89497fff3892b7ff37526f1a6cbc929"  # API key do OpenWeatherMap
        self.cache = {}
        self.cache_timeout = timedelta(minutes=30)
        
    def verificar_api_key(self):
        """Verifica se a API key está configurada e é válida"""
        if not self.api_key or self.api_key == "sua_api_key_aqui":
            messagebox.showerror("Erro", "API key não configurada. Por favor, configure sua chave API do OpenWeatherMap.")
            return False
            
        try:
            # Testa a API key com uma cidade conhecida
            url = f"http://api.openweathermap.org/data/2.5/weather?q=São Paulo&appid={self.api_key}&units=metric&lang=pt_br"
            response = requests.get(url)
            
            if response.status_code == 401:
                messagebox.showerror("Erro", "API key inválida. Por favor, verifique sua chave API do OpenWeatherMap.")
                return False
                
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar API key: {str(e)}")
            return False
            
    def obter_coordenadas(self, cidade):
        """Obtém as coordenadas geográficas de uma cidade"""
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if not data:
                messagebox.showerror("Erro", f"Cidade '{cidade}' não encontrada.")
                return None
                
            return {
                'lat': data[0]['lat'],
                'lon': data[0]['lon']
            }
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter coordenadas: {str(e)}")
            return None
            
    def obter_clima(self, cidade):
        """Obtém os dados do clima para uma cidade"""
        # Verifica se há dados em cache
        if cidade in self.cache:
            cache_data = self.cache[cidade]
            if datetime.now() - cache_data['timestamp'] < self.cache_timeout:
                return cache_data['data']
                
        # Obtém as coordenadas
        coords = self.obter_coordenadas(cidade)
        if not coords:
            return None
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={self.api_key}&units=metric&lang=pt_br"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200:
                messagebox.showerror("Erro", f"Erro ao obter dados do clima: {data.get('message', 'Erro desconhecido')}")
                return None
                
            clima = {
                'cidade': cidade,
                'temperatura': data['main']['temp'],
                'sensacao': data['main']['feels_like'],
                'umidade': data['main']['humidity'],
                'descricao': data['weather'][0]['description']
            }
            
            # Atualiza o cache
            self.cache[cidade] = {
                'data': clima,
                'timestamp': datetime.now()
            }
            
            return clima
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter dados do clima: {str(e)}")
            return None 