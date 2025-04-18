import tkinter as tk
from tkinter import ttk
from styles import COLORS, setup_fonts
import time

class ChatBubble(ttk.Frame):
    def __init__(self, parent, message, is_monika=True, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configurar estilo do balão
        bg_color = COLORS['monika_message_bg'] if is_monika else COLORS['user_message_bg']
        text_color = COLORS['monika_message_fg'] if is_monika else COLORS['user_message_fg']
        
        # Frame do balão
        self.bubble = ttk.Frame(self, style="Monika.TFrame")
        self.bubble.pack(side="left" if is_monika else "right", pady=5, padx=10)
        
        # Avatar (apenas para mensagens da Monika)
        if is_monika:
            self.avatar = tk.Label(
                self.bubble,
                text="💖",
                font=("Segoe UI", 16),
                bg=bg_color,
                fg=COLORS['heart_color']
            )
            self.avatar.pack(side="left", padx=(5, 10))
        
        # Texto da mensagem
        self.message = tk.Label(
            self.bubble,
            text=message,
            font=setup_fonts()['message'],
            bg=bg_color,
            fg=text_color,
            wraplength=400,
            justify="left",
            padx=15,
            pady=10
        )
        self.message.pack(side="left", fill="x", expand=True)

class AnimatedTyping(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.dots = ["", ".", "..", "..."]
        self.current_dot = 0
        
        self.label = tk.Label(
            self,
            text="Monika está digitando",
            font=setup_fonts()['message'],
            fg=COLORS['monika_message_fg'],
            bg=COLORS['background_gradient_start']
        )
        self.label.pack(pady=5)
        
        self.animate()
    
    def animate(self):
        self.current_dot = (self.current_dot + 1) % len(self.dots)
        self.label.config(text=f"Monika está digitando{self.dots[self.current_dot]}")
        self.after(500, self.animate)

class CustomEntry(ttk.Entry):
    def __init__(self, parent, placeholder="Digite uma mensagem...", **kwargs):
        super().__init__(parent, style="Monika.TEntry", **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = COLORS['input_fg']
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        self._add_placeholder()
    
    def _clear_placeholder(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(foreground=self.default_fg_color)
    
    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground=self.placeholder_color)

class HeartButton(ttk.Button):
    def __init__(self, parent, command=None):
        super().__init__(
            parent,
            text="💖",
            command=command,
            style="Monika.TButton",
            width=4
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self.configure(style="Monika.TButton.Hover")
        
    def on_leave(self, e):
        self.configure(style="Monika.TButton") 