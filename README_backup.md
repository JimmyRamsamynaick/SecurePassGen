# 🔐 SecurePassGen

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Pytest-orange.svg)](tests/)
[![Security](https://img.shields.io/badge/Security-AES--256-red.svg)](src/utils/file_manager.py)

**SecurePassGen** est un générateur de mots de passe sécurisé avec interface graphique moderne, conçu pour créer, analyser et gérer vos mots de passe en toute sécurité.

## ✨ Fonctionnalités

### 🎯 Génération de Mots de Passe
- **Algorithmes cryptographiques sécurisés** utilisant le module `secrets`
- **Personnalisation complète** : longueur, types de caractères, exclusions
- **Génération de phrases de passe** mémorables
- **Génération multiple** pour comparer les options
- **Exclusion des caractères ambigus** (0, O, 1, l, I)

### 📊 Analyse de Force
- **Évaluation en temps réel** de la force des mots de passe
- **Calcul d'entropie** et estimation du temps de crack
- **Détection de patterns** et mots de passe communs
- **Recommandations personnalisées** pour l'amélioration

### 💾 Gestion Sécurisée
- **Chiffrement AES-256** pour le stockage local
- **Protection par mot de passe maître**
- **Sauvegarde et restauration** des données
- **Import/Export** sécurisé
- **Recherche et organisation** des mots de passe

### 🖥️ Interface Utilisateur
- **Interface graphique moderne** avec Tkinter
- **Copie automatique** dans le presse-papiers
- **Thème sombre/clair** adaptatif
- **Notifications** et feedback utilisateur
- **Raccourcis clavier** pour une utilisation rapide

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/JimmyRamsamynaick/SecurePassGen.git
cd SecurePassGen

# Installer les dépendances
pip install -r requirements.txt
```

### Installation en mode développement

```bash
# Installer les dépendances de développement
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

## 🎮 Utilisation

### Lancement de l'application

```bash
python main.py
```

### Utilisation en ligne de commande

```python
from src.core.password_generator import PasswordGenerator
from src.core.password_strength import PasswordStrengthAnalyzer

# Générer un mot de passe
generator = PasswordGenerator()
password = generator.generate_password(length=16, use_special=True)
print(f"Mot de passe généré : {password}")

# Analyser la force
analyzer = PasswordStrengthAnalyzer()
result = analyzer.analyze_password(password)
print(f"Force : {result['strength']} (Score: {result['score']}/100)")
```

### Exemples d'utilisation

#### Génération de mots de passe personnalisés

```python
# Mot de passe pour un site web
web_password = generator.generate_password(
    length=12,
    use_lowercase=True,
    use_uppercase=True,
    use_digits=True,
    use_special=True,
    exclude_ambiguous=True
)

# Phrase de passe mémorable
passphrase = generator.generate_passphrase(
    word_count=4,
    separator="-",
    capitalize=True,
    add_numbers=True
)
```

#### Sauvegarde sécurisée

```python
from src.utils.file_manager import PasswordFileManager

manager = PasswordFileManager("my_passwords.json")

# Sauvegarder un mot de passe
manager.save_password(
    site="example.com",
    username="user@example.com",
    password=web_password,
    master_password="mon_mot_de_passe_maitre",
    notes="Compte principal"
)

# Charger les mots de passe
passwords = manager.load_passwords("mon_mot_de_passe_maitre")
```

## 🏗️ Architecture

```
SecurePassGen/
├── main.py                 # Point d'entrée de l'application
├── src/
│   ├── core/
│   │   ├── password_generator.py    # Génération de mots de passe
│   │   └── password_strength.py     # Analyse de force
│   ├── gui/
│   │   └── main_window.py          # Interface graphique
│   └── utils/
│       └── file_manager.py         # Gestion des fichiers
├── tests/
│   ├── test_password_generator.py  # Tests du générateur
│   └── test_file_manager.py        # Tests du gestionnaire
├── docs/                   # Documentation
├── assets/                 # Ressources (icônes, images)
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 🧪 Tests

### Exécution des tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_password_generator.py -v
```

### Couverture de code

Le projet vise une couverture de code de 90%+ avec des tests unitaires complets pour :
- Génération de mots de passe
- Analyse de force
- Chiffrement/déchiffrement
- Gestion des fichiers
- Interface utilisateur

## 🔒 Sécurité

### Mesures de sécurité implémentées

- **Génération cryptographique** : Utilisation du module `secrets` de Python
- **Chiffrement AES-256** : Protection des données stockées
- **Dérivation de clé PBKDF2** : Renforcement du mot de passe maître
- **Effacement sécurisé** : Nettoyage de la mémoire après utilisation
- **Validation d'entrée** : Protection contre les injections

### Bonnes pratiques

- Ne jamais stocker le mot de passe maître en plain text
- Utiliser des mots de passe uniques pour chaque service
- Activer l'authentification à deux facteurs quand possible
- Effectuer des sauvegardes régulières chiffrées

## 🛠️ Développement

### Configuration de l'environnement

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances de développement
pip install -r requirements.txt
```

### Standards de code

```bash
# Formatage du code
black src/ tests/

# Vérification du style
flake8 src/ tests/

# Vérification des types
mypy src/
```

### Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📋 Roadmap

### Version 1.1
- [ ] Support des gestionnaires de mots de passe externes
- [ ] Synchronisation cloud sécurisée
- [ ] Plugin navigateur
- [ ] Application mobile

### Version 1.2
- [ ] Authentification biométrique
- [ ] Audit de sécurité automatisé
- [ ] Partage sécurisé de mots de passe
- [ ] Intégration avec des services d'authentification

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Jimmy Ramsamynaick** - *Développeur principal* - [GitHub](https://github.com/JimmyRamsamynaick)

## 🙏 Remerciements

- Communauté Python pour les excellentes bibliothèques
- Contributeurs et testeurs
- Experts en sécurité pour les recommandations

## 📞 Support

Pour toute question ou problème :
- Ouvrir une [issue](https://github.com/JimmyRamsamynaick/SecurePassGen/issues)
- Consulter la [documentation](docs/)
- Contacter l'équipe de développement

---

**⚠️ Avertissement de sécurité** : Bien que SecurePassGen utilise des pratiques de sécurité robustes, aucun logiciel n'est parfait. Utilisez toujours des pratiques de sécurité appropriées et maintenez vos systèmes à jour.
