class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description
        })

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": -amount,
                "description": description
            })
            return True
        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def __str__(self):
        title = self.name.center(30, "*")
        output = title

        for item in self.ledger:
            description = item["description"][:23]
            amount = f"{item['amount']:.2f}"
            output += "\n" + description.ljust(23) + amount.rjust(7)

        output += f"\nTotal: {self.get_balance():.2f}"

        return output


def create_spend_chart(categories):
    output = "Percentage spent by category\n"

    # Calculate total spending for each category
    spent = []

    for category in categories:
        total = 0

        for item in category.ledger:
            if item["amount"] < 0:
                total += abs(item["amount"])

        spent.append(total)

    # Calculate total spending
    total_spent = sum(spent)

    # Calculate percentages
    percentages = []

    for amount in spent:
        if total_spent == 0:
            percentage = 0
        else:
            percentage = int((amount / total_spent) * 100)

        percentage = (percentage // 10) * 10
        percentages.append(percentage)

    # Create bars from 100 to 0
    for level in range(100, -1, -10):
        output += f"{level:>3}|"

        for percentage in percentages:
            if percentage >= level:
                output += " o "
            else:
                output += "   "

        output += " \n"

    # Horizontal line
    output += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Find longest category name
    max_length = max(len(category.name) for category in categories)

    # Write category names vertically
    for i in range(max_length):
        output += "     "

        for category in categories:
            if i < len(category.name):
                output += category.name[i] + "  "
            else:
                output += "   "

        if i < max_length - 1:
            output += "\n"

    return output