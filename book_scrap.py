import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

def authors_startwith(text):
	if text.startswith('/authors'):
		return True
	else:
		return False

books = []

for i in tqdm(range(1, 33)):

	response = requests.get("https://www.haymarketbooks.org/books??page="+str(i))

	soup = BeautifulSoup(response.text, 'html.parser')

	editions = soup.find_all("li", class_='edition_item')
	for edition in editions:

		title = edition.find("h3").text
		teaser = edition.find("span", class_='teaser').find("p").text

		authors = [author.text for author in edition.find_all("a", href=authors_startwith)]

		cover_style = edition.find("div", class_="cover-image")["style"]
		cover = cover_style.split("(")[1].replace(");","")

		book = {
			"title": title,
			"teaser": teaser,
			"authors": authors,
			"cover": cover
		}

		books.append(book)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)