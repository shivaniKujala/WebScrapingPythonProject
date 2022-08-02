import json
import sqlite3

with open('quotes.toscrape.json','r') as f:
    data = json.load(f)

#Creating new DataBase and Connecting to database
#Cursor used to make queries from Database
connection = sqlite3.connect('quotes.db')
c = connection.cursor()

quotes = data['quotes']
authors = data['authors']

#Creating Author table using authors data
#c.execute('''CREATE TABLE author_table(id INTEGER NOT NULL PRIMARY KEY,name VARCHAR(200),born VARCHAR(200), reference)''')

#Inserting data about authors by iterating over the authors list
for each_author in authors:
    name = each_author['name']
    born = each_author['born']
    reference = each_author['reference']
    #c.execute('''INSERT INTO author_table VALUES(?,?,?)''',(name,born,reference))


#Creating Quotes Table using data in quotes list
#c.execute('''CREATE TABLE quotes_table(id INTEGER NOT NULL PRIMARY KEY,quote VARCHAR(200), tags VARCHAR(200),author_id INTEGER
# FOREIGN KEY (author_id) REFERENCES author_table(id) ON DELETE CASCADE)''')
for each_quote in quotes:
    quote = each_quote['quote']
    tags = each_quote['tags']
    

    #c.execute('''INSERT INTO quotes_table VALUES(?,?,?)'''(quote,tags))




c.close()