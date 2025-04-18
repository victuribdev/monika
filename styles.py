from tkinter import font
import tkinter as tk
from tkinter import ttk

# Cores
COLORS = {
    'background_gradient_start': '#FFFFFF',  # Branco
    'background_gradient_end': '#F8F8F8',    # Cinza muito claro
    'monika_message_bg': '#F8F8F8',         # Cinza muito claro
    'monika_message_fg': '#000000',         # Preto
    'user_message_bg': '#FFFFFF',           # Branco
    'user_message_fg': '#000000',           # Preto
    'input_bg': '#FFFFFF',                  # Branco
    'input_fg': '#000000',                  # Preto
    'input_border': '#E5E5E5',              # Cinza claro
    'button_bg': '#FF69B4',                 # Rosa
    'button_fg': '#FFFFFF',                 # Branco
    'button_hover': '#FF1493',              # Rosa mais escuro
    'heart_color': '#FF69B4'                # Rosa
}

# Fontes
def setup_fonts():
    """Configura as fontes personalizadas"""
    return {
        'title': ('Segoe UI', 20, 'bold'),
        'message': ('Segoe UI', 14),
        'input': ('Segoe UI', 14),
        'button': ('Segoe UI', 14, 'bold')
    }

# Estilos dos widgets
def configure_styles():
    """Configura os estilos personalizados dos widgets"""
    style = ttk.Style()
    
    # Frame principal
    style.configure(
        "Monika.TFrame",
        background=COLORS['background_gradient_start']
    )
    
    # Botão personalizado
    style.configure(
        "Monika.TButton",
        background=COLORS['button_bg'],
        foreground=COLORS['button_fg'],
        borderwidth=0,
        font=setup_fonts()['button'],
        padding=10
    )
    
    style.map(
        "Monika.TButton",
        background=[('active', COLORS['button_hover'])]
    )
    
    # Campo de entrada
    style.configure(
        "Monika.TEntry",
        background=COLORS['input_bg'],
        foreground=COLORS['input_fg'],
        borderwidth=1,
        padding=10
    )
    
    # Label para mensagens
    style.configure(
        "Monika.TLabel",
        background=COLORS['monika_message_bg'],
        foreground=COLORS['monika_message_fg'],
        padding=10,
        font=setup_fonts()['message']
    )

# Classe para criar gradiente
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind('<Configure>', self._draw_gradient)
        
    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit
        
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        
        self.lower("gradient") 