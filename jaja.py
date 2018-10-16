<<<<<<< HEAD

page = requests.get("https://coins.live/news/")
soup = bs4.BeautifulSoup(page.content, 'html.parser')
headings = soup.body.find_all('span', attrs={'class': 'card-title'})
for x in headings:
    print(x.text,'\n')
=======
import requests
import bs4
page = requests.get("https://coinranking.com/")
a = bs4.BeautifulSoup(page.content, 'html.parser')
print(a)
>>>>>>> facbff95e19e8ada55f236a083a73a04b853c9fe
