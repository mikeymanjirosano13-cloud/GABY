class GabyBrain:
    def __init__(self):
        self.name = "G.A.B.Y."
        self.version = "0.1.0"
        self.status = "Online"

    def speak(self, message):
        return f"{self.name}: {message}"


if __name__ == "__main__":
    gaby = GabyBrain()
    print(gaby.speak("Sistema iniciado com sucesso!"))
