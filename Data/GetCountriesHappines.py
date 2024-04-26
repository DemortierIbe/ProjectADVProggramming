class GetCountriesHappines:
    def __init__(self, HappinessMin: float, HappinessMax: float) -> None:
        self.HappinessMin = HappinessMin
        self.HappinessMax = HappinessMax
        self.countries = []

    def __str__(self) -> str:
        return "\n".join(self.countries)
