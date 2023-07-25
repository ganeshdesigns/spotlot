class carmap:
    def __init__(self, make, model, license_plate):
        self.make = make
        self.model = model
        self.license_plate = license_plate
        self.parked = False
        
    def park(self, parking_lot):
        """Park the car in the given parking lot"""
        if not self.parked:
            parking_response = parking_lot.park_car(self)
            if "success" in parking_response:
                self.parked = True
                self.parking_lot = parking_lot
            return parking_response
        else:
            return f"Car with license plate {self.license_plate} already parked at {self.parking_lot.name}."
    
    def remove(self):
        """Remove the car from the parking lot"""
        if self.parked:
            remove_response = self.parking_lot.remove_car(self)
            if "success" in remove_response:
                self.parked = False
                self.parking_lot = None
            return remove_response
        else:
            return f"Car with license plate {self.license_plate} not parked in any lot"
