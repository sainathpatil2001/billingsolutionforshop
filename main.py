import customtkinter as ctk
import billing
import search
import settings
import stats
import update_fragment
from database_management import initialize_database  # Import the function from your database module
from PIL import Image, ImageTk  # Import required modules to handle image loading
from customtkinter import CTkImage


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Biller Solution 2024")
        self.state('zoomed')  # Fullscreen for Windows OS

        # Frame to hold the top menu buttons and logo
        self.top_menu_frame = ctk.CTkFrame(self)
        self.top_menu_frame.pack(fill="x")

        # Add logo image
        self.logo = self.load_logo("images-removebg-preview.png")  # Provide the correct path to your logo image
        self.logo_label = ctk.CTkLabel(self.top_menu_frame, image=self.logo, text="")
        self.logo_label.pack(side="left", padx=10, pady=10)

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

    def load_logo(self, logo_path):
        """Load the logo image and return it in a format suitable for display."""
        try:
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality downsampling
            return ImageTk.PhotoImage(logo_img)
        except FileNotFoundError:
            print("Logo image not found.")
            return None

    def show_billing(self):
        self.clear_frame()
        billing_fragment = billing.BillingFragment(self.fragment_frame)
        billing_fragment.pack(fill="both", expand=True)

    def show_search(self):
        self.clear_frame()

        # Define the callback to display the update fragment with `bill_id`
        def update_callback(bill_id):
            self.show_update_fragment(bill_id)

        # Initialize the SearchFragment with update_callback
        search_fragment = search.SearchFragment(self.fragment_frame, update_callback=update_callback)
        search_fragment.pack(fill="both", expand=True)

    def show_settings(self):
        self.clear_frame()
        settings_fragment = settings.SettingsFragment(self.fragment_frame)
        settings_fragment.pack(fill="both", expand=True)

    def show_stats(self):
        self.clear_frame()
        stats_fragment = stats.StatsFragment(self.fragment_frame)
        stats_fragment.pack(fill="both", expand=True)

    def show_update_fragment(self, bill_id):
        """Show the update fragment with the provided bill ID."""
        self.clear_frame()
        update_fragment_obj = update_fragment.UpdateFragment(self.fragment_frame, bill_id, self.show_search)
        update_fragment_obj.pack(fill="both", expand=True)

    def clear_frame(self):
        """Clear all widgets in the fragment frame."""
        for widget in self.fragment_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    initialize_database()  # Ensure the database is initialized at startup
    app = MainApp()
    app.mainloop()
