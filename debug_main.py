#!/usr/bin/env python3

import sys
import os
from pathlib import Path

print("=== DEBUG SECUREPASSGEN ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
print(f"Added to path: {src_path}")

try:
    print("Importing tkinter...")
    import tkinter as tk
    print("✓ tkinter imported successfully")
    
    print("Importing application modules...")
    from gui.main_window import SecurePassGenApp
    print("✓ SecurePassGenApp imported successfully")
    
    print("Creating application instance...")
    app = SecurePassGenApp()
    print("✓ Application instance created")
    
    print("Starting application...")
    app.run()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)