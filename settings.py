import customtkinter as ctk

class SettingsFragment(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Settings Functionality Coming Soon!", font=("Arial", 24)).pack(pady=20)
