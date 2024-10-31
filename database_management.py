import sqlite3

def initialize_database():
    """Initialize the SQLite database and create the Bills and Bill Items tables."""
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()
        print('Database initialized.')

        # Create the Bills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_city TEXT NOT NULL,
                customer_mobile TEXT NOT NULL,
                bill_date TEXT DEFAULT (DATETIME('now', 'localtime')),
                total_price REAL NOT NULL
            )
        ''')

        # Create the Bill Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bill_Items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price_per_item REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (bill_id) REFERENCES Bills (bill_id) ON DELETE CASCADE
            )
        ''')

        sqliteConnection.commit()
        print('Tables created successfully.')

    except sqlite3.Error as error:
        print('Error occurred while initializing database - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


#add bill to the database
def add_bill(customer_name, customer_city, customer_mobile, total_price, items):
    """Add a new bill to the database, including associated items."""
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Insert into Bills table
        cursor.execute('''
            INSERT INTO Bills (customer_name, customer_city, customer_mobile, total_price)
            VALUES (?, ?, ?, ?)
        ''', (customer_name, customer_city, customer_mobile, total_price))

        # Get the last inserted bill ID
        bill_id = cursor.lastrowid

        # Insert associated items into Bill_Items table
        for item in items:
            cursor.execute('''
                INSERT INTO Bill_Items (bill_id, product_name, quantity, price_per_item, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (bill_id, item['product_name'], item['quantity'], item['price_per_item'], item['total_price']))

        sqliteConnection.commit()
        print('Bill and items added successfully.')
        return True  # Success

    except sqlite3.Error as error:
        print('Error while adding bill - ', error)
        return False  # Failure

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')



def update_bill(bill_id, customer_name, customer_city, customer_mobile, total_price, items):
    """Update an existing bill and its items in the database."""
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Update the Bills table
        cursor.execute('''
            UPDATE Bills
            SET customer_name = ?, customer_city = ?, customer_mobile = ?, total_price = ?
            WHERE bill_id = ?
        ''', (customer_name, customer_city, customer_mobile, total_price, bill_id))

        # Delete old items
        cursor.execute('DELETE FROM Bill_Items WHERE bill_id = ?', (bill_id,))

        # Insert new items
        for item in items:
            cursor.execute('''
                INSERT INTO Bill_Items (bill_id, product_name, quantity, price_per_item, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (bill_id, item['product_name'], item['quantity'], item['price_per_item'], item['total_price']))

        sqliteConnection.commit()
        print('Bill updated successfully.')

    except sqlite3.Error as error:
        print('Error while updating bill - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')


def delete_bill(bill_id):
    """Delete a bill from the database, along with its items."""
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        cursor.execute('DELETE FROM Bills WHERE bill_id = ?', (bill_id,))
        sqliteConnection.commit()

        print('Bill deleted successfully.')

    except sqlite3.Error as error:
        print('Error while deleting bill - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')

def search_bills(query):
    """Search bills in the database based on the query."""
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

def view_bills():
    """Retrieve and display all bills and their items."""
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        cursor.execute('SELECT * FROM Bills')
        bills = cursor.fetchall()

        for bill in bills:
            bill_id = bill[0]
            print(f'Bill ID: {bill_id}, Customer Name: {bill[1]}, City: {bill[2]}, Mobile: {bill[3]}, Date: {bill[4]}, Total Price: {bill[5]}')

            # Fetch items associated with this bill
            cursor.execute('SELECT * FROM Bill_Items WHERE bill_id = ?', (bill_id,))
            items = cursor.fetchall()

            for item in items:
                print(f'    Item: {item[2]}, Quantity: {item[3]}, Price per Item: {item[4]}, Total Price: {item[5]}')

        sqliteConnection.commit()

    except sqlite3.Error as error:
        print('Error while viewing bills - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')

def get_next_bill_id():
    """Retrieve the next available bill ID for user input."""
    try:
        sqliteConnection = sqlite3.connect('billing_solution_database.db')
        cursor = sqliteConnection.cursor()

        # Query to get the maximum bill_id from the Bills table
        cursor.execute('SELECT MAX(bill_id) FROM Bills')
        max_id = cursor.fetchone()[0]

        # If there are no bills, the next ID will be 1
        next_id = 1 if max_id is None else max_id + 1
        return next_id

    except sqlite3.Error as error:
        print('Error while fetching next bill ID - ', error)
        return None

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed.')



# Example Usage
initialize_database()
