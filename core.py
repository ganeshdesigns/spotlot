class coremap:
    def __init__(self, parking_lot, parking_spots):
        self.parking_lot = parking_lot
        self.parking_spots = parking_spots
        
    def check_spot_availability(self):
        """Check if any spot is available in the parking lot"""
        for spot in self.parking_spots:
            if not spot.occupied:
                return f"Spot number {spot.spot_number} is available."
        return "Sorry, all spots are occupied."
    
    def park_car(self, car):
        """Park a car in an available spot"""
        for spot in self.parking_spots:
            if not spot.occupied:
                return spot.occupy(car)
        return "Sorry, all spots are occupied."
    
    def remove_car(self, car):
        """Remove a car from its parked spot"""
        for spot in self.parking_spots:
            if spot.occupied and spot.occupying_car == car:
                return spot.vacate()
        return "Sorry, car not found in any spot."