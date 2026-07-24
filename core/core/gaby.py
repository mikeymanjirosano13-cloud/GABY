"""
core/gaby.py

Ponto central do sistema G.A.B.Y.

Diferença em relação a core/brain.py:
    O Brain (criado na Fase 1) é o orquestrador "completo", incluindo
    estado emocional e status operacional. A classe Gaby, criada aqui,
    é um ponto de entrada mais direto e enxuto, focado apenas no fluxo
    essencial de conversa: personalidade + memória + raciocínio.

    Nenhum arquivo da Fase 1 foi alterado. Este arquivo apenas
    REUTILIZA os módulos já existentes (Personality, SessionMemory,
    ReasoningEngine), respeitando Clean Architecture: cada classe
    continua com sua responsabilidade única, e o Gaby apenas coordena.
"""

from core.personality import Personality
from core.memory import SessionMemory
from core.reasoning import ReasoningEngine, ReasoningResult


class Gaby:
    """
    Classe central da G.A.B.Y.

    Coordena os três módulos essenciais já implementados na Fase 1:
        - Personality: identidade e forma de expressão da IA.
        - SessionMemory: histórico de curto prazo da conversa.
        - ReasoningEngine: geração da resposta em si.
    """

    # Nome padrão usado apenas quando nenhum nome é informado pelo
    # chamador. Existe só como um "último recurso" - o valor real da
    # aplicação deve vir de fora (ex: config/settings.py), mantendo o
    # core desacoplado de config (Clean Architecture: dependências
    # apontam para dentro, não o contrário).
    _DEFAULT_NAME = "G.A.B.Y."

    def __init__(
        self,
        name: str | None = None,
        default_traits: dict[str, float] | None = None,
    ) -> None:
        """
        Inicializa todos os módulos necessários para o funcionamento
        básico da G.A.B.Y.

        Cada módulo é instanciado de forma independente, seguindo o
        princípio de responsabilidade única: o Gaby não sabe COMO
        cada módulo funciona internamente, apenas que eles existem
        e podem ser usados.

        Args:
            name: nome da IA a ser usado pela Personality. Se omitido,
                usa `_DEFAULT_NAME`. Permite que o chamador injete
                `settings.ai_name` sem que este arquivo precise
                importar config/ diretamente.
            default_traits: traços de personalidade iniciais (ex:
                `settings.default_traits`). Se omitido, a Personality
                é criada sem traços pré-definidos, exatamente como
                antes desta revisão (comportamento 100% compatível).
        """
        # Personalidade padrão da IA (nome usado na apresentação).
        self.personality = Personality(
            name=name or self._DEFAULT_NAME,
            traits=dict(default_traits) if default_traits else {},
        )

        # Memória de curto prazo (histórico da sessão atual).
        self.memory = SessionMemory()

        # Motor de raciocínio responsável por gerar as respostas.
        self.reasoning = ReasoningEngine()

    def chat(self, message: str) -> str:
        """
        Fluxo principal de conversa da G.A.B.Y.

        Etapas:
            1. Salva a mensagem do usuário na memória de sessão.
            2. Envia a mensagem para o motor de raciocínio processar.
            3. Salva a resposta gerada pela G.A.B.Y. na memória.
            4. Retorna apenas o texto da resposta ao chamador.

        Args:
            message: mensagem enviada pelo usuário.

        Returns:
            Texto de resposta gerado pela G.A.B.Y.
        """
        # Etapa 1: registra a mensagem do usuário no histórico.
        self.memory.add(role="user", content=message)

        # Etapa 2: envia a mensagem ao motor de raciocínio, que
        # devolve um ReasoningResult (contendo o texto de resposta).
        resultado: ReasoningResult = self.reasoning.process(message)

        # Etapa 3: registra a resposta da G.A.B.Y. no histórico,
        # mantendo a conversa completa e rastreável.
        self.memory.add(role="gaby", content=resultado.response_text)

        # Etapa 4: retorna apenas o texto da resposta, sem expor
        # detalhes internos (como o nível de confiança do raciocínio).
        return resultado.response_text
      
