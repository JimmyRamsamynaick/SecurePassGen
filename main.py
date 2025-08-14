#!/usr/bin/env python3
"""
SecurePassGen - Générateur de mots de passe sécurisé
Auteur: Assistant IA
Version: 1.0.0

Point d'entrée principal de l'application.
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.main_window import SecurePassGenApp

def main():
    """
    Fonction principale de l'application.
    """
    try:
        app = SecurePassGenApp()
        app.run()
    except KeyboardInterrupt:
        print("\n🔐 SecurePassGen fermé par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
