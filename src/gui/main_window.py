"""
Interface graphique principale de SecurePassGen.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
from pathlib import Path
import sys
import platform

# Import des modules locaux
sys.path.append(str(Path(__file__).parent.parent))
from core.password_generator import PasswordGenerator
from core.password_strength import PasswordStrengthAnalyzer
from utils.file_manager import PasswordFileManager

class SecurePassGenApp:
    """
    Application principale SecurePassGen.
    """
    
    def __init__(self):
        print("Initializing SecurePassGenApp...")
        self.root = tk.Tk()
        print("✓ Tkinter root created")
        
        self.generator = PasswordGenerator()
        self.analyzer = PasswordStrengthAnalyzer()
        self.file_manager = PasswordFileManager()
        print("✓ Core components initialized")
        
        # Configuration cross-platform
        print("Setting up cross-platform configuration...")
        self.setup_cross_platform()
        print("✓ Cross-platform setup complete")
        
        print("Setting up window...")
        self.setup_window()
        print("✓ Window setup complete")
        
        print("Setting up styles...")
        self.setup_styles()
        print("✓ Styles setup complete")
        
        print("Creating widgets...")
        self.create_widgets()
        print("✓ Widgets created successfully")
        
        print("✓ SecurePassGenApp initialization complete")
        
        # Forcer le rafraîchissement de l'affichage
        self.root.update_idletasks()
        self.root.update()
        print("Application initialization complete!")
        
    def setup_cross_platform(self):
        """Configuration spécifique pour la compatibilité cross-platform."""
        import platform
        import os
        
        system = platform.system()
        
        if system == "Darwin":  # macOS
            # Supprimer l'avertissement de dépréciation Tk
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            
            # Configuration spéciale pour macOS
            try:
                # Forcer l'activation de l'application
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.after_idle(lambda: self.root.attributes('-topmost', False))
                
                # Améliorer le rendu sur macOS
                self.root.tk.call('tk', 'scaling', 1.5)
            except Exception as e:
                print(f"Erreur configuration macOS: {e}")
                
        elif system == "Windows":
            # Améliorer l'apparence sur Windows
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
    
    def setup_window(self):
        """Configure la fenêtre principale."""
        print("  Setting title...")
        self.root.title("🔐 SecurePassGen - Générateur de Mots de Passe Sécurisé")
        
        print("  Setting geometry...")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        print("  Setting background color...")
        self.root.configure(bg='#f0f0f0')
        
        print("  Forcing display...")
        self.root.deiconify()
        self.root.focus_force()
        
        print("  Centering window...")
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            print(f"  Window centered at {x},{y}")
        except Exception as e:
            print(f"  Warning: Could not center window: {e}")
        
        print("  Setting icon...")
        try:
            icon_path = Path(__file__).parent.parent.parent / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"  Warning: Could not set icon: {e}")
            
        print("  Final refresh...")
        try:
            self.root.update()
        except Exception as e:
            print(f"  Warning: Could not update: {e}")
    
    def setup_styles(self):
        """Configure les styles de l'interface."""
        print("Setting up styles...")
        try:
            import platform
            
            style = ttk.Style()
            print("  TTK Style created")
            
            # Sélection du thème selon la plateforme
            available_themes = style.theme_names()
            print(f"  Available themes: {available_themes}")
            
            if platform.system() == "Darwin":  # macOS
                if 'aqua' in available_themes:
                    style.theme_use('aqua')
                    print("  Using 'aqua' theme")
                elif 'clam' in available_themes:
                    style.theme_use('clam')
                    print("  Using 'clam' theme")
            elif platform.system() == "Windows":
                if 'vista' in available_themes:
                    style.theme_use('vista')
                    print("  Using 'vista' theme")
                elif 'winnative' in available_themes:
                    style.theme_use('winnative')
                    print("  Using 'winnative' theme")
                elif 'clam' in available_themes:
                    style.theme_use('clam')
                    print("  Using 'clam' theme")
            else:  # Linux et autres
                if 'clam' in available_themes:
                    style.theme_use('clam')
                    print("  Using 'clam' theme")
            
            print("  Configuring custom styles...")
            # Couleurs personnalisées
            style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
            style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
            style.configure('Generate.TButton', font=('Arial', 12, 'bold'))
            print("✓ Styles setup complete")
        except Exception as e:
            print(f"  Error in setup_styles: {e}")
            import traceback
            traceback.print_exc()
        
    def create_widgets(self):
        """Crée tous les widgets de l'interface."""
        print("Creating widgets...")
        try:
            print("  Creating main frame...")
            # Frame principal avec scrollbar
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            print("  Configuring grid...")
            # Configuration du grid
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            
            print("  Updating display...")
            # Forcer l'affichage du frame principal
            self.root.update_idletasks()
            
            row = 0
            
            print("  Creating title...")
            # Titre
            title_label = ttk.Label(main_frame, text="🔐 SecurePassGen", style='Title.TLabel')
            title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
            row += 1
            
            print("  Title created successfully")
            
            # Section Configuration
            config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuration", padding="15")
            config_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
            config_frame.columnconfigure(1, weight=1)
            row += 1
        
            # Longueur
            ttk.Label(config_frame, text="Longueur:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
            self.length_var = tk.IntVar(value=12)
            length_spinbox = ttk.Spinbox(config_frame, from_=4, to=128, textvariable=self.length_var, width=10)
            length_spinbox.grid(row=0, column=1, sticky=tk.W)
            
            # Options de caractères
            self.use_lowercase = tk.BooleanVar(value=True)
            self.use_uppercase = tk.BooleanVar(value=True)
            self.use_digits = tk.BooleanVar(value=True)
            self.use_special = tk.BooleanVar(value=True)
            self.exclude_ambiguous = tk.BooleanVar(value=False)
            
            ttk.Checkbutton(config_frame, text="Minuscules (a-z)", variable=self.use_lowercase).grid(row=1, column=0, sticky=tk.W, pady=5)
            ttk.Checkbutton(config_frame, text="Majuscules (A-Z)", variable=self.use_uppercase).grid(row=1, column=1, sticky=tk.W, pady=5)
            ttk.Checkbutton(config_frame, text="Chiffres (0-9)", variable=self.use_digits).grid(row=2, column=0, sticky=tk.W, pady=5)
            ttk.Checkbutton(config_frame, text="Caractères spéciaux", variable=self.use_special).grid(row=2, column=1, sticky=tk.W, pady=5)
            ttk.Checkbutton(config_frame, text="Exclure caractères ambigus (0,O,1,l,I)", variable=self.exclude_ambiguous).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            # Caractères personnalisés
            ttk.Label(config_frame, text="Caractères personnalisés:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
            self.custom_chars_var = tk.StringVar()
            custom_entry = ttk.Entry(config_frame, textvariable=self.custom_chars_var, width=30)
            custom_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(10, 5))
        
            # Section Génération
            gen_frame = ttk.LabelFrame(main_frame, text="🎲 Génération", padding="15")
            gen_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
            gen_frame.columnconfigure(1, weight=1)
            row += 1
            
            # Boutons de génération
            button_frame = ttk.Frame(gen_frame)
            button_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15))
            
            ttk.Button(button_frame, text="🎲 Générer Mot de Passe", command=self.generate_password, style='Generate.TButton').pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="📝 Générer Phrase de Passe", command=self.generate_passphrase).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="🔄 Générer Plusieurs", command=self.generate_multiple).pack(side=tk.LEFT)
            
            # Zone de résultat
            ttk.Label(gen_frame, text="Résultat:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
            
            result_frame = ttk.Frame(gen_frame)
            result_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
            result_frame.columnconfigure(0, weight=1)
            
            self.result_var = tk.StringVar()
            self.result_entry = ttk.Entry(result_frame, textvariable=self.result_var, font=('Courier', 12), state='readonly')
            self.result_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
            
            ttk.Button(result_frame, text="📋 Copier", command=self.copy_to_clipboard).grid(row=0, column=1)
        
            # Section Analyse
            analysis_frame = ttk.LabelFrame(main_frame, text="📊 Analyse de Force", padding="15")
            analysis_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
            analysis_frame.columnconfigure(1, weight=1)
            row += 1
            
            # Zone de test
            ttk.Label(analysis_frame, text="Tester un mot de passe:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
            
            test_frame = ttk.Frame(analysis_frame)
            test_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
            test_frame.columnconfigure(0, weight=1)
            
            self.test_var = tk.StringVar()
            self.test_entry = ttk.Entry(test_frame, textvariable=self.test_var, show="*")
            self.test_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
            self.test_entry.bind('<KeyRelease>', self.on_password_change)
            
            self.show_password_var = tk.BooleanVar()
            ttk.Checkbutton(test_frame, text="👁️ Afficher", variable=self.show_password_var, command=self.toggle_password_visibility).grid(row=0, column=1, padx=(0, 10))
            
            ttk.Button(test_frame, text="🔍 Analyser", command=self.analyze_password).grid(row=0, column=2)
            
            # Résultats d'analyse
            self.analysis_text = tk.Text(analysis_frame, height=8, wrap=tk.WORD, font=('Arial', 10))
            self.analysis_text.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
            
            # Scrollbar pour l'analyse
            analysis_scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=self.analysis_text.yview)
            analysis_scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S))
            self.analysis_text.configure(yscrollcommand=analysis_scrollbar.set)
            
            # Section Sauvegarde
            save_frame = ttk.LabelFrame(main_frame, text="💾 Sauvegarde", padding="15")
            save_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E))
            row += 1
            
            save_button_frame = ttk.Frame(save_frame)
            save_button_frame.grid(row=0, column=0, columnspan=3)
        
            ttk.Button(save_button_frame, text="💾 Sauvegarder", command=self.save_password).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(save_button_frame, text="📂 Charger", command=self.load_passwords).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(save_button_frame, text="📋 Voir Sauvegardés", command=self.view_saved_passwords).pack(side=tk.LEFT)
            
            # Finaliser l'affichage
            self.root.update_idletasks()
            self.root.update()
            
        except Exception as e:
            # En cas d'erreur, afficher un message et créer une interface minimale
            messagebox.showerror("Erreur d'initialisation", f"Erreur lors de la création de l'interface: {e}")
            self._create_minimal_interface()
        
    def _create_minimal_interface(self):
        """Crée une interface minimale en cas d'erreur."""
        try:
            # Interface de secours
            fallback_frame = tk.Frame(self.root, bg='#f0f0f0')
            fallback_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            tk.Label(fallback_frame, text="🔐 SecurePassGen", font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=10)
            tk.Label(fallback_frame, text="Interface de secours - Fonctionnalités limitées", bg='#f0f0f0').pack(pady=5)
            
            # Génération simple
            self.simple_result = tk.StringVar()
            tk.Entry(fallback_frame, textvariable=self.simple_result, width=50, font=('Courier', 12)).pack(pady=10)
            tk.Button(fallback_frame, text="Générer Mot de Passe", command=self._simple_generate).pack(pady=5)
            
        except Exception:
            # Dernière tentative avec Tkinter basique
            tk.Label(self.root, text="Erreur critique - Redémarrez l'application").pack()
    
    def _simple_generate(self):
        """Génération simple pour l'interface de secours."""
        try:
            import secrets
            import string
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(chars) for _ in range(12))
            self.simple_result.set(password)
        except Exception:
            self.simple_result.set("Erreur de génération")
    
    def generate_password(self):
        """Génère un nouveau mot de passe."""
        try:
            password = self.generator.generate_password(
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_digits=self.use_digits.get(),
                use_special=self.use_special.get(),
                exclude_ambiguous=self.exclude_ambiguous.get(),
                custom_chars=self.custom_chars_var.get()
            )
            self.result_var.set(password)
            self.test_var.set(password)
            self.analyze_password()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {e}")
    
    def generate_passphrase(self):
        """Génère une phrase de passe."""
        try:
            passphrase = self.generator.generate_passphrase()
            self.result_var.set(passphrase)
            self.test_var.set(passphrase)
            self.analyze_password()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {e}")
    
    def generate_multiple(self):
        """Génère plusieurs mots de passe."""
        try:
            passwords = self.generator.generate_multiple(
                count=5,
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_digits=self.use_digits.get(),
                use_special=self.use_special.get(),
                exclude_ambiguous=self.exclude_ambiguous.get(),
                custom_chars=self.custom_chars_var.get()
            )
            
            # Afficher dans une nouvelle fenêtre
            self.show_multiple_passwords(passwords)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {e}")
    
    def show_multiple_passwords(self, passwords):
        """Affiche plusieurs mots de passe dans une nouvelle fenêtre."""
        window = tk.Toplevel(self.root)
        window.title("🔄 Mots de Passe Multiples")
        window.geometry("600x400")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Mots de passe générés:", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=('Courier', 11))
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        for i, password in enumerate(passwords, 1):
            analysis = self.analyzer.analyze_password(password)
            text_widget.insert(tk.END, f"{i}. {password}\n")
            text_widget.insert(tk.END, f"   Force: {analysis['strength']} (Score: {analysis['score']}/100)\n\n")
        
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(frame, text="📋 Copier Tout", command=lambda: pyperclip.copy('\n'.join(passwords))).pack()
    
    def copy_to_clipboard(self):
        """Copie le résultat dans le presse-papiers."""
        password = self.result_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers !")
        else:
            messagebox.showwarning("Attention", "Aucun mot de passe à copier.")
    
    def toggle_password_visibility(self):
        """Bascule la visibilité du mot de passe."""
        if self.show_password_var.get():
            self.test_entry.config(show="")
        else:
            self.test_entry.config(show="*")
    
    def on_password_change(self, event=None):
        """Appelé quand le mot de passe de test change."""
        # Auto-analyse après une courte pause
        self.root.after(500, self.analyze_password)
    
    def analyze_password(self):
        """Analyse le mot de passe de test."""
        password = self.test_var.get()
        if not password:
            self.analysis_text.delete(1.0, tk.END)
            return
        
        analysis = self.analyzer.analyze_password(password)
        
        # Effacer le texte précédent
        self.analysis_text.delete(1.0, tk.END)
        
        # Afficher les résultats
        self.analysis_text.insert(tk.END, f"🔍 ANALYSE DU MOT DE PASSE\n")
        self.analysis_text.insert(tk.END, f"{'='*50}\n\n")
        
        # Force et score
        strength_color = self.get_strength_color(analysis['strength'])
        self.analysis_text.insert(tk.END, f"💪 Force: {analysis['strength']}\n")
        self.analysis_text.insert(tk.END, f"📊 Score: {analysis['score']}/100\n")
        self.analysis_text.insert(tk.END, f"🔢 Entropie: {analysis['entropy']} bits\n")
        self.analysis_text.insert(tk.END, f"⏱️ Temps de crack estimé: {analysis['time_to_crack']}\n\n")
        
        # Feedback
        if analysis['feedback']:
            self.analysis_text.insert(tk.END, f"💡 RECOMMANDATIONS:\n")
            for feedback in analysis['feedback']:
                self.analysis_text.insert(tk.END, f"• {feedback}\n")
        
        self.analysis_text.config(state=tk.DISABLED)
    
    def get_strength_color(self, strength):
        """Retourne une couleur basée sur la force."""
        colors = {
            "Très faible": "#e74c3c",
            "Faible": "#f39c12",
            "Moyen": "#f1c40f",
            "Fort": "#27ae60",
            "Très fort": "#2ecc71"
        }
        return colors.get(strength, "#34495e")
    
    def save_password(self):
        """Sauvegarde le mot de passe actuel."""
        password = self.result_var.get()
        if not password:
            messagebox.showwarning("Attention", "Aucun mot de passe à sauvegarder.")
            return
        
        # Demander un nom/description
        name = tk.simpledialog.askstring("Sauvegarde", "Nom/Description pour ce mot de passe:")
        if name:
            try:
                self.file_manager.save_password(name, password)
                messagebox.showinfo("Succès", "Mot de passe sauvegardé avec succès !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def load_passwords(self):
        """Charge les mots de passe sauvegardés."""
        try:
            passwords = self.file_manager.load_passwords()
            if passwords:
                self.show_saved_passwords(passwords)
            else:
                messagebox.showinfo("Information", "Aucun mot de passe sauvegardé trouvé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
    
    def view_saved_passwords(self):
        """Affiche les mots de passe sauvegardés."""
        self.load_passwords()
    
    def show_saved_passwords(self, passwords):
        """Affiche les mots de passe sauvegardés dans une nouvelle fenêtre."""
        window = tk.Toplevel(self.root)
        window.title("💾 Mots de Passe Sauvegardés")
        window.geometry("700x500")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Mots de passe sauvegardés:", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Treeview pour afficher les mots de passe
        columns = ('Name', 'Password', 'Date')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        tree.heading('Name', text='Nom/Description')
        tree.heading('Password', text='Mot de passe')
        tree.heading('Date', text='Date de création')
        
        tree.column('Name', width=200)
        tree.column('Password', width=300)
        tree.column('Date', width=150)
        
        for entry in passwords:
            tree.insert('', tk.END, values=(entry['name'], entry['password'], entry['date']))
        
        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Boutons
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        def copy_selected():
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                password = item['values'][1]
                pyperclip.copy(password)
                messagebox.showinfo("Succès", "Mot de passe copié !")
        
        ttk.Button(button_frame, text="📋 Copier Sélectionné", command=copy_selected).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Supprimer Tout", command=lambda: self.clear_saved_passwords(window)).pack(side=tk.LEFT)
    
    def clear_saved_passwords(self, parent_window):
        """Supprime tous les mots de passe sauvegardés."""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer tous les mots de passe sauvegardés ?"):
            try:
                self.file_manager.clear_passwords()
                messagebox.showinfo("Succès", "Tous les mots de passe ont été supprimés.")
                parent_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def run(self):
        """Lance l'application."""
        try:
            print("Starting application run...")
            
            # Configuration spéciale pour macOS
            if sys.platform == "darwin":
                print("Applying macOS-specific configuration...")
                # Éviter la destruction automatique sur macOS
                self.root.createcommand('::tk::mac::Quit', self.root.quit)
                
                # Forcer l'affichage
                self.root.deiconify()
                self.root.lift()
                self.root.focus_force()
                
                # Attendre un peu avant de continuer
                self.root.after(100, self._delayed_start)
            else:
                self._force_display()
                self.root.mainloop()
                
        except Exception as e:
            print(f"Error in run: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution: {e}")
    
    def _delayed_start(self):
        """Démarre l'application avec un délai pour macOS."""
        try:
            print("Starting delayed mainloop...")
            self.root.mainloop()
        except Exception as e:
            print(f"Error in delayed start: {e}")
        
    def _force_display(self):
        """Force l'affichage de la fenêtre."""
        try:
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.after(100, lambda: self.root.attributes('-topmost', False))
            self.root.focus_force()
            self.root.update()
        except Exception as e:
            print(f"Erreur lors du forçage d'affichage: {e}")
