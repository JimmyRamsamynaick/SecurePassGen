"""
Générateur de mots de passe sécurisé avec algorithmes cryptographiques.
"""

import secrets
import string
import random
from typing import List, Dict, Optional

class PasswordGenerator:
    """
    Générateur de mots de passe sécurisé utilisant des algorithmes cryptographiques.
    """
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous_chars = "0O1lI"
        
    def generate_password(self, 
                         length: int = 12,
                         use_lowercase: bool = True,
                         use_uppercase: bool = True,
                         use_digits: bool = True,
                         use_special: bool = True,
                         exclude_ambiguous: bool = False,
                         custom_chars: str = "") -> str:
        """
        Génère un mot de passe sécurisé selon les critères spécifiés.
        
        Args:
            length: Longueur du mot de passe (minimum 4)
            use_lowercase: Inclure les minuscules
            use_uppercase: Inclure les majuscules
            use_digits: Inclure les chiffres
            use_special: Inclure les caractères spéciaux
            exclude_ambiguous: Exclure les caractères ambigus
            custom_chars: Caractères personnalisés à inclure
            
        Returns:
            Mot de passe généré
            
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        if length < 4:
            raise ValueError("La longueur minimale est de 4 caractères")
            
        # Construction du jeu de caractères
        charset = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            charset += chars
            required_chars.append(secrets.choice(chars))
            
        if use_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            charset += chars
            required_chars.append(secrets.choice(chars))
            
        if use_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            charset += chars
            required_chars.append(secrets.choice(chars))
            
        if use_special:
            charset += self.special_chars
            required_chars.append(secrets.choice(self.special_chars))
            
        if custom_chars:
            charset += custom_chars
            
        if not charset:
            raise ValueError("Au moins un type de caractère doit être sélectionné")
            
        # Génération du mot de passe
        password_chars = required_chars.copy()
        
        # Compléter avec des caractères aléatoires
        for _ in range(length - len(required_chars)):
            password_chars.append(secrets.choice(charset))
            
        # Mélanger les caractères de manière sécurisée
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_passphrase(self, 
                           word_count: int = 4,
                           separator: str = "-",
                           capitalize: bool = True,
                           add_numbers: bool = True) -> str:
        """
        Génère une phrase de passe mémorable.
        
        Args:
            word_count: Nombre de mots
            separator: Séparateur entre les mots
            capitalize: Capitaliser les mots
            add_numbers: Ajouter des chiffres
            
        Returns:
            Phrase de passe générée
        """
        # Liste de mots courants (version simplifiée)
        words = [
            "apple", "banana", "cherry", "dragon", "eagle", "forest", "guitar", "house",
            "island", "jungle", "kitten", "lemon", "mountain", "ocean", "piano", "queen",
            "river", "sunset", "tiger", "umbrella", "violet", "wizard", "yellow", "zebra",
            "bridge", "castle", "diamond", "elephant", "flower", "garden", "harmony", "ice",
            "journey", "kingdom", "liberty", "melody", "nature", "orange", "paradise", "quiet",
            "rainbow", "silver", "thunder", "universe", "victory", "wisdom", "crystal", "dream"
        ]
        
        selected_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            if capitalize:
                word = word.capitalize()
            selected_words.append(word)
            
        passphrase = separator.join(selected_words)
        
        if add_numbers:
            # Ajouter 2-3 chiffres à la fin
            numbers = ''.join(secrets.choice(self.digits) for _ in range(secrets.randbelow(2) + 2))
            passphrase += separator + numbers
            
        return passphrase
    
    def generate_multiple(self, count: int, **kwargs) -> List[str]:
        """
        Génère plusieurs mots de passe.
        
        Args:
            count: Nombre de mots de passe à générer
            **kwargs: Arguments pour generate_password
            
        Returns:
            Liste de mots de passe
        """
        return [self.generate_password(**kwargs) for _ in range(count)]
