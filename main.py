#!/usr/bin/env python3
"""
SecurePassGen - Générateur de Mots de Passe Sécurisé
Version simplifiée pour macOS
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import secrets
import string
import re
import math
import platform
import os
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

class SecurePassGenApp:
    def __init__(self):
        print("Initializing SecurePassGen...")
        
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.setup_platform_specific()
        self.setup_window()
        
        # Créer l'interface
        self.create_interface()
        
        print("SecurePassGen initialized successfully")
    
    def setup_platform_specific(self):
        """Configuration spécifique à la plateforme"""
        self.system = platform.system().lower()
        
        # Configuration macOS
        if self.system == "darwin":
            # Désactiver les avertissements de dépréciation Tk
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            
            # Configuration spécifique macOS
            try:
                self.root.createcommand('::tk::mac::Quit', self.on_quit)
                self.root.tk.call('tk', 'scaling', 1.0)
            except:
                pass
        
        # Configuration Windows
        elif self.system == "windows":
            try:
                # Améliorer l'affichage sur Windows
                self.root.tk.call('tk', 'scaling', 1.0)
                # Support DPI élevé
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
    
    def setup_window(self):
        """Configure la fenêtre principale"""
        self.root.title("🔐 SecurePassGen - Générateur de Mots de Passe Sécurisé")
        
        # Taille adaptative selon la plateforme
        if hasattr(self, 'system') and self.system == "darwin":
            self.root.geometry("750x650")
        else:
            self.root.geometry("700x600")
            
        self.root.configure(bg='#f0f0f0')
        
        # Centrer la fenêtre
        self.center_window()
        
        # Configuration de l'icône selon la plateforme
        self.setup_icon()
        
        # Configuration des polices selon la plateforme
        self.setup_fonts()
    
    def setup_icon(self):
        """Configure l'icône de l'application"""
        try:
            # Chemin vers l'icône (si elle existe)
            icon_path = Path(__file__).parent / "assets" / "icon.ico"
            if icon_path.exists():
                if hasattr(self, 'system') and self.system == "windows":
                    self.root.iconbitmap(str(icon_path))
                else:
                    # Pour macOS et Linux, utiliser photoimage
                    icon = tk.PhotoImage(file=str(icon_path))
                    self.root.iconphoto(False, icon)
        except Exception as e:
            print(f"Impossible de charger l'icône: {e}")
    
    def setup_fonts(self):
        """Configure les polices selon la plateforme"""
        try:
            if hasattr(self, 'system') and self.system == "darwin":  # macOS
                self.default_font = font.Font(family="SF Pro Display", size=12)
                self.title_font = font.Font(family="SF Pro Display", size=16, weight="bold")
                self.mono_font = font.Font(family="SF Mono", size=11)
            elif hasattr(self, 'system') and self.system == "windows":
                self.default_font = font.Font(family="Segoe UI", size=10)
                self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")
                self.mono_font = font.Font(family="Consolas", size=10)
            else:  # Linux
                self.default_font = font.Font(family="Ubuntu", size=10)
                self.title_font = font.Font(family="Ubuntu", size=14, weight="bold")
                self.mono_font = font.Font(family="Ubuntu Mono", size=10)
        except:
            # Fallback vers les polices par défaut
            self.default_font = font.nametofont("TkDefaultFont")
            self.title_font = font.nametofont("TkDefaultFont")
            self.mono_font = font.nametofont("TkFixedFont")
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculer la position
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Assurer que la fenêtre reste dans les limites de l'écran
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Crée l'interface utilisateur"""
        # Frame principal avec padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🔐 SecurePassGen", 
                               font=getattr(self, 'title_font', ('Arial', 18, 'bold')))
        title_label.pack(pady=(0, 20))
        
        # Section Configuration
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuration", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Longueur
        length_frame = ttk.Frame(config_frame)
        length_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(length_frame, text="Longueur:").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(length_frame, from_=4, to=128, 
                                   textvariable=self.length_var, width=10)
        length_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Options de caractères
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(config_frame, text="Minuscules (a-z)", 
                       variable=self.use_lowercase).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Majuscules (A-Z)", 
                       variable=self.use_uppercase).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Chiffres (0-9)", 
                       variable=self.use_digits).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Caractères spéciaux (!@#$%^&*)", 
                       variable=self.use_special).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Exclure caractères ambigus (0,O,1,l,I)", 
                       variable=self.exclude_ambiguous).pack(anchor=tk.W, pady=2)
        
        # Section Génération
        gen_frame = ttk.LabelFrame(main_frame, text="🎲 Génération", padding="15")
        gen_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Boutons de génération
        button_frame = ttk.Frame(gen_frame)
        button_frame.pack(pady=(0, 15))
        
        ttk.Button(button_frame, text="🎲 Générer Mot de Passe", 
                  command=self.generate_password).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔄 Générer Plusieurs", 
                  command=self.generate_multiple).pack(side=tk.LEFT)
        
        # Zone de résultat
        ttk.Label(gen_frame, text="Résultat:").pack(anchor=tk.W, pady=(0, 5))
        
        result_frame = ttk.Frame(gen_frame)
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(result_frame, textvariable=self.result_var, 
                                    font=getattr(self, 'mono_font', ('Courier', 12)), state='readonly')
        self.result_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(result_frame, text="📋 Copier", 
                  command=self.copy_to_clipboard).pack(side=tk.RIGHT)
        
        # Section Analyse
        analysis_frame = ttk.LabelFrame(main_frame, text="📊 Analyse de Force", padding="15")
        analysis_frame.pack(fill=tk.BOTH, expand=True)
        
        # Zone de test
        ttk.Label(analysis_frame, text="Tester un mot de passe:").pack(anchor=tk.W, pady=(0, 5))
        
        test_frame = ttk.Frame(analysis_frame)
        test_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.test_var = tk.StringVar()
        self.test_entry = ttk.Entry(test_frame, textvariable=self.test_var, show="*")
        self.test_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.test_entry.bind('<KeyRelease>', self.on_password_change)
        
        ttk.Button(test_frame, text="🔍 Analyser", 
                  command=self.analyze_password).pack(side=tk.RIGHT)
        
        # Résultats d'analyse
        self.analysis_text = tk.Text(analysis_frame, height=6, wrap=tk.WORD, 
                                   font=getattr(self, 'default_font', ('Arial', 10)))
        self.analysis_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Scrollbar pour l'analyse
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", 
                                command=self.analysis_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.analysis_text.configure(yscrollcommand=scrollbar.set)
    
    def generate_password(self):
        """Génère un mot de passe"""
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
            
            if self.exclude_ambiguous.get():
                chars = chars.replace('0', '').replace('O', '').replace('1', '')
                chars = chars.replace('l', '').replace('I', '')
            
            if not chars:
                messagebox.showwarning("Attention", 
                                     "Veuillez sélectionner au moins un type de caractère.")
                return
            
            password = ''.join(random.choice(chars) for _ in range(length))
            self.result_var.set(password)
            
            # Analyser automatiquement le mot de passe généré
            self.test_var.set(password)
            self.analyze_password()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {e}")
    
    def generate_multiple(self):
        """Génère plusieurs mots de passe"""
        passwords = []
        for _ in range(5):
            self.generate_password()
            if self.result_var.get():
                passwords.append(self.result_var.get())
        
        if passwords:
            self.show_multiple_passwords(passwords)
    
    def show_multiple_passwords(self, passwords):
        """Affiche plusieurs mots de passe dans une nouvelle fenêtre"""
        window = tk.Toplevel(self.root)
        window.title("Mots de passe générés")
        window.geometry("500x400")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Mots de passe générés:", 
                 font=getattr(self, 'title_font', ('Arial', 12, 'bold'))).pack(pady=(0, 10))
        
        text_widget = tk.Text(frame, font=getattr(self, 'mono_font', ('Courier', 10)))
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        for i, password in enumerate(passwords, 1):
            text_widget.insert(tk.END, f"{i}. {password}\n")
        
        text_widget.config(state=tk.DISABLED)
    
    def copy_to_clipboard(self):
        """Copie le résultat dans le presse-papiers avec gestion multiplateforme"""
        password = self.result_var.get()
        if password:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                
                # Forcer la mise à jour du presse-papiers selon la plateforme
                if hasattr(self, 'system') and self.system == "darwin":
                    # Sur macOS, utiliser une approche différente
                    self.root.update_idletasks()
                    self.root.after(100, lambda: self.root.update())
                else:
                    self.root.update()
                
                messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de copier: {e}")
        else:
            messagebox.showwarning("Attention", "Aucun mot de passe à copier.")
    
    def on_password_change(self, event=None):
        """Appelé quand le mot de passe de test change"""
        # Analyser automatiquement après une pause
        self.root.after(500, self.analyze_password)
    
    def analyze_password(self):
        """Analyse la force du mot de passe"""
        password = self.test_var.get()
        if not password:
            return
        
        # Analyse simple de la force
        score = 0
        feedback = []
        
        # Longueur
        if len(password) >= 12:
            score += 2
            feedback.append("✓ Longueur excellente (12+ caractères)")
        elif len(password) >= 8:
            score += 1
            feedback.append("✓ Longueur correcte (8+ caractères)")
        else:
            feedback.append("✗ Longueur insuffisante (moins de 8 caractères)")
        
        # Types de caractères
        if any(c.islower() for c in password):
            score += 1
            feedback.append("✓ Contient des minuscules")
        
        if any(c.isupper() for c in password):
            score += 1
            feedback.append("✓ Contient des majuscules")
        
        if any(c.isdigit() for c in password):
            score += 1
            feedback.append("✓ Contient des chiffres")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
            feedback.append("✓ Contient des caractères spéciaux")
        
        # Évaluation finale
        if score >= 5:
            strength = "Très fort"
            color = "green"
        elif score >= 3:
            strength = "Fort"
            color = "orange"
        elif score >= 2:
            strength = "Moyen"
            color = "yellow"
        else:
            strength = "Faible"
            color = "red"
        
        # Afficher les résultats
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        
        self.analysis_text.insert(tk.END, f"Force du mot de passe: {strength}\n\n")
        self.analysis_text.insert(tk.END, f"Score: {score}/6\n\n")
        
        for item in feedback:
            self.analysis_text.insert(tk.END, f"{item}\n")
        
        self.analysis_text.config(state=tk.DISABLED)
    
    def on_quit(self):
        """Gestionnaire de fermeture pour macOS"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Lance l'application"""
        print("Starting SecurePassGen...")
        
        # Configuration spéciale pour macOS
        if sys.platform == "darwin":
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.root.update()
        
        print("Application ready!")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted")
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            print("Application closed")

def check_dependencies():
    """Vérifie les dépendances système"""
    try:
        # Vérifier Tkinter
        import tkinter
        return True
    except ImportError:
        print("❌ Tkinter n'est pas disponible")
        return False

def main():
    """Fonction principale avec gestion d'erreurs améliorée"""
    print("🚀 Initialisation de SecurePassGen...")
    print(f"📱 Système détecté: {platform.system()} {platform.release()}")
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Dépendances manquantes. Veuillez installer Tkinter.")
        return 1
    
    try:
        # Configuration spécifique macOS
        if platform.system() == "Darwin":
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
        
        app = SecurePassGenApp()
        print("✅ Application initialisée avec succès")
        print("🎯 Lancement de l'interface graphique...")
        
        app.run()
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
        return 0
    except Exception as e:
        error_msg = f"Erreur lors de l'initialisation: {e}"
        print(f"❌ {error_msg}")
        
        # Afficher l'erreur dans une boîte de dialogue si possible
        try:
            messagebox.showerror("Erreur Fatale", f"Impossible de démarrer l'application:\n{e}")
        except:
            pass
        
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
