#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import os

def test_simple_window():
    # Configuration macOS
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    root = tk.Tk()
    root.title("Test Simple")
    root.geometry("400x300")
    root.configure(bg='white')
    
    # Forcer l'affichage
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    root.deiconify()
    root.focus_force()
    
    # Widget simple
    label = tk.Label(root, text="Test d'affichage", font=('Arial', 16), bg='white')
    label.pack(expand=True)
    
    button = tk.Button(root, text="Cliquez-moi", command=lambda: print("Bouton cliqué!"))
    button.pack(pady=20)
    
    # Forcer l'update
    root.update_idletasks()
    root.update()
    
    print("Fenêtre créée et affichée")
    root.mainloop()

if __name__ == "__main__":
    test_simple_window()