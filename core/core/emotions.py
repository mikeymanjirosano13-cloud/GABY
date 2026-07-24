"""
core/emotions.py

Simula um estado emocional simples para a G.A.B.Y.

Por que isso existe:
    Uma IA pessoal inspirada no J.A.R.V.I.S. ganha "personalidade viva"
    quando reage de forma sutilmente diferente dependendo do contexto
    (ex: cansada após muitas interações, mais alerta em emergências).

Importante:
    Isso NÃO é uma simulação de emoções reais/conscientes - é apenas
    uma variável de estado que outras partes do sistema (personality.py,
    reasoning.py) podem consultar para ajustar respostas.
"""

from dataclasses import dataclass
from enum import Enum


class Mood(str, Enum):
    """Estados de humor possíveis da G.A.B.Y."""

    NEUTRO = "neutro"
    ANIMADO = "animado"
    CANSADO = "cansado"
    ALERTA = "alerta"       # usado em situações de urgência/erro
    FOCADO = "focado"


@dataclass
class EmotionState:
    """
    Representa o estado emocional atual da IA.

    Attributes:
        mood: humor atual, um valor do enum Mood.
        energy: energia de 0 a 100 (diminui com uso, pode ser "recarregada").
    """

    mood: Mood = Mood.NEUTRO
    energy: int = 100

    def register_interaction(self) -> None:
        """
        Deve ser chamado a cada interação processada pelo cérebro.
        Reduz levemente a energia, simulando "esforço" da IA.
        Quando a energia cai muito, o humor muda para CANSADO.
        """
        # Reduz energia com limite mínimo de 0 (nunca fica negativa).
        self.energy = max(0, self.energy - 1)

        if self.energy < 20:
            self.mood = Mood.CANSADO
        elif self.mood == Mood.CANSADO:
            # Se a energia se recuperou, volta ao normal.
            self.mood = Mood.NEUTRO

    def register_error(self) -> None:
        """
        Chamado quando algo dá errado (ex: exceção no reasoning.py).
        Coloca a IA em estado de ALERTA, sinalizando que algo precisa
        de atenção do usuário ou de outra parte do sistema.
        """
        self.mood = Mood.ALERTA

    def recharge(self, amount: int = 100) -> None:
        """
        Restaura a energia da IA (ex: chamado ao reiniciar o sistema
        ou em um "ciclo de descanso" programado).
        """
        self.energy = min(100, self.energy + amount)
        if self.mood == Mood.CANSADO:
            self.mood = Mood.NEUTRO

    def describe(self) -> str:
        """Retorna uma descrição textual do estado emocional atual."""
        return f"Humor: {self.mood.value} | Energia: {self.energy}/100"
      
