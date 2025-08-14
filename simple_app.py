#!/usr/bin/env python3
"""
Version simplifiée de SecurePassGen pour diagnostiquer les problèmes d'affichage
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

class SimpleSecurePassGen:
    def __init__(self):
        print("Initializing SimpleSecurePassGen...")
        
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("SecurePassGen - Simple")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration macOS
        if sys.platform == "darwin":
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.after_idle(lambda: self.root.attributes('-topmost', False))
        
        print("Creating simple interface...")
        self.create_simple_interface()
        print("Interface created successfully")
    
    def create_simple_interface(self):
        """Crée une interface simplifiée"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🔐 SecurePassGen (Simple)", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Configuration de longueur
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(length_frame, text="Longueur:").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(length_frame, from_=4, to=64, textvariable=self.length_var, width=10)
        length_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Minuscules", variable=self.use_lowercase).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Majuscules", variable=self.use_uppercase).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Chiffres", variable=self.use_digits).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Caractères spéciaux", variable=self.use_special).pack(anchor=tk.W)
        
        # Bouton de génération
        generate_btn = ttk.Button(main_frame, text="🎲 Générer Mot de Passe", command=self.generate_password)
        generate_btn.pack(pady=20)
        
        # Zone de résultat
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(result_frame, text="Résultat:").pack(anchor=tk.W)
        
        self.result_var = tk.StringVar()
        result_entry = ttk.Entry(result_frame, textvariable=self.result_var, font=('Courier', 12), state='readonly')
        result_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Bouton copier
        copy_btn = ttk.Button(main_frame, text="📋 Copier", command=self.copy_to_clipboard)
        copy_btn.pack(pady=10)
    
    def generate_password(self):
        """Génère un mot de passe simple"""
        try:
            length = self.length_var.get()
            chars = ""
            
            if self.use_lowercase.get():
                chars += string.ascii_lowercase
            if self.use_uppercase.get():
                chars += string.ascii_uppercase
            if self.use_digits.get():
                chars += string.digits
            if self.use_special.get():
                chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            if not chars:
                messagebox.showwarning("Attention", "Veuillez sélectionner au moins un type de caractère.")
                return
            
            password = ''.join(random.choice(chars) for _ in range(length))
            self.result_var.set(password)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {e}")
    
    def copy_to_clipboard(self):
        """Copie le résultat dans le presse-papiers"""
        password = self.result_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers!")
        else:
            messagebox.showwarning("Attention", "Aucun mot de passe à copier.")
    
    def run(self):
        """Lance l'application"""
        print("Starting application...")
        
        # Forcer l'affichage
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.update()
        
        print("Application ready, starting mainloop...")
        self.root.mainloop()
        print("Application closed.")

if __name__ == "__main__":
    print("=== SIMPLE SECUREPASSGEN ===")
    try:
        app = SimpleSecurePassGen()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()