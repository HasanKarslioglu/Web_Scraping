from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import re


url = "https://www.booking.com/searchresults.html?ss=Roma%2C+Lazio%2C+Italia&ssne=Ankaran&ssne_untouched=Ankaran&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEXyAEM2AEB6AEB-AECiAIBqAIDuAKW_82xBsACAdICJGE0NTBkOTFiLTZiMWYtNDRhYy1hZTI3LWZlNmE4YTkwMmQ4YtgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-126693&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=it&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=09ae5d26e81c0663&ac_meta=GhAwOWFlNWQyNmU4MWMwNjYzIAEoATICaXQ6BHJvbWFAAEoAUAA%3D&checkin=2024-06-21&checkout=2024-06-22&group_adults=1&no_rooms=1&group_children=0"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-US, en;q=0.5"}

response = requests.get(url, headers=headers)
      

soup = BeautifulSoup(response.text, 'html.parser')
hotels = soup.findAll('div', {'data-testid': 'property-card'})
hotels_data = []

pattern = r'(\d+(?:\.\d+)?)\s*(km|m)'

def get_element_text(type, hotel, data_testid):
    element = hotel.find(type, {'data-testid': data_testid})
    if element is not None:
        text = element.text.strip()
        if text:
            return text
    return "NOT GIVEN"

for hotel in hotels: 
  name = get_element_text("div", hotel, "title")
  price = get_element_text("span", hotel, "price-and-discounted-price")
  address = get_element_text("span", hotel, "address")
  
  distance = get_element_text("span", hotel, "distance")
  match = re.search(pattern, distance)
  if match:
      distance = match.group(1) +" "+ match.group(2) 
  
  #RATING HOOKING
  rating_div = hotel.find('div', {'data-testid': 'review-score'})
  if rating_div is not None:
    rating_number = rating_div.find("div",{"class":"a3b8729ab1"}).contents[0]
    if rating_number is not None:
        rating_number = rating_number.text.strip()
    rating_text = rating_div.find("div",{"class":"a3b8729ab1 e6208ee469 cb2cbb3ccb"})
    if rating_text is not None:
        rating_text = rating_text.text.strip()
    overall_rating = "NOT GIVEN"
    if rating_text != "NOT GIVEN" and rating_number != "NOT GIVEN":
      overall_rating = rating_text +" "+ rating_number
  
  hotels_data.append({
  "name": name,
  "address": address,
  "distance": distance,
  "overall_rating": overall_rating,
  "price": price
  })

hotels = pd.DataFrame(hotels_data[:10])
hotels.head()
hotels.to_csv('test_hotels.csv', header=True, index=False)