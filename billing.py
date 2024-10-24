# main.py

import customtkinter as ctk
import tkinter as tk
import datetime
import tkinter.messagebox as msgbox
import database_management


class BillingFragment(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global bill_id
        bill_id = 00
        bill_id = database_management.get_next_bill_id()
        # Set up frame and widgets as before
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.entries = []  # List to store entry widgets
        self.total_labels = []  # List to store total labels
        self.create_widgets()

        # Bind keyboard navigation for scrolling
        self.bind("<Up>", self.scroll_up)
        self.bind("<Down>", self.scroll_down)

        # Fixed bottom buttons
        self.fixed_button_frame = ctk.CTkFrame(self)
        self.fixed_button_frame.pack(side="bottom", fill="x")

        # Add total price label to fixed button frame
        self.label_total_price = ctk.CTkLabel(self.fixed_button_frame, text="Total Price: ₹0.00",
                                              font=("Arial", 20, "bold"))
        self.label_total_price.pack(side="right", padx=5, pady=10)  # Position it to the right side

        self.clear_all_button = ctk.CTkButton(self.fixed_button_frame, text="Clear All", width=120, height=40,
                                              command=self.reset_fields)
        self.clear_all_button.pack(side="left", padx=5, pady=10)

        self.print_button = ctk.CTkButton(self.fixed_button_frame, text="Print Bill", width=120, height=40,
                                          command=self.handle_print_bill)
        self.print_button.pack(side="left", padx=5, pady=10)

        self.save_button = ctk.CTkButton(self.fixed_button_frame, text="Save Bill", width=120, height=40,
                                         command=self.handle_save_bill)
        self.save_button.pack(side="left", padx=5, pady=10)

    def create_widgets(self):
        # Configure grid to expand and fit full screen
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)
        self.scrollable_frame.grid_columnconfigure(3, weight=1)

        # Bill No. Label
        self.label_bill_no = ctk.CTkLabel(self.scrollable_frame,
                                          text=f"Bill No.: {bill_id}",
                                          font=("Arial", 16, "bold"))
        self.label_bill_no.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # Customer details section
        self.create_label_entry("Customer Name:", 1)
        self.entry_customer_name = self.create_entry(1, 1)

        self.create_label_entry("Customer City:", 2)
        self.entry_city = self.create_entry(2, 1)

        self.create_label_entry("Mobile No.:", 3)
        self.entry_mobile = self.create_entry(3, 1)

        # Labels for product table
        ctk.CTkLabel(self.scrollable_frame, text="Product Name", font=("Arial", 16, "bold")).grid(row=4, column=0,
                                                                                                  padx=5, pady=(5, 0),
                                                                                                  sticky="w")
        ctk.CTkLabel(self.scrollable_frame, text="Quantity", font=("Arial", 16, "bold")).grid(row=4, column=1, padx=5,
                                                                                              pady=(5, 0), sticky="w")
        ctk.CTkLabel(self.scrollable_frame, text="Price per Item", font=("Arial", 16, "bold")).grid(row=4, column=2,
                                                                                                    padx=5, pady=(5, 0),
                                                                                                    sticky="w")
        ctk.CTkLabel(self.scrollable_frame, text="Total Price", font=("Arial", 16, "bold")).grid(row=4, column=3,
                                                                                                 padx=5, pady=(5, 0),
                                                                                                 sticky="w")

        # Product entry section for each product
        for i in range(40):  # Support for 40 products
            product_name_entry = self.create_entry(i + 5, 0, width=180)
            quantity_entry = self.create_entry(i + 5, 1, width=80)
            price_entry = self.create_entry(i + 5, 2, width=130)
            total_label = self.create_label(f"₹0.00", i + 5, 3)  # Total price label for each product

            self.entries.append((product_name_entry, quantity_entry, price_entry, total_label))
            self.create_clear_button(i + 5, 4, i)

            # Bind quantity and price entry updates to update total
            quantity_entry.bind("<KeyRelease>", self.update_total)
            price_entry.bind("<KeyRelease>", self.update_total)

        # Current date and time display
        self.label_datetime = ctk.CTkLabel(self.scrollable_frame, text="", font=("Arial", 16, "bold"))
        self.label_datetime.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky="e")
        self.update_time()

    def handle_save_bill(self):
        """Handle the save bill functionality."""
        customer_name = self.entry_customer_name.get()
        customer_city = self.entry_city.get()
        customer_mobile = self.entry_mobile.get()

        items = []
        total_bill_price = 0.0

        # Process each product entry
        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name = product_name_entry.get()
            quantity = quantity_entry.get()
            price_per_item = price_entry.get()

            if product_name and quantity.isdigit() and price_per_item.replace('.', '', 1).isdigit():
                quantity = int(quantity)
                price_per_item = float(price_per_item)
                total_price = quantity * price_per_item

                items.append({
                    'product_name': product_name,
                    'quantity': quantity,
                    'price_per_item': price_per_item,
                    'total_price': total_price
                })
                total_bill_price += total_price

                total_label.configure(text=f"₹{total_price:.2f}")

        # Validate customer details
        if not customer_name or not customer_city or not customer_mobile:
            msgbox.showwarning("Input Error", "Please fill in all customer details.")
            return

        # Save bill to the database
        if database_management.add_bill(customer_name, customer_city, customer_mobile, total_bill_price, items):
            msgbox.showinfo("Success", f"Bill saved successfully.")

            # Reset fields for new entry
            self.reset_fields()

            # Generate the new bill_id
            global bill_id
            bill_id = database_management.get_next_bill_id()

            # Update the Bill No. label in the GUI
            self.label_bill_no.configure(text=f"Bill No.: {bill_id}")

        else:
            msgbox.showerror("Error", "Failed to save bill.")

    def create_label_entry(self, label_text, row):
        """Create a label and an entry for customer details."""
        label = ctk.CTkLabel(self.scrollable_frame, text=label_text, font=("Arial", 16))
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

    def create_entry(self, row, column, width=150):
        """Create an entry widget."""
        entry = ctk.CTkEntry(self.scrollable_frame, width=width)
        entry.grid(row=row, column=column, padx=5, pady=5, sticky="w")
        return entry

    def create_label(self, text, row, column):
        """Create a label to display text."""
        label = ctk.CTkLabel(self.scrollable_frame, text=text, font=("Arial", 16))
        label.grid(row=row, column=column, padx=5, pady=5, sticky="w")
        return label

    def create_clear_button(self, row, column, index):
        """Create a clear button for each product entry."""
        button = ctk.CTkButton(self.scrollable_frame, text="Clear", command=lambda idx=index: self.clear_entry(idx))
        button.grid(row=row, column=column, padx=5, pady=5, sticky="w")

    def reset_fields(self):
        """Reset all fields for a new bill."""
        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name_entry.delete(0, 'end')
            quantity_entry.delete(0, 'end')
            price_entry.delete(0, 'end')
            total_label.configure(text="₹0.00")

        self.entry_customer_name.delete(0, 'end')
        self.entry_city.delete(0, 'end')
        self.entry_mobile.delete(0, 'end')
        self.label_total_price.configure(text="Total Price: ₹0.00")


    def clear_entry(self, index):
        """Clear specific product entry fields."""
        product_name_entry, quantity_entry, price_entry, total_label = self.entries[index]
        product_name_entry.delete(0, 'end')
        quantity_entry.delete(0, 'end')
        price_entry.delete(0, 'end')
        total_label.configure(text="₹0.00")

        self.update_total()

    def update_total(self, event=None):
        """Update the total price based on the quantity and price per item."""
        total_bill_price = 0.0

        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name = product_name_entry.get()
            quantity = quantity_entry.get()
            price_per_item = price_entry.get()

            if product_name and quantity.isdigit() and price_per_item.replace('.', '', 1).isdigit():
                quantity = int(quantity)
                price_per_item = float(price_per_item)
                total_price = quantity * price_per_item
                total_label.configure(text=f"₹{total_price:.2f}")
                total_bill_price += total_price
            else:
                total_label.configure(text="₹0.00")

        self.label_total_price.configure(text=f"Total Price: ₹{total_bill_price:.2f}")

    def update_time(self):
        """Update the current date and time."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_datetime.configure(text=now)
        self.after(1000, self.update_time)  # Update every second

    def scroll_up(self, event):
        """Scroll the frame up."""
        self.scrollable_frame.yview_scroll(-1, "units")

    def scroll_down(self, event):
        """Scroll the frame down."""
        self.scrollable_frame.yview_scroll(1, "units")

    def handle_print_bill(self):
        """Placeholder for print bill functionality."""
        msgbox.showinfo("Print Bill", "Print functionality is not implemented yet.")


# Main application
if __name__ == "__main__":
    # Initialize the database first
    database_management.initialize_database()

    app = ctk.CTk()
    app.title("Billing Solution")
    app.geometry("800x600")

    billing_fragment = BillingFragment(app)
    billing_fragment.pack(fill="both", expand=True)

    app.mainloop()
