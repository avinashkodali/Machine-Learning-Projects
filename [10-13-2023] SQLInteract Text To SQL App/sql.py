import sqlite3

# Connect to SQlite
connection=sqlite3.connect("ecommerce.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

# create the table
orders_table_info="""
Create table Orders(OrderId INT,CustomerID INT,
OrderDate DATE,TotalAmount INT);

"""
cursor.execute(orders_table_info)

# Insert Some more records

cursor.execute('''Insert Into Orders values(1, 101,	"2023-05-10", 150.00)''')
cursor.execute('''Insert Into Orders values(2, 102,	"2023-06-15", 200.00)''')
cursor.execute('''Insert Into Orders values(3, 103,	"2023-07-20", 100.00)''')
cursor.execute('''Insert Into Orders values(4, 101,	"2023-08-05", 300.00)''')
cursor.execute('''Insert Into Orders values(5, 104,	"2023-09-10", 250.00)''')

# Dispaly All the records

print("The inserted records on Orders table are")
data=cursor.execute('''Select * from Orders''')
for row in data:
    print(row)

# create the table
customers_table_info="""
Create table Customers(CustomerID INT,FirstName VARCHAR(50),
LastName VARCHAR(50),Email VARCHAR(50));

"""
cursor.execute(customers_table_info)

# Insert Some more records

cursor.execute('''Insert Into Customers values(101, "John", "Doe", "john@example.com")''')
cursor.execute('''Insert Into Customers values(102, "Jane", "Smith", "jane@example.com")''')
cursor.execute('''Insert Into Customers values(103, "Mark", "Johnson", "mark@example.com")''')
cursor.execute('''Insert Into Customers values(104, "Emily", "Brown", "emily@example.com")''')
cursor.execute('''Insert Into Customers values(105, "Michael", "Williams", "michael@example.com")''')

# Dispaly All the records
print("The inserted records on Customers table are")
data=cursor.execute('''Select * from Customers''')
for row in data:
    print(row)

# Commit your changes in the databse
connection.commit()
connection.close()