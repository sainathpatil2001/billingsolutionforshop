import customtkinter as ctk
import sqlite3

from plyer import notification


class UpdateFragment(ctk.CTkFrame):
    def __init__(self, parent, bill_id, back_callback):
        super().__init__(parent)
        self.bill_id = bill_id
        self.back_callback = back_callback

        # Initialize UI components first
        self.initialize_ui()

        # Load the customer and product details after UI components are initialized
        self.load_bill_details()

    def initialize_ui(self):
        """Initialize the UI components."""
        # Header
        self.update_label = ctk.CTkLabel(self, text=f"Update Bill No: {self.bill_id}", font=("Arial", 22))
        self.update_label.pack(pady=10)

        # Customer Details
        self.customer_frame = ctk.CTkFrame(self)
        self.customer_frame.pack(pady=5)

        self.name_label = ctk.CTkLabel(self.customer_frame, text="Customer Name:", font=("Arial", 16))
        self.name_label.grid(row=0, column=0, padx=5)
        self.name_entry = ctk.CTkEntry(self.customer_frame, font=("Arial", 16), width=200)
        self.name_entry.grid(row=0, column=1, padx=5)

        self.mobile_label = ctk.CTkLabel(self.customer_frame, text="Customer Mobile:", font=("Arial", 16))
        self.mobile_label.grid(row=1, column=0, padx=5)
        self.mobile_entry = ctk.CTkEntry(self.customer_frame, font=("Arial", 16), width=200)
        self.mobile_entry.grid(row=1, column=1, padx=5)

        self.city_label = ctk.CTkLabel(self.customer_frame, text="Customer City:", font=("Arial", 16))
        self.city_label.grid(row=2, column=0, padx=5)
        self.city_entry = ctk.CTkEntry(self.customer_frame, font=("Arial", 16), width=200)
        self.city_entry.grid(row=2, column=1, padx=5)

        # Product Items Frame
        self.items_frame = ctk.CTkFrame(self)
        self.items_frame.pack(pady=10)
        self.items_entries = []

        # Update Button
        self.update_button = ctk.CTkButton(self, text="Update Bill", command=self.update_bill_details)
        self.update_button.pack(pady=20)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back_to_search)
        self.back_button.pack(pady=10)

    def load_bill_details(self):
        """Load customer and product details from the database to populate the entries."""
        try:
            sqliteConnection = sqlite3.connect('billing_solution_database.db')
            cursor = sqliteConnection.cursor()

            # Fetch customer details
            cursor.execute('''
                SELECT customer_name, customer_mobile, customer_city
                FROM Bills
                WHERE bill_id = ?
            ''', (self.bill_id,))
            customer_details = cursor.fetchone()

            if customer_details:
                self.name_entry.insert(0, customer_details[0])
                self.mobile_entry.insert(0, customer_details[1])
                self.city_entry.insert(0, customer_details[2])

            # Fetch product items associated with this bill
            cursor.execute('''
                SELECT product_name, quantity, price_per_item, total_price
                FROM Bill_Items
                WHERE bill_id = ?
            ''', (self.bill_id,))
            items = cursor.fetchall()

            for idx, item in enumerate(items):
                self.add_item_entry(idx, item[0], item[1], item[2], item[3])

        except sqlite3.Error as error:
            print('Error loading bill details:', error)

        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def add_item_entry(self, index, product_name, quantity, price_per_item, total_price):
        """Create entry fields for a single product item."""
        row_frame = ctk.CTkFrame(self.items_frame)
        row_frame.grid(row=index, column=0, pady=5)

        name_entry = ctk.CTkEntry(row_frame, width=150)
        name_entry.insert(0, product_name)
        name_entry.grid(row=0, column=0, padx=5)

        quantity_entry = ctk.CTkEntry(row_frame, width=100)
        quantity_entry.insert(0, quantity)
        quantity_entry.grid(row=0, column=1, padx=5)

        price_entry = ctk.CTkEntry(row_frame, width=100)
        price_entry.insert(0, price_per_item)
        price_entry.grid(row=0, column=2, padx=5)

        total_entry = ctk.CTkEntry(row_frame, width=100)
        total_entry.insert(0, total_price)
        total_entry.grid(row=0, column=3, padx=5)

        # Save references to entries for update purposes
        self.items_entries.append((name_entry, quantity_entry, price_entry, total_entry))

    def update_bill_details(self):
        """Update customer and product details in the database."""
        customer_name = self.name_entry.get()
        customer_mobile = self.mobile_entry.get()
        customer_city = self.city_entry.get()

        # Calculate total price from items
        total_price = 0
        updated_items = []
        for (name_entry, quantity_entry, price_entry, total_entry) in self.items_entries:
            product_name = name_entry.get()
            quantity = int(quantity_entry.get())
            price_per_item = float(price_entry.get())
            item_total_price = quantity * price_per_item

            total_price += item_total_price
            updated_items.append({
                'product_name': product_name,
                'quantity': quantity,
                'price_per_item': price_per_item,
                'total_price': item_total_price
            })

        # Database update logic
        try:
            sqliteConnection = sqlite3.connect('billing_solution_database.db')
            cursor = sqliteConnection.cursor()

            # Update customer details in Bills
            cursor.execute(''' 
                UPDATE Bills
                SET customer_name = ?, customer_city = ?, customer_mobile = ?, total_price = ?
                WHERE bill_id = ?
            ''', (customer_name, customer_city, customer_mobile, total_price, self.bill_id))

            # Delete old items and insert updated items
            cursor.execute('DELETE FROM Bill_Items WHERE bill_id = ?', (self.bill_id,))
            for item in updated_items:
                cursor.execute('''
                    INSERT INTO Bill_Items (bill_id, product_name, quantity, price_per_item, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    self.bill_id, item['product_name'], item['quantity'], item['price_per_item'], item['total_price']))

            sqliteConnection.commit()
            print("Bill and items updated successfully.")

            # Show notification
            notification.notify(
                title="Bill Updated",
                message=f"Bill updated for {customer_name}\nMobile: {customer_mobile}",
                app_name="Billing Solution",
                timeout=10  # Duration in seconds for the notification to stay on the screen
            )

        except sqlite3.Error as error:
            print('Error while updating bill:', error)

        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def back_to_search(self):
        """Return to the search fragment."""
        self.back_callback()
