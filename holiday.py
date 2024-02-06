# This is a program to calculate a user's total holiday cost.
# The total cost includes flight, hotel and car-rental costs.

def hotel_cost(num_nights):
    """
    We calculate the total hotel cost based on the number of nights.
    We assume a fixed price per night.
    """
    num_nights = int(num_nights)
    price_per_night = 100  # Assumed price per night
    return num_nights * price_per_night

def plane_cost(city_flight):
    """
    We calculate the flight cost based on the destination.
    Different cities have different flight costs.
    """
    city_prices = {
        "Paris": 300,
        "London": 250,
        "New York": 800,
        "Tokyo": 900,
        "Sydney": 700
    }
    return city_prices.get(city_flight, 0)  # returns 0 if city is not in the list

def car_rental(rental_days):
    """
    We calculate the total car-rental cost based on the number of rental days.
    We assume a fixed daily rental cost.
    """
    rental_days = int(rental_days)
    daily_rental_cost = 40  # example daily rental cost
    return rental_days * daily_rental_cost

def holiday_cost(city_flight, num_nights, rental_days):
    """
    We calculate the total holiday cost by summing up the hotel, plane and car-rental costs.
    """
    return hotel_cost(num_nights) + plane_cost(city_flight) + car_rental(rental_days)

# User input
print("Please enter your holiday details to calculate the total cost.")
city_flight = input("Which city will you be flying to (Paris, London, New York, Tokyo, Sydney)? ").capitalize()
if city_flight not in ["Paris", "London", "New York", "Tokyo", "Sydney"]:
    print("Invalid city. Please enter one of the specified cities.")
else:
    try:
        num_nights = int(input("How many nights will you be staying at a hotel? "))
        rental_days = int(input("How many days will you be hiring a car for? "))
        
        # Calculate and print the total holiday cost
        total_cost = holiday_cost(city_flight, num_nights, rental_days)
        print(f"The total holiday cost for your trip to {city_flight} is ${total_cost}.")
    except ValueError:
        print("Invalid input. Please enter numeric values for nights and rental days.")
