"""
core/reasoning.py

Motor de raciocínio da G.A.B.Y. (versão inicial - Fase 1).

Escopo atual:
    Nesta fase, o motor de raciocínio é um ESQUELETO funcional:
    ele recebe uma entrada de texto e devolve uma resposta básica,
    sem ainda consultar internet, GitHub, plugins, etc.

Como vai evoluir:
    Nas próximas fases, este módulo passará a:
    - Consultar plugins registrados (plugins/)
    - Buscar informações na internet (internet/search.py)
    - Executar automações (automation/tasks.py)
    - Decidir qual "habilidade" da IA deve responder a cada pedido

    A interface pública (o método `process`) foi projetada para
    NÃO mudar de assinatura conforme essas capacidades forem
    adicionadas - apenas sua implementação interna crescerá.
    Isso segue o princípio de Clean Architecture de estabilidade
    de interfaces entre camadas.
"""

from dataclasses import dataclass


@dataclass
class ReasoningResult:
    """
    Resultado de um ciclo de raciocínio.

    Attributes:
        response_text: texto de resposta gerado.
        confidence: confiança estimada da resposta (0.0 a 1.0).
            Usado futuramente para decidir se a IA deve pedir
            mais informações ao usuário em vez de "adivinhar".
    """

    response_text: str
    confidence: float = 1.0


class ReasoningEngine:
    """
    Motor de raciocínio central da G.A.B.Y.

    Por enquanto, implementa apenas lógica de eco/reconhecimento
    simples, servindo como ponto de extensão para as próximas fases.
    """

    def process(self, input_text: str) -> ReasoningResult:
        """
        Processa uma entrada de texto e retorna um resultado de raciocínio.

        Args:
            input_text: texto enviado pelo usuário.

        Returns:
            ReasoningResult contendo a resposta gerada.
        """
        # Validação básica: entrada vazia não gera raciocínio válido.
        if not input_text or not input_text.strip():
            return ReasoningResult(
                response_text="Não recebi nenhuma entrada para processar.",
                confidence=0.0,
            )

        # Fase 1: lógica de resposta ainda é um placeholder.
        # Isso será substituído por um pipeline real de decisão
        # (busca em plugins, internet, memória de longo prazo, etc.)
        resposta = (
            f"Recebi sua mensagem: '{input_text.strip()}'. "
            "Ainda estou aprendendo a raciocinar sobre isso."
        )

        return ReasoningResult(response_text=resposta, confidence=0.5)
      
