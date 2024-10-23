import customtkinter as ctk
import tkinter as tk
import datetime
import tkinter.messagebox as msgbox
import database_management

class BillingFragment(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a scrollable frame for product entries
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
        self.label_total_price = ctk.CTkLabel(self.fixed_button_frame, text="Total Price: ₹0.00", font=("Arial", 20, "bold"))
        self.label_total_price.pack(side="right", padx=5, pady=10)  # Position it to the right side

        self.clear_all_button = ctk.CTkButton(self.fixed_button_frame, text="Clear All", width=120, height=40, command=self.reset_fields)
        self.clear_all_button.pack(side="left", padx=5, pady=10)

        self.print_button = ctk.CTkButton(self.fixed_button_frame, text="Print Bill", width=120, height=40, command=self.handle_print_bill)
        self.print_button.pack(side="left", padx=5, pady=10)

        self.save_button = ctk.CTkButton(self.fixed_button_frame, text="Save Bill", width=120, height=40, command=self.handle_save_bill)
        self.save_button.pack(side="left", padx=5, pady=10)

    def create_widgets(self):
        # Configure grid to expand and fit full screen
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)
        self.scrollable_frame.grid_columnconfigure(3, weight=1)
        self.scrollable_frame.grid_columnconfigure(4, weight=1)  # For Clear button

        # Bill No. Label
        self.label_bill_no = ctk.CTkLabel(self.scrollable_frame, text="Bill No.: Demo No.", font=("Arial", 16, "bold"))
        self.label_bill_no.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # Customer details section with larger input boxes
        self.create_label_entry("Customer Name:", 1)
        self.entry_customer_name = self.create_entry(1, 1)

        self.create_label_entry("Customer City:", 2)
        self.entry_city = self.create_entry(2, 1)

        self.create_label_entry("Mobile No.:", 3)
        self.entry_mobile = self.create_entry(3, 1)

        # Labels for product table
        ctk.CTkLabel(self.scrollable_frame, text="Product Name", font=("Arial", 16, "bold")).grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")
        ctk.CTkLabel(self.scrollable_frame, text="Quantity", font=("Arial", 16, "bold")).grid(row=4, column=1, padx=5, pady=(5, 0), sticky="w")
        ctk.CTkLabel(self.scrollable_frame, text="Price per Item", font=("Arial", 16, "bold")).grid(row=4, column=2, padx=5, pady=(5, 0), sticky="w")
        ctk.CTkLabel(self.scrollable_frame, text="Total Price", font=("Arial", 16, "bold")).grid(row=4, column=3, padx=5, pady=(5, 0), sticky="w")

        # Product entry section with larger input boxes for each product
        for i in range(40):  # Support for 40 products
            product_name_entry = self.create_entry(i + 5, 0, width=180)
            quantity_entry = self.create_entry(i + 5, 1, width=80)
            price_entry = self.create_entry(i + 5, 2, width=130)
            total_label = self.create_label(f"₹0.00", i + 5, 3)  # Total price label for each product

            # Store entries and total labels in their respective lists for navigation and calculations
            self.entries.append((product_name_entry, quantity_entry, price_entry, total_label))
            self.create_clear_button(i + 5, 4, i)

            # Bind quantity and price entry updates to update total
            quantity_entry.bind("<KeyRelease>", self.update_total)
            price_entry.bind("<KeyRelease>", self.update_total)

        # Current date and time display at the top right corner
        self.label_datetime = ctk.CTkLabel(self.scrollable_frame, text="", font=("Arial", 16, "bold"))
        self.label_datetime.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky="e")
        self.update_time()

    def create_label_entry(self, text, row):
        """Helper function to create label-entry pairs with correct positioning."""
        label = ctk.CTkLabel(self.scrollable_frame, text=text, font=("Arial", 16, "bold"))
        label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky="w")  # Align label to the left
        return label

    def create_entry(self, row, col=1, width=300):
        """Helper function to create larger entry fields."""
        entry = ctk.CTkEntry(self.scrollable_frame, width=width)
        entry.grid(row=row, column=col, padx=5, pady=(5, 0), sticky="w")
        return entry

    def create_label(self, text, row, col):
        """Helper function to create labels for total price per product."""
        label = ctk.CTkLabel(self.scrollable_frame, text=text, font=("Arial", 16, "bold"))
        label.grid(row=row, column=col, padx=5, pady=(5, 0))
        return label

    def create_clear_button(self, row, col, index):
        """Helper function to create a Clear button for each product row."""
        button = ctk.CTkButton(self.scrollable_frame, text="Clear", command=lambda: self.clear_row(index))
        button.grid(row=row, column=col, padx=5, pady=(5, 0))
        return button

    def clear_row(self, index):
        """Clear the input fields for a specific product row."""
        self.entries[index][0].delete(0, tk.END)  # Product Name
        self.entries[index][1].delete(0, tk.END)  # Quantity
        self.entries[index][2].delete(0, tk.END)  # Price
        self.entries[index][3].configure(text="₹0.00")  # Reset total price label
        self.calculate_total()  # Recalculate total after clearing

    def reset_fields(self):
        """Clear all input fields."""
        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name_entry.delete(0, tk.END)  # Clear Product Name
            quantity_entry.delete(0, tk.END)  # Clear Quantity
            price_entry.delete(0, tk.END)  # Clear Price
            total_label.configure(text="₹0.00")  # Reset total price label
        self.label_total_price.configure(text="Total Price: ₹0.00")  # Reset overall total price

    def handle_save_bill(self):
        """Handle the save bill functionality."""
        # Gather customer details
        customer_name = self.entry_customer_name.get()
        customer_city = self.entry_city.get()
        customer_mobile = self.entry_mobile.get()

        # Set the special customer flag to 0 (not a special customer)
        is_special_customer = 0

        # Gather product details
        items = []
        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name = product_name_entry.get()
            try:
                quantity = int(quantity_entry.get())
                price_per_item = float(price_entry.get())
                total_price = quantity * price_per_item
            except ValueError:
                quantity = 0
                price_per_item = 0.0
                total_price = 0.0

            if product_name:  # Add only if the product name is not empty
                items.append({
                    'product_name': product_name,
                    'quantity': quantity,
                    'price_per_item': price_per_item,
                    'total_price': total_price,
                })

        # Calculate total bill price
        total_bill_price = sum(item['total_price'] for item in items)

        # Save bill to database
        if items:
            bill_id = database_management.add_bill(customer_name, customer_city, customer_mobile, total_bill_price,
                                                   items)
            msgbox.showinfo("Success", f"Bill saved successfully with Bill ID: {bill_id}")
            self.reset_fields()  # Reset fields after saving
        else:
            msgbox.showwarning("No Items", "No items to save.")

    def update_total(self, event=None):
        """Update total price for each product row and overall total."""
        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            try:
                quantity = int(quantity_entry.get())
                price_per_item = float(price_entry.get())
                total_price = quantity * price_per_item
            except ValueError:
                total_price = 0.0  # Default to 0 if input is invalid

            total_label.configure(text=f"₹{total_price:.2f}")  # Update total price label

        self.calculate_total()  # Calculate overall total price

    def calculate_total(self):
        """Calculate the overall total price."""
        total_price = sum(float(total_label.cget("text")[1:]) for _, _, _, total_label in self.entries)
        self.label_total_price.configure(text=f"Total Price: ₹{total_price:.2f}")

    def scroll_up(self, event=None):
        """Scroll up in the frame."""
        self.scrollable_frame.yview_scroll(-1, "units")

    def scroll_down(self, event=None):
        """Scroll down in the frame."""
        self.scrollable_frame.yview_scroll(1, "units")

    def update_time(self):
        """Update the date and time display."""
        now = datetime.datetime.now()
        self.label_datetime.configure(text=now.strftime("%Y-%m-%d %H:%M:%S"))
        self.after(1000, self.update_time)  # Update every second

    def handle_print_bill(self):
        """Placeholder for print bill functionality."""
        msgbox.showinfo("Print Bill", "Print functionality is not implemented yet.")
