class Vergelijk2Landen:
    def __init__(self, Country1, Country2):
        self.Country1 = Country1
        self.Country2 = Country2
        self.Comparison = []

    def __str__(self) -> str:
        return "\n".join(self.Comparison)
