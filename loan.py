from math import floor


def calculate_totals(initial_balance, interest, graduation):
    amounts = range(0, int(floor(initial_balance)), int(floor(initial_balance/100)))
    initial_balance_iter = [initial_balance for _ in range(len(amounts))]
    interest_iter = [interest for _ in range(len(amounts))]
    graduation_iter = [graduation for _ in range(len(amounts))]

    # iterable of totals
    totals = map(
        calculate_total,
        initial_balance_iter,
        interest_iter,
        graduation_iter,
        amounts
    )

    # iterable of tuples in the form (amount, total)
    amounts_totals = zip(amounts, totals)

    result = dict(amounts_totals)
    return result


def calculate_total(initial_balance, interest, graduation, payment):
    balance = initial_balance
    total_paid = 0
    year = 1
    while balance > 0:
        if year > 30:
            break
        else:
            # Use interest as a percentage
            balance += balance * interest * 0.01
            if balance > payment:
                balance -= payment
                total_paid += payment
            else:
                total_paid += balance
                balance = 0
        year += 1

    return total_paid


def calculate_loan(initial_balance, interest, graduation):
    minimum_payment = 2500
    balance = initial_balance
    total_paid = 0
    year = 1
    while balance > 0:
        if year > 30:
            break
        else:
            # Use interest as a percentage
            balance += balance * interest * 0.01
            if balance > minimum_payment:
                balance -= minimum_payment
                total_paid += minimum_payment
            else:
                total_paid += balance
                balance = 0
        year += 1

    print(initial_balance)
    return Loan(
        initial_balance,
        interest,
        graduation,
        total_paid,
        year,
        balance
    )

class Loan:
    def __init__(
            self,
            initial_balance,
            interest,
            graduation,
            total_paid,
            years_to_pay_off,
            final_balance
    ):
        self.initial_balance = initial_balance
        self.interest = interest
        self.graduation = graduation
        self.total_paid = total_paid
        self.years_to_pay_off = years_to_pay_off
        self.final_balance = final_balance
