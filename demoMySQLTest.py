#demoMySQLTets.py
""" Excercise to access MySQL functions.
    Try http://localhost/phpMyAdmin/?lang=en to administer MySQL database
    on local Apache server."""

import mysql.connector
import sys
import os

# Try to connect to MySQL server w/o database in case it must be created.
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root"
        #,database="mydatabase"
    )
except:
    print("Did not connect to MySQL server.\nTrying to start MySQL server.")
    #os.system('sudo /etc/init.d/mysql start')
    print ("Exiting program...")
    sys.exit()  #Server not running or account not setup.

# Check if database exists
mycursor = mydb.cursor(buffered=True)  #if don't state that buffer get results not read error when deleting.
foundDB = False
mycursor.execute("SHOW DATABASES")
#mycursor returns a tuple with database name and an empty element
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
    mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

mycursor.execute("SHOW TABLES")
print("Tables:")
for x in mycursor:
    print(x[0])

# Check if data in table?
sqlCnt = "SELECT COUNT(*) FROM customers"
mycursor.execute(sqlCnt)
myresults = mycursor.fetchone()
if myresults[0] == 0:       # returns tuple with row count as first element
    #insert data if needed
    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = [
    ('James Caan', '14 Highway 101, Long Beach CA'),
    ('Sandra Bullock', '45 Ventura Blvd, Hollywood, CA'),
    ('James Dean', '1 Deadsville, Death Valley, CA'),
    ("Barbara Streisand", "5670 Wilshire Blvd, Hollywood, CA"),
    ("George Washington", "51 Whitehouse, Washington, DC"),
    ("James Taft", "20 N. High Street, Columbus, OH"),
    ("Vicky Williamson", "86763 Sunshine, Dollywood, TN"),
    ("Chuck Strong", "563 Woholo St, Jupiter, KS"),
    ("Viola Black", "234 Rush St, New Orleans, LA")
    ]
    mycursor.executemany(sql,val)
    mydb.commit()
    print(mycursor.rowcount,"Record(s) inserted, last ID: {}".format(mycursor.lastrowid))

#mycursor.execute("SELECT name, address FROM customers")
mycursor.execute("SELECT * FROM customers")
myresults = mycursor.fetchall()
print("Customer list:")
for x in myresults:
    print("{:3} {:20} {}".format(x[0],x[1],x[2]))

mycursor.execute("SELECT name, address FROM customers WHERE address like '%CA'")
myresults = mycursor.fetchone()
print("First one from CA is: ",myresults[0])

#clean up getting rid of table and database.
print("\nDo you wish to remove database (y/n)?",end="")
a = input()
if a.lower() == 'y':
    try:
        mycursor.execute("DROP TABLE customers")
        mydb.commit()
        mycursor.execute("DROP DATABASE mydatabase")
        mydb.commit()
        print ("customers TABLE and mydatabase deleted")
    except Exception as e:
        print("Failed to Delete table and database: {}".format(e))
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed.")
else :
    print('Database was not removed.')