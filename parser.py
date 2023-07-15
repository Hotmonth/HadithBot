import requests
from bs4 import BeautifulSoup
from db import conn, cursor

url = "https://sunnah.com/bukhari/"
for i in range(0,  98):

    response = requests.get(f'{url}{i}')
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    text_details_list = soup.find_all('div', class_='text_details')

    for text_details in text_details_list:
        text = text_details.get_text(strip=True)
        narrator_element = text_details.find_previous_sibling(
                'div', class_='hadith_narrated')
        narrator = narrator_element.get_text(strip=True) if narrator_element else ""
        cursor.execute('INSERT INTO hadith (narrator, text_details) VALUES (?, ?)', (narrator, text))
        conn.commit()

conn.close()
