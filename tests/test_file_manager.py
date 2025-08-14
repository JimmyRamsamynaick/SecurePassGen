"""
Tests unitaires pour le gestionnaire de fichiers.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.file_manager import PasswordFileManager

class TestPasswordFileManager:
    """
    Tests pour la classe PasswordFileManager.
    """
    
    def setup_method(self):
        """Configuration avant chaque test."""
        # Créer un fichier temporaire pour les tests
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_passwords.json")
        self.manager = PasswordFileManager(self.test_file)
        self.master_password = "test_master_password"
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_encrypt_decrypt(self):
        """Test de chiffrement et déchiffrement."""
        original_data = "Test data to encrypt"
        
        # Chiffrer
        encrypted = self.manager._encrypt_data(original_data, self.master_password)
        assert encrypted != original_data
        assert isinstance(encrypted, str)
        
        # Déchiffrer
        decrypted = self.manager._decrypt_data(encrypted, self.master_password)
        assert decrypted == original_data
    
    def test_encrypt_decrypt_wrong_password(self):
        """Test de déchiffrement avec mauvais mot de passe."""
        original_data = "Test data to encrypt"
        
        # Chiffrer avec un mot de passe
        encrypted = self.manager._encrypt_data(original_data, self.master_password)
        
        # Essayer de déchiffrer avec un mauvais mot de passe
        with pytest.raises(Exception):  # Devrait lever une exception
            self.manager._decrypt_data(encrypted, "wrong_password")
    
    def test_save_password(self):
        """Test de sauvegarde de mot de passe."""
        password_data = {
            "site": "example.com",
            "username": "user@example.com",
            "password": "secure_password_123",
            "notes": "Test account"
        }
        
        # Sauvegarder
        result = self.manager.save_password(
            password_data["site"],
            password_data["username"],
            password_data["password"],
            self.master_password,
            password_data["notes"]
        )
        
        assert result is True
        assert os.path.exists(self.test_file)
    
    def test_load_passwords(self):
        """Test de chargement des mots de passe."""
        # Sauvegarder d'abord un mot de passe
        self.manager.save_password(
            "example.com",
            "user@example.com",
            "secure_password_123",
            self.master_password,
            "Test account"
        )
        
        # Charger
        passwords = self.manager.load_passwords(self.master_password)
        
        assert len(passwords) == 1
        assert passwords[0]["site"] == "example.com"
        assert passwords[0]["username"] == "user@example.com"
        assert passwords[0]["password"] == "secure_password_123"
        assert passwords[0]["notes"] == "Test account"
    
    def test_load_passwords_wrong_master_password(self):
        """Test de chargement avec mauvais mot de passe maître."""
        # Sauvegarder d'abord un mot de passe
        self.manager.save_password(
            "example.com",
            "user@example.com",
            "secure_password_123",
            self.master_password
        )
        
        # Essayer de charger avec un mauvais mot de passe
        passwords = self.manager.load_passwords("wrong_password")
        assert passwords == []
    
    def test_delete_password(self):
        """Test de suppression de mot de passe."""
        # Sauvegarder plusieurs mots de passe
        self.manager.save_password("site1.com", "user1", "pass1", self.master_password)
        self.manager.save_password("site2.com", "user2", "pass2", self.master_password)
        
        # Supprimer un mot de passe
        passwords = self.manager.load_passwords(self.master_password)
        password_id = passwords[0]["id"]
        
        result = self.manager.delete_password(password_id, self.master_password)
        assert result is True
        
        # Vérifier que le mot de passe a été supprimé
        remaining_passwords = self.manager.load_passwords(self.master_password)
        assert len(remaining_passwords) == 1
        assert remaining_passwords[0]["site"] == "site2.com"
    
    def test_search_passwords(self):
        """Test de recherche de mots de passe."""
        # Sauvegarder plusieurs mots de passe
        self.manager.save_password("gmail.com", "user@gmail.com", "pass1", self.master_password)
        self.manager.save_password("facebook.com", "user@facebook.com", "pass2", self.master_password)
        self.manager.save_password("github.com", "user@github.com", "pass3", self.master_password)
        
        # Rechercher
        results = self.manager.search_passwords("gmail", self.master_password)
        assert len(results) == 1
        assert results[0]["site"] == "gmail.com"
        
        # Recherche avec plusieurs résultats
        results = self.manager.search_passwords("user@", self.master_password)
        assert len(results) == 3
    
    def test_export_import_passwords(self):
        """Test d'export et import de mots de passe."""
        # Sauvegarder des mots de passe
        self.manager.save_password("site1.com", "user1", "pass1", self.master_password)
        self.manager.save_password("site2.com", "user2", "pass2", self.master_password)
        
        # Exporter
        export_file = os.path.join(self.temp_dir, "export.json")
        result = self.manager.export_passwords(export_file, self.master_password)
        assert result is True
        assert os.path.exists(export_file)
        
        # Créer un nouveau gestionnaire et importer
        new_file = os.path.join(self.temp_dir, "new_passwords.json")
        new_manager = PasswordFileManager(new_file)
        
        result = new_manager.import_passwords(export_file, self.master_password)
        assert result is True
        
        # Vérifier que les mots de passe ont été importés
        imported_passwords = new_manager.load_passwords(self.master_password)
        assert len(imported_passwords) == 2
    
    def test_backup_restore(self):
        """Test de sauvegarde et restauration."""
        # Sauvegarder des mots de passe
        self.manager.save_password("site1.com", "user1", "pass1", self.master_password)
        
        # Créer une sauvegarde
        backup_file = os.path.join(self.temp_dir, "backup.json")
        result = self.manager.create_backup(backup_file, self.master_password)
        assert result is True
        assert os.path.exists(backup_file)
        
        # Ajouter un autre mot de passe
        self.manager.save_password("site2.com", "user2", "pass2", self.master_password)
        
        # Restaurer la sauvegarde
        result = self.manager.restore_backup(backup_file, self.master_password)
        assert result is True
        
        # Vérifier que seul le premier mot de passe est présent
        passwords = self.manager.load_passwords(self.master_password)
        assert len(passwords) == 1
        assert passwords[0]["site"] == "site1.com"
    
    def test_get_statistics(self):
        """Test des statistiques."""
        # Sauvegarder des mots de passe
        self.manager.save_password("site1.com", "user1", "weak", self.master_password)
        self.manager.save_password("site2.com", "user2", "StrongP@ssw0rd!", self.master_password)
        
        # Obtenir les statistiques
        stats = self.manager.get_statistics(self.master_password)
        
        assert "total_passwords" in stats
        assert "password_strength" in stats
        assert "creation_dates" in stats
        assert stats["total_passwords"] == 2
    
    def test_file_not_exists(self):
        """Test avec fichier inexistant."""
        non_existent_file = os.path.join(self.temp_dir, "non_existent.json")
        manager = PasswordFileManager(non_existent_file)
        
        # Charger depuis un fichier inexistant devrait retourner une liste vide
        passwords = manager.load_passwords(self.master_password)
        assert passwords == []
    
    @patch('builtins.open', side_effect=PermissionError)
    def test_permission_error(self, mock_file):
        """Test avec erreur de permission."""
        result = self.manager.save_password(
            "site.com", "user", "pass", self.master_password
        )
        assert result is False
    
    def test_invalid_json_file(self):
        """Test avec fichier JSON invalide."""
        # Créer un fichier avec du JSON invalide
        with open(self.test_file, 'w') as f:
            f.write("invalid json content")
        
        # Essayer de charger devrait retourner une liste vide
        passwords = self.manager.load_passwords(self.master_password)
        assert passwords == []


if __name__ == "__main__":
    pytest.main([__file__])
