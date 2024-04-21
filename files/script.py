import csv
import mysql.connector
from datetime import datetime
from decimal import Decimal

### Connect to database ###

print('\nThis script creates a new MySQL database called supermarket.\n')

db_host = input('Host: ')
db_user = input('User: ')
db_password = input('Password: ')

def connect_db():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
    )

### Insert tables ###

def create_database(connection):

    # Open cursor
    cursor = connection.cursor()

    # Supermarket Database
    cursor.execute("CREATE DATABASE supermarket")
    cursor.execute("USE supermarket")

    # Branch Table
    cursor.execute('''CREATE TABLE `Branch` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `city` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))'''
    )

    # Product Table
    cursor.execute('''CREATE TABLE `Product` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `type` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))'''
    )

    # Payment Table
    cursor.execute('''CREATE TABLE `Payment` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))'''
    )

    # Customer Type Table
    cursor.execute('''CREATE TABLE `Customer_type` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))'''
    )

    # Gender Table
    cursor.execute('''CREATE TABLE `Gender` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))'''
    )

    # Customer Table
    cursor.execute('''CREATE TABLE `Customer` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `customer_type_id` INT NOT NULL,
        `gender_id` INT NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `fk_customer_type`
            FOREIGN KEY (`customer_type_id`)
            REFERENCES `Customer_type` (`id`),
        CONSTRAINT `fk_gender`
            FOREIGN KEY (`gender_id`)
            REFERENCES `Gender` (`id`))'''
    )

    # Sales Table
    cursor.execute('''CREATE TABLE `Sales` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `branch_id` INT NOT NULL,
        `product_id` INT NOT NULL,
        `payment_id` INT NOT NULL,
        `customer_id` INT NOT NULL,
        `invoice_id` VARCHAR(11) NOT NULL,
        `datetime` DATETIME NOT NULL,
        `price` DECIMAL(6,2) NOT NULL,
        `quantity` INT NOT NULL,
        `rating` DECIMAL(3,1) NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `fk_branch`
            FOREIGN KEY (`branch_id`)
            REFERENCES `supermarket`.`Branch` (`id`),
        CONSTRAINT `fk_payment`
            FOREIGN KEY (`payment_id`)
            REFERENCES `supermarket`.`Payment` (`id`),
            CONSTRAINT `fk_product`
            FOREIGN KEY (`product_id`)
            REFERENCES `supermarket`.`Product` (`id`),
        CONSTRAINT `fk_customer`
            FOREIGN KEY (`customer_id`)
            REFERENCES `supermarket`.`Customer` (`id`))'''
    )

    # Close cursor
    cursor = cursor.close()

### Foreign Key List ###

fk_gender_list = ['Male', 'Female']
fk_customer_type_list = ['Member', 'Normal']
fk_branch_list = ['Yangon', 'Mandalay', 'Naypyitaw']
fk_product_list = ['Electronic accessories', 'Fashion accessories', 'Food and beverages',
                   'Health and beauty', 'Home and lifestyle', 'Sports and travel']
fk_payment_list = ['Cash', 'Credit card', 'Ewallet']

### First Insertion ###

def fk_insert_data(connection):

    # Open cursor
    cursor = connection.cursor()

    # Insert Branch
    for i in range(len(fk_branch_list)):
        sql_branch = "INSERT INTO Branch (city) VALUES (%s)"
        cursor.execute(sql_branch, (fk_branch_list[i],))
        connection.commit()

    # Insert Product
    for i in range(len(fk_product_list)):
        sql_product = "INSERT INTO Product (type) VALUES (%s)"
        cursor.execute(sql_product, (fk_product_list[i],))
    
    # Insert Payment
    for i in range(len(fk_payment_list)):
        sql_payment = "INSERT INTO Payment (name) VALUES (%s)"
        cursor.execute(sql_payment, (fk_payment_list[i],))
    
    # Insert Customer Type
    for i in range(len(fk_customer_type_list)):
        sql_customer_type = "INSERT INTO Customer_type (name) VALUES (%s)"
        cursor.execute(sql_customer_type, (fk_customer_type_list[i],))

    # Insert Gender
    for i in range(len(fk_gender_list)):
        sql_gender = "INSERT INTO Gender (name) VALUES (%s)"
        cursor.execute(sql_gender, (fk_gender_list[i],))

    # Insert Customer
    for i in range(len(fk_customer_type_list)):
        for j in range(len(fk_gender_list)):
            sql_customer = "INSERT INTO Customer (customer_type_id, gender_id) VALUES (%s, %s)"
            cursor.execute(sql_customer, (i+1, j+1))
            connection.commit()

    # Close cursor
    cursor = cursor.close()

### Second Insertion ###

def insert_data(line, connection):

    # 0 - Invoice ID, 1 - City, 2 - Customer type, 3 - Gender, 4 - Product line
    # 5 - Unit price, 6 - Quantity, 7 - Datetime, 8 - Payment, 9 - Rating

    # Open cursor
    cursor = connection.cursor()

    # Insert Sales

    consumer_adj = fk_customer_type_list.index(line[2]) * 2 + fk_gender_list.index(line[3]) + 1 # Permutation adjustment
    sql_sales = "INSERT INTO Sales (branch_id, product_id, payment_id, customer_id, invoice_id, datetime, price, quantity, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_sales, (fk_branch_list.index(line[1])+1, fk_product_list.index(line[4])+1,
                               fk_payment_list.index(line[8])+1, consumer_adj,
                               line[0], line[7], line[5], line[6], line[9]))

    # Close cursor
    cursor.close()
    print(line) # Debug

### Data processing ###

def read_csv_insert_db(file_name, connection):
    with open(file_name, 'r') as file_csv:
        read_csv = csv.reader(file_csv)
        next(read_csv) # Skip header
        try:

            # Start SQL transaction
            connection.start_transaction()

            # Create database
            create_database(connection)

            # Start first insertion
            fk_insert_data(connection)

            # Start second insertion
            for line in read_csv:
                del line[1] # Remove useless data (branch name)
                del line[7:9] # Remove useless data (tax 5%, total)
                del line[10:13] # Remove useless data (cogs, gross margin percentage, gross income)
                line[5] = Decimal(line[5]) # Convert to DECIMAL
                line[6] = int(line[6]) # Convert to INT
                line[7] = datetime.strptime(f'{line[7]} {line[8]}', '%m/%d/%Y %H:%M') # DATETIME
                del line[8] # Remove time since it was merged into line 7
                line[9] = Decimal(line[9]) # Convert to DECIMAL
                insert_data(line, connection) # Start insertion

            # connection.commit() # Save insertions

            connection.commit()
            print('\nProcess finished!')
        except Exception as e:
            print('Error inserting data:', e)
            cursor = connection.cursor()
            cursor.execute("DROP DATABASE supermarket")
            cursor.close()
            connection.close()
            exit(1)
        finally:
            connection.close()

if __name__ == '__main__':
    # Start connection to database
    connection = connect_db()
    # Begin data process
    read_csv_insert_db('src\\supermarket_sheet.csv', connection)
