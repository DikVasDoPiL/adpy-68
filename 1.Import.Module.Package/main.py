import application.salary as salary
import application.db.people as people
import pandas as pd


if __name__ == '__main__':

    file_ = 'logs.csv'
    print(salary.calculate_salary())
    print(people.get_employees())
    print(pd.read_csv(file_, sep=';'))
