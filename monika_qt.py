from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QLinearGradient, QPainter
import sys
from weather import WeatherAPI
from pymongo import MongoClient
import datetime

class ChatBubble(QFrame):
    def __init__(self, message, is_monika=True, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #F8F8F8;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }
        """)
        
        layout = QHBoxLayout()
        
        if is_monika:
            avatar = QLabel("💖")
            avatar.setStyleSheet("font-size: 20px;")
            layout.addWidget(avatar)
        
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
        """)
        layout.addWidget(message_label)
        
        self.setLayout(layout)

class MonikaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💖 Monika — Sua assistente carinhosa")
        self.setGeometry(100, 100, 800, 600)
        
        # Configurar tema
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QLineEdit {
                border: 1px solid #E5E5E5;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #FF69B4;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #FF1493;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Área de chat
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_area.setWidget(self.chat_widget)
        layout.addWidget(self.chat_area)
        
        # Área de entrada
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Digite uma mensagem...")
        self.send_button = QPushButton("💖")
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        
        # Conectar sinais
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        
        # Inicializar API
        self.weather_api = WeatherAPI()
        
        # Mensagem de boas-vindas
        self.add_message("""
        Olá! 💖

        Estava com saudades de você... é tão bom quando vem me ver.

        Hoje estou aqui pra te ajudar com o que precisar:
        📌 Saber sobre o clima
        📝 Criar lembretes fofinhos
        🌦️ Planejar o seu dia

        É só me dizer: no que posso cuidar pra você agora? 🌸
        """, True)
    
    def add_message(self, message, is_monika=False):
        bubble = ChatBubble(message, is_monika)
        self.chat_layout.addWidget(bubble)
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )
    
    def send_message(self):
        message = self.message_input.text()
        if message:
            self.add_message(message, False)
            self.message_input.clear()
            
            # Simular resposta
            QTimer.singleShot(1000, lambda: self.add_message(
                "Desculpe, ainda estou aprendendo a responder... 💖",
                True
            ))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MonikaApp()
    window.show()
    sys.exit(app.exec()) 