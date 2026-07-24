"""
core/brain.py

Classe central da G.A.B.Y.: o "cérebro" que orquestra todas as
outras partes do sistema.

Papel na Clean Architecture:
    O Brain é a camada de "casos de uso" do núcleo (core/). Ele NÃO
    implementa a lógica de personalidade, memória, emoção ou raciocínio
    diretamente - ele apenas COORDENA essas classes especializadas.

    Isso significa que, quando a IA ganhar novas capacidades (GitHub,
    internet, voz, visão, plugins), o Brain apenas passará a chamar
    esses novos módulos - sem precisar reescrever sua lógica interna.

Relação com core/gaby.py:
    O Brain é o núcleo COMPLETO da G.A.B.Y., incluindo status
    operacional (BrainStatus) e estado emocional (EmotionState).
    Já a classe Gaby (core/gaby.py) é uma fachada mais enxuta,
    pensada para consumidores que precisam apenas do ciclo básico
    de conversa (personalidade + memória + raciocínio), sem os
    conceitos de status/emoção. As duas coexistem intencionalmente
    e não são redundantes: escolha Brain quando precisar do
    "painel de saúde" completo da IA, e Gaby para integrações
    simples de chat.
"""

from dataclasses import dataclass, field
from enum import Enum

from core.emotions import EmotionState
from core.memory import SessionMemory
from core.personality import Personality
from core.reasoning import ReasoningEngine, ReasoningResult


class BrainStatus(str, Enum):
    """Possíveis estados operacionais da G.A.B.Y."""

    INICIALIZANDO = "inicializando"
    ONLINE = "online"
    OCIOSO = "ocioso"
    ERRO = "erro"
    DESLIGADA = "desligada"


@dataclass
class Brain:
    """
    Núcleo central da G.A.B.Y.

    Attributes:
        name: nome da IA (ex: "G.A.B.Y.").
        version: versão atual do sistema.
        status: estado operacional atual.
        personality: instância de Personality (opcional; criada
            automaticamente em __post_init__ se não for fornecida).
        memory: instância de SessionMemory (opcional; idem acima).
        emotions: instância de EmotionState.
        reasoning: instância de ReasoningEngine.
        default_traits: traços de personalidade a serem aplicados
            automaticamente quando uma Personality é criada
            internamente (isto é, quando `personality` não é
            fornecido pelo chamador). Isso permite que quem
            "monta" a aplicação (ex: config/settings.py, ou o
            futuro main.py da API) injete os traços padrão sem
            que o Brain precise importar config/ diretamente -
            preservando a direção de dependência do Clean
            Architecture (core não depende de config).
    """

    name: str
    version: str
    status: BrainStatus = BrainStatus.INICIALIZANDO
    personality: Personality | None = field(default=None)
    memory: SessionMemory | None = field(default=None)
    emotions: EmotionState = field(default_factory=EmotionState)
    reasoning: ReasoningEngine = field(default_factory=ReasoningEngine)
    default_traits: dict[str, float] | None = field(default=None)

    def __post_init__(self) -> None:
        """
        Inicialização adicional após a criação do dataclass.

        Garante que, se personality/memory não forem fornecidos
        explicitamente, valores padrão sensatos sejam criados -
        evitando que o Brain seja instanciado em estado inconsistente.

        Se `default_traits` for informado pelo chamador e nenhuma
        Personality tiver sido passada explicitamente, os traços são
        aplicados automaticamente à Personality recém-criada.
        """
        if self.personality is None:
            self.personality = Personality(name=self.name)

            # Aplica traços padrão apenas quando a Personality foi
            # criada aqui dentro (não sobrescreve uma Personality
            # customizada fornecida pelo chamador).
            if self.default_traits:
                for traço, valor in self.default_traits.items():
                    self.personality.adjust_trait(traço, valor)

        if self.memory is None:
            self.memory = SessionMemory()

        # Assim que tudo estiver pronto, a IA passa a operar normalmente.
        self.status = BrainStatus.ONLINE

    def think(self, user_input: str) -> str:
        """
        Ciclo principal de pensamento da G.A.B.Y.

        Fluxo:
            1. Registra a entrada do usuário na memória.
            2. Atualiza o estado emocional (custo de energia).
            3. Envia a entrada ao motor de raciocínio.
            4. Registra a resposta da IA na memória.
            5. Retorna o texto de resposta.

        Args:
            user_input: mensagem enviada pelo usuário.

        Returns:
            Texto de resposta gerado pela G.A.B.Y.
        """
        try:
            self.memory.add(role="user", content=user_input)
            self.emotions.register_interaction()

            resultado: ReasoningResult = self.reasoning.process(user_input)

            self.memory.add(role="gaby", content=resultado.response_text)
            return resultado.response_text

        except Exception as erro:
            # Qualquer falha inesperada muda o estado emocional para
            # ALERTA e o status do cérebro para ERRO, permitindo que
            # camadas superiores (API, logs) percebam o problema.
            self.emotions.register_error()
            self.status = BrainStatus.ERRO
            return f"Ocorreu um erro ao processar sua mensagem: {erro}"

    def get_status_report(self) -> dict:
        """
        Retorna um resumo do estado atual da G.A.B.Y.

        Útil para debug agora, e futuramente será exposto por um
        endpoint da API (Fase 2), como um "painel de saúde" da IA.
        """
        return {
            "nome": self.name,
            "versão": self.version,
            "status": self.status.value,
            "personalidade": self.personality.describe(),
            "estado_emocional": self.emotions.describe(),
            "entradas_em_memória": len(self.memory),
        }

    def shutdown(self) -> None:
        """
        Encerra a G.A.B.Y. de forma controlada.

        Por enquanto apenas atualiza o status; futuramente poderá
        salvar a memória de sessão em disco/banco antes de encerrar.
        """
        self.status = BrainStatus.DESLIGADA
  
