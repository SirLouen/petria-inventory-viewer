import tkinter as tk
from inventory_viewer import InventoryViewer
import ctypes
import sys
import os

def main():
    
    if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if sys.platform.startswith('win'):
        myappid = 'SirLouen.PetriaInventoryViewer.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    root = tk.Tk()
    app = InventoryViewer(root, application_path)
    root.mainloop()

if __name__ == "__main__":
    main()