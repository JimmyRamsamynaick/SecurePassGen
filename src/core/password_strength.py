"""
Évaluateur de force des mots de passe.
"""

import re
import math
from typing import Dict, List, Tuple

class PasswordStrengthAnalyzer:
    """
    Analyse la force et la sécurité des mots de passe.
    """
    
    def __init__(self):
        # Mots de passe communs à éviter
        self.common_passwords = {
            "password", "123456", "password123", "admin", "qwerty", 
            "letmein", "welcome", "monkey", "1234567890", "abc123",
            "password1", "123456789", "welcome123", "admin123"
        }
        
        # Patterns dangereux
        self.dangerous_patterns = [
            r'(.)\1{2,}',  # Répétitions
            r'(012|123|234|345|456|567|678|789|890)',  # Séquences numériques
            r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Séquences alphabétiques
            r'(qwe|wer|ert|rty|tyu|yui|uio|iop|asd|sdf|dfg|fgh|ghj|hjk|jkl|zxc|xcv|cvb|vbn|bnm)'  # Patterns clavier
        ]
    
    def analyze_password(self, password: str) -> Dict:
        """
        Analyse complète d'un mot de passe.
        
        Args:
            password: Mot de passe à analyser
            
        Returns:
            Dictionnaire avec les résultats d'analyse
        """
        if not password:
            return {
                'score': 0,
                'strength': 'Très faible',
                'feedback': ['Le mot de passe ne peut pas être vide'],
                'entropy': 0,
                'time_to_crack': '0 secondes'
            }
        
        score = 0
        feedback = []
        
        # Analyse de la longueur
        length_score, length_feedback = self._analyze_length(password)
        score += length_score
        feedback.extend(length_feedback)
        
        # Analyse de la complexité
        complexity_score, complexity_feedback = self._analyze_complexity(password)
        score += complexity_score
        feedback.extend(complexity_feedback)
        
        # Analyse des patterns
        pattern_score, pattern_feedback = self._analyze_patterns(password)
        score += pattern_score
        feedback.extend(pattern_feedback)
        
        # Vérification des mots de passe communs
        common_score, common_feedback = self._check_common_passwords(password)
        score += common_score
        feedback.extend(common_feedback)
        
        # Calcul de l'entropie
        entropy = self._calculate_entropy(password)
        
        # Estimation du temps de crack
        time_to_crack = self._estimate_crack_time(entropy)
        
        # Détermination de la force
        strength = self._determine_strength(score)
        
        return {
            'score': min(100, max(0, score)),
            'strength': strength,
            'feedback': feedback if feedback else ['Excellent mot de passe !'],
            'entropy': round(entropy, 2),
            'time_to_crack': time_to_crack
        }
    
    def _analyze_length(self, password: str) -> Tuple[int, List[str]]:
        """Analyse la longueur du mot de passe."""
        length = len(password)
        feedback = []
        
        if length < 8:
            feedback.append('Trop court (minimum 8 caractères recommandé)')
            return 0, feedback
        elif length < 12:
            feedback.append('Longueur acceptable, mais 12+ caractères seraient mieux')
            return 20, feedback
        elif length < 16:
            return 30, feedback
        else:
            return 40, feedback
    
    def _analyze_complexity(self, password: str) -> Tuple[int, List[str]]:
        """Analyse la complexité du mot de passe."""
        score = 0
        feedback = []
        
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        complexity_count = sum([has_lower, has_upper, has_digit, has_special])
        
        if complexity_count == 1:
            feedback.append('Utilisez différents types de caractères')
            score = 5
        elif complexity_count == 2:
            feedback.append('Ajoutez plus de variété dans les caractères')
            score = 15
        elif complexity_count == 3:
            score = 25
        else:
            score = 35
        
        if not has_lower:
            feedback.append('Ajoutez des lettres minuscules')
        if not has_upper:
            feedback.append('Ajoutez des lettres majuscules')
        if not has_digit:
            feedback.append('Ajoutez des chiffres')
        if not has_special:
            feedback.append('Ajoutez des caractères spéciaux')
            
        return score, feedback
    
    def _analyze_patterns(self, password: str) -> Tuple[int, List[str]]:
        """Analyse les patterns dangereux."""
        feedback = []
        penalty = 0
        
        for pattern in self.dangerous_patterns:
            if re.search(pattern, password.lower()):
                feedback.append('Évitez les séquences et répétitions')
                penalty += 10
                break
        
        return -penalty, feedback
    
    def _check_common_passwords(self, password: str) -> Tuple[int, List[str]]:
        """Vérifie si le mot de passe est commun."""
        if password.lower() in self.common_passwords:
            return -50, ['Ce mot de passe est trop commun']
        return 0, []
    
    def _calculate_entropy(self, password: str) -> float:
        """Calcule l'entropie du mot de passe."""
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        return len(password) * math.log2(charset_size)
    
    def _estimate_crack_time(self, entropy: float) -> str:
        """Estime le temps nécessaire pour craquer le mot de passe."""
        if entropy < 30:
            return "Quelques secondes"
        elif entropy < 40:
            return "Quelques minutes"
        elif entropy < 50:
            return "Quelques heures"
        elif entropy < 60:
            return "Quelques jours"
        elif entropy < 70:
            return "Quelques mois"
        elif entropy < 80:
            return "Quelques années"
        else:
            return "Plusieurs siècles"
    
    def _determine_strength(self, score: int) -> str:
        """Détermine la force du mot de passe basée sur le score."""
        if score < 20:
            return "Très faible"
        elif score < 40:
            return "Faible"
        elif score < 60:
            return "Moyen"
        elif score < 80:
            return "Fort"
        else:
            return "Très fort"
