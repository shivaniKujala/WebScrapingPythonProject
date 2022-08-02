import requests
from bs4 import BeautifulSoup
import json


#Fetch HTML content using url
url = "http://quotes.toscrape.com/"
request = requests.get(url)
html_content = request.content

#Parsing HTML content using BeautifulSoup which converts into Python objects

soup = BeautifulSoup(html_content,"html.parser") #Converting into Parsed HTML

#print(soup.prettify())

# Need to fetch all the content from all pages
# Need to get content by using tags of each html page of quotes.We can easily findout at the end of HTML Pages of each Tag

# follow below steps to understand fetching and parsing of HTML page

#First Step:Fetching anchor tags of quotes
tag_elements_in_html_content = soup.find_all("span", class_ = "tag-item")

# Below lists are used to store the data of Quotes and Authors
quotes_data = []
authors_data = []  #list of authors information
list_of_about_authors_link = []  #making list of authors link




# Fetching quotes from next page for each_tag =>maximum pages for each_tag element having only two pages
# Here using while loop to to get the data from next page
#Scrape_page method used to get the parsed HTML of each tag element which will include next page content also.
def scrape_page(link_url, quotes_data , list_of_about_authors_link):
    max_pages = 2
    current_page = 1
    while current_page <= max_pages:
        current_url = f'{link_url}page/{current_page}/'
        #print(current_url)

        raw_html = requests.get(current_url)    #Fetching current HTML Content by using Get Method
        soup_raw_html = BeautifulSoup(raw_html.text,"html.parser")
        #print(soup_raw_html.prettify())
        for quotes in soup_raw_html.find_all("div" , class_="quote"):
            each_quote = dict()
            summary_quote = quotes.span.text
            #print(summary_quote)
            each_quote["quote"] = summary_quote

            author_name = quotes.select_one("small")
            #print(author_name.string)
            each_quote["author"] = author_name.string
            name = author_name.string

            about_author_link = quotes.a['href']
            list_of_about_authors_link.append((about_author_link))

            tags = quotes.find("div" , class_="tags")
            tags_list = []
            anchor_tags = tags.find_all("a")
            for i in anchor_tags:
                tags_list.append(i.text)
            #print(tags_list)
            each_quote["tags"] = tags_list
            quotes_data.append(each_quote)
        current_page += 1




#links_url_list = []


#Second Step:method used to fetch the information of different tag elements => love,smile,inspirational
def making_link_for_tag_elements(each_tag_element):

    link = each_tag_element.select_one('.tag-item a')["href"]
    string_link = each_tag_element.a.text
    link_url = "http://quotes.toscrape.com" + link # Fetching url for all tag elements to scrape data

    scrape_page(link_url,quotes_data,list_of_about_authors_link)



# Getting tag elements with their links to make url to fetch data in next pages => Iteration makes every tag element
# availble to make links to extract data from HTML
for each_tag_element in tag_elements_in_html_content:
    making_link_for_tag_elements(each_tag_element)

#This method used to get the authors data
def get_about_author_information(each_link_about_author,authors_data):
    information = dict()       # Each Author informating storing in dictionary
    url = "http://quotes.toscrape.com/" + each_link_about_author + '/'



    request_url = requests.get(url)
    soup = BeautifulSoup(request_url.content,"html.parser")
    #print(soup.prettify())


    author_details = soup.find("div", "author-details")

    author_name_row = author_details.find('h3')
    name = ''
    for row in author_name_row:
        name += row.text
        break

    author_born_location = author_details.p
    list_of_born_location = author_born_location.select("span")

    information['name'] = name
    information['born'] = list_of_born_location[0].text + "," + list_of_born_location[1].text
    information['reference'] = url
    authors_data.append(information)


links = list(set(list_of_about_authors_link))

for each_link_about_author in links:
    get_about_author_information(each_link_about_author,authors_data)


data = dict()
data["quotes"] = quotes_data
data["authors"] = authors_data



print(data)
#Saving data in a file

with open("quotes.toscrape.json","w") as f:
    json.dump(data,f)