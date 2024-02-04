from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
import pandas as pd

from selenium.webdriver.common.by import By

# Disable geolocation
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

base_url = "https://fancons.com/events/schedule.php?loc="
# Start with North America

con_data = []

continents = {'na': "North America", 'eu': "Europe", 'af': "Africa", 'as': "Asia", 'oc': "Oceania"}
types = ['comic', 'horror', 'tv']

for continent in continents.keys():
    for type in types:

        driver.get(base_url+continent+'&'+type)

        con_list_table = driver.find_element(By.ID, "ConListTable")
        con_list_container = con_list_table.find_element(By.TAG_NAME, 'tbody')
        con_list_rows = con_list_container.find_elements(By.TAG_NAME, 'tr')

        for row in con_list_rows:
            column = row.find_elements(By.TAG_NAME, 'td')
            
            con_link = column[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            con_name = column[0].text

            con_date = column[1].text

            loc_and_venue = column[2].text.split('\n')
            
            con_venue = loc_and_venue[0]
            con_location = loc_and_venue[1]

            con_data.append({'link': con_link, 'name': con_name, 'date': con_date, 'location': con_location, 'venue': con_venue, 'continent': continents[continent], 'type': type})
    
con_data_df = pd.DataFrame(con_data)
# print(con_data_df)

con_data_df.to_csv('./ComicCons.csv')
# print(example_link.get_attribute('outerHTML'))
# columns = example_link.find_elements(By.TAG_NAME, 'td')
# print(len(columns))

# print(con_list_links)
# print(len(con_list_links))
# print(con_list_links[0].get_attribute('href'))

# link name date location venue_name | contact_name phone_number
