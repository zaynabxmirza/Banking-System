"""
Name: Zaynab Mirza
Date: 01/12/2022
Objective: Application for Entrepreneur
Programme name: BEng Software engineering
Module title: Computer science fundamentals (SWE4207)
assessment title: Design, development, and testing
student ID: 2202467
marking tutor: Dr Mohammed Benmubarak
date of submission: 13/01/22
"""
import sqlite3 #allows access to API library to connect to sqlite3
import bcrypt # hashes and verifies passwords
import maskpass # hides input of password
import time # allows access to real time
import datetime # allows access to real date and time
import string # allows use of punctuation

#connect to database in current directory
con = sqlite3.connect("sustainable.db")
# create a cursor
cur = con.cursor()

# create tables for the database
def create_db_tables ():
    """Creates database tables if not already exists"""
    cur = con.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        user_role TEXT NOT NULL
    );
    """)
 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        customerid INTEGER PRIMARY KEY AUTOINCREMENT,
        forename TEXT NOT NULL,
        surname TEXT,
        dob DATE NOT NULL
    );
    """)
 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS address (
        addressid INTEGER PRIMARY KEY AUTOINCREMENT,
        streetnumber INTEGER,
        firstline TEXT NOT NULL,
        postcode TEXT,
        region TEXT NOT NULL,
        country TEXT NOT NULL,
        customerid INTEGER NOT NULL,
        FOREIGN KEY(customerid) REFERENCES customer(customerid)
    );
    """)
 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS account (
        accountid INTEGER PRIMARY KEY AUTOINCREMENT,
        balance REAL NOT NULL,
        opendate DATE NOT NULL,
        closedate DATE,
        status TEXT NOT NULL DEFAULT "ACTIVE",
        customerid INTEGER NOT NULL,
        FOREIGN KEY(customerid) REFERENCES customer(customerid)
    );
    """)
 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transact (
        transactid INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        date DATE NOT NULL,
        accountid INTEGER NOT NULL,
        FOREIGN KEY(accountid)REFERENCES account(accountid)
    );
    """)

# username: admin12
# password: Admin123#

# function to login
def login():
    """function uses bcrypt to check if user is in database with matching password"""
    # to allow user to exit the application if they wish to 
    print("Welcome to the banking application!")
    username= input("Please login by entering your username: "
                    ).strip()
    # Check if the username is at least one letter long
    if len(username) <= 6:
        print("Username must be at least six characters long. Please try again.")
        login()

    # Prompt the user for their password, and display asterisks as they type
    password_to_check = maskpass.askpass(prompt = f"Please enter password for <{username}>: ", mask='*').strip().encode('utf-8')
    password_to_check = password_to_check.decode()

    # Check if the password is at least 8 characters long and contains at least one number, one uppercase letter, and one special character
    if len(password_to_check) >= 8 and any(c.isdigit() for c in password_to_check) and any(c.isupper() for c in password_to_check) and any(c in string.punctuation for c in password_to_check):
        print('Password meets requirements')
    else:
        print("Wrong password, please try again.")
        login()

    cur.execute(""" SELECT password, user_role FROM user
                    WHERE username =?""", (username,)) 
    result= cur.fetchall()
    
    if len(result) > 0:
        fetched_password = result[0][0]
        fetched_role = result[0][1]
        if bcrypt.checkpw(password_to_check.encode('utf-8'), fetched_password): 
            print(f"Record match found with <{fetched_role.upper()}> role.")
        else:
            print("Incorrect details have been entered, try again, ")# to handle the error in case a user logs in with no existing account
    else:
        print("No records were found for the given username.")
        login()


# the main menu to carry out all functions
def main_menu ():
    """Allows user to choose operation"""
    create_db_tables () #creates database tables if does not exist
    print("""
1. User menu
2. Customer menu
3. Account menu
4. Transaction menu
5. Exit """)

# while loop to handle errors
    menu_choice = input("Please choose options between (1-5): ")
    menu_option = ["1", "2", "3", "4", "5"]
    
    while menu_choice not in menu_option:
        menu_choice = input("Error!, You have entered the wrong input, please choose options between (1-5):  ")

    if menu_choice == "1":
        user_menu()
    elif menu_choice == "2":
        customer_menu()
    elif menu_choice == "3":
        account_menu()
    elif menu_choice == "4":
        transaction_menu()
    else:
        answer = input("Would you like to exit? (Y/N): ").upper()
        if answer == 'Y':
            print("Exiting program...")
            time.sleep(2)
            print("You have exited the program")
            con.close()
            exit()
        else:
            print("Continuing...")
            main_menu()


def user_menu():
    """Allows choosing operations related to user management"""
    print("""
