import sqlite3
import csv
import datetime

# ----------------------------------------------------------------------------------------------------------------------#
# set var for files
# ----------------------------------------------------------------------------------------------------------------------#
print('start, loading values')
# menu items
item_index = 'item_index'

# pre-defined paths for csv files
inventory_list = "DataSets\Subcontent\Inventory.csv"
sub_inventory_list = "DataSets\Subcontent\Sub_Inventory.csv"
category_list = "DataSets\Subcontent\Category.csv"
current_ticket = []
current_order_number = ''

# Date and time
date_and_time = datetime.datetime.now()
dates = date_and_time.date()
times = date_and_time.strftime("%I:%M:%S %p")
date = str(dates)
time = str(times)
date_time = 'DATE | ' + date + ' TIME | ' + time
print(date_time)
temp_order = [100, 0.00, 0.00, 0.00, date_time, 0, 0, 10001, 1001, 10000001, 0]

# ----------------------------------------------------------------------------------------------------------------------#
# initialization process
# ----------------------------------------------------------------------------------------------------------------------#
order_column = ['Order_number',
                'Total',
                'Tax',
                'Subtotal',
                'Order_date',
                'Order_discounts',
                'Credit',
                'User_ID',
                'Customer_ID',
                'Payment_ID',
                'Points']

item_columns = ['Item_ID',
                'Item_name',
                'Price',
                'Category_ID',
                'Subcategory_ID']

category_columns = [
    'Category_ID',
    'Category_name'
]

items_in_orders_columns = [
                           'Item_ID',
                           'Order_ID',
                           'IIO_name',
                           'IIO_price',
                           'IIO_tax',
                           'IIO_discount'
                           ]

ItemCategory = 'ItemCategory'
Orders = 'Orders'
ItemsIndex = 'ItemsIndex'
ItemsInOrders = 'ItemsInOrders'


# ----------------------------------------------------------------------------------------------------------------------#
# Data base
# ----------------------------------------------------------------------------------------------------------------------#

