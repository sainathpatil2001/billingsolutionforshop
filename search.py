import customtkinter as ctk
import sqlite3


class SearchFragment(ctk.CTkFrame):
    def __init__(self, parent, update_callback):
        super().__init__(parent)

        self.update_callback = update_callback

        # Main search bar frame
        self.search_bar_frame = ctk.CTkFrame(self)
        self.search_bar_frame.pack(fill="x", padx=10, pady=10)

        # Search by customer info (Name, Mobile, or City)
        self.search_label = ctk.CTkLabel(self.search_bar_frame, text="Search by Customer Info:", font=("Arial", 18))
        self.search_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.search_entry = ctk.CTkEntry(self.search_bar_frame, width=300, font=("Arial", 16))
        self.search_entry.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.search_bills)  # Trigger search on typing

        # Search button for general info
        self.search_button = ctk.CTkButton(self.search_bar_frame, text="Search", width=120, command=self.search_bills)
        self.search_button.grid(row=0, column=2, padx=5, pady=10, sticky="w")

        # Bill No. specific search label
        self.bill_no_label = ctk.CTkLabel(self.search_bar_frame, text="Bill No.:", font=("Arial", 18))
        self.bill_no_label.grid(row=0, column=3, padx=(20, 5), pady=10, sticky="w")

        # Bill No. specific search entry
        self.bill_no_entry = ctk.CTkEntry(self.search_bar_frame, width=200, font=("Arial", 16))
        self.bill_no_entry.grid(row=0, column=4, padx=(5, 10), pady=10, sticky="w")
        self.bill_no_entry.bind("<KeyRelease>", self.search_by_bill_no)  # Trigger Bill No. search

        # Result container frame (scrollable)
        self.result_frame = ctk.CTkScrollableFrame(self, width=800, height=400)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def search_bills(self, event=None):
        """Search for bills based on customer info and display the results."""
        search_query = self.search_entry.get()

        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Query the database based on general info
        results = self.search_bills_in_db(search_query)

        if results:
            for result in results:
                self.create_bill_card(result)
        else:
            no_result_label = ctk.CTkLabel(self.result_frame, text="No bills found.", font=("Arial", 16))
            no_result_label.pack(pady=10)

    def search_by_bill_no(self, event=None):
        """Search for a bill using the Bill No. only."""
        bill_no = self.bill_no_entry.get()

        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Query the database by Bill No. only
        result = self.search_bill_by_no(bill_no)

        if result:
            self.create_bill_card(result)  # Display the single result as a card
        else:
            no_result_label = ctk.CTkLabel(self.result_frame, text="No bill found with this Bill No.", font=("Arial", 16))
            no_result_label.pack(pady=10)

    def search_bills_in_db(self, query):
        """Search bills from the database based on customer info."""
        try:
            sqliteConnection = sqlite3.connect('billing_solution_database.db')
            cursor = sqliteConnection.cursor()

            wildcard_query = f"%{query}%"
            cursor.execute('''
                SELECT bill_id, customer_name, customer_mobile, customer_city
                FROM Bills
                WHERE customer_name LIKE ? OR customer_mobile LIKE ? OR customer_city LIKE ?
            ''', (wildcard_query, wildcard_query, wildcard_query))

            bills = cursor.fetchall()
            return bills

        except sqlite3.Error as error:
            print('Error occurred while searching bills - ', error)
            return []

        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def search_bill_by_no(self, bill_no):
        """Search for a bill by Bill No. only."""
        try:
            sqliteConnection = sqlite3.connect('billing_solution_database.db')
            cursor = sqliteConnection.cursor()

            cursor.execute('''
                SELECT bill_id, customer_name, customer_mobile, customer_city
                FROM Bills
                WHERE bill_id = ?
            ''', (bill_no,))

            result = cursor.fetchone()
            return result

        except sqlite3.Error as error:
            print('Error occurred while searching for Bill No. - ', error)
            return None

        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def create_bill_card(self, bill_data):
        """Create a card for each bill in the result."""
        bill_id, customer_name, mobile, city = bill_data

        card_frame = ctk.CTkFrame(self.result_frame, corner_radius=10)
        card_frame.pack(fill="x", padx=10, pady=10, ipady=10)

        # Display bill information in the card
        bill_label = ctk.CTkLabel(card_frame, text=f"Bill No: {bill_id}", font=("Arial", 16, "bold"))
        bill_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        name_label = ctk.CTkLabel(card_frame, text=f"Name: {customer_name}", font=("Arial", 16))
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        mobile_label = ctk.CTkLabel(card_frame, text=f"Mobile: {mobile}", font=("Arial", 16))
        mobile_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        city_label = ctk.CTkLabel(card_frame, text=f"City: {city}", font=("Arial", 16))
        city_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Update button for each card
        update_button = ctk.CTkButton(card_frame, text="Update", width=120, command=lambda: self.update_bill(bill_id))
        update_button.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="e")

    def update_bill(self, bill_id):
        """Handle bill update logic (redirect to update page)."""
        print(f"Redirecting to update bill with Bill No: {bill_id}")
        self.update_callback(bill_id)
