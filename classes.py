from datetime import date
from abc import ABC, abstractmethod
from math import ceil, floor

USD_TO_TENGE = 377
RMB_TO_USD = 6.9614


class Tax(ABC):
    min_sal = 42500

    pension_rate = 0.1
    pension_thresh = 50

    income_tax_rate = 0.1

    social_ins_rate = 0.035
    social_ins_thresh = 7

    med_ins_rate = 0.01
    med_thresh = 10
    med_ded_rate = 0.02

    social_tax_rate = 0.095

    @abstractmethod
    def __init__(self):
        pass


class Person:

    def __init__(self, l_name: str, f_name: str, p_name: str, birth_date: date, iin: str):
        self.last_name = l_name
        self.first_name = f_name
        self.patronymic = p_name
        self.birth_date = birth_date
        self.iin = iin

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return str(self)


class Employee(Person):
    employee_count = 1

    def __init__(self, l_name: str, f_name: str, p_name: str, birth_date: date, iin: str,
                 pay: float, position: str):
        super().__init__(l_name, f_name, p_name, birth_date, iin)
        self.id = Employee.employee_count
        self.pay = pay
        self.position = position
        Employee.employee_count += 1

    def __str__(self):
        return super().__str__() + ': ' + self.position

    def __repr__(self):
        return str(self)

    def salary(self):
        # soup = BeautifulSoup(requests.get(BOC_URL).text, features='html.parser')
        # rate_table = soup.find('table', attrs={'class':'courses_yur'})
        # exchange_rate = float(rate_table.find('td', text='USD').find_next_sibling('td').text)
        pay_usd = round(self.pay / RMB_TO_USD, 2)
        pay_tenge = floor(pay_usd * USD_TO_TENGE)

        salary = floor((pay_tenge - 0.1905 * Tax.min_sal) / 1.0855)
        a = self.social_tax(salary)
        b = self.social_ins(salary)
        c = self.med_ded(salary)
        if salary + a + b + c == pay_tenge:
            return salary

        salary = floor(pay_tenge/1.10455)
        a = self.social_tax(salary)
        b = self.social_ins(salary)
        c = self.med_ded(salary)
        if salary + a + b + c == pay_tenge:
            return salary

        salary = floor((pay_tenge + 0.2845*Tax.min_sal)/1.095)
        print(salary)
        if salary + self.social_tax(salary) + self.social_ins(salary) + self.med_ded(salary) == pay_tenge:
            return salary

        return 'Error calculating salary'


    def pension(self, salary):
        if salary >= Tax.pension_thresh * Tax.min_sal:
            return ceil(Tax.pension_thresh * Tax.min_sal * Tax.pension_rate)
        else:
            return ceil(salary * Tax.pension_rate)

    def income_tax(self, salary):
        return ceil((salary - self.pension(salary)) * Tax.income_tax_rate)

    def social_ins(self, salary):
        if salary >= Tax.social_ins_thresh * Tax.min_sal:
            return ceil(Tax.social_ins_thresh * Tax.min_sal * Tax.social_ins_rate)
        else:
            return ceil(salary * Tax.social_ins_rate)

    def med_ins(self, salary):
        if salary >= Tax.med_thresh * Tax.min_sal:
            return ceil(Tax.med_thresh * Tax.min_sal * Tax.med_ins_rate)
        else:
            return ceil(salary * Tax.med_ins_rate)

    def med_ded(self, salary):
        if salary >= Tax.med_thresh * Tax.min_sal:
            return ceil(Tax.med_thresh * Tax.min_sal * Tax.med_ded_rate)
        else:
            return ceil(salary * Tax.med_ded_rate)

    def social_tax(self, salary):
        return ceil((salary - self.pension(salary) - self.med_ins(salary)) * Tax.social_tax_rate - self.social_ins(salary))


if __name__ == '__main__':
    Daulet = Employee('Alibi', 'Daulet', 'Yerzhanuly', date(1991, 2, 23), '910223301734', 13470.0, 'Assistant')
    Dulat = Employee('Alibi', 'Daulet', 'Yerzhanuly', date(1991, 2, 23), '910223301734', 8415.0, 'Assistant')
    print(Dulat.salary())
