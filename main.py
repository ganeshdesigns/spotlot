#modules
from core import coremap
from car import carmap
from lot import lotmap
from spot import spotmap
from plates import platesmap
import re

# Create a parking lot
LT1 = lotmap("My Parking Lot", "123 Main St", 10)

# Create some parking spots
A1 = spotmap('A1')
A2 = spotmap('A2')
A3 = spotmap('A3')
B1 = spotmap('B1')
B2 = spotmap("B2")
B3 = spotmap("B3")
parking_spots = [A1,A2,A3,B1,B2,B3]

# Create a parking system
parking_system = coremap(LT1, parking_spots)

# Create a parking system
parking_system = coremap(LT1, parking_spots)

# platesmap.main()
# fileptr = open("log.txt","r")
# content = fileptr.readlines()
# fileptr.close()
    
# def remove_special_characters(text):
#     return re.sub(r'[^a-zA-Z0-9 ]', '', text)
# carnumber = remove_special_characters(content[0])
# print(carnumber)

# Create some cars
car_1 = carmap("Toyota", "Camry", "AP39GD3999")
car_2 = carmap("Honda", "Civic", "DEF456")
car_3 = carmap("Ford", "Mustang", "GHI789")



# Simulate cars entering the parking lot
print(car_1.park(LT1)) # "Car with license plate ABC123 parked successfully."
print(car_2.park(LT1)) # "Car with license plate DEF456 parked successfully."

# Check the number of available spots
print(parking_system.check_spot_availability()) # "Spot number 3 is available."

# Simulate a car entering the parking lot and not finding a spot
print(car_3.park(LT1)) # "Sorry, all spots are occupied."

# Simulate a car leaving the parking lot
print(car_1.remove()) # "Car with license plate ABC123 removed successfully."

# Check the number of available spots
print(parking_system.check_spot_availability()) # "Spot number 1 is available."git 