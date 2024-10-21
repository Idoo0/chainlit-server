import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host= os.getenv("DB_HOST"),
  user= os.getenv("DB_USER"),
  password= os.getenv("DB_PASSWORD"),
  database= os.getenv("DB_NAME")
)

mycursor = mydb.cursor()

def getResultFromQuery(query):
    mycursor.execute(str(query))
    myresult = mycursor.fetchall()
    return str(myresult)