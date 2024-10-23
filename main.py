import customtkinter as ctk
import billing
import search
import settings
import stats
from database_management import initialize_database  # Import the function from your database module

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Billing Solution")
        self.state('zoomed')  # Fullscreen for Windows OS

        # Frame to hold the top menu buttons
        self.top_menu_frame = ctk.CTkFrame(self)
        self.top_menu_frame.pack(fill="x")

        # Create buttons for the top menu
        self.btn_billing = ctk.CTkButton(self.top_menu_frame, text="Billing", command=self.show_billing)
        self.btn_billing.pack(side="left", padx=10, pady=10)

        self.btn_search = ctk.CTkButton(self.top_menu_frame, text="Search", command=self.show_search)
        self.btn_search.pack(side="left", padx=10, pady=10)

        self.btn_settings = ctk.CTkButton(self.top_menu_frame, text="Settings", command=self.show_settings)
        self.btn_settings.pack(side="left", padx=10, pady=10)

        self.btn_stats = ctk.CTkButton(self.top_menu_frame, text="Statistics", command=self.show_stats)
        self.btn_stats.pack(side="left", padx=10, pady=10)

        # Frame to hold the current fragment
        self.fragment_frame = ctk.CTkFrame(self)
        self.fragment_frame.pack(fill="both", expand=True)

        # Show the billing fragment by default
        self.show_billing()

    def show_billing(self):
        self.clear_frame()
        billing_fragment = billing.BillingFragment(self.fragment_frame)
        billing_fragment.pack(fill="both", expand=True)

    def show_search(self):
        self.clear_frame()
        search_fragment = search.SearchFragment(self.fragment_frame)
        search_fragment.pack(fill="both", expand=True)

    def show_settings(self):
        self.clear_frame()
        settings_fragment = settings.SettingsFragment(self.fragment_frame)
        settings_fragment.pack(fill="both", expand=True)

    def show_stats(self):
        self.clear_frame()
        stats_fragment = stats.StatsFragment(self.fragment_frame)
        stats_fragment.pack(fill="both", expand=True)

    def clear_frame(self):
        for widget in self.fragment_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    initialize_database()  # Ensure the database is initialized at startup
    app = MainApp()
    app.mainloop()