1. Create a user account
2. View all user accounts
3. View single user account
4. Update a user account 
5. Delete a user
6. Back to main menu""")

# while loop to handle errors
    menu_choice = input("Please choose options between (1-6): ")
    menu_option = ["1", "2", "3", "4", "5", "6"]
    while menu_choice not in menu_option:
        menu_choice = input("Error!, You have entered the wrong input, please choose options between (1-6):  ")

    if menu_choice == "1":
        create_user()
        # create user
    elif menu_choice == "2":
        view_all_users()
        # view all users
    elif menu_choice == "3":
        view_single_user()
        # view single user
    elif menu_choice == "4":
        update_user()
        # update user
    elif menu_choice == "5":
        delete_user()
        # delete user
    elif menu_choice == "6":
        main_menu()
        # back to main menu
        


def create_user():
    while True:
        # prompt the user for their username
        username = input("Please enter your username: ").strip()
        
        # check the length of the username
        if len(username) >= 6:
            # if the length is greater than or equal to 6, break out of loop
            print(f"Successfully added: {username}.")
            break
        else:
            # if the length is not 6 letters, print an error message and prompt the user to try again
            print("Error: username must be at least 6 characters long. Please try again.")
        
    while True:
        # Prompt the user for their password, and display asterisks as they type
        password_to_check = maskpass.askpass(prompt = f"Please enter password for <{username}>: ", mask='*').strip().encode('utf-8')
        password_to_check = password_to_check.decode()

        # Check if the password is at least 8 characters long and contains at least one number, one uppercase letter, and one special character
        if len(password_to_check) >= 8 and any(c.isdigit() for c in password_to_check) and any(c.isupper() for c in password_to_check) and any(c in string.punctuation for c in password_to_check):
            print('password meets requirements')
            password = hash_password(password_to_check) 
            break
        else:
            print('password does not meet requirements')
    
    # give user role 
    role_choice = input("Is user admin? (Y/N): ").strip().upper()
    if role_choice == "Y":
        user_role = "admin"
    else:
        user_role = "default"
    
    # send values to be inserted as a record in database 
    store_users(username, password, user_role)
    
    print(f"The following details have been entered",
    f"\nusername = {username}",
    f"\npassword = {password}",
    f"\nuser role = {user_role}")
    
    # choice to create a new user
    add_another = input("Would you like to add another [Y/N]: "
                            ).strip().upper()
    
    # handle errors
    while add_another not in ["Y","N"]:
        add_another = input("Invalid option, choose [Y/N]"
                        ).strip().upper()
    if add_another == 'Y':
        create_user()
    else:
        user_menu()
    
def hash_password(plain_password:str):
    """Hash and return user_password"""
    salt = bcrypt.gensalt()
    hashed_passsword = bcrypt.hashpw(plain_password.encode(),salt)
    return hashed_passsword


def store_users(username:str, password:str, user_role:str):
    """accepts and stores users data into the database"""
    cur.execute("INSERT INTO user VALUES (?,?,?) ",
                    (   
                        username,
                        password,
                        user_role
                    )
    
                )
    con.commit()

def view_all_users():
    """output all user records"""
    cur = con.cursor()
    print("{:<12} {:<12} {:<10}"
    .format("username","password", "user_role")
    )
    for row in cur.execute("SELECT username, password, user_role FROM user"):
        # Convert the values in the row to strings
        row_str = [str(x) for x in row]        
        print("{:<12} {:<12} {:<10}"
        .format(row_str[0], "********" ,row_str[2])
        )
    #return to menu
    user_menu()

def view_single_user():
    """output user record for the given username"""
    cur = con.cursor()
    while True:
        # Prompt the user to enter their username
        username = input("Enter the username of the user you would like to view: ")
        try:
            # Check if the username exists in the user table
            for row in cur.execute("SELECT * FROM user WHERE username = ?", (username,)):
                # Convert the values in the row to strings
                row_str = [str(x) for x in row]

                print("{:<12} {:<12} {:<10}".format("username","password", "user_role"))
                print("{:<12} {:<12} {:<10}".format(row_str[0], "********", row_str[2]))
                
            # If the username exists, break out of the loop
            break
        except sqlite3.OperationalError:
            # If the username doesn't exist, print an error message and continue the loop
            username= input("Username not found. Please try again.")
    #return to menu
    user_menu()

def update_user():
    """allows user record to be altered"""
    username= input("Enter username for update: ")
    while True:
        cur.execute("SELECT * FROM user WHERE username =?", (username,))
        if cur.fetchone():
            break
        username = input("Invalid username, please enter a valid username: ")

    while True:
        # prompt user for updated password
        password= maskpass.askpass(prompt = f"Please enter updated password for <{username}>: ", mask='*').strip().encode('utf-8')
        password = password.decode()
        # Check if the password is at least 8 characters long and contains at least one number, one uppercase letter, and one special character
        if len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isupper() for c in password) and any(c in string.punctuation for c in password):
            print('password meets requirements')
            password = hash_password(password) 
            break
        else:
            print('password does not meet requirements')

    # prompt user to enter role
    user_role= input("Enter updated user_role: [admin/default] ").lower()

    # handle errors
    while not (user_role == "admin" or user_role == "default"): 
        user_role  = input("Wrong input, please enter admin or default: ") # handle errors of inputting something else
    cur.execute("""UPDATE user SET password =?, user_role =? WHERE username =?""",(password, user_role, username))
    
    #return to menu
    user_menu()

def delete_user():
    """delete a user account"""
    cur= con.cursor()
    username= input("Enter username of the account to delete: ")
    # handle errors
    while True:
        cur.execute("SELECT * FROM user WHERE username =?", (username,))
        if cur.fetchone():
            break
        username = input("Invalid username, please enter a valid username: ")
    
    # confirmation message to prevent accidents
    confirm = input("Are you sure you want to delete this user? (Y/N): ").strip().upper()
    
    while confirm not in ["Y","N"]:
        confirm = input("Invalid option, choose [Y/N]").strip().upper()
    if confirm == 'Y':
        cur.execute("DELETE from user WHERE username=?", (username,))
        con.commit()
        print(f"Successfully removed <{username}>")
    else:
        print("Aborted")
    
    #return to menu
    user_menu()


def customer_menu ():
    """Allows choosing operations related to customer management"""
    print("""
