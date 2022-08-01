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

#Fetching anchor tags of quotes
tag_elements_in_html_content = soup.find_all("span", class_ = "tag-item")

author_names_list = []
quotes_data = []
authors_data = []  #list of authors information



# Fetching quotes from next page for each_tag =>maximum pages for each_tag element having only two pages
# Here using while loop to to get the data from next page of


def scrape_page(link_url, quotes_data,author_names_list):

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
            author_names_list.append((name))






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

def making_link_for_tag_elements(each_tag_element):

    link = each_tag_element.select_one('.tag-item a')["href"]
    string_link = each_tag_element.a.text
    link_url = "http://quotes.toscrape.com" + link # Fetching url for all tag elements to scrape data

    scrape_page(link_url,quotes_data,author_names_list)

def get_unique_author_name_to_fetch_html(unique_author_names):
    list_links = []
    for i in unique_author_names:
        result = ''
        update = i.split(" ")
        for i in update:
            if '.' in i:
                res = ''
                for j in i:
                    if j == ".":
                        res += "-"
                    else:
                        res += j
                # print(res)
                result += res
            elif "'" in i:
                r = ''
                for k in i:
                    if k == "'":
                        continue
                    r += k
                result += r
            else:
                result += i + "-"
        list_links.append(result)
    updated_name_list = []
    for p in list_links:
        length_ = len(p)
        updated_name = p[:length_ - 1]
        updated_name_list.append(updated_name)
    return updated_name_list


# Getting tag elements with their links to make url to fetch data in next pages => Iteration makes every tag element
# availble to make links to extract data from HTML
for each_tag_element in tag_elements_in_html_content:
    making_link_for_tag_elements(each_tag_element)

unique_author_names = list(set(author_names_list))

# Get list_of_unique_author_names in string format in order to put in link to get parsed HTML

list_of_authors = get_unique_author_name_to_fetch_html(unique_author_names)


# Fetch the author information by iterating the list_of_authors
authors_data = []
for each_author_inform in list_of_authors:
    information = dict()
    url = "http://quotes.toscrape.com/author/" + each_author_inform + "/"

    request_url = requests.get(url)
    soup = BeautifulSoup(request_url.content,"html.parser")

    author_details = soup.find("div", "author-details")
    author_name = each_author_inform.split('-')
    name = " ".join(author_name)


    author_born_location = author_details.p
    list_of_born_location = author_born_location.select("span")

    information['name'] = name
    information['born'] = list_of_born_location[0].text + "," + list_of_born_location[1].text
    information['reference'] = url
    authors_data.append(information)

data = dict()
data["quotes"] = quotes_data
data["author"] = authors_data



#Saving data in a file

with open("quotes.toscrape.json","w") as f:
    json.dump(data,f)