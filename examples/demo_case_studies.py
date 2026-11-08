from mctev.cases.slavery import evaluate_slavery
from mctev.cases.capital_punishment import evaluate_capital_punishment


def main():
    print(evaluate_slavery().summary())
    print()
    print(evaluate_capital_punishment().summary())


if __name__ == "__main__":
    main()