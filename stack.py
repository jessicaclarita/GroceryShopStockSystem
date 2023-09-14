import ast


class Stack:    # last in first out - LIFO
    def __init__(self):
        f = open("transactions.txt", "a+")
        self.list = f.readlines()  # for transaction log

    def push(self, item):   # to append transaction
        f = open("transactions.txt", "a+")
        f.write(str(item) + "\n")
        return True

    def validate(self, x):   # x = input("Please Enter No.") - to validate digit input
        if x.strip().isdigit() and x != 0:
            return x.strip()
        else:
            ask = input("Invalid input. Please Re-enter: ")
            return self.validate(ask)

    def displayAll(self):       # View Latest n transactions
        f = open("transactions.txt", "r+")
        self.list = f.read().split("\n")
        print("Total transactions made in the past:", str(len(self.list) - 1) + str("\n"))
        while True:
            try:
                n = int(self.validate(input("How many latest transactions do you want to view? Please enter number: ")))
            except(TypeError, ValueError, SyntaxError, AttributeError):
                print("Invalid Input. Please Re-enter.")
            else:
                f = open("transactions.txt", "r+")
                self.list = f.readlines()
                c = []
                for items in self.list:
                    item = ast.literal_eval(items)
                    date = item[0]
                    Id = item[1]
                    desc = item[2]
                    quantity = item[3]
                    price = item[4]
                    c.append([date, Id, desc, quantity, price])
                c.reverse()
                if 0 < n <= len(self.list):
                    print("\n", n, "Latest Transaction Log:")
                    print("===================================================================================================================")
                    print("{:<7} {:<35} {:<20} {:<20} {:<10} {:<15}".format('No.', 'Date', 'Product ID', 'Description', 'Quantity', 'Average Unit Price'))
                    for i in range(0, n):
                        d = {i + 1: [c[i][0], c[i][1], c[i][2], c[i][3], c[i][4]]}
                        for key, value in d.items():
                            date, Id, desc, quantity, price = value
                            print("{:<7} {:<35} {:<20} {:<20} {:<10} {:<15}".format(key, date, Id, desc, quantity, price))
                    print("===================================================================================================================")
                else:
                    print("Invalid input, the value you entered exceeds the number of transactions. Please re-enter.")
                    print("\nTotal transactions made in the past:", len(c))
                    continue
                break
