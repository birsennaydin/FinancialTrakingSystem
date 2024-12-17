import tkinter as tk
from presentation.application import Application

def run_application():
    """Function to initialize and run the Tkinter application"""
    root = tk.Tk()
    Application(root)  # Creating an instance of the Application class
    root.mainloop()  # Starts the Tkinter event loop