1. Create a customer 
2. View all customer 
3. View single customer
4. Update a customer
5. Delete a customer
6. Back to main menu""")

# while loop to handle errors
    menu_choice = input("Please choose options between (1-6): ")
    menu_option = ["1", "2", "3", "4", "5", "6"]
    while menu_choice not in menu_option:
        menu_choice = input("Error!, You have entered the wrong input, please choose options between (1-6):  ")

    if menu_choice == "1":
        create_customer()
        # create customer
    elif menu_choice == "2":
        view_all_customers()
        # view all customer
    elif menu_choice == "3":
        view_single_customer()
        # view single customer
    elif menu_choice == "4":
        update_customer()
        #update customer
    elif menu_choice == "5":
        delete_customer()
        # delete customer
    elif menu_choice == "6":
        main_menu()
        # back to main menu

def create_customer():
    forename = input("Enter customer forename: ").title().strip()
    surname = input("Enter customer surname: ").title().strip()
    while True:
        try:
            dob = input("Enter customer date of birth (YYYY-MM-DD): ").strip()
            datetime.datetime.strptime(dob, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD")

    insert_customer_data(forename,surname,dob)

def insert_customer_data(forename:str, surname:str, dob:str):
    """accepts customer data as arguments and inserts into customer table"""
    cur= con.cursor()
    cur.execute("INSERT INTO customer (forename, surname, dob) VALUES(?, ?, ?)", (forename,surname,dob))
    con.commit()
    #retrieve customer id 
    customerid = cur.lastrowid
    add_address(customerid)
    return

def add_address(customerid):
    """prompts the user for a customer ID and address attributes and inserts them into the addresses table"""
    cur = con.cursor()
    streetnumber = input("Enter the street number: ").title().strip()
    firstline = input("Enter the first line of the address: ").title()
    postcode = input("Enter the postcode: ").upper()
    region = input("Enter the region: ").title()
    country = input("Enter the country: ").title()
    
    cur.execute(
        "INSERT INTO address (streetnumber, firstline, postcode, region, country, customerid) "
        "VALUES (?, ?, ?, ?, ?, ?)", (streetnumber, firstline, postcode, region, country, customerid)
                )
    con.commit()
    print("Customer added successfully!")
    
    # to view new update
    cur.execute("SELECT customer.rowid, customer.forename, customer.surname, customer.dob, address.streetnumber, address.firstline, address.postcode, address.region, address.country FROM customer LEFT JOIN address ON customer.rowid = address.customerid WHERE customer.rowid = ?", (customerid,))
    customer = cur.fetchone()
    if customer is None:
        print("Error: customer not found")
        return
    print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format("ID","Forename","Surname", "DOB", "Street Number", "First Line", "Postcode", "Region", "Country")
        )
    print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7], customer[8])
        )
    # back to menu
    customer_menu()


def view_all_customers():
    """output all customer records and their addresses"""
    cur = con.cursor()
    print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
    .format("ID","Forename","Surname", "DOB", "Street Number", "First Line", "Postcode", "Region", "Country")
    )
    for row in cur.execute("SELECT customer.rowid, customer.forename, customer.surname, customer.dob, address.streetnumber, address.firstline, address.postcode, address.region, address.country FROM customer LEFT JOIN address ON customer.rowid = address.customerid"):
        # Convert the values in the row to strings
        row_str = [str(x) for x in row]        
        print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format(row_str[0], row_str[1] ,row_str[2],row_str[3], row_str[4], row_str[5],row_str[6],row_str[7],row_str[8])
        )
    #return to menu
    customer_menu()

def view_single_customer():
    """output customer record for the given ID with address"""
    cur = con.cursor()
    # prompts user until a valid customer id is entered
    while True:
        customer_id = input("Enter the id of the customer you would like to view: ")
        cur.execute("SELECT * FROM customer WHERE rowid = ?", (customer_id,))
        customer = cur.fetchone()
        if customer:
            break
        else:
            print("Error: customer not found. Please enter a valid customer id.")

    cur.execute("SELECT customer.rowid, customer.forename, customer.surname, customer.dob, address.streetnumber, address.firstline, address.postcode, address.region, address.country FROM customer LEFT JOIN address ON customer.rowid = address.customerid WHERE customer.rowid = ?", (customer_id,))
    row = cur.fetchone()
    if row:
        row_str = [str(x) for x in row]
        print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format("ID", "Forename","Surname", "DOB","Street Number","First Line","Postcode","Region","Country")
        )

        print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format(row_str[0], row_str[1], row_str[2],row_str[3], row_str[4], row_str[5],row_str[6],row_str[7],row_str[8])
        )
    else:
        print("Customer not found")
    #return to menu
    customer_menu()

def update_customer():
    """allows customer and address records to be altered"""
    # prompts user until a valid customer id is entered
    while True:
        customerid= input("Enter the ID of the customer to update: ")
        cur.execute("SELECT rowid FROM customer WHERE rowid = ?", (customerid,))
        customer = cur.fetchone()
        
        if customer: # displays error if not found
            break
        else:
            print("Error: Customer not found. Please enter a valid customer ID.")
    
    # enter updated information for chosen customer
    customerid = input("Enter customer id for update: ")
    forename= input("Enter updated forename  ").title()
    surname= input("Enter updated surname: ").title()
    
    while True: # handle format errors
        try:
            dob = input("Enter updated customer date of birth (YYYY-MM-DD): ").strip()
            datetime.datetime.strptime(dob, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD")

    # update customer info
    cur.execute("""UPDATE customer SET forename =?, surname =?, dob =? WHERE rowid = ?""",(forename, surname, dob, customerid))
    
    #update address info
    streetnumber = input("Enter the updated street number: ").strip()
    firstline = input("Enter the updated first line of the address: ").title()
    postcode = input("Enter the updated postcode: ").upper()
    region = input("Enter the updated region: ").title()
    country = input("Enter the updated country: ").title()
    cur.execute("""UPDATE address SET streetnumber =?, firstline =?, postcode =?, region =?, country =? WHERE customerid = ?""",(streetnumber, firstline, postcode, region, country,customerid))
    con.commit()
    
    # to view new update
    cur.execute("SELECT customer.rowid, customer.forename, customer.surname, customer.dob, address.streetnumber, address.firstline, address.postcode, address.region, address.country FROM customer LEFT JOIN address ON customer.rowid = address.customerid WHERE customer.rowid = ?", (customerid,))
    customer = cur.fetchone()
    
    # displays new update
    if customer is None:
        print("Error: customer not found")
        return
    print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format("ID","Forename","Surname", "DOB", "Street Number", "First Line", "Postcode", "Region", "Country")
        )
    print("{:<2} {:<12} {:<12} {:<10} {:<15} {:<25} {:<10} {:<10} {:<10}"
        .format(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7], customer[8])
        )
    #return to menu
    customer_menu()

def delete_customer():
    """delete one student and its address from database"""
    cur= con.cursor()
    while True:
        customerid= input("Enter the ID of the customer to delete: ")
        cur.execute("SELECT rowid FROM customer WHERE rowid = ?", (customerid,))
        customer = cur.fetchone()
        if customer is None:
            print("Error: customer not found")
        else:
            break
    
    cur.execute("DELETE FROM address WHERE customerid =?", (customerid,))
    cur.execute("DELETE FROM customer WHERE rowid =?", (customerid,))
    con.commit()
    #return to menu
    customer_menu()


def account_menu ():
    """Allows choosing operations related to account management"""
    print("""
