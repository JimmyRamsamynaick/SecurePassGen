"""
Tests unitaires pour le générateur de mots de passe.
"""

import pytest
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.password_generator import PasswordGenerator
from core.password_strength import PasswordStrengthAnalyzer

class TestPasswordGenerator:
    """
    Tests pour la classe PasswordGenerator.
    """
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.generator = PasswordGenerator()
    
    def test_generate_password_default(self):
        """Test de génération avec paramètres par défaut."""
        password = self.generator.generate_password()
        
        assert len(password) == 12
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    def test_generate_password_length(self):
        """Test de génération avec différentes longueurs."""
        for length in [4, 8, 16, 32, 64]:
            password = self.generator.generate_password(length=length)
            assert len(password) == length
    
    def test_generate_password_character_types(self):
        """Test de génération avec différents types de caractères."""
        # Seulement minuscules
        password = self.generator.generate_password(
            use_lowercase=True,
            use_uppercase=False,
            use_digits=False,
            use_special=False
        )
        assert all(c.islower() for c in password)
        
        # Seulement majuscules
        password = self.generator.generate_password(
            use_lowercase=False,
            use_uppercase=True,
            use_digits=False,
            use_special=False
        )
        assert all(c.isupper() for c in password)
        
        # Seulement chiffres
        password = self.generator.generate_password(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=True,
            use_special=False
        )
        assert all(c.isdigit() for c in password)
    
    def test_generate_password_exclude_ambiguous(self):
        """Test d'exclusion des caractères ambigus."""
        password = self.generator.generate_password(
            length=100,  # Longueur élevée pour augmenter les chances
            exclude_ambiguous=True
        )
        
        ambiguous_chars = "0O1lI"
        assert not any(c in ambiguous_chars for c in password)
    
    def test_generate_password_custom_chars(self):
        """Test avec caractères personnalisés."""
        custom_chars = "@#$"
        password = self.generator.generate_password(
            length=50,
            custom_chars=custom_chars
        )
        
        # Au moins un caractère personnalisé devrait être présent
        assert any(c in custom_chars for c in password)
    
    def test_generate_password_invalid_length(self):
        """Test avec longueur invalide."""
        with pytest.raises(ValueError):
            self.generator.generate_password(length=3)
    
    def test_generate_password_no_character_types(self):
        """Test sans aucun type de caractère sélectionné."""
        with pytest.raises(ValueError):
            self.generator.generate_password(
                use_lowercase=False,
                use_uppercase=False,
                use_digits=False,
                use_special=False
            )
    
    def test_generate_passphrase(self):
        """Test de génération de phrase de passe."""
        passphrase = self.generator.generate_passphrase()
        
        # Vérifier la structure (mots séparés par des tirets)
        parts = passphrase.split('-')
        assert len(parts) >= 4  # Au moins 4 mots + potentiellement des chiffres
        
        # Vérifier que les mots sont capitalisés
        for part in parts[:-1]:  # Exclure la dernière partie qui peut être des chiffres
            if part.isalpha():
                assert part[0].isupper()
    
    def test_generate_passphrase_custom_params(self):
        """Test de génération de phrase de passe avec paramètres personnalisés."""
        passphrase = self.generator.generate_passphrase(
            word_count=3,
            separator="_",
            capitalize=False,
            add_numbers=False
        )
        
        parts = passphrase.split('_')
        assert len(parts) == 3
        
        # Vérifier que les mots ne sont pas capitalisés
        for part in parts:
            if part.isalpha():
                assert part.islower()
    
    def test_generate_multiple(self):
        """Test de génération multiple."""
        passwords = self.generator.generate_multiple(count=5, length=10)
        
        assert len(passwords) == 5
        assert all(len(p) == 10 for p in passwords)
        
        # Vérifier que tous les mots de passe sont différents
        assert len(set(passwords)) == 5
    
    def test_password_uniqueness(self):
        """Test d'unicité des mots de passe générés."""
        passwords = [self.generator.generate_password() for _ in range(100)]
        
        # Tous les mots de passe devraient être uniques
        assert len(set(passwords)) == 100


class TestPasswordStrengthAnalyzer:
    """
    Tests pour la classe PasswordStrengthAnalyzer.
    """
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.analyzer = PasswordStrengthAnalyzer()
    
    def test_analyze_empty_password(self):
        """Test avec mot de passe vide."""
        result = self.analyzer.analyze_password("")
        
        assert result['score'] == 0
        assert result['strength'] == 'Très faible'
        assert 'vide' in result['feedback'][0]
    
    def test_analyze_weak_password(self):
        """Test avec mot de passe faible."""
        result = self.analyzer.analyze_password("123")
        
        assert result['score'] < 20
        assert result['strength'] == 'Très faible'
    
    def test_analyze_medium_password(self):
        """Test avec mot de passe moyen."""
        result = self.analyzer.analyze_password("Password123")
        
        assert 40 <= result['score'] < 80
        assert result['strength'] in ['Moyen', 'Fort']
    
    def test_analyze_strong_password(self):
        """Test avec mot de passe fort."""
        result = self.analyzer.analyze_password("MyStr0ng!P@ssw0rd2023")
        
        assert result['score'] >= 60
        assert result['strength'] in ['Fort', 'Très fort']
    
    def test_analyze_common_password(self):
        """Test avec mot de passe commun."""
        result = self.analyzer.analyze_password("password")
        
        assert result['score'] < 50  # Pénalité pour mot de passe commun
        assert any('commun' in feedback for feedback in result['feedback'])
    
    def test_analyze_pattern_password(self):
        """Test avec mot de passe contenant des patterns."""
        result = self.analyzer.analyze_password("aaa123bbb")
        
        # Devrait détecter les répétitions
        assert any('séquence' in feedback.lower() or 'répétition' in feedback.lower() 
                  for feedback in result['feedback'])
    
    def test_entropy_calculation(self):
        """Test du calcul d'entropie."""
        # Mot de passe simple
        result1 = self.analyzer.analyze_password("abc")
        
        # Mot de passe complexe
        result2 = self.analyzer.analyze_password("Abc123!@#")
        
        # Le mot de passe complexe devrait avoir plus d'entropie
        assert result2['entropy'] > result1['entropy']
    
    def test_crack_time_estimation(self):
        """Test de l'estimation du temps de crack."""
        # Mot de passe faible
        result1 = self.analyzer.analyze_password("123")
        
        # Mot de passe fort
        result2 = self.analyzer.analyze_password("MyVeryStr0ng!P@ssw0rd2023WithL0tsOfCh@rs")
        
        # Le temps de crack devrait être différent
        assert result1['time_to_crack'] != result2['time_to_crack']
    
    def test_feedback_generation(self):
        """Test de génération des recommandations."""
        result = self.analyzer.analyze_password("abc")
        
        # Devrait avoir des recommandations
        assert len(result['feedback']) > 0
        assert all(isinstance(feedback, str) for feedback in result['feedback'])
    
    def test_score_bounds(self):
        """Test que le score reste dans les limites."""
        # Test avec différents mots de passe
        test_passwords = [
            "",
            "a",
            "password",
            "MyStr0ng!P@ssw0rd",
            "VeryL0ng@ndC0mpl3xP@ssw0rdW1thM@nyDiff3r3ntCh@r@ct3rs!"
        ]
        
        for password in test_passwords:
            result = self.analyzer.analyze_password(password)
            assert 0 <= result['score'] <= 100


if __name__ == "__main__":
    pytest.main([__file__])
