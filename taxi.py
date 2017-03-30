import random


class Constants:
    class Diesel:
        OVERHAUL_MILEAGE = 150000
        OVERHAUL_COSTS = 700
        DEPRECIATION = 10.5
        FUEL_RATE = 6
        FUEL_COST = 1.8

    class Gas:
        OVERHAUL_MILEAGE = 100000
        OVERHAUL_COSTS = 500
        DEPRECIATION = 9.5
        FUEL_RATE = 8
        FUEL_COST = 2.2  # default
        AI92_COST = 2.2
        AI95_COST = 2.4

    PRICE = 10000
    ENGINE_REPLACEMENT_COST = 3000
    MILEAGE_LIMIT_AI92_REQUIRED = 50000


class Car(object):
    def __init__(self, serial_number, tachograph, gas_or_diesel):
        # class attributes initialized by constants
        self.engine_replacement_cost = Constants.ENGINE_REPLACEMENT_COST
        self.overhaul_mileage = gas_or_diesel.OVERHAUL_MILEAGE
        self.overhaul_costs = gas_or_diesel.OVERHAUL_COSTS
        self.depreciation = gas_or_diesel.DEPRECIATION
        self.new_engine_fuel_rate = self.fuel_rate = gas_or_diesel.FUEL_RATE
        self.fuel_cost = gas_or_diesel.FUEL_COST
        self.fuel_tank = 75 if serial_number % 5 else 60
        self.total_fuel_sp = self.fuel_costs = self.number_of_fil = self.number_of_engine_replacements = 0
        self.tachograph = tachograph

    def __setattr__(self, key, mileage):
        if key == "tachograph":
            try:
                old_key = object.__getattribute__(self, key)
            except AttributeError:
                old_key = 0
            # Cannot decrease the tachograph reading. If we try to decrease, just use old_key
            object.__setattr__(self, key, mileage if mileage > old_key else old_key)
        else:
            object.__setattr__(self, key, mileage)

    def drive(self, distance):
        self.tachograph += distance
        # Every 1000 km current_fuel_rate changed
        i_1000 = 0
        while i_1000 <= distance:
            # after the 1st 50000 km fuel_cost changed (for Gas only)
            if i_1000 == Constants.MILEAGE_LIMIT_AI92_REQUIRED and self.fuel_cost == Constants.Gas.AI92_COST:
                self.fuel_cost = Constants.Gas.AI95_COST
            if self.number_of_engine_replacements > 0 and self.fuel_cost == Constants.Gas.AI95_COST:
                self.fuel_cost = Constants.Gas.AI92_COST
            self.fuel_rate += (self.fuel_rate / 100)
            self.fuel_costs += self.fuel_rate * 10 * self.fuel_cost
            self.total_fuel_sp += self.fuel_rate * 10
            i_1000 += 1000

        self.number_of_fil = self.total_fuel_sp // self.fuel_tank

    def value_calc(self):
        second_hand_v = Constants.PRICE - self.depreciation * self.tachograph / 1000 - self.depreciation * (self.tachograph / self.overhaul_mileage)
        # engine replacement
        if second_hand_v <= 0 and self.number_of_engine_replacements == 0:
            self.number_of_engine_replacements += 1
            second_hand_v -= Constants.ENGINE_REPLACEMENT_COST
            self.fuel_rate = self.new_engine_fuel_rate
        return second_hand_v


# easy to check the engine type -- if isinstance(Taxi[1], Diesel_Car):
class DieselCar(Car):
    def __init__(self, sn, tachograph):
        super().__init__(sn, tachograph, Constants.Diesel())


class GasCar(Car):
    def __init__(self, sn, tachograph):
        super().__init__(sn, tachograph, Constants.Gas())

# Cars initialization
Number_of_cars = m = 100
total_value = Loan_amount = 0
Taxi = {i: DieselCar(i, 0) if i % 5 else GasCar(i, 0) for i in range(1, Number_of_cars + 1)}  #  +1?

while True:
    # just drive from 55.000 to 286.000 km
    for i in range(1, Number_of_cars + 1):
        Taxi[i].drive(random.randint(55000, 286000))
        if Taxi[i].value_calc() < 0:
            Loan_amount -= Taxi[i].value_calc()

    # bubble sorting
    while m > 0:
        for i in range(1, m - 1):
            if Taxi[i].value_calc() > Taxi[i+1].value_calc():
                Taxi[i], Taxi[i+1] = Taxi[i+1], Taxi[i]
        m -= 1

    for i in range(1, Number_of_cars): total_value += Taxi[i].value_calc()

    print("Please see below the parameters of the most worn car.\nAre you sure you don't need to order some new cars?")
    print("\t Mileage = " + str(Taxi[Number_of_cars].tachograph))
    print("\t Fuel tank volume = " + str(Taxi[Number_of_cars].fuel_tank) + " litres")
    print("\t Depreciation value = {:0,.2f}".format(Taxi[Number_of_cars].value_calc()).replace(u',', u' ') + " USD")
    print("\t Total fuel cost = {:0,.2f}".format(Taxi[Number_of_cars].fuel_costs).replace(u',', u' ') + " USD")
    print("\t Number of refuelling = %.0f" % Taxi[Number_of_cars].number_of_fil)
    print("\t Number of engine replacements = %.0f" % Taxi[Number_of_cars].number_of_engine_replacements)
    print("\nTotal value of all cars = {:0,.2f}".format(total_value).replace(u',', u' ') + " USD")
    print("Total loan amount = {:0,.2f}".format(Loan_amount).replace(u',', u' ') + " USD")
    question = str(input("Do you want to continue (yes/no)?  :"))
    if question.lower() == "no":
        raise SystemExit(1)
