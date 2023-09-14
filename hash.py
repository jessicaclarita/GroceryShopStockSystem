from datetime import datetime
from stack import Stack
import re
import ast


class HashTable(Stack):
    def __init__(self):  # initializing constructors
        super().__init__()
        f = open("inventory.txt", "r+")
        r = f.readlines()
        self.__MAX = 10    # inventory size
        self.arr = [[] for i in range(self.__MAX)]  # inserting empty [] to the hash table
        for items in r:
            item = ast.literal_eval(items)      # turning string values into the original data structure
            key = item[0]
            value = item[1]
            index = self.get_hash(key)
            self.arr[index].append([key, value])     # appending keys and values from inventory lists

    def get_hash(self, key):         # takes key which is the product ID and return the hash element's position or index
        index = 0                    # to store the ASCII value of key elements
        for characters in key:
            index += ord(characters)    # find the ASCII code for each characters and sum it together
        return index % self.__MAX         # sum of ASCII code mod it with the array's size to get the element's index

    def __getitem__(self, key):             # function to return value when user enter the key
        index = self.get_hash(key)          # getting the key's index by calling the get_hash function
        for element in self.arr[index]:     # for the current element in the inserted index(key)
            if element[0] == key:           # if the element's key is same as inserted key, then...
                return element[1]           # it will return the value

    def stockIn(self, key, newValue):  # set the value and pair it with the key
        index = self.get_hash(key)         # getting the key's index by calling the get_hash function
        found = False                      # to handle when collision happens: ,, pattern: [[key, value] , [], [], []]
        for idx, element in enumerate(self.arr[index]):   # for the current element in the inserted index, index each
            if len(element) == 2 and element[0] == key:   # if element's length is 2 and first element same as old key
                found = True  # values will be replaced if same exact key was entered
                print("The product is already existed. The current value of the product is:", self.__getitem__(key))
                rpl = self.string(input("Do you wish to replace it's details? Please enter 'Yes' or 'No': "))
                if rpl == "yes" or rpl == "y":
                    oldValue = element[1]         # storing old values - to count and replace quantity and price
                    description = newValue[0]                 # new description
                    old_elements = oldValue[1] * oldValue[2]  # old quantity x old price
                    new_elements = newValue[1] * newValue[2]  # new quantity x new price
                    total_quantity = oldValue[1] + newValue[1]  # old quantity + new quantity
                    newAveragePrice = int((old_elements + new_elements) / total_quantity)  # totalElements/totalQuantity
                    newValue = [description, total_quantity, newAveragePrice]
                    self.arr[index][idx] = [key, newValue]  # new element in the index inserted will replace the old one
                    print(key, "'s details have been replaced successfully.")

                    # transaction log - date, id, desc, quantity, unit price
                    date = self.getTime()    # get date/time
                    newQuantity = total_quantity - oldValue[1]
                    self.push([date, key, description, str('+') + str(newQuantity), newAveragePrice])

                    # asking if users want to continue and proceed to main page
                    self.con()

                else:
                    a = self.string(input("Do you wish to add the product using a new product ID? Please enter 'Yes' or 'No': "))
                    if a == "yes" or a == "y":
                        Id = self.getID()
                        desc = self.getDescription(input("Description: "))
                        quantity = self.getQuantity()
                        price = self.getPrice()
                        self.stockIn(Id, [desc, quantity, price])
                    else:
                        self.con()   # asking if users want to continue and proceed to main page
        if not found:                                    # if not the same key but same index, then ...
            self.arr[index].append([key, newValue])      # it will just append it to the element
            print(key, self.__getitem__(key), "has been added successfully.")

            # transaction log - date, id, desc, quantity, unit price
            date = self.getTime()
            self.push([date, key, newValue[0], str('+') + str(newValue[1]), newValue[2]])

            # asking if users want to continue and proceed to main page
            self.con()

    def stockOut(self, key):
        index = self.get_hash(key)
        found = False
        print("The current value of the product is:", self.__getitem__(key))
        for idx, element in enumerate(self.arr[index]):
            if len(element) == 2 and element[0] == key:
                found = True
                description = element[1][0]
                quantity = int(element[1][1])
                price = element[1][2]
                if quantity > 0:
                    w = int(self.digit(input("Please enter quantity you want to withdraw: ")))
                    while quantity < w:
                        print("Sorry the requested quantity exceeds the stock limit.")
                        w = int(self.digit(input("Please re-enter quantity: ")))
                    quantity -= w
                    self.arr[index][idx] = [key, [description, quantity, price]]
                    print(w, "items has been withdrawn successfully.")
                    print("The current value of the product is: ", self.__getitem__(key))

                    # transaction log
                    date = self.getTime()  # get date/time
                    self.push([date, key, description, str('-') + str(w), price])

                    # asking if users want to continue and proceed to main page
                    self.con()

                else:   # if product's quantity = 0
                    print("Sorry, the product is obsolete (out of stock).")
                    rmv = self.string(input("Do you wish to remove the product? Please enter 'Yes' or 'No': "))
                    if rmv == "y" or rmv == "yes":
                        self.remove(key)
                    else:
                        print("Ok!", key, self.__getitem__(key), "is still kept in the product list.")
                        self.con()   # asking if users want to continue and proceed to main page
        if not found:
            self.viewInventory()
            print("Sorry, the product ID you entered does not exist in the program.")
            c = self.string(input("Do you still want to continue stocking out? Please enter 'Yes' or 'No': "))
            if c == "yes" or c == "y":
                print(self.arr)
                d = input("Please re-enter product ID: ").upper()
                i = self.get_hash(d)
                for element in self.arr[i]:  # for the current element in the inserted index, index each
                    if len(element) == 2 and element[0] == d:
                        found = True
                        self.stockOut(d)
                if not found:
                    ask = input("This product ID is not available. Please re-enter: ").upper()
                    self.stockOut(ask)
            else:
                self.con()   # asking if users want to continue and proceed to main page


    def remove(self, key):             # function to delete the value
        index = self.get_hash(key)          # getting the key's index by calling the get_hash function
        found = False
        for idx, element in enumerate(self.arr[index]):  # for the current element in the inserted index, index each
            if len(element) == 2 and element[0] == key:  # if element's length is 2 and first element same as old key
                found = True
                print(key, self.__getitem__(key), "has been removed successfully.")
                del self.arr[index][idx]    # then delete the key in the inserted index
                self.con()   # asking if users want to continue and proceed to main page
        if not found:
            self.viewInventory()
            print("Sorry, the product ID you entered does not exist in the program.")
            o = self.string(input("Do you still want to continue removing? Please enter 'Yes' or 'No': "))
            if o == "yes" or o == "y":
                print(self.arr)
                e = input("Please re-enter product ID: ").upper()
                g = self.get_hash(e)
                for element in self.arr[g]:
                    if len(element) == 2 and element[0] == e:
                        found = True
                        self.remove(e)
                if not found:
                    ask = input("This product ID is not available. Please re-enter: ").upper()
                    self.remove(ask)
            else:
                self.con()   # asking if users want to continue and proceed to main page

    def viewInventory(self):    # to view the inventory report
        c = []
        for items in self.arr:
            if items != [] and len(items) == 1:     # [['ID', ['desc', 'quantity']]]
                c.append([items[0][0], items[0][1][0], items[0][1][1]])
                c.sort(key=lambda row: row[0])  # sort by product id
            elif items != [] and len(items) > 1:
                for item in items:      # [['ID', ['desc', 'quantity']], ['ID', ['desc', 'quantity']]]
                    c.append([item[0], item[1][0], item[1][1]])
                    c.sort(key=lambda row: row[0])  # sort by product id


        print("==========================================================")
        print("{:<5} {:<20} {:<20} {:<10}".format('No.', 'Product ID', 'Description', 'Quantity'))
        for i in range(0, len(c)):
            d = {i+1: [c[i][0], c[i][1], c[i][2]]}
            for key, value in d.items():
                Id, desc, quantity = value
                print("{:<5} {:<20} {:<20} {:<10}".format(key, Id, desc, quantity))
        print("===========================================================")

        grandTotalQuantity = 0
        grandTotalValues = 0
        for elements in self.arr:
            if elements != [] and len(elements) == 1:   # [['ID', ['desc', 'quantity']]]
                quantity = elements[0][1][1]
                price = elements[0][1][2]
                value = quantity*price
                grandTotalQuantity += quantity
                grandTotalValues += value
            elif elements != [] and len(elements) > 1:  # [['ID', ['d', 'q', 'p']], ['ID', ['d', 'q', 'p']]]
                for element in elements:
                    q = element[1][1]
                    p = element[1][2]
                    v = q * p
                    grandTotalQuantity += q
                    grandTotalValues += v




        print("\nThe total product in inventory:", len(c))
        print("The grand total quantity of all the products:", grandTotalQuantity)
        print("The grand total values of all the products: 💲" + str(grandTotalValues) + "\n")

    def reInput(self):  # re-input data to inventory.txt file before exiting the program
        f = open("inventory.txt", "w+")
        data = []
        for elements in self.arr:
            if elements != [] and len(elements) == 1:      # [['ID', ['desc', 'quantity']]]
                Id = elements[0][0]
                desc = elements[0][1][0]
                quantity = elements[0][1][1]
                price = elements[0][1][2]
                data.append(str([Id, [desc, quantity, price]]) + "\n")
            elif elements != [] and len(elements) > 1:  # [['ID', ['d', 'q', 'p']], ['ID', ['d', 'q', 'p']]]
                for element in elements:
                    i = element[0]
                    d = element[1][0]
                    q = element[1][1]
                    p = element[1][2]
                    data.append(str([i, [d, q, p]]) + "\n")

        f.writelines(data)
        f.close()

    def mainPage(self):
        print("\nWelcome to Grocery Shop Stock Main System 📦\n")
        self.action(int(self.digit(input("What action would you like to perform?"
                                 "\n1. Stock In Product\n2. Stock Out Product"
                                 "\n3. Remove Product\n4. View Inventory report"
                                 "\n5. View Latest Transaction Log\n6. Exit Program"
                                 "\n\nPlease enter the number based on the list above: "))))

    def con(self):  # asking if users want to continue and proceed to main page
        c = self.string(input("\nWould you like to continue and proceed to main page? \nPlease enter 'Yes' or 'No': "))
        if c == 'yes' or c == 'y':
            self.mainPage()
        else:
            self.reInput()  # re-input data to inventory.txt file before exiting the program
            print("\n-------Program Exited. Thank You.-------")
            quit()

    def action(self, p):  # to access each function from main page
        if p == 1:
            print("\n\n-------Stock In Product-------\n")
            Id = self.getID()
            desc = self.getDescription(input("Description: "))
            quantity = self.getQuantity()
            price = self.getPrice()
            self.stockIn(Id, [desc, quantity, price])
        elif p == 2:
            print("\n\n-------Stock Out Product-------\n")
            self.stockOut(self.getID())
        elif p == 3:
            print("\n\n-------Remove Product-------\n")
            self.remove(self.getID())
        elif p == 4:
            print("\n\n-------View Inventory report-------\n")
            self.viewInventory()
            self.con()  # asking if users want to continue and proceed to main page
        elif p == 5:
            print("\n\n-------View Latest Transaction Log-------\n")
            self.displayAll()  # method in stack class to print transaction log
            self.con()
        elif p == 6:
            self.reInput()  # re-input data to inventory.txt file before exiting the program
            print("\n-------Program Exited. Thank You.-------")
            exit()
        else:
            ask = int(self.digit(input('Invalid Input. Please Re-enter: ')))
            return self.action(ask)

    def string(self, x):  # x = input("Please Enter 'Yes' or 'No': ") - to validate yes no input
        answer = ['y', 'n', 'yes', 'no']

        if x.strip().lower() in answer:
            return x.lower()
        else:
            ask = input("Invalid input. Please Re-enter 'Yes' or 'No': ")
            return self.string(ask)

    def digit(self, x):  # x = input("Please Enter No.") - to validate digit input
        if x.strip().isdigit() and x != 0:
            return x.strip()
        else:
            ask = input("Invalid input. Please Re-enter: ")
            return self.digit(ask)

    def getTime(self):  # to get current date and time
        today = datetime.now()
        return today.strftime("%d-%B-%Y,%I:%M:%S %p")

    def getID(self):  # validating ID input
        while True:
            try:
                i = input("Product ID: ").upper()
            except (TypeError, SyntaxError):
                print("Invalid Input. Please enter 3-15 characters within: 'A-Z', '/', '-', '_' only.")
            else:
                if re.match("[a-zA-Z0-9_/.]", i) and 3 <= len(i) <= 15:
                    return i.strip()
                else:
                    print("Invalid Input. Please enter 3-15 characters within: 'A-Z', '/', '-', '_' only.")
                    continue

    def getDescription(self, d):  # d = input("Description: ") - to validate description input
        while len(d) > 20:
            d = input("Invalid input. Please enter shorter description: ")
        return d

    def getQuantity(self):  # validating quantity input
        while True:
            try:
                q = int(input("Quantity: "))
            except (TypeError, ValueError, SyntaxError, AttributeError):
                print("Invalid Input. Please Re-enter.")
            else:
                if type(q) is int and q >= 0:
                    return q
                else:
                    print("Invalid Input. Please Re-enter.")
                    continue

    def getPrice(self):  # validating price input
        while True:
            try:
                p = float(input("Average Unit Price: "))
            except (TypeError, ValueError, SyntaxError, AttributeError):
                print("Invalid Input. Please Re-enter.")
            else:
                if type(p) is float and p > 0:
                    return p
                else:
                    print("Invalid Input. Please Re-enter.")
                    continue
