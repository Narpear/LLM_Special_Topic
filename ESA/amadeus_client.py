import amadeus

class AmadeusClient:
    def __init__(self):
        self.amadeus = amadeus.Client(
            client_id='id_here',
            client_secret='secret_here'
        )

    def get_flight_offers(self, origin, destination, departure_date, n_adults):
        response = self.amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=n_adults
        )
        return response.data

    def get_hotel_by_city(self, city_code):
        response = self.amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)
        return response.data
    
client = AmadeusClient()
def getting_flight_offers(origin, destination, departure_date, n_adults):
    return client.get_flight_offers(origin, destination, departure_date, n_adults)

def getting_hotels(city_code):
    return client.get_hotel_by_city(city_code)



# flight_data = client.get_flight_offers(origin = 'ATH', destination = 'LAX', departure_date = '2024-11-01', n_adults = 2)
# print(flight_data)
# print('------------------------------------------------------------------------------------------------------')
# hotel_data = client.get_hotel_by_city('PAR')
# print(hotel_data)