def initialization_process():
    global category_columns
    global item_columns
    global order_column
    global current_order_number
    global temp_order
    global ItemCategory
    global Orders
    global ItemsIndex
    print('check1-------------------------')
    connections = sqlite3.connect('DataSets/Subcontent/data_mang.db')
    sql_cmd = connections.cursor()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS ItemCategory('
                    'Category_ID INTEGER PRIMARY KEY,'
                    'Category_name TEXT'
                    ')')
    sql_cmd.execute("SELECT * FROM ItemCategory")
    item_category_list = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS SubcategoryIndex('
                    'Subcategory_number INTEGER PRIMARY KEY,'
                    'Subcategory_item TEXT,'
                    'Subcategory_price REAL,'
                    'Subcategory_name TEXT,'
                    'Subcategory_ID INTEGER'
                    ')')
    sql_cmd.execute("SELECT * FROM SubcategoryIndex")
    Subcategory_index_list = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS ItemsIndex('
                    'Item_ID INTEGER PRIMARY KEY,'
                    'Item_name TEXT,'
                    'Price REAL,'
                    'Category_ID TEXT,'
                    'Subcategory_ID INTEGER,'
                    'FOREIGN KEY (Category_ID) REFERENCES ItemCategory(Category_ID),'
                    'FOREIGN KEY (Subcategory_ID) REFERENCES SubcategoryIndex(Subcategory_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM ItemsIndex")
    item_index_list = sql_cmd.fetchall()

    '''sql_cmd.execute(' CREATE TABLE IF NOT EXISTS ItemsWithSubcat('
                    'IWS_number INTEGER,'
                    'Item_ID INTEGER,'
                    'IIO_name TEXT,'
                    'IIO_price REAL,'
                    'Subcategory_ID, INTEGER,'
                    'FOREIGN KEY (Item_ID) REFERENCES ItemsIndex(Item_ID),'
                    'FOREIGN KEY (Subcategory_ID) REFERENCES Subcategory(Subcategory_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM ItemsWithSubcat")
    items_with_sub = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS ItemCategory('
                    'Category_ID INTEGER PRIMARY KEY,'
                    'Category_name TEXT'
                    ')')
    sql_cmd.execute("SELECT * FROM ItemCategory")
    item_category = sql_cmd.fetchall()'''

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Orders('
                    'Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'Order_number INTEGER,'
                    'Total REAL,'
                    'Tax REAL,'
                    'Subtotal REAL,'
                    'Order_date TEXT,'
                    'Order_discounts INTEGER,'
                    'Credit REAL,'
                    'User_ID INTEGER,'
                    'Customer_ID INTEGER,'
                    'Payment_ID INTEGER,'
                    'Points INTEGER,'
                    'FOREIGN KEY (User_ID) REFERENCES Users(User_ID),'
                    'FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),'
                    'FOREIGN KEY (Payment_ID) REFERENCES Payments(Payment_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM Orders")
    orders = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS ItemsInOrders('
                    'IIO_number INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'Item_ID INTEGER,'
                    'Order_ID INTEGER,'
                    'IIO_name TEXT,'
                    'IIO_price REAL,'
                    'IIO_tax REAL,'
                    'IIO_discount INTEGER,'
                    'FOREIGN KEY (Item_ID) REFERENCES ItemsIndex(Item_ID),'
                    'FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM ItemsInOrders")
    items_in_Orders = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Employees('
                    'Employee_ID INTEGER PRIMARY KEY,'
                    'Employee_firstname TEXT,'
                    'Employee_lastname TEXT,'
                    'Employee_phone TEXT,'
                    'Employee_email TEXT,'
                    'Employee_street1 TEXT,'
                    'Employee_street2 TEXT,'
                    'Employee_city TEXT,'
                    'Employee_state TEXT,'
                    'Employee_zip TEXT,'
                    'Employee_birth TEXT,'
                    'Employee_role TEXT'
                    ')')
    sql_cmd.execute("SELECT * FROM Employees")
    employees = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Customers('
                    'Customer_ID INTEGER PRIMARY KEY,'
                    'Customer_firstname TEXT,'
                    'Customer_lastname TEXT,'
                    'Customer_phone TEXT,'
                    'Customer_email TEXT,'
                    'Customer_street1 TEXT,'
                    'Customer_street2 TEXT,'
                    'Customer_city TEXT,'
                    'Customer_state TEXT,'
                    'Customer_zip TEXT,'
                    'Customer_birth TEXT,'
                    'Customer_Points INTEGER'
                    ')')
    sql_cmd.execute("SELECT * FROM Customers")
    customers = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Suppliers('
                    'Supplier_ID INTEGER PRIMARY KEY,'
                    'Supplier_name TEXT,'
                    'Supplier_contact TEXT,'
                    'Supplier_address TEXT,'
                    'Supplier_phone TEXT,'
                    'Supplier_email TEXT'
                    ')')
    sql_cmd.execute("SELECT * FROM Suppliers")
    suppliers = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Inventory('
                    'Item_ID INTEGER,'
                    'Quantity INTEGER,'
                    'Cost REAL,'
                    'FOREIGN KEY (Item_ID) REFERENCES ItemsIndex(Item_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM Inventory")
    inventory = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Payments('
                    'Payment_ID INTEGER PRIMARY KEY,'
                    'Payment_date TEXT,'
                    'Amount REAL,'
                    'Payment_method TEXT,'
                    'Payment_status TEXT'
                    ')')
    sql_cmd.execute("SELECT * FROM Payments")
    payments = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Discounts('
                    'Discount_ID INTEGER PRIMARY KEY,'
                    'Discount_name TEXT,'
                    'Discount_percentage INTEGER'
                    ')')
    sql_cmd.execute("SELECT * FROM Discounts")
    discounts = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS Returns('
                    'Return_ID INTEGER PRIMARY KEY,'
                    'Order_ID INTEGER,'
                    'Return_date TEXT,'
                    'Return_reason TEXT,'
                    'Return_amount REAL,'
                    'FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM Returns")
    returns = sql_cmd.fetchall()

    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS StoreCredit('
                    'Credit_ID INTEGER PRIMARY KEY,'
                    'Customer_ID INTEGER,'
                    'Credit_amount REAL,'
                    'Expiration_date TEXT,'
                    'FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)'
                    ')')
    sql_cmd.execute("SELECT * FROM StoreCredit")
    store_credit = sql_cmd.fetchall()
    print('check1, tables created or loaded')
    print('check2')

    # ------------------------------------------------------------------------------------------------------------------#
    # Data base checks for key tables in the system.
    """ 
        If no data exist at the time of running the application 
        a protocol needs to be created to handle initial user setup, 
        consider toplevel condition that will take the 
        user to a different GUI object, using new module. 5/30/23
    """
    # ------------------------------------------------------------------------------------------------------------------#

    # ------------------------------------------------------------------------------------------------------------------#
    # database check for orders
    # ------------------------------------------------------------------------------------------------------------------#
    print('check3')
    if not orders:
        print(' New order log, starting at 100 ')
        insert_into_orders = f"INSERT INTO {Orders} ({', '.join(order_column)})" \
                             f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        sql_cmd.execute(insert_into_orders, temp_order)
        current_order_number = 101
    else:
        print('Order log located')
        last_order = orders[-1]
        last_order_number = last_order[1]
        current_order_number = last_order_number + 1
        print('Last order:', last_order, '\n' +
              'Last order number:', last_order[1], '\n' +
              'Current order number:', current_order_number)

    # ------------------------------------------------------------------------------------------------------------------#
    # database check for item index/inventory
    # ------------------------------------------------------------------------------------------------------------------#
    print('check4')
    if not item_index_list:
        print('loading inventory from backup csv files')
        with open(inventory_list, 'r') as item_list_csv:
            read_item_list = csv.reader(item_list_csv)
            next(read_item_list)
            for item_data in read_item_list:
                print(item_data)
                item_ID = item_data[0]
                item_name = item_data[1]
                item_price = item_data[2]
                category_name = item_data[3]
                sub_category_name = item_data[4]
                item_row_data = (item_ID, item_name, item_price, category_name, sub_category_name)
                insert_into_item_index = f"INSERT INTO {ItemsIndex} ({', '.join(item_columns)})" \
                                         f"VALUES (?, ?, ?, ?, ?)"
                sql_cmd.execute(insert_into_item_index, item_row_data)
            rows_in_list = len(item_index_list)
            print('Created item index list:', rows_in_list, 'items')
        item_list_csv.close()
    else:
        print('Item index located')
    rows_in_list = len(item_index_list)
    print('item index list:', rows_in_list, 'items')
    # ------------------------------------------------------------------------------------------------------------------#
    # database check for category
    # ------------------------------------------------------------------------------------------------------------------#

    print('check5')
    if not item_category_list:
        print('loading inventory from backup csv files')
        with open(category_list, 'r') as category_list_csv:
            read_category_list = csv.reader(category_list_csv)
            next(read_category_list)
            for cat_row in read_category_list:
                cat_num = cat_row[0]
                cat_name = cat_row[1]
                cat_row_data = (cat_num, cat_name)
                insert_into_item_category = f"INSERT INTO {ItemCategory} ({', '.join(category_columns)})" \
                                            f"VALUES (?, ?)"
                sql_cmd.execute(insert_into_item_category, cat_row_data)
        category_list_csv.close()
    else:
        print('Category list located')

    print('CheckOmega')
    sql_cmd.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sql_cmd.fetchall()
    print("Tables in the database:", len(tables))

    connections.commit()
    connections.close()


# ----------------------------------------------------------------------------------------------------------------------#
# Write to database objects
# ----------------------------------------------------------------------------------------------------------------------#


def log_to_order(order_passed):
    global category_columns
    global item_columns
    global order_column
    global current_order_number
    global items_in_orders_columns
    # global var
    global ItemsInOrders
    global Orders
    link = sqlite3.connect('DataSets/Subcontent/data_mang.db')
    sql_cmd = link.cursor()
    print('--------------------- logg process 1 ---------------------')

    print(order_passed)

    insert_into_orders = f"INSERT INTO {Orders} ({', '.join(order_column)})" \
                         f"VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    sql_cmd.execute(insert_into_orders, order_passed)
    link.commit()
    link.close()

def log_to_item_orders(ticket_passed):
    global category_columns
    global item_columns
    global order_column
    global current_order_number
    global items_in_orders_columns
    # global var
    global ItemsInOrders
    global Orders
    link = sqlite3.connect('DataSets/Subcontent/data_mang.db')
    sql_cmd = link.cursor()
    print('--------------------- logg process 2 ---------------------')
    print(ticket_passed)
    insert_into_item_in_orders = f"INSERT INTO {ItemsInOrders} ({', '.join(items_in_orders_columns)})" \
                                 f"VALUES ( ?, ?, ?, ?, ?, ?)"
    sql_cmd.execute(insert_into_item_in_orders, ticket_passed)
    link.commit()
    link.close()

# ----------------------------------------------------------------------------------------------------------------------#
# Read from Database
# ----------------------------------------------------------------------------------------------------------------------#


class GUIObjectList:
    def __init__(self):
        super().__init__()
        self.link = sqlite3.connect('DataSets/Subcontent/data_mang.db')
        self.sql_cmd = self.link.cursor()

    def tab_category_list(self):
        print('--------------------- menu process 1 ---------------------')
        self.sql_cmd.execute("SELECT * FROM ItemCategory")
        item_categories = self.sql_cmd.fetchall()
        tabs_to_pass = []
        for cat in item_categories:
            cat_name = cat[1]
            cat_number = cat[0]
            tabs_to_pass.append([cat_name, cat_number])
        return tabs_to_pass

    def item_in_list(self, cat_number_pass):
        print('--------------------- menu process 2 ---------------------')
        self.sql_cmd.execute(f"SELECT * FROM ItemsIndex WHERE Category_ID = {cat_number_pass} ")
        item_button_index = self.sql_cmd.fetchall()
        items_to_pass = []
        for items in item_button_index:
            items_name = items[1]
            items_cost = items[2]
            items_id = items[0]
            items_to_pass.append([items_name, items_cost, items_id])
        return items_to_pass

    def get_order_number(self):
        self.sql_cmd.execute("SELECT * FROM Orders")
        orders_in_list = self.sql_cmd.fetchall()
        last_order = orders_in_list[-1]
        last_order_number = last_order[1]
        new_order_number = last_order_number + 1
        return new_order_number

    def logged_tickets(self):
        pass_order_list = []
        pass_ticket_list = []
        print('\n' + '\n' + 'log check1' + '\n' + '\n')
        self.sql_cmd.execute("SELECT * FROM Orders")
        orders_list = self.sql_cmd.fetchall()
        for order in orders_list:
            pass_order_list.append(order)

        self.sql_cmd.execute("SELECT * FROM ItemsInOrders")
        IIO_list = self.sql_cmd.fetchall()
        for ticket in IIO_list:
            pass_ticket_list.append(ticket)
        return pass_order_list, pass_ticket_list

    def close_database(self):
        self.link.commit()
        self.link.close()
