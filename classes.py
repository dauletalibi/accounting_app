from datetime import date
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


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
                 salary: float, position: str):
        super().__init__(l_name, f_name, p_name, birth_date, iin)
        self.id = Employee.employee_count
        self.salary = salary
        self.position = position
        Employee.employee_count += 1

    def __str__(self):
        return super().__str__() + ': ' + self.position

    def __repr__(self):
        return str(self)

    def pension(self):
        if self.salary >= Tax.pension_thresh * Tax.min_sal:
            return Tax.pension_thresh * Tax.min_sal * Tax.income_tax_rate
        else:
            return self.salary * Tax.pension_rate

    def income_tax(self):
        return (self.salary - self.pension()) * Tax.income_tax_rate

    def social_ins(self):
        if self.salary >= Tax.social_ins_thresh * Tax.min_sal:
            return Tax.social_ins_thresh * Tax.min_sal * Tax.social_ins_rate
        else:
            return self.salary * Tax.social_ins_rate

    def med_ins(self):
        if self.salary >= Tax.med_thresh * Tax.min_sal
            return Tax.med_thresh * Tax.min_sal * Tax.med_ins_rate
        else:
            return self.salary * Tax.med_ins_rate

    def social_tax(self):
        return (self.salary - self.pension()) * Tax.social_tax_rate - self.social_ins()

    def med_ded(self):
        if self.salary >= Tax.med_thresh * Tax.min_sal
            return Tax.med_thresh * Tax.min_sal * Tax.med_ded_rate
        else:
            return self.salary * Tax.med_ded_rate

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


if __name__ == '__main__':
    Daulet = Employee('Alibi', 'Daulet', 'Yerzhanuly', date(1991, 2, 23), '910223301734', 13400.0, 'Assistant')
    print(Daulet.pension())
    print(Daulet.income_tax())
