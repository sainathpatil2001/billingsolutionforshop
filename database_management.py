import sqlite3


# Database Initialization
def initialize_database():
    try:
        # Connect to the SQLite database (it will create one if it doesn't exist)
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()
        print('Database initialized.')

        # Create a table for billing records if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS billing_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                customer_name TEXT,
                customer_city TEXT,
                customer_mobile TEXT,
                date_time TEXT NOT NULL
            )
        ''')
        sqliteConnection.commit()
        print('Billing records table created.')

    except sqlite3.Error as error:
        print('Error occurred while initializing database - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


# Function to add a bill to the database
def add_bill(product_name, quantity, price, total, customer_name, customer_city, customer_mobile, date_time):
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Insert a new billing record
        cursor.execute('''
            INSERT INTO billing_records (product_name, quantity, price, total, customer_name, customer_city, customer_mobile, date_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product_name, quantity, price, total, customer_name, customer_city, customer_mobile, date_time))

        sqliteConnection.commit()
        print('Bill added successfully.')

    except sqlite3.Error as error:
        print('Error occurred while adding bill - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


# Function to search for a bill by customer name
def search_bills(customer_name):
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Fetch billing records by customer name
        cursor.execute('SELECT * FROM billing_records WHERE customer_name = ?', (customer_name,))
        records = cursor.fetchall()

        if records:
            for record in records:
                print(record)
        else:
            print('No records found for the customer:', customer_name)

    except sqlite3.Error as error:
        print('Error occurred while searching bills - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


# Function to update a bill by id
def update_bill(bill_id, product_name, quantity, price, total, customer_name, customer_city, customer_mobile,
                date_time):
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Update the billing record
        cursor.execute('''
            UPDATE billing_records
            SET product_name = ?, quantity = ?, price = ?, total = ?, customer_name = ?, customer_city = ?, customer_mobile = ?, date_time = ?
            WHERE id = ?
        ''', (product_name, quantity, price, total, customer_name, customer_city, customer_mobile, date_time, bill_id))

        sqliteConnection.commit()
        print('Bill updated successfully.')

    except sqlite3.Error as error:
        print('Error occurred while updating bill - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


# Function to retrieve all billing records
def get_all_bills():
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Fetch all billing records
        cursor.execute('SELECT * FROM billing_records')
        records = cursor.fetchall()

        if records:
            for record in records:
                print(record)
        else:
            print('No records found.')

    except sqlite3.Error as error:
        print('Error occurred while retrieving bills - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


# Example usage (You can remove this part later)
if __name__ == '__main__':
    initialize_database()  # Initialize the database
    # Add a bill (example)
    add_bill('Product A', 2, 100.0, 200.0, 'John Doe', 'City A', '1234567890', '2024-10-20 10:30:00')
    # Search for bills
    search_bills('John Doe')
    # Update a bill (example, use the actual id of the bill you want to update)
    # update_bill(1, 'Product A', 3, 100.0, 300.0, 'John Doe', 'City A', '1234567890', '2024-10-20 10:30:00')
    # Get all bills
    get_all_bills()
