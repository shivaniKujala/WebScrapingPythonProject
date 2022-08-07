import sqlite3
import json


with open('quotes.toscrape.json','r') as f:
    data = json.load(f)
    #print(data)



# Connecting to Quotes Database
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()  # cursor object used to create and insert data into database . And we can also used to excute the quires

#If author table exists => deleting author table and recreating table again
cursor.execute("DROP TABLE IF EXISTS AUTHORS")
cursor.execute("DROP TABLE IF EXISTS quotes")


# creating Author table
authors = data['authors']
cursor.execute('''CREATE TABLE authors(id INTEGER NOT NULL, name VARCHAR(50) NOT NULL , born VARCHAR(100) ,reference VARCHAR2(50))''')
# Updating id of prrimary key by initializing with id = 1
id = 1
for each_author in authors:
    for key,value in each_author.items():
        name = each_author['name']
        born = each_author['born']
        reference = each_author['reference']
        cursor.execute('''INSERT INTO authors VALUES(?,?,?,?) ''', (id,name,born,reference))
        break
    id += 1

#creating quotes table
quotes = data['quotes']

cursor.execute('''CREATE TABLE quotes (quote_id INTEGER NOT NULL, quote VARCHAR(200), author_name VARCHAR(20), 
author_id INTEGER NOT NULL,FOREIGN KEY(author_id) REFERENCES authors(id))''')

quote_id = 1

for each_quote in quotes:
    for key , value in each_quote.items():
        quote = each_quote["quote"]
        author = each_quote['author']
        tags = each_quote['tags']

        cursor.execute('''INSERT INTO quotes VALUES(?,?,?,?)''',(quote_id,quote,author,author_id))
        break
    quote_id += 1

cursor.execute('''SELECT * FROM quotes''')
results = cursor.fetchall()
print(results)

connection.commit()
connection.close() # It is mandatory to close