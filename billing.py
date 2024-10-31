import os
import subprocess
import os
import subprocess
import platform
import tkinter.messagebox as msgbox
import customtkinter as ctk
import tkinter as tk
import datetime
import tkinter.messagebox as msgbox
import database_management
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch



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

        # Validate customer details
        if not customer_name or not customer_city or not customer_mobile:
            msgbox.showwarning("Input Error", "Please fill in all customer details.")
            return

        # Validate mobile number (numeric and 10 digits)
        if not customer_mobile.isdigit() or len(customer_mobile) != 10:
            msgbox.showwarning("Input Error", "Mobile number must be exactly 10 digits.")
            return

        # Process each product entry
        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name = product_name_entry.get()
            quantity = quantity_entry.get()
            price_per_item = price_entry.get()

            # Validate quantity and price (both must be numeric)
            if product_name:
                if not quantity.isdigit():
                    msgbox.showwarning("Input Error", f"Quantity for {product_name} must be a valid number.")
                    return
                if not price_per_item.replace('.', '', 1).isdigit():
                    msgbox.showwarning("Input Error", f"Price for {product_name} must be a valid number.")
                    return

                # Calculate total price if valid
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

        # Get the next bill ID before saving
        bill_id = database_management.get_next_bill_id()

        # Save bill to the database if all validations pass
        if database_management.add_bill(customer_name, customer_city, customer_mobile, total_bill_price, items):
            msgbox.showinfo("Success", f"Bill saved successfully with Bill ID: {bill_id}.")

            # Generate PDF of the bill after saving
            pdf_file_path = self.generate_pdf_bill(bill_id, customer_name, customer_city, customer_mobile, items,
                                                   total_bill_price)

            # Notify that the PDF has been saved
            msgbox.showinfo("PDF Saved", f"Bill saved as PDF at {pdf_file_path}")

            self.reset_fields()  # Clear fields for a new bill

            # Prepare for the next bill
            bill_id = database_management.get_next_bill_id()
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
        """Clear a specific product entry."""
        product_name_entry, quantity_entry, price_entry, total_label = self.entries[index]
        product_name_entry.delete(0, 'end')
        quantity_entry.delete(0, 'end')
        price_entry.delete(0, 'end')
        total_label.configure(text="₹0.00")
        self.update_total()

    def update_total(self, event=None):
        """Update the total price based on the quantity and price per item with validation."""
        total_bill_price = 0.0

        for product_name_entry, quantity_entry, price_entry, total_label in self.entries:
            product_name = product_name_entry.get()
            quantity = quantity_entry.get()
            price_per_item = price_entry.get()

            if product_name:
                if quantity.isdigit() and price_per_item.replace('.', '', 1).isdigit():
                    quantity = int(quantity)
                    price_per_item = float(price_per_item)
                    total_price = quantity * price_per_item
                    total_label.configure(text=f"₹{total_price:.2f}")
                    total_bill_price += total_price
                else:
                    total_label.configure(text="₹0.00")

        self.label_total_price.configure(text=f"Total Price: ₹{total_bill_price:.2f}")

    def update_time(self):
        """Update the current time display."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_datetime.configure(text=current_time)
        self.after(1000, self.update_time)  # Update time every second

    def scroll_up(self, event):
        """Scroll up event."""
        self.scrollable_frame.yview_scroll(-1, "units")

    def scroll_down(self, event):
        """Scroll down event."""
        self.scrollable_frame.yview_scroll(1, "units")

#print the bill in inter
    import subprocess
    import os

    def handle_print_bill(self):
        """Handle printing the bill using the default system PDF viewer."""
        pdf_file_path = f"bill_{bill_id}.pdf"

        try:
            # Check the operating system
            if platform.system() == "Windows":
                os.startfile(pdf_file_path, "print")  # Open the PDF in the default viewer and print
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Preview", pdf_file_path], check=True)
            else:  # Linux or other OS
                subprocess.run(["xdg-open", pdf_file_path], check=True)

            msgbox.showinfo("Print", "Bill opened in the default PDF viewer. Please print manually.")
        except Exception as e:
            msgbox.showerror("Error", f"Failed to print the bill: {str(e)}")

    import os

    def generate_pdf_bill(self, bill_id, customer_name, customer_city, customer_mobile, items, total_bill_price):
        """Generate the bill as a PDF."""
        # Create a directory named 'saved_bill' if it doesn't exist
        directory = "saved_bill"
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory

        # PDF file path
        pdf_file_path = os.path.join(directory, f"bill_{bill_id}.pdf")  # Save in 'saved_bill' folder

        # Create PDF document
        pdf = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        elements = []

        # Styles
        styles = getSampleStyleSheet()

        # Add Business Information at the top
        business_info = """
        <b>Raj Eletricals jamner</b><br/>
        Bajrang puara road jamaner<br/>
        Phone: +91-7219585666<br/>
        Email: Patilsainath517@gmail.com<br/>
        """
        elements.append(Paragraph(business_info, styles["Normal"]))
        bill_id = int(database_management.get_next_bill_id()) - 1

        # Add a title for the bill
        elements.append(Paragraph(f"Bill No.: {bill_id}", styles["Title"]))

        # Add customer details
        customer_info = f"""
        <b>Customer Information:</b><br/>
        Name: {customer_name}<br/>
        City: {customer_city}<br/>
        Mobile: {customer_mobile}<br/>
        <br/>
        """
        elements.append(Paragraph(customer_info, styles["Normal"]))

        # Create a table with product details (Product Name, Quantity, Price, Total Price)
        table_data = [["Product Name", "Quantity", "Price per Item (Rs.)", "Total Price (Rs.)"]]

        # Add rows for each item in the bill
        for item in items:
            row = [item['product_name'], item['quantity'], f"Rs.{item['price_per_item']:.2f}",
                   f"Rs.{item['total_price']:.2f}"]
            table_data.append(row)

        # Create the table with style
        table = Table(table_data, colWidths=[2.5 * inch, 1.0 * inch, 1.5 * inch, 1.5 * inch])

        # Add table styling (colors, grid lines, etc.)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        # Add total price
        elements.append(Paragraph(f"<b>Total Amount: Rs{total_bill_price:.2f}</b>", styles["Title"]))

        # Build the PDF
        pdf.build(elements)

        return pdf_file_path