1. Create an account 
2. View all accounts
3. View single account
4. Update/close an account
5. Delete an account
6. Back to main menu""")

# while loop to handle errors
    menu_choice = input("Please choose options between (1-6): ")
    menu_option = ["1", "2", "3", "4", "5", "6"]
    while menu_choice not in menu_option:
        menu_choice = input("Error!, You have entered the wrong input, please choose options between (1-6):  ")

    if menu_choice == "1":
        #create an account
        create_account()
    elif menu_choice == "2":
        #read list of accounts (view all customers)
        view_all_accounts()
    elif menu_choice == "3":
        #read single account based on customer chosen
        view_single_account()
    elif menu_choice == "4":
        #update an account
        update_account()
    elif menu_choice == "5":
        #delete an account
        delete_account()
    elif menu_choice == "6":
        # back to main menu
        main_menu()
        
 
def create_account():
    balance = input("To create an account, please enter the balance: ")
    print(f'Your balance is £{balance}')
    # check for correct date format
    while True:
        try:
            opendate = input("Enter the date that the account is open: ")
            datetime.datetime.strptime(opendate, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please enter a date in the format yyyy-mm-dd")
    
    customerid =input("Enter the ID of the customer to find their account: ")
    check_customer = cur.execute('Select customerid from customer where customerid = ?', (customerid))
    if check_customer != []:
        insert_account_data(balance,opendate,customerid)
    else:
        print("Customer does not exists, please re-enter a valid customer ID: ")


def insert_account_data(balance: int, opendate: str, customerid: int):
    """accepts account data as arguments and inserts into account table"""
    cur= con.cursor()
    cur.execute("INSERT INTO account (balance, opendate, customerid) VALUES(?, ?, ?)", (balance,opendate,customerid))
    con.commit()
    #return to menu
    account_menu()

def view_all_accounts():
    """output all active account records with customer details"""
    cur = con.cursor()
    print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<10} {:<12} {:<12}"
    .format("Account ID", "Customer ID", "Balance", "Opendate", "Closedate", "Status", "Forename", "Surname")
    )
    for row in cur.execute("SELECT account.rowid, account.customerid, account.balance, account.opendate, account.closedate, account.status, customer.forename, customer.surname FROM account JOIN customer ON account.customerid = customer.rowid WHERE status = 'ACTIVE'"):
        # Convert the values in the row to strings
        row_str = [str(x) for x in row]        
        print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<10} {:<12} {:<12}"
        .format(row_str[0], row_str[1] ,row_str[2],row_str[3], row_str[4], row_str[5], row_str[6], row_str[7])
        )
    #return to menu
    account_menu()


def view_single_account():
    """output account record for the given ID"""
    cur = con.cursor()
    customerid = input("Enter the id of the customer you would like to view: ")
    check_customer = cur.execute('Select customerid from account where customerid = ?', (customerid))
    if check_customer != []:
        print("Here is the account you requested to see: ")
    else:
        print("Customer does not exists, please re-enter a valid customer ID: ")
    
    for row in cur.execute("SELECT rowid, * FROM account WHERE rowid=?", (customerid,)):
        # Convert the values in the row to strings
        row_str = [str(x) for x in row]
        
        print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<10}"
        .format("Account ID", "Customer ID", "Balance", "Opendate", "Closedate", "Status")
        )
        
        print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<10}"
        .format(row_str[0], row_str[1] ,row_str[2],row_str[3], row_str[4], row_str[5])
        )
    #return to menu
    account_menu()


def update_account():
    """allows account record to be altered"""
    cur= con.cursor()
    customerid = input("Enter the ID of the customer you would like to update: ")
    check_customer = cur.execute('Select customerid from account where customerid = ?', (customerid))
    if check_customer != []:
        print("Here is the account you requested to see: ")
    else:
        print("Customer does not exists, please re-enter a valid customer ID: ")
    while True:
        try:
            closedate = input("Enter the closedate (YYYY-MM-DD): ")
            datetime.datetime.strptime(closedate, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please enter a date in the format yyyy-mm-dd")
    cur.execute("UPDATE account SET status = 'closed', closedate = ? WHERE status = 'ACTIVE' AND customerid =?", (closedate, customerid))
    con.commit()
    # return to menu
    account_menu()


def delete_account():
    """delete an account from customer"""
    cur= con.cursor() 
    while True:
        customerid= input("Enter the ID of the account to delete: ")
        cur.execute("DELETE from account WHERE rowid =?", (customerid,))
        if cur.rowcount > 0:
            break
        else:
            print("Error: Account not found. Please enter a valid account ID.")
    con.commit()
    #return to menu
    account_menu()



def transaction_menu ():
    """Allows choosing operations related to transaction"""
    print("""
