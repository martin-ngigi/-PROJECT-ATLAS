from  enum import  Enum

class ClimateTypes(Enum):
    TEMPERATURE = ("Temperature", "°C")
    PRECIPITATION= ("Precipitation", "mm")

    @property
    def label(self):
        return self.value[0]

    @property
    def unit(self):
        return self.value[1]

    @classmethod
    def choices(cls):
        return [(member.label, member.unit) for member in cls]
