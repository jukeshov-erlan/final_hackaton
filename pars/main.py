import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

url = 'https://www.kinopoisk.ru/lists/movies/top250/'
driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

film_links = soup.find_all('div', class_='styles_root__ti07r')

titles = []
years = []
casts = []
descriptions = []

for link in film_links:
    title = link.find('span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj').text.strip().replace(',', '')
    description = link.find('span', class_='desktop-list-main-info_truncatedText__IMQRP').text.strip().replace(',', '')
    year = link.find('span', class_='desktop-list-main-info_secondaryText__M_aus').text.strip().replace(',', '')
    cast = link.find_all('span', class_='desktop-list-main-info_truncatedText__IMQRP')[1].text.strip().replace(',', '')

    title = title.replace('"', '').replace('•', '')
    description = description.replace('"', '').replace('•', '')
    cast = cast.replace('"', '').replace('•', '')

    titles.append(title)
    descriptions.append(description)
    years.append(year)
    casts.append(cast)

    if len(titles) == 50:
        break

with open('movies.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Year', 'Cast', 'Description'])
    for title, year, cast, description in zip(titles, years, casts, descriptions):
        writer.writerow([title, year, cast, description])

driver.quit()
