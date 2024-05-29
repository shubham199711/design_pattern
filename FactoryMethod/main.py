from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    def translate(self, msg: str) -> str:
        pass

class EnglishLocalizer(Translator):
    def translate(self, msg: str) -> str:
        return msg

class FrenchLocalizer(Translator):
   def __init__(self) -> None:
       self.translations = {"car": "voiture", "bike": "bicyclette",
                             "cycle":"cyclette"}

   def translate(self, msg: str) -> str:
       return self.translations.get(msg, msg)


class SpanishLocalizer(Translator):
    def __init__(self) -> None:
        super().__init__()
        self.translations = {"car": "coche", "bike": "bicicleta", "cycle":"ciclo"}
    
    def translate(self, msg: str) -> str:
        return self.translations.get(msg, msg)


def Factory(language = "English"):
    if language == "English":
        return EnglishLocalizer()
    elif language == "French":
        return FrenchLocalizer()
    elif language == "Spanish":
        return SpanishLocalizer()
    else:
        raise ValueError("Language not supported")


if __name__ == "__main__":
    e = Factory("English")
    f = Factory("French")
    s = Factory("Spanish")
    for msg in ["car", "bike", "cycle"]:
        print(f"English translation of '{msg}' is: {e.translate(msg)}")
        print(f"French translation of '{msg}' is: {f.translate(msg)}")
        print(f"Spanish translation of '{msg}' is: {s.translate(msg)}")