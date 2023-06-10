import sqlite3
import csv
import datetime
import Order_Number_Counter as onc

#----------------------------------------------------------------------------------------------------------------------#
# set var for files
#----------------------------------------------------------------------------------------------------------------------#
print('start, loading values')
# menu items
item_index = 'item_index'
item_columns = ['product_number', 'product_name', 'price']

#pre-defined paths for csv files
section_cvs = "Master_List.csv"
full_items_csv = "DataSets/cat1.csv", "DataSets/cat2.csv", "DataSets/cat3.csv", "DataSets/cat4.csv"


master_log = "DataSets/Subcontent/Order_Log.csv"


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

#----------------------------------------------------------------------------------------------------------------------#
# initialization process
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
# Data base is structured off of seven tables, below shows the header structure.

#ItemsIndex:
# Item_ID, Item_name, Price, Category_name

#Orders
# Order_ID, Order_number, Total, Tax, Subtotal, Order_discounts, Credit, User_ID, Customer_ID, CRP_ID, Customer_Points

#ItemsInOrders
# IIO_number, Item_ID,  IIO_name, IIO_price, IIO_tax, IIO_discount, Order_ID

#ItemCategory
# Category_ID, Category_name

#Users
# User_ID, User_firstname, User_lastname, User_phone, User_email, User_street1, User_street2, User_city, User_state,
# User_zip, User_birth

#Customers
# Customer_ID, Customer_firstname, Customer_lastname, Customer_phone, Customer_email, Customer_street1,
# Customer_street2, Customer_city, Customer_state, Customer_zip, Customer_birth, Customer_Points



def initialization_process():
    print('check1-------------------------')
    connections = sqlite3.connect('DataSets/Subcontent/data_mang.db')
    sql_cmd = connections.cursor()
    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS item_index('
                    'product_number TEXT,'
                    'product_name TEXT, '
                    'price REAL'
                    ')')
    sql_cmd.execute("SELECT * FROM item_index")
    item_index_list = sql_cmd.fetchall()
    sql_cmd.execute(' CREATE TABLE IF NOT EXISTS order_logged('
                    'Order_number REAL,'
                    'Date_time TEXT,'
                    'Total REAL,'
                    'Tax REAL,'
                    'Subtotal REALl'
                    'Order_discount REAL,'
                    'Credit REAL'
                    ')')
    sql_cmd.execute("SELECT * FROM order_logged")
    order_logged = sql_cmd.fetchall()

    global current_order_number

    try:
        current_order_number = onc.get_last_order_number()

        with open(master_log, "a", newline='') as order_log:
            dated = csv.writer(order_log, delimiter=',', quotechar='"')
            dated.writerow([date_time, current_order_number, 'NEW LOG APPENDED', '0.00'])
            order_log.close()

            print("Found log")
    except FileNotFoundError:
        with open(master_log, "x", newline='') as order_log:
            dated = csv.writer(order_log,  delimiter=',', quotechar='"')
            dated.writerow([date_time, 0, 'Start NEW LOG', '0.00'])
            order_log.close()
            print('Created log')

        current_order_number = 0
    # ---------------------#
    # used to pull all the menu items into one tabel, to be used for button push methods.
    # ---------------------#
    item_index_row = len(item_index_list)
    if item_index_row == 0:
        print('Importing data from Tabels')
        for item_list in full_items_csv:
            with open(item_list, 'r') as item_list_csv:
                read_list_csv = csv.reader(item_list_csv)
                next(read_list_csv)
                for item_data in read_list_csv:
                    product_number = item_data[0]
                    product_name = item_data[1]
                    price = item_data[2]
                    form_headers = (product_number, product_name, price)
                    pull_items = f"INSERT INTO {item_index} ({', '.join(item_columns)}) VALUES (?, ?, ?)"
                    sql_cmd.execute(pull_items, form_headers)
    elif item_index_row >= 1:
        print('found index of items')

    sql_cmd.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sql_cmd.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

    connections.commit()
    connections.close()
    print("current_order_number", current_order_number)

def log_order(order_placed):
    pass


connections = sqlite3.connect('DataSets/Subcontent/data_mang.db')
sql_cmd = connections.cursor()
sql_cmd.fetchall()
print(item_index)
