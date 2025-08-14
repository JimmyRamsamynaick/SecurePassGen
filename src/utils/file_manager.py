"""
Gestionnaire de fichiers pour la sauvegarde sécurisée des mots de passe.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass
from typing import List, Dict, Optional

class PasswordFileManager:
    """
    Gestionnaire pour la sauvegarde et le chargement sécurisé des mots de passe.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.passwords_file = self.data_dir / "passwords.enc"
        self.key_file = self.data_dir / "key.key"
        
    def _generate_key(self, password: str, salt: bytes = None) -> bytes:
        """
        Génère une clé de chiffrement à partir d'un mot de passe.
        
        Args:
            password: Mot de passe maître
            salt: Salt pour la dérivation (généré si None)
            
        Returns:
            Clé de chiffrement
        """
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def _get_master_password(self) -> str:
        """
        Demande le mot de passe maître à l'utilisateur.
        
        Returns:
            Mot de passe maître
        """
        import tkinter as tk
        from tkinter import simpledialog
        
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        
        password = simpledialog.askstring(
            "Mot de passe maître",
            "Entrez votre mot de passe maître pour chiffrer/déchiffrer:",
            show='*'
        )
        
        root.destroy()
        return password or ""
    
    def _encrypt_data(self, data: str) -> bytes:
        """
        Chiffre les données avec le mot de passe maître.
        
        Args:
            data: Données à chiffrer
            
        Returns:
            Données chiffrées
        """
        master_password = self._get_master_password()
        if not master_password:
            raise ValueError("Mot de passe maître requis")
        
        # Générer une nouvelle clé et salt
        key, salt = self._generate_key(master_password)
        
        # Chiffrer les données
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        
        # Combiner salt et données chiffrées
        return salt + encrypted_data
    
    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Déchiffre les données avec le mot de passe maître.
        
        Args:
            encrypted_data: Données chiffrées
            
        Returns:
            Données déchiffrées
        """
        master_password = self._get_master_password()
        if not master_password:
            raise ValueError("Mot de passe maître requis")
        
        # Extraire le salt et les données
        salt = encrypted_data[:16]
        data = encrypted_data[16:]
        
        # Régénérer la clé
        key, _ = self._generate_key(master_password, salt)
        
        # Déchiffrer
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(data)
        
        return decrypted_data.decode()
    
    def save_password(self, name: str, password: str, description: str = "") -> None:
        """
        Sauvegarde un mot de passe de manière sécurisée.
        
        Args:
            name: Nom/identifiant du mot de passe
            password: Mot de passe à sauvegarder
            description: Description optionnelle
        """
        # Charger les mots de passe existants
        try:
            passwords = self.load_passwords()
        except:
            passwords = []
        
        # Ajouter le nouveau mot de passe
        new_entry = {
            "name": name,
            "password": password,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        passwords.append(new_entry)
        
        # Sauvegarder
        data = json.dumps(passwords, indent=2)
        encrypted_data = self._encrypt_data(data)
        
        with open(self.passwords_file, 'wb') as f:
            f.write(encrypted_data)
    
    def load_passwords(self) -> List[Dict]:
        """
        Charge tous les mots de passe sauvegardés.
        
        Returns:
            Liste des mots de passe
        """
        if not self.passwords_file.exists():
            return []
        
        try:
            with open(self.passwords_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self._decrypt_data(encrypted_data)
            passwords = json.loads(decrypted_data)
            
            return passwords
        except Exception as e:
            raise Exception(f"Erreur lors du déchiffrement: {e}")
    
    def delete_password(self, name: str) -> bool:
        """
        Supprime un mot de passe spécifique.
        
        Args:
            name: Nom du mot de passe à supprimer
            
        Returns:
            True si supprimé, False si non trouvé
        """
        passwords = self.load_passwords()
        
        # Filtrer le mot de passe à supprimer
        new_passwords = [p for p in passwords if p['name'] != name]
        
        if len(new_passwords) == len(passwords):
            return False  # Pas trouvé
        
        # Sauvegarder la nouvelle liste
        if new_passwords:
            data = json.dumps(new_passwords, indent=2)
            encrypted_data = self._encrypt_data(data)
            
            with open(self.passwords_file, 'wb') as f:
                f.write(encrypted_data)
        else:
            # Supprimer le fichier s'il n'y a plus de mots de passe
            self.passwords_file.unlink(missing_ok=True)
        
        return True
    
    def clear_passwords(self) -> None:
        """
        Supprime tous les mots de passe sauvegardés.
        """
        self.passwords_file.unlink(missing_ok=True)
    
    def export_passwords(self, export_path: str, include_passwords: bool = False) -> None:
        """
        Exporte les mots de passe vers un fichier.
        
        Args:
            export_path: Chemin du fichier d'export
            include_passwords: Inclure les mots de passe en clair
        """
        passwords = self.load_passwords()
        
        if not include_passwords:
            # Masquer les mots de passe
            for entry in passwords:
                entry['password'] = '*' * len(entry['password'])
        
        export_data = {
            "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_passwords": len(passwords),
            "passwords": passwords
        }
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def import_passwords(self, import_path: str) -> int:
        """
        Importe des mots de passe depuis un fichier.
        
        Args:
            import_path: Chemin du fichier d'import
            
        Returns:
            Nombre de mots de passe importés
        """
        with open(import_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        if 'passwords' not in import_data:
            raise ValueError("Format de fichier invalide")
        
        imported_passwords = import_data['passwords']
        existing_passwords = self.load_passwords()
        
        # Fusionner les mots de passe (éviter les doublons par nom)
        existing_names = {p['name'] for p in existing_passwords}
        new_passwords = [p for p in imported_passwords if p['name'] not in existing_names]
        
        if new_passwords:
            all_passwords = existing_passwords + new_passwords
            data = json.dumps(all_passwords, indent=2)
            encrypted_data = self._encrypt_data(data)
            
            with open(self.passwords_file, 'wb') as f:
                f.write(encrypted_data)
        
        return len(new_passwords)
    
    def backup_passwords(self, backup_path: str) -> None:
        """
        Crée une sauvegarde chiffrée des mots de passe.
        
        Args:
            backup_path: Chemin de la sauvegarde
        """
        if self.passwords_file.exists():
            import shutil
            shutil.copy2(self.passwords_file, backup_path)
        else:
            raise FileNotFoundError("Aucun fichier de mots de passe à sauvegarder")
    
    def restore_passwords(self, backup_path: str) -> None:
        """
        Restaure les mots de passe depuis une sauvegarde.
        
        Args:
            backup_path: Chemin de la sauvegarde
        """
        if not Path(backup_path).exists():
            raise FileNotFoundError("Fichier de sauvegarde introuvable")
        
        import shutil
        shutil.copy2(backup_path, self.passwords_file)
    
    def get_statistics(self) -> Dict:
        """
        Retourne des statistiques sur les mots de passe sauvegardés.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            passwords = self.load_passwords()
        except:
            passwords = []
        
        if not passwords:
            return {
                "total": 0,
                "oldest_date": None,
                "newest_date": None,
                "average_length": 0
            }
        
        dates = [datetime.strptime(p['date'], "%Y-%m-%d %H:%M:%S") for p in passwords]
        lengths = [len(p['password']) for p in passwords]
        
        return {
            "total": len(passwords),
            "oldest_date": min(dates).strftime("%Y-%m-%d %H:%M:%S"),
            "newest_date": max(dates).strftime("%Y-%m-%d %H:%M:%S"),
            "average_length": round(sum(lengths) / len(lengths), 1)
        }
