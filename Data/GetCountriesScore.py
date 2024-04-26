class GetCountriesScore:
    def __init__(self, Country) -> None:
        self.Country = Country
        self.Score = []

    def __str__(self) -> str:
        return "\n".join(self.Score)
