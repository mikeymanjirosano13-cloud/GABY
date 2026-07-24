"""
core/personality.py

Define a personalidade da G.A.B.Y.

Responsabilidade única (Clean Architecture):
    Esta classe cuida SOMENTE de "como a IA se comporta e se expressa".
    Ela não sabe nada sobre memória, API, ou raciocínio lógico -
    isso é responsabilidade de outras classes (memory.py, reasoning.py).

Como vai evoluir:
    Futuramente, os traços de personalidade poderão ser ajustados
    dinamicamente pelo usuário (ex: "seja mais formal") e até
    influenciados pelo estado emocional (emotions.py).
"""

from dataclasses import dataclass, field


@dataclass
class Personality:
    """
    Representa a personalidade da G.A.B.Y.

    Attributes:
        name: Nome pelo qual a IA se apresenta.
        traits: Dicionário de traços de 0.0 a 1.0 (ex: humor, empatia).
        catchphrase: Frase de efeito usada em saudações.
    """

    name: str
    traits: dict[str, float] = field(default_factory=dict)
    catchphrase: str = "Estou pronta para ajudar."

    def describe(self) -> str:
        """
        Retorna uma descrição textual legível da personalidade atual.
        Útil para debug e para endpoints da API (Fase 2) que queiram
        expor "quem é a G.A.B.Y." para o usuário.
        """
        if not self.traits:
            return f"{self.name}: personalidade ainda não configurada."

        traços_formatados = ", ".join(
            f"{traço}={valor:.1f}" for traço, valor in self.traits.items()
        )
        return f"{self.name} | Traços: {traços_formatados}"

    def greeting(self) -> str:
        """
        Gera uma saudação simples, ajustada de forma básica pelo
        traço de 'formalidade'. Esta lógica é intencionalmente simples
        na Fase 1 e será refinada quando o motor de raciocínio
        (reasoning.py) estiver mais completo.
        """
        formalidade = self.traits.get("formalidade", 0.5)

        if formalidade >= 0.7:
            return f"Boa noite. Sou {self.name}. {self.catchphrase}"
        elif formalidade <= 0.3:
            return f"E aí! Aqui é a {self.name}. {self.catchphrase}"
        else:
            return f"Olá, sou a {self.name}. {self.catchphrase}"

    def adjust_trait(self, trait_name: str, value: float) -> None:
        """
        Ajusta um traço de personalidade específico.

        Args:
            trait_name: nome do traço (ex: "humor").
            value: novo valor, sempre limitado entre 0.0 e 1.0.
        """
        # Garante que o valor esteja sempre dentro do intervalo válido,
        # evitando estados inconsistentes de personalidade.
        valor_limitado = max(0.0, min(1.0, value))
        self.traits[trait_name] = valor_limitado
      
