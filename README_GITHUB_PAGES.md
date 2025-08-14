# 🔐 SecurePassGen - GitHub Pages

## Version Web Statique

Cette version de SecurePassGen fonctionne entièrement côté client et est hébergée sur GitHub Pages.

### 🌐 Accès Direct

**[Ouvrir SecurePassGen](https://jimmyramsamynaick.github.io/SecurePassGen/)**

### ✨ Fonctionnalités

- **Génération sécurisée** : Utilise `crypto.getRandomValues()` pour une génération cryptographiquement sécurisée
- **Interface moderne** : Design responsive avec Bootstrap 5
- **Analyse de force** : Évaluation en temps réel de la robustesse des mots de passe
- **Génération multiple** : Création de plusieurs mots de passe en une fois
- **Copie rapide** : Copie dans le presse-papiers en un clic
- **Confidentialité totale** : Aucune donnée n'est envoyée sur internet, tout fonctionne localement

### 🔧 Configuration

- **Longueur** : De 4 à 64 caractères
- **Types de caractères** :
  - Minuscules (a-z)
  - Majuscules (A-Z)
  - Chiffres (0-9)
  - Caractères spéciaux (!@#$%^&*)
- **Option** : Exclusion des caractères ambigus (0, O, 1, l, I)

### 🛡️ Sécurité

- **Génération côté client** : Aucune donnée ne quitte votre navigateur
- **API Crypto Web** : Utilise l'API cryptographique native du navigateur
- **Pas de stockage** : Aucun mot de passe n'est sauvegardé
- **HTTPS** : Servi via HTTPS par GitHub Pages

### 📱 Compatibilité

- **Navigateurs modernes** : Chrome, Firefox, Safari, Edge
- **Appareils mobiles** : Interface responsive pour smartphones et tablettes
- **Hors ligne** : Fonctionne sans connexion internet après le premier chargement

### 🚀 Déploiement

Cette version est automatiquement déployée sur GitHub Pages à partir du fichier `index.html` dans la branche principale.

### 📋 Autres Versions

- **Application Desktop** : Version Tkinter pour Windows, macOS, Linux
- **Application Web Flask** : Version serveur avec API Python
- **Lanceur Universel** : Script de détection automatique de plateforme

### 🔗 Liens

- [Repository GitHub](https://github.com/jimmyramsamynaick/SecurePassGen)
- [Documentation complète](README.md)
- [Releases](https://github.com/jimmyramsamynaick/SecurePassGen/releases)

---

**SecurePassGen** - Générateur de mots de passe sécurisé multiplateforme