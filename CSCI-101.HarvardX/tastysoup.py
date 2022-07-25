'''
HarvardX Summer 2022
CSCI-101: Foundations of Data Science and Engineering
PSET #7: Object Oriented Programming
Name: Roger Zeng
'''


class Account():
    def __init__(self, cn, un):
        if len(str(cn)) != 4:
            if not submission:
                print("cust_num NOT valid")
        self.cust_num = cn
        self.u_name = un


class Order(Account):
    def __init__(self, cust_num, u_name, mt, pwd, mc, bal):
        super().__init__(cust_num, u_name)

        # Validate password and midterm score
        if pwd == 0:
            if not submission:
                print("Forgot password!")
            bal = 0  # clear balance
        elif pwd > 9999 or pwd < 1000:
            if not submission:
                print("Bad password!")

        # Validate midterm score
        if mt < 0 or mt > 100:
            if not submission:
                print("Invalid midterm!")

        self.__midterm = mt
        self.__password = pwd
        self.meal_cost = mc
        self.balance = bal


    def UpdateBalance(self):
        # frequent eater points
        points = (self.meal_cost // 15 + 1) * 5

        # application rules
        if self.meal_cost >= 15:
            self.balance += points

            # favors to Harvard & MIT students
            if self.u_name == 'HARVARD':
                self.balance += 5
            elif self.u_name == 'MIT':
                self.balance += 3

        # bonus for A students
        if self.__midterm > 80:
            self.balance += 3

        # bad to forget password
        if self.__password == 0:
            self.balance = 0

    def getBalance(self):
        return self.balance

    def getMidterm(self):
        return self.__midterm

    def getPassword(self):
        return self.__password

    def updateMidterm(self, midterm):
        # Validate midterm, will not update if invalid
        if midterm < 0 or midterm > 100:
            if not submission:
                print("Invalid midterm score!")
        else:
            self.__midterm = midterm


submission = True


def main():
    o = list(range(1000, 1006))
    u = ['HARVARD', 'MIT', 'UOFT', '123', 'Harvard']
    m = [100, 90, 81, 75, 160]
    p = [1234, 3214, 12345, 0, 999]
    mc = [15, 30, 45, 80, 13]
    b = [100, 100, 100, 100, 100]
    ind = list(zip(o, u, m, p, mc, b))

    for i in ind:
        print(f"\nOrder: {i}")
        order = Order(i[0], i[1], i[2], i[3], i[4], i[5])
        order.UpdateBalance()
        order.updateMidterm(i[2])
        print(f"New Balance: {order.getBalance()} \
                New midterm: {order.getMidterm()}")


if __name__ == '__main__':
    main()