1. Create a transaction
2. Read list of all transactions
3. Read a list of transactions for a date range
4. Read single transaction
5. Update a transaction
6. Delete a transaction
7. Back to main menu""")

# while loop to handle errors
    menu_choice = input("Please choose options between (1-7): ")
    menu_option = ["1", "2", "3", "4", "5", "6", "7"]
    while menu_choice not in menu_option:
        menu_choice = input("Error!, You have entered the wrong input, please choose options between (1-7):  ")

    if menu_choice == "1":
        #create a transaction
        create_transaction()
    elif menu_choice == "2":
        #read list of all transactions based on a date range
        view_all_transactions()
    elif menu_choice == "3":
        #read list of all transactions
        read_transaction_date()
    elif menu_choice == "4":
        #read single transaction based on customer chosen and date
        view_single_transaction()
    elif menu_choice == "5":
        #update a transaction
        update_transaction()
    elif menu_choice == "6":
        #delete an transaction
        delete_transaction()
    elif menu_choice == "7":
        main_menu()
        # back to main menu


def create_transaction():
    cur = con.cursor()
    
    while True:
        accountid = input("Enter the account ID for this transaction: ")
        
        cur.execute('SELECT balance FROM account WHERE accountid = ?', (accountid,))
        balance = cur.fetchone()

        if balance is not None:
            # Account exists, break out of the loop
            balance = balance[0]
            break
        else:
            print("Account does not exist. Please enter a valid account ID.")

    print("Current balance: ", balance)

    # Prompt the user for the amount of the transaction
    amount = float(input("Please enter the amount of this transaction: "))
    
    # Round the amount to two decimal places
    amount = round(amount, 2)

    # Check the type of the transaction
    while True:
    # Prompt the user for the type of the transaction
        type = input("Please enter the type of this transaction (debit/credit): ").lower()
        if type == "debit" or type == "credit":
            break
        else:
            print("Error: unknown transaction type. Please enter 'debit' or 'credit'.")
        
    date = input("Please enter the date of this transaction (YYYY-MM-DD): ")
    cur = con.cursor()
    insert_transaction_data(amount, type, date, accountid)
    cur.close()
    answer = input("Would you like to add another transaction? [Y/N]: ").upper()
    if answer == 'Y':
        create_transaction()
    else:
        print("New transaction has been recorded.")

def insert_transaction_data(amount: int, type: str, date: str, accountid: int):
    """accepts transaction data as arguments and inserts into transaction table"""
    cur = con.cursor()
    try:
        # Get the balance of the account
        cur.execute('SELECT balance FROM account WHERE accountid = ?', (accountid,))
        balance = cur.fetchone()[0]
        balance = int(balance)
    
        if type == 'debit':
            new_balance = balance - amount
            amount = -amount
            # Update the balance of the account
            cur.execute(
                "UPDATE account "
                "SET balance = ? "
                "WHERE accountid = ?", (new_balance, accountid)
            )
        
            # Insert the transaction into the transactions table
            cur.execute(
                "INSERT INTO transact (amount, type, date, accountid) "
                "VALUES (?, ?, ?, ?)", (amount, type, date, accountid)
            )
        
            # Commit the transaction
            con.commit()
            print("Transaction successful. New balance: {}".format(new_balance))
        elif type == 'credit':
            new_balance = balance + amount
            # Update the balance of the account
            cur.execute(
                "UPDATE account "
                "SET balance = ? "
                "WHERE accountid = ?", (new_balance, accountid)
            )
        
            # Insert the transaction into the transactions table
            cur.execute(
                "INSERT INTO transact (amount, type, date, accountid) "
                "VALUES (?, ?, ?, ?)", (amount, type, date, accountid)
                        )
        # Commit the transaction
        con.commit()

    except Exception as e:
        # handle the exception
        print("Error occured:", e)
        con.rollback()
    finally:
        cur.close()
        
    transaction_menu()

def view_all_transactions():
    """output all transaction records for a date range"""
    cur = con.cursor()
    accountid = input("Enter the id of the account you would like to view: ")
    check_account = cur.execute('Select accountid from account where accountid = ?', (accountid))
    if check_account != []:
        print("Here is the transaction you requested to see: ")
    else:
        print("Account does not exists, please re-enter a valid account ID: ")
    
    # output results
    print("{:<14} {:<10} {:<12} {:<10} {:<10}"
    .format("Transaction ID", "Account ID", "Amount", "Date", "Type")
    )
    for row in cur.execute("SELECT rowid, * FROM transact WHERE accountid = ?", (accountid,)):
        # Convert the values in the row to strings
        row_str = [str(x) for x in row]
        print("{:<14} {:<10} {:<12} {:<10} {:<10}"
        .format(row_str[0], row_str[1], row_str[2], row_str[3], row_str[4])
        )
    transaction_menu()



def read_transaction_date():
    """output all transaction records for a date range"""
    cur = con.cursor()
    accountid = input("Enter the id of the account you would like to view: ")
    check_account = cur.execute('Select accountid from account where accountid = ?', (accountid))
    if check_account != []:
        print("Here is the transaction you requested to see: ")
    else:
        print("Account does not exists, please re-enter a valid account ID: ")
    
    # enter date range for desired transaction
    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    while True:
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        try:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    # output results
    print("{:<14} {:<10} {:<12} {:<10} {:<10}"
    .format("Transaction ID", "Account ID", "Amount", "Date", "Type")
    )
    for row in cur.execute("SELECT rowid, * FROM transact WHERE accountid = ? AND date BETWEEN ? AND ? ", (accountid, start_date, end_date)):
        # Convert the values in the row to strings
        row_str = [str(x) for x in row]
        print("{:<14} {:<10} {:<12} {:<10} {:<10}"
        .format(row_str[0], row_str[1], row_str[2], row_str[3], row_str[4])
        )
    transaction_menu()


def view_single_transaction():
    """output transaction record for the given account and date"""
    cur = con.cursor()
    while True:
            accountid = input("Enter the id of the account you would like to view: ")
            check_account = cur.execute('Select accountid from account where accountid = ?', (accountid,))

            if check_account.fetchone() is not None:
                print("Here is the transaction you requested to see: ")
                cur.execute("SELECT * FROM transact WHERE accountid = ?", (accountid,))
                transactions = cur.fetchall()
                for transaction in transactions:
                    print(transaction)
                break
            else:
                print("Account does not exist, please re-enter a valid account ID: ")
        
    # Ask the user for the date and execute the SELECT statement
    date = input("Enter the date of the transaction (YYYY-MM-DD): ")
    cur.execute(
        "SELECT rowid, * FROM transact "
        "WHERE date = ? AND accountid = ?", (date, accountid)
    )
    
    # Fetch and print the results
    results = cur.fetchall()
    for result in results:
        print("{:<14} {:<10} {:<12} {:<10} {:<10}"
              .format("Transaction ID", "Account ID", "Amount", "Type", "Date"))
        print("{:<14} {:<10} {:<12} {:<10} {:<10}"
              .format(result[0], result[1], result[2], result[3], result[4])
             )

    transaction_menu()

def update_transaction():
    """update a transaction by reversing it and creating a new one"""
    try:
        cur = con.cursor()
        
        while True:
            accountid = input("Enter the id of the account you would like to view: ")
            check_account = cur.execute('Select accountid from account where accountid = ?', (accountid,))

            if check_account.fetchone() is not None:
                print("Here is the transaction you requested to see: ")
                print("{:<14} {:<10} {:<12} {:<10} {:<10}".format("Transaction ID", "Account ID", "Amount", "Date", "Type"))
                for row in cur.execute("SELECT rowid, * FROM transact WHERE accountid = ?", (accountid,)):
                    # Convert the values in the row to strings
                    row_str = [str(x) for x in row]
                    print("{:<14} {:<10} {:<12} {:<10} {:<10}".format(row_str[0], row_str[1], row_str[2], row_str[3], row_str[4])
                    )
                break
            else:
                print("Account does not exist, please re-enter a valid account ID: ")

        while True:
            transaction_id = input("Enter the id of the transaction you would like to update: ")
            cur.execute("SELECT * FROM transact WHERE transactid = ?", (transaction_id,))
            transaction = cur.fetchone()
            if transaction is not None:
                break
            print("Error: transaction not found, please enter a valid transaction id.")
        if not transaction:
            return   

        # retrieve the account details
        accountid = transaction[4]
        cur.execute("SELECT * FROM account WHERE accountid = ?", (accountid,))
        account = cur.fetchone()

        # reverse the transaction
        amount = transaction[1]
        type = "credit" if transaction[2] == "debit" else "debit"
        date = transaction[3]

        # delete the old transaction
        cur.execute("DELETE FROM transact where transactid = ?", (transaction_id,))
        con.commit()
        print("Old transaction removed successfully")

        # prompt the user for the new transaction details
        new_amount = float(input("Please enter the new amount for this transaction: "))
        new_amount = round(new_amount, 2)
        new_type = input("Please enter the new type of this transaction (debit/credit): ").lower()
        new_date = input("Please enter the new date of this transaction (YYYY-MM-DD): ")

        # insert the new transaction
        cur.execute("INSERT INTO transact (amount, type, date, accountid) VALUES (?,?,?,?)", (new_amount, new_type, new_date, accountid))
        con.commit()
        print("New transaction added successfully")
        
        # to view new update
        cur.execute("SELECT * FROM transact WHERE transactid = ?", (transaction_id,))
        transaction = cur.fetchone()
        if transaction is None:
            return
        print("{:<14} {:<10} {:<12} {:<10} {:<10}"
            .format("Transaction ID", "Account ID", "Amount", "Type", "Date"))
        print("{:<14} {:<10} {:<12} {:<10} {:<10}"
            .format(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4])
            )
    except Exception as e:
        # handle the exception
        print("Error occured:", e)
        con.rollback()
    finally:
        cur.close()

        transaction_menu()

def delete_transaction():
    """Remove a transaction from an account by reversing it"""
    cur = con.cursor()
    try:
        account_id = input("Enter account id: ")
        
        # retrieve all transactions for the account
        cur.execute("SELECT * FROM transact WHERE accountid = ?", (account_id,))
        transactions = cur.fetchall()
        if not transactions:
            print("Error: no transactions found for this account.")
            return

        # display the transactions
        print("{:<2} {:<10} {:<10} {:<10} {:<10}".format("ID", "Amount", "Type", "Date", "Account ID"))
        for transaction in transactions:
            print("{:<2} {:<10} {:<10} {:<10} {:<10}".format(*transaction))

        # prompt the user to select the transaction to be reversed
        transaction_id = input("Enter transaction id to be reversed: ")
        
        # retrieve the transaction details
        cur.execute("SELECT * FROM transact WHERE transactid = ?", (transaction_id,))
        transaction = cur.fetchone()
        if not transaction:
            print("Error: transaction not found")
            return
        
        # retrieve the account details
        accountid = transaction[4]
        cur.execute("SELECT * FROM account WHERE accountid = ?", (accountid,))
        account = cur.fetchone()

        #reverse the transaction
        amount = transaction[1]
        type = "credit" if transaction[2] == "debit" else "debit"
        date = transaction[3]
        
        insert_transaction_data(amount, type, date, accountid)
        cur.execute("DELETE FROM transact where transactid = ?", (transaction_id,))
        con.commit()
        print("Transaction reversed and removed successfully")
    
    except Exception as e:
        # handle the exception
        print("Error occured:", e)
        con.rollback()
    finally:
        cur.close()

    transaction_menu()

# Main
login()
main_menu()