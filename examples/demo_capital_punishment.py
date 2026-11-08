"""Run the capital-punishment case study with (R1)-(R3)."""

from mctev.cases.capital_punishment import evaluate_capital_punishment


def main():
    diag = evaluate_capital_punishment()
    print(diag.summary())


if __name__ == "__main__":
    main()