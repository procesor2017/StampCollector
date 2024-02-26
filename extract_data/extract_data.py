import requests
from bs4 import BeautifulSoup

url = 'https://www.burda-auction.com/cz/aukce-72/show/2765/filatelie-evropa-rakousko-i-emise-1850/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Return or items for sale
# div_elements = soup.find_all('div', class_='flex-item w25 polozka')

div_elements = [div for div in soup.find_all('div', class_='flex-item w25 polozka') if 'Znak 1Kr' in div.get_text()]

# Prochází a vypisuje nalezené prvky
for div in div_elements:
    print(div.prettify())