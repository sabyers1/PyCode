#PathSQLTest.py
""" Exercise to test SQL knowledge. """

# -- Example case create statement:
# CREATE TABLE customers (
#   id INTEGER NOT NULL PRIMARY KEY,
#   name VARCHAR(30) NOT NULL
# );

# CREATE TABLE transactions (
#   id INTEGER NOT NULL PRIMARY KEY,
#   customerId INTEGER REFERENCES customers(id),
#   amount DECIMAL(15,2) NOT NULL
# );

# INSERT INTO customers(id, name) VALUES(1, 'Steve');
# INSERT INTO customers(id, name) VALUES(2, 'Jeff');
# INSERT INTO transactions(id, customerId, amount) VALUES(1, 1, 100);

# -- Expected output (in any order):
# -- name     transactions
# -- -------------------------------
# -- Steve    1
# -- Jeff     0

# -- Explanation:
# -- In this example.
# -- There are two customers, Steve and Jeff.
# -- Steve has made one transaction. Jeff has made zero transactions.

# Answer:
# SELECT customers.name, COUNT(transactions.customerid) as transactions from customers
# LEFT JOIN transactions 
# ON customers.id = transactions.customerId GROUP BY Customers.name

# The LEFT JOIN gets all values in 'left' table (customers) and values in 'right' table
# (transactions) which match ON clause.  The GROUP BY term captures the null (zero) counts
# which are normally ignored by COUNT.

# Can add 'ORDER BY transactions DESC' to end to get most to least transactions.

import mysql.connector
import sys #sys.exit()

# Try to connect to MySQL server
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='root'
        #,database="mydatabase"
    )
except:
    print("Did not connect to MySQL server.\nExiting program...")
    sys.exit()  #Server not running or account not setup

# Check if database exists
# mycursor returns a tuple with database name and an empty element
mycursor = mydb.cursor(buffered=True)  #if don't state that buffer get results not read error when deleting.
foundDB = False
mycursor.execute("SHOW DATABASES")

for x in mycursor:
     #print("Database Name: {}".format(x[0]))
     if x[0] == "mydatabase" :
         foundDB=True

if not foundDB:
    print ("Creating 'mydatabase' on MySQL server")
    mycursor.execute("CREATE DATABASE mydatabase")
else:
    print("Found 'mydatabase' on MySQL server.")
mycursor.execute("USE mydatabase")

def checkTableExists(dbcon, tablename):
    """ Method looks to see if a table exists in a database connection """
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

if not checkTableExists(mydb,"customers"):    
    #Create table with primary key in database
    mycursor.execute("CREATE TABLE customers (id INT NOT NULL PRIMARY KEY, name VARCHAR(30) NOT NULL)")
if not checkTableExists(mydb,"transactions"):
    mycursor.execute("CREATE TABLE transactions (id INT NOT NULL PRIMARY KEY, customerId INTEGER REFERENCES customers(id),amount DECIMAL(15,2) NOT NULL)")

# Setup the data if not already loaded.
sqlCnt = "SELECT COUNT(*) FROM customers"
mycursor.execute(sqlCnt)
myresults = mycursor.fetchone()
if myresults[0] == 0:       # returns tuple with row count as first element
    # insert data
    sql = "INSERT INTO customers (id, name) VALUE (%s,%s)"
    val = [ ('1','Steve'), ('2','Jeff')]
    mycursor.executemany(sql,val)
    mydb.commit()
    print(mycursor.rowcount,"Record(s) inserted")
    sql = "INSERT INTO transactions(id, customerId, amount) VALUES(1, 1, 100)"
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount,"Record inserted")

# Make selection
sql = "SELECT customers.name, COUNT(transactions.customerId) as transactions FROM customers "\
     "LEFT JOIN transactions ON customers.id = transactions.customerId GROUP BY customers.name"
mycursor.execute(sql)
myresults = mycursor.fetchall()
print("\nname      transactions")
for x in myresults:
    print("{:10}   {}".format(x[0],x[1]))

#clean up getting rid of table and database.
print("\nDo you wish to remove database (y/n)?",end="")
a = input()
if a.lower() == 'y':
    try:
        mycursor.execute("DROP TABLE customers")
        mydb.commit()
        mycursor.execute("DROP TABLE transactions")
        mydb.commit()
        mycursor.execute("DROP DATABASE mydatabase")
        mydb.commit()
        print ("customers, transactions TABLEs and mydatabase deleted")
    except Exception as e:
        print("Failed to Delete tables and database: {}".format(e))
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed.")
else :
    print('Database was not removed.')