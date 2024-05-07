from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

city_destId = {
    "Rome": -126693,
    "Venice": -132007,
    "Amsterdam": -2140479,
    "Vilnius": -2620663,
    "Prague": -553173,
    "London": -2601889,
    "Paris": -1456928,
    "Berlin": -1746443,
    "Milano": -121726,
    "Florence": -117543
}

def create_booking_url_template(city,dest_id, checkin_date, checkout_date):
    return "https://www.booking.com/searchresults.html?ss={city}&ssne={city}&ssne_untouched={city}&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4YzkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id={dest_id}&dest_type=city&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0".format(city=city, dest_id=dest_id,checkin_date=checkin_date, checkout_date=checkout_date)

def request(city, checkin_date, checkout_date):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "en-US, en;q=0.5"}
    url = create_booking_url_template(city,city_destId.get(city), checkin_date, checkout_date)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return False

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
    count = 0
    for hotel in hotels:
        count += 1
        if count == 11:
            break

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

        hotels_data.append({
        "name": name,
        "address": address,
        "distance": distance,
        "ratingText": rating_text,
        "ratingNumber": rating_number,
        "price": price
        })

    hotels = pd.DataFrame(hotels_data)
    hotels.head()
    hotels.to_csv('myhotels.csv', header=True, index=False)

    return True