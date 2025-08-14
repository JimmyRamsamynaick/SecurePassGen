#!/usr/bin/env python3
"""
SecurePassGen - Version Web
Générateur de Mots de Passe Sécurisé
"""

from flask import Flask, render_template, request, jsonify
import random
import string
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    try:
        data = request.json
        length = int(data.get('length', 12))
        use_lowercase = data.get('lowercase', True)
        use_uppercase = data.get('uppercase', True)
        use_digits = data.get('digits', True)
        use_special = data.get('special', True)
        exclude_ambiguous = data.get('exclude_ambiguous', False)
        
        chars = ""
        
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if exclude_ambiguous:
            chars = chars.replace('0', '').replace('O', '').replace('1', '')
            chars = chars.replace('l', '').replace('I', '')
        
        if not chars:
            return jsonify({'error': 'Veuillez sélectionner au moins un type de caractère.'}), 400
        
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Analyse de la force
        strength_analysis = analyze_password_strength(password)
        
        return jsonify({
            'password': password,
            'strength': strength_analysis
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la génération: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_password():
    try:
        data = request.json
        password = data.get('password', '')
        
        if not password:
            return jsonify({'error': 'Mot de passe requis'}), 400
        
        analysis = analyze_password_strength(password)
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de l\'analyse: {str(e)}'}), 500

def analyze_password_strength(password):
    """Analyse la force d'un mot de passe"""
    score = 0
    feedback = []
    
    # Longueur
    if len(password) >= 12:
        score += 2
        feedback.append("✓ Longueur excellente (12+ caractères)")
    elif len(password) >= 8:
        score += 1
        feedback.append("✓ Longueur correcte (8+ caractères)")
    else:
        feedback.append("✗ Longueur insuffisante (moins de 8 caractères)")
    
    # Types de caractères
    if any(c.islower() for c in password):
        score += 1
        feedback.append("✓ Contient des minuscules")
    
    if any(c.isupper() for c in password):
        score += 1
        feedback.append("✓ Contient des majuscules")
    
    if any(c.isdigit() for c in password):
        score += 1
        feedback.append("✓ Contient des chiffres")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
        feedback.append("✓ Contient des caractères spéciaux")
    
    # Évaluation finale
    if score >= 5:
        strength = "Très fort"
        color = "success"
    elif score >= 3:
        strength = "Fort"
        color = "warning"
    elif score >= 2:
        strength = "Moyen"
        color = "info"
    else:
        strength = "Faible"
        color = "danger"
    
    return {
        'strength': strength,
        'score': score,
        'max_score': 6,
        'color': color,
        'feedback': feedback
    }

if __name__ == '__main__':
    # Créer le dossier templates s'il n'existe pas
    os.makedirs('templates', exist_ok=True)
    
    print("🔐 SecurePassGen Web - Démarrage...")
    print("📱 Accédez à l'application sur: http://localhost:8080")
    
    app.run(debug=True, host='0.0.0.0', port=8080)