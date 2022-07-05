# %%
import requests
from functools import lru_cache


@lru_cache
def get_coordinates(api_key, place_query):
    response = requests.get(
        f"https://api.myptv.com/geocoding/v1/locations/by-text?searchText={place_query}&apiKey={api_key}"
    )
    location = response.json()["locations"][0]
    return {
        "longitude": location["referencePosition"]["longitude"],
        "latitude": location["referencePosition"]["latitude"],
        "country": location["address"]["countryName"],
        "city": location["address"]["city"],
    }
