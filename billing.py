import customtkinter as ctk
import tkinter.messagebox as msgbox
import datetime


class BillingFragment(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.products = []
        self.is_special_customer = False

    def create_widgets(self):
        # Product entry section
        ctk.CTkLabel(self, text="Product Name:", font=("Arial", 18, "bold")).grid(row=0, column=0, padx=20, pady=10,
                                                                                  sticky="e")
        self.entry_product_name = ctk.CTkEntry(self, width=300)
        self.entry_product_name.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.entry_product_name.bind('<Return>', self.add_product)

        ctk.CTkLabel(self, text="Quantity:", font=("Arial", 18, "bold")).grid(row=1, column=0, padx=20, pady=10,
                                                                              sticky="e")
        self.entry_quantity = ctk.CTkEntry(self, width=300)
        self.entry_quantity.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(self, text="Price per Item:", font=("Arial", 18, "bold")).grid(row=2, column=0, padx=20, pady=10,
                                                                                    sticky="e")
        self.entry_price = ctk.CTkEntry(self, width=300)
        self.entry_price.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        # Customer details section
        ctk.CTkLabel(self, text="Customer Name:", font=("Arial", 18, "bold")).grid(row=3, column=0, padx=20, pady=10,
                                                                                   sticky="e")
        self.entry_customer_name = ctk.CTkEntry(self, width=300)
        self.entry_customer_name.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(self, text="Customer City:", font=("Arial", 18, "bold")).grid(row=4, column=0, padx=20, pady=10,
                                                                                   sticky="e")
        self.entry_city = ctk.CTkEntry(self, width=300)
        self.entry_city.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(self, text="Mobile No.:", font=("Arial", 18, "bold")).grid(row=5, column=0, padx=20, pady=10,
                                                                                sticky="e")
        self.entry_mobile = ctk.CTkEntry(self, width=300)
        self.entry_mobile.grid(row=5, column=1, padx=20, pady=10, sticky="w")

        # Special customer markdown toggle
        ctk.CTkLabel(self, text="Special Customer Markdown:", font=("Arial", 18, "bold")).grid(row=6, column=0, padx=20,
                                                                                               pady=10, sticky="e")
        self.toggle_special_customer_switch = ctk.CTkSwitch(self, text="Enable", command=self.toggle_special_customer)
        self.toggle_special_customer_switch.grid(row=6, column=1, padx=20, pady=10, sticky="w")

        # Product list display
        ctk.CTkLabel(self, text="Product List:", font=("Arial", 18, "bold")).grid(row=7, column=0, padx=20, pady=10,
                                                                                  sticky="e")
        self.product_list = ctk.CTkTextbox(self, width=700, height=150)
        self.product_list.grid(row=7, column=1, padx=20, pady=10)

        # Total products and price
        self.label_total_product = ctk.CTkLabel(self, text="Total Products: 0", font=("Arial", 18, "bold"))
        self.label_total_product.grid(row=8, column=0, padx=20, pady=10, sticky="e")
        self.label_total_price = ctk.CTkLabel(self, text="Total Price: ₹0.00", font=("Arial", 18, "bold"))
        self.label_total_price.grid(row=8, column=1, padx=20, pady=10, sticky="w")

        self.label_customer_details = ctk.CTkLabel(self, text="", font=("Arial", 18, "bold"))
        self.label_customer_details.grid(row=9, columnspan=2, padx=20, pady=10, sticky="n")

        # Reset and process buttons
        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=11, column=0, padx=20, pady=20)
        self.process_button = ctk.CTkButton(self, text="Process Billing", command=self.process_billing)
        self.process_button.grid(row=11, column=1, padx=20, pady=20)

        # Current date and time display
        self.label_datetime = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"))
        self.label_datetime.grid(row=10, columnspan=2, padx=20, pady=10)
        self.update_time()

    def add_product(self, event=None):
        product_name = self.entry_product_name.get().strip()
        if not product_name:
            msgbox.showwarning("Input Error", "Please enter a product name.")
            return

        self.entry_product_name.delete(0, ctk.END)

        try:
            quantity = int(self.entry_quantity.get())
            price_per_item = float(self.entry_price.get())

            self.products.append({
                'name': product_name,
                'quantity': quantity,
                'price_per_item': price_per_item,
                'total': quantity * price_per_item
            })

            self.update_product_list()
            self.entry_quantity.delete(0, ctk.END)
            self.entry_price.delete(0, ctk.END)

        except ValueError:
            msgbox.showerror("Input Error", "Please enter valid numeric values for quantity and price.")

    def update_product_list(self):
        self.product_list.delete("1.0", ctk.END)
        total_amount = sum(product['total'] for product in self.products)
        total_quantity = sum(product['quantity'] for product in self.products)

        for product in self.products:
            self.product_list.insert(ctk.END,
                                     f"{product['name']} - {product['quantity']} @ ₹{product['price_per_item']:.2f} each, Total: ₹{product['total']:.2f}\n")

        self.label_total_product.configure(text=f"Total Products: {total_quantity}")
        self.label_total_price.configure(text=f"Total Price: ₹{total_amount:.2f}")

    def toggle_special_customer(self):
        self.is_special_customer = not self.is_special_customer

    def process_billing(self):
        customer_name = self.entry_customer_name.get().strip()
        customer_city = self.entry_city.get().strip()
        customer_mobile = self.entry_mobile.get().strip()

        if self.is_special_customer:
            total_price = sum(product['total'] for product in self.products) * 0.90  # 10% discount
            msgbox.showinfo("Billing Summary",
                            f"Customer: {customer_name}\nCity: {customer_city}\nMobile: {customer_mobile}\nTotal after 10% discount: ₹{total_price:.2f}")
        else:
            total_price = sum(product['total'] for product in self.products)
            msgbox.showinfo("Billing Summary",
                            f"Customer: {customer_name}\nCity: {customer_city}\nMobile: {customer_mobile}\nTotal: ₹{total_price:.2f}")

    def reset_fields(self):
        self.products.clear()
        self.product_list.delete("1.0", ctk.END)
        self.entry_product_name.delete(0, ctk.END)
        self.entry_quantity.delete(0, ctk.END)
        self.entry_price.delete(0, ctk.END)
        self.entry_customer_name.delete(0, ctk.END)
        self.entry_city.delete(0, ctk.END)
        self.entry_mobile.delete(0, ctk.END)
        self.toggle_special_customer_switch.select()  # Reset switch
        self.label_total_product.configure(text="Total Products: 0")
        self.label_total_price.configure(text="Total Price: ₹0.00")

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_datetime.configure(text=current_time)
        self.after(1000, self.update_time)  # Update every second
