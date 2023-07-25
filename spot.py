class spotmap:
    def __init__(self, spot_number):
        self.spot_number = spot_number
        self.occupied = False
        self.occupying_car = None
        
    def occupy(self, car):
        """Occupy the spot with a car"""
        if not self.occupied:
            self.occupied = True
            self.occupying_car = car
            return f"Spot number {self.spot_number} occupied by car with license plate {car.license_plate}."
        else:
            return f"Spot number {self.spot_number} already occupied by car with license plate {self.occupying_car.license_plate}."
        
    def vacate(self):
        """Vacate the spot"""
        if self.occupied:
            vacating_car = self.occupying_car
            self.occupied = False
            self.occupying_car = None
            return f"Spot number {self.spot_number} vacated by car with license plate {vacating_car.license_plate}."
        else:
            return f"Spot number {self.spot_number} is already vacant."