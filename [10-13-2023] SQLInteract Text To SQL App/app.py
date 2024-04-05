from click import prompt
from dotenv import load_dotenv
load_dotenv() # load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
# Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define Your Prompt
prompt = [
    """
    I'm currently working on a project that involves querying a database, and I could use your expertise in crafting SQL queries. Below are the details of the database:\n
    Database Schema:\n
    Table1: Create table Orders(OrderId INT, CustomerID INT, OrderDate DATE, TotalAmount INT);\n
    Table2: Create table Customers(CustomerID INT, FirstName VARCHAR(50), LastName VARCHAR(50), Email VARCHAR(50);\n
    
    Example Queries:\n
    1) Retrieve the total number of orders made by each customer along with their full names and email addresses.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, COUNT(Orders.OrderId) AS TotalOrders FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID;\n
    
    2) Retrieve the total amount spent by each customer along with their full names and email addresses.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, SUM(Orders.TotalAmount) AS TotalSpent FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID;\n

    3) Retrieve the total number of orders made by each customer along with their full names and email addresses, sorted by the total number of orders in descending order.\n      
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, COUNT(Orders.OrderId) AS TotalOrders FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalOrders DESC;\n

    4) Retrieve the total amount spent by each customer along with their full names and email addresses, sorted by the total amount spent in descending order.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, SUM(Orders.TotalAmount) AS TotalSpent FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalSpent DESC;\n

    5) Retrieve the total number of orders made by each customer along with their full names and email addresses, sorted by the total number of orders in descending order, and display only the top 5 customers.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, COUNT(Orders.OrderId) AS TotalOrders FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalOrders DESC LIMIT 5;\n

    6) Retrieve the total amount spent by each customer along with their full names and email addresses, sorted by the total amount spent in descending order, and display only the top 5 customers.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, SUM(Orders.TotalAmount) AS TotalSpent FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalSpent DESC LIMIT 5;\n

    7) Retrieve the total number of orders made by each customer along with their full names and email addresses, sorted by the total number of orders in descending order, and display only the top 10 customers.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, COUNT(Orders.OrderId) AS TotalOrders FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalOrders DESC LIMIT 10;\n

    8) Retrieve the total amount spent by each customer along with their full names and email addresses, sorted by the total amount spent in descending order, and display only the top 10 customers.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, SUM(Orders.TotalAmount) AS TotalSpent FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalSpent DESC LIMIT 10;\n

    9) Retrieve the total number of orders made by each customer along with their full names and email addresses, sorted by the total number of orders in descending order, and display only the top 20 customers.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, COUNT(Orders.OrderId) AS TotalOrders FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalOrders DESC LIMIT 20;\n

    10) Retrieve the total amount spent by each customer along with their full names and email addresses, sorted by the total amount spent in descending order, and display only the top 20 customers.\n
    Response: SELECT Customers.FirstName, Customers.LastName, Customers.Email, SUM(Orders.TotalAmount) AS TotalSpent FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID ORDER BY TotalSpent DESC LIMIT 20;\n

    I would greatly appreciate it if you could help me with the following SQL query:\n

    The response should contain only the SQL query, don't output ``` and sql word. \n
    """
]

## Streamlit App

st.set_page_config(page_title="SQLInteract")
st.header("SQLInteract: Text To SQL App")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    llm_response=get_gemini_response(question,prompt)
    print(llm_response)
    response=read_sql_query(llm_response,"ecommerce.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.text(row)
    
    st.subheader("The SQL Query is")
    st.text(llm_response)
