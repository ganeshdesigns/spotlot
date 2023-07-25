class lotmap:
    def __init__(self, name, address, total_spots):
        self.name = name
        self.address = address
        self.total_spots = total_spots
        self.available_spots = total_spots
        self.parking_history = []
        
    def check_availability(self):
        """Return the number of available spots in the parking lot"""
        return self.available_spots
    
    def park_car(self, car):
        """Park a car in the parking lot and update the available spots"""
        if self.available_spots > 0:
            self.available_spots -= 1
            self.parking_history.append(car)
            return f"Car with license plate {car.license_plate} parked successfully."
        else:
            return "Sorry, parking lot is full."
    
    def remove_car(self, car):
        """Remove a car from the parking lot and update the available spots"""
        if car in self.parking_history:
            self.available_spots += 1
            self.parking_history.remove(car)
            return f"Car with license plate {car.license_plate} removed successfully."
        else:
            return "Sorry, car not found in parking history."