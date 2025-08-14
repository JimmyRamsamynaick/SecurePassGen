#!/usr/bin/env python3
"""
Test d'affichage Tkinter minimal pour diagnostiquer les problèmes
"""

import tkinter as tk
from tkinter import ttk
import sys
import time

print("=== TEST DISPLAY TKINTER ===")
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

try:
    print("Creating Tk root...")
    root = tk.Tk()
    print("✓ Tk root created")
    
    print("Configuring window...")
    root.title("Test Display")
    root.geometry("400x300")
    root.configure(bg='lightblue')
    
    # Configuration macOS
    if sys.platform == "darwin":
        print("Applying macOS configuration...")
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(lambda: root.attributes('-topmost', False))
    
    print("Creating widgets...")
    label = tk.Label(root, text="Test d'affichage réussi!", font=('Arial', 16), bg='lightblue')
    label.pack(pady=50)
    
    button = tk.Button(root, text="Fermer", command=root.quit, font=('Arial', 12))
    button.pack(pady=20)
    
    print("Forcing display...")
    root.deiconify()
    root.lift()
    root.focus_force()
    root.update()
    
    print("Window should be visible now!")
    print("Testing update loop...")
    
    # Test d'affichage sans mainloop
    for i in range(10):
        try:
            root.update()
            print(f"Update {i+1}/10 successful")
            time.sleep(0.5)
        except tk.TclError as e:
            print(f"TclError during update {i+1}: {e}")
            break
        except Exception as e:
            print(f"Error during update {i+1}: {e}")
            break
    
    print("Starting mainloop for 5 seconds...")
    root.after(5000, root.quit)  # Fermer après 5 secondes
    root.mainloop()
    
    print("Mainloop finished")
    root.destroy()
    print("Window destroyed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed")