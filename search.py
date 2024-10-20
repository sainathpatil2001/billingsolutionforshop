import customtkinter as ctk

class SearchFragment(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Search Functionality Coming Soon!", font=("Arial", 24)).pack(pady=20)
