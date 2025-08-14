# 🔐 SecurePassGen

**Générateur de Mots de Passe Sécurisé Multiplateforme**

Une application moderne et sécurisée pour générer et analyser des mots de passe robustes, disponible en version web et desktop.

> ⚠️ **STATUT ACTUEL** : Seule la version web GitHub Pages est actuellement fonctionnelle.  
> 🌐 **Accès direct** : [https://jimmyramsamynaick.github.io/SecurePassGen/](https://jimmyramsamynaick.github.io/SecurePassGen/)  
> 🚧 **Développement en cours** : Les versions desktop et serveur local sont en cours de développement.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Fonctionnalités

- 🎯 **Génération de mots de passe personnalisables**
  - Longueur ajustable (4-128 caractères)
  - Options: majuscules, minuscules, chiffres, symboles
  - Exclusion de caractères ambigus

- 🔍 **Analyse de robustesse en temps réel**
  - Évaluation de la force du mot de passe
  - Suggestions d'amélioration
  - Indicateurs visuels de sécurité

- 📋 **Fonctionnalités pratiques**
  - Copie automatique vers le presse-papiers
  - Génération multiple de mots de passe
  - Interface intuitive et responsive

- 🌐 **Multiplateforme**
  - Application web (Flask) - **Recommandée**
  - Application desktop (Tkinter)
  - Compatible Windows, macOS, Linux

## 🚀 Installation Rapide

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/votre-username/SecurePassGen.git
   cd SecurePassGen
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python launcher.py
   ```

## 🎮 Utilisation

### 🌐 Version GitHub Pages (Actuellement Disponible)

**Accès direct sans installation :**

👉 **[https://jimmyramsamynaick.github.io/SecurePassGen/](https://jimmyramsamynaick.github.io/SecurePassGen/)**

**Avantages :**
- ✅ Fonctionne immédiatement
- ✅ Aucune installation requise
- ✅ Interface moderne et responsive
- ✅ Compatible avec tous les navigateurs
- ✅ Fonctionnement 100% côté client (sécurisé)
- ✅ Accessible depuis n'importe quel appareil

---

### 🚧 Versions en Développement

> ⚠️ **Note** : Les versions ci-dessous sont actuellement en cours de développement et peuvent ne pas fonctionner correctement.

#### Lanceur Universel

Le script `launcher.py` détecte automatiquement votre système et propose les meilleures options :

```bash
# Lancement automatique avec interface de sélection
python launcher.py

# Lancement direct en mode web
python launcher.py web

# Lancement direct en mode desktop
python launcher.py desktop

# Lancement en mode console
python launcher.py console
```

#### Application Web Locale

```bash
python web_app.py
```

Puis ouvrez votre navigateur sur `http://localhost:8080`

#### Application Desktop

```bash
python main.py
```

**Avantages (une fois développée) :**
- Application native
- Fonctionne hors ligne
- Intégration système

## 🛠️ Configuration

### Variables d'environnement

```bash
# Port pour l'application web (défaut: 8080)
export FLASK_PORT=8080

# Mode debug Flask (défaut: True)
export FLASK_DEBUG=True

# Désactiver les avertissements Tkinter sur macOS
export TK_SILENCE_DEPRECATION=1
```

## 🔧 Développement

### Structure du projet

```
SecurePassGen/
├── launcher.py          # Lanceur universel
├── main.py             # Application desktop (Tkinter)
├── web_app.py          # Application web (Flask)
├── requirements.txt    # Dépendances Python
├── README.md          # Documentation
└── templates/
    └── index.html     # Interface web
```

## 🌍 Compatibilité

### Systèmes d'exploitation testés

| OS | Version | Application Web | Application Desktop |
|---|---|---|---|
| **Windows** | 10/11 | ✅ | ✅ |
| **macOS** | 10.15+ | ✅ | ✅ |
| **Linux** | Ubuntu 20.04+ | ✅ | ✅ |

### Navigateurs supportés

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔒 Sécurité

- **Génération cryptographiquement sécurisée** : Utilise `secrets` de Python
- **Pas de stockage** : Aucun mot de passe n'est sauvegardé
- **Exécution locale** : Toutes les opérations sont effectuées localement
- **Code open source** : Transparence totale du code

## 🐛 Dépannage

### Problèmes courants

**1. Erreur "command not found: pip"**
```bash
# Utiliser pip3 à la place
pip3 install -r requirements.txt
```

**2. Problème Tkinter sur macOS**
```bash
# Utiliser l'application web à la place
python launcher.py web
```

**3. Port 5000 déjà utilisé**
```bash
# L'application utilise automatiquement le port 8080
# Ou modifier le port dans web_app.py
```

**4. Problèmes d'affichage Tkinter**
```bash
# Définir la variable d'environnement
export TK_SILENCE_DEPRECATION=1
python main.py
```

## 📝 Changelog

### Version 2.0.0
- ✨ Ajout de l'application web Flask
- 🚀 Lanceur universel multiplateforme
- 🎨 Interface web moderne et responsive
- 🔧 Amélioration de la compatibilité macOS
- 📱 Support mobile pour l'interface web

### Version 1.0.0
- 🎯 Application desktop Tkinter
- 🔐 Génération de mots de passe sécurisés
- 🔍 Analyse de robustesse
- 📋 Copie vers le presse-papiers

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT.

## 👨‍💻 Auteur

**Jimmy Ramsamynaick**

---

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !**
