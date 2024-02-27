import requests
from bs4 import BeautifulSoup

url = 'https://www.burda-auction.com/cz/aukce-72/show/2765/filatelie-evropa-rakousko-i-emise-1850/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Return or items for sale
# div_elements = soup.find_all('div', class_='flex-item w25 polozka')

div_elements = [div for div in soup.find_all('div', class_='flex-item w25 polozka') if 'Znak 1Kr' in div.get_text()]

final_list = []

# Prochází a vypisuje nalezené prvky
for div in div_elements:
    # stamp_type_id, description, strip, price, sale_date, name_of_auction, url_on_auction
    # itemCondition quality
    nested_list = []
    description_span = div.find('span', {'itemprop': 'description'})
    if description_span:
        # Type Hell
        if "Znak 1Kr" in description_span.get_text(strip=True):
            print(description_span.get_text(strip=True))
            if "ruční" in description_span.get_text(strip=True):
                if "okrově žlutá" in description_span.get_text(strip=True):
                    used_condition_meta = div.find('meta', {'itemprop': 'itemCondition'})
                    
                    # Get Jakost
                    jakost_div = div.find('div', class_='p_ctj help')
                    data_jakost_value = jakost_div.get('data-jakost')

                    if data_jakost_value:
                        print(data_jakost_value)
                        if data_jakost_value == "**":
                            nested_list.append(1)
                        elif data_jakost_value == "*":
                            nested_list.append(2)
                        elif data_jakost_value == "razítko" or data_jakost_value == "(*)":
                            nested_list.append(3)
                        else:
                            nested_list.append("X")

            if "strojový" in description_span.get_text(strip=True):
                nested_list.append(4)

        nested_list.append(description_span.get_text(strip=True))
        
        # Strip
        if "-pásky" in description_span.get_text(strip=True):
            nested_list.append(True)
        else:
            nested_list.append(False)

        # Money or back
        returned_div = div.find('div', class_='tbc')
        if returned_div:
            print(returned_div.get_text(strip=True))
            if "Vráceno" in returned_div.get_text(strip=True):
                nested_list.append(0)
            else:
                string_from_web = returned_div.get_text(strip=True)
                final_str_list = string_from_web.split('za:')
                final_str = final_str_list[1].replace('\xa0', '').replace('Kč', '')
                nested_list.append(int(final_str))
        
        # Sale date dont know how to get it maybe i create csv where is save it?:
        nested_list.append('date')

        nested_list.append("Burda")
        nested_list.append(url)
    print('---')  # Oddělovací řádek mezi jednotlivými prvky pro lepší čitelnost
    final_list.append(nested_list)

print(final_list)
