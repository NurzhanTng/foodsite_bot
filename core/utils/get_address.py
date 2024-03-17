# from geopy.geocoders import Nominatim


def get_address(latitude: float, longitude: float):
    # geolocator = Nominatim(user_agent="tutorial")
    location = f"{latitude}, {longitude}"
    # address = geolocator.reverse(location, language="ru")

    # if address is None:
    #     print(f'---- get_address ----: Address not found: {latitude}, {longitude}')
    #     return ''

    # return address.address
