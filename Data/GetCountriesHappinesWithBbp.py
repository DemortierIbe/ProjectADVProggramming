class GetCountriesHappinesWithBbp:

    def __init__(self, BbpMin: float, BbpMax: float) -> None:
        self.BbpMin = BbpMin
        self.BbpMax = BbpMax
        self.countries = []

    def __str__(self) -> str:
        return "\n".join(self.countries)
