#!/usr/bin/env python3
"""
SecurePassGen - Lanceur Universel
Détecte automatiquement le système d'exploitation et lance l'interface appropriée
"""

import sys
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox
import webbrowser
import time
import threading
from pathlib import Path

class SecurePassGenLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_executable = sys.executable
        self.base_dir = Path(__file__).parent
        
    def check_dependencies(self):
        """Vérifie si les dépendances sont installées"""
        try:
            import flask
            return True
        except ImportError:
            return False
    
    def install_dependencies(self):
        """Installe les dépendances manquantes"""
        print("📦 Installation des dépendances...")
        try:
            subprocess.check_call([
                self.python_executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Dépendances installées avec succès!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation: {e}")
            return False
    
    def test_tkinter(self):
        """Teste si Tkinter fonctionne correctement"""
        try:
            # Test simple de création de fenêtre
            root = tk.Tk()
            root.withdraw()  # Cache la fenêtre
            
            # Test spécifique pour macOS
            if self.system == "darwin":
                try:
                    root.tk.call('tk', 'scaling')
                    root.destroy()
                    return True
                except:
                    root.destroy()
                    return False
            else:
                root.destroy()
                return True
                
        except Exception as e:
            print(f"⚠️  Tkinter non disponible: {e}")
            return False
    
    def launch_web_app(self):
        """Lance l'application web Flask"""
        print("🌐 Lancement de l'application web...")
        
        def run_flask():
            try:
                subprocess.run([
                    self.python_executable, 
                    str(self.base_dir / "web_app.py")
                ])
            except Exception as e:
                print(f"❌ Erreur lors du lancement web: {e}")
        
        # Lancer Flask dans un thread séparé
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Attendre que le serveur démarre
        time.sleep(3)
        
        # Ouvrir le navigateur
        try:
            webbrowser.open("http://localhost:8080")
            print("🚀 Application web lancée sur http://localhost:8080")
            return True
        except Exception as e:
            print(f"❌ Erreur ouverture navigateur: {e}")
            return False
    
    def launch_desktop_app(self):
        """Lance l'application desktop Tkinter"""
        print("🖥️  Lancement de l'application desktop...")
        
        try:
            if self.system == "darwin":
                # Configuration spéciale pour macOS
                env = {**subprocess.os.environ, 'TK_SILENCE_DEPRECATION': '1'}
                subprocess.run([
                    self.python_executable,
                    str(self.base_dir / "main.py")
                ], env=env)
            else:
                # Windows et Linux
                subprocess.run([
                    self.python_executable,
                    str(self.base_dir / "main.py")
                ])
            return True
        except Exception as e:
            print(f"❌ Erreur lors du lancement desktop: {e}")
            return False
    
    def show_launcher_gui(self):
        """Affiche une interface de sélection"""
        try:
            root = tk.Tk()
            root.title("SecurePassGen - Lanceur")
            root.geometry("400x300")
            root.resizable(False, False)
            
            # Centrer la fenêtre
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (400 // 2)
            y = (root.winfo_screenheight() // 2) - (300 // 2)
            root.geometry(f"400x300+{x}+{y}")
            
            # Interface
            tk.Label(root, text="🔐 SecurePassGen", 
                    font=('Arial', 18, 'bold')).pack(pady=20)
            
            tk.Label(root, text="Choisissez votre mode de lancement:", 
                    font=('Arial', 12)).pack(pady=10)
            
            # Informations système
            system_info = f"Système: {platform.system()} {platform.release()}"
            tk.Label(root, text=system_info, 
                    font=('Arial', 10), fg='gray').pack(pady=5)
            
            # Boutons
            button_frame = tk.Frame(root)
            button_frame.pack(pady=20)
            
            def launch_web():
                root.destroy()
                self.launch_web_app()
            
            def launch_desktop():
                root.destroy()
                self.launch_desktop_app()
            
            tk.Button(button_frame, text="🌐 Application Web\n(Recommandé)", 
                     command=launch_web, width=15, height=3,
                     bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
            
            tk.Button(button_frame, text="🖥️ Application Desktop\n(Tkinter)", 
                     command=launch_desktop, width=15, height=3,
                     bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
            
            # Note
            note_text = "Note: L'application web fonctionne sur tous les systèmes\net offre la meilleure expérience utilisateur."
            tk.Label(root, text=note_text, 
                    font=('Arial', 9), fg='gray', wraplength=350).pack(pady=20)
            
            root.mainloop()
            
        except Exception as e:
            print(f"❌ Erreur interface lanceur: {e}")
            # Fallback vers le mode console
            self.console_launcher()
    
    def console_launcher(self):
        """Lanceur en mode console"""
        print("\n🔐 SecurePassGen - Lanceur")
        print("=" * 40)
        print(f"Système détecté: {platform.system()} {platform.release()}")
        print("\nModes disponibles:")
        print("1. 🌐 Application Web (Recommandé)")
        print("2. 🖥️  Application Desktop (Tkinter)")
        print("3. ❌ Quitter")
        
        while True:
            try:
                choice = input("\nVotre choix (1-3): ").strip()
                
                if choice == "1":
                    self.launch_web_app()
                    break
                elif choice == "2":
                    if self.test_tkinter():
                        self.launch_desktop_app()
                    else:
                        print("❌ Tkinter non disponible. Lancement de l'application web...")
                        self.launch_web_app()
                    break
                elif choice == "3":
                    print("👋 Au revoir!")
                    break
                else:
                    print("❌ Choix invalide. Veuillez entrer 1, 2 ou 3.")
                    
            except KeyboardInterrupt:
                print("\n👋 Au revoir!")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
    
    def run(self):
        """Point d'entrée principal"""
        print("🚀 SecurePassGen - Lanceur Universel")
        print(f"📱 Système: {platform.system()} {platform.release()}")
        
        # Vérifier les dépendances
        if not self.check_dependencies():
            print("📦 Dépendances manquantes détectées.")
            if input("Installer automatiquement? (o/N): ").lower().startswith('o'):
                if not self.install_dependencies():
                    print("❌ Impossible d'installer les dépendances.")
                    return
            else:
                print("❌ Dépendances requises non installées.")
                return
        
        # Détecter le meilleur mode de lancement
        if len(sys.argv) > 1:
            mode = sys.argv[1].lower()
            if mode == "web":
                self.launch_web_app()
            elif mode == "desktop":
                self.launch_desktop_app()
            elif mode == "console":
                self.console_launcher()
            else:
                print(f"❌ Mode inconnu: {mode}")
                print("Modes disponibles: web, desktop, console")
        else:
            # Mode automatique
            if self.test_tkinter():
                try:
                    self.show_launcher_gui()
                except:
                    self.console_launcher()
            else:
                print("⚠️  Interface graphique non disponible.")
                self.console_launcher()

def main():
    """Fonction principale"""
    try:
        launcher = SecurePassGenLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur.")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()