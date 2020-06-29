# -*- coding: utf-8 -*-
from random import randint
from copy import deepcopy

class Elevator(object):
    """An elevator class. Elevator has its position, customers inside and direction."""
    register_list = list()
    current_floor = 0
    direction = 1

    def move(self):
        """Step function for elevator movement.
        In every step elevator come one floor higher or one floor lower."""
        self.current_floor += self.direction

    def exit_customers(self):
        """Function to clear all customers on their desired floor.
        Called automatically in run method of building class.
        """
        for customer in list(self.register_list):
            if customer.dst_floor == self.current_floor:
                self.cancel_customer(customer)

    def register_customer(self, customer):
        """Function to add specific customer to elevator list"""
        self.register_list.append(customer)

    def cancel_customer(self, customer):
        """Function to erase specific customer from elevator list"""
        self.register_list.remove(customer)

class Customer(object):
    """A customer class. Customer has his/hers unique ID number,
    starting floor number and destination floor number.
    """
    start_floor = None
    dst_floor = None
    ID = None

    def __init__(self, ID, floorsNum):
        """Initializes customer and selects random value of start and destined floor.
        Destination floor differ from starting floor by default.
        """
        self.ID = ID
        self.start_floor = randint(0, floorsNum-1)
        self.dst_floor = randint(0, floorsNum-2)
        if self.dst_floor >= self.start_floor:
            self.dst_floor += 1

class Building(object):
    """A building class. Building has number of floors, list of customers outside the elevator and
    its own elevator object. Strategy of an elevator is set by integer, where 0 is default strategy
    and 1 is an example very bad strategy.
    """
    num_of_floors = None
    customer_list = list()
    elevator = None

    strategy = 0

    def __init__(self):
        """Creates building class and adds list of customers to handle.
        Customer list is sorted by starting floor value for performance reasons.
        """
        self.num_of_floors = self.get_value("Please write number of floors in the building: ",\
        "Incorrect value. Number of floors should be integer higher than 1.", 2)
        customers_num = self.get_value("Please write number of customers: ",\
        "Incorrect value. Number of customers should be non-negative integer.", 0)
        for i in range(customers_num):
            self.customer_list.append(Customer(i, self.num_of_floors))
        self.customer_list = sorted(self.customer_list, key=lambda x: x.start_floor)
        self.elevator = Elevator()

    def get_value(self, message, incorrect_message, minimal_value):
        """Interface method for acquiring integer value from user, higher than minimal value."""
        val = None
        try:
            val = int(raw_input(message))
        except ValueError:
            print incorrect_message
            return self.get_value(message, incorrect_message, minimal_value)
        if val < minimal_value:
            print incorrect_message
            return self.get_value(message, incorrect_message, minimal_value)
        else:
            return val



    def direction_default_strategy(self):
        """Default function of elewator work - it starts with going to the roof of building, then
        comes back to the first floor."""
        if self.elevator.current_floor >= self.num_of_floors - 1:
            self.elevator.direction = -1
        elif self.elevator.current_floor <= 0:
            self.elevator.direction = 1

    def direction_bad_strategy(self):
        """Example function of very bad strategy. Elevator takes desired floor of the first
        customer and elevates him to desired location, then repeats for the next customer.
        If no customer is in elevator it just goes to the up and down, as in default strategy.
        """
        if len(self.elevator.register_list) is 0:
            self.direction_default_strategy()
            return
        firstval = self.elevator.register_list[0].dst_floor
        if self.elevator.current_floor > firstval:
            self.elevator.direction = -1
        else:
            self.elevator.direction = 1

    def enter_customers(self):
        """Function to get all customers on elevators floor and erase them from class list."""
        for customer in list(self.customer_list):
            if customer.start_floor == self.elevator.current_floor:
                self.elevator.register_customer(customer)
                self.customer_list.remove(customer)

    def run(self):
        """Core step function. Every time when called:
        - awaiting customers enter the elevator (register_customer is called)
        - the elevator direction value (+/-1) is chosen
        - elevator moves one floor up or one floor down, depending on direction value
        - any customer on his/hers floor leaves the elevator (cancel_customer is called)
        """

        self.enter_customers()
        if self.strategy == 0:
            self.direction_default_strategy()
        else:
            self.direction_bad_strategy()
        self.elevator.move()
        self.elevator.exit_customers()


    def output(self):
        """Returns total number of steps done by elevator in set strategy.
        """
        total_number = 0
        while self.awaiting_customers():
            self.run()
            total_number += 1
        return total_number

    def awaiting_customers(self):
        """returns True if there is at least one customer not on his/hers destinated floor.
        Otherwise returns False."""
        if len(self.customer_list) > 0 or len(self.elevator.register_list) > 0:
            return True
        return False


def main():
    """main function"""

    building_def = Building()
    building_bad = deepcopy(building_def)
    print "Number of steps for default strategy:", building_def.output()
    building_bad.strategy = 1
    print "Number of steps for bad strategy:", building_bad.output()



if __name__ == "__main__":
    main()



"""
Comparision of strategies: default strategy in pesimistic case needs 2*N steps (order O(N)), where N is total number of
floors in building. For large number of customers mean number of steps is very close to pesimistic cases
value. 
Example bad strategy goes to the floor desired by the first customer, then goes to the floor chosen
by the customer next in line and so on. Because elevator stops on every floor, during this travel
all other customers come in and out as well. For small number of customers (less than 5) and comparable
big number of floors this strategy can actually work better than default one, but for larger number of
customers it becomes very unstable. Estimated pesimistic number of steps is of the order N^2 (O(N^2)) for 
large number of customers, where N again is equal to total number of floors (case when first customer goes to 3*N/4-th floor,
second goes to N/2-th, third goes to 3*N/4+1-th, fourth goes to N/2-1 -th... and so on). Mean value
is about 3*N for case of large number of customers.

"""