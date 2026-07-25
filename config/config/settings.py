"""
config/settings.py

Configurações centrais da G.A.B.Y.

Por que este arquivo existe:
    Seguindo Clean Architecture, nenhuma configuração "hardcoded"
    deve viver dentro das classes de domínio (core/). Tudo que pode
    mudar entre ambientes (dev, produção, testes) ou ao longo do
    tempo deve estar centralizado aqui.

Como vai crescer:
    Nas próximas fases, este arquivo passará a ler variáveis de
    ambiente (.env) para segredos (tokens do GitHub, chaves de API,
    etc.). Por enquanto, na Fase 1, usamos apenas valores padrão,
    pois ainda não existem integrações externas.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """
    Configurações imutáveis da aplicação.

    Usamos `frozen=True` para garantir que, uma vez carregadas,
    as configurações não sejam alteradas acidentalmente durante
    a execução (evita bugs difíceis de rastrear).
    """

    # Identidade básica da IA
    ai_name: str = "G.A.B.Y."
    ai_full_name: str = "General Artificial Brain for You"
    ai_version: str = "0.1.0"

    # Idioma padrão de resposta
    default_language: str = "pt-BR"

    # Modo de depuração (logs mais verbosos)
    debug: bool = True

    # Limite de histórico mantido em memória de sessão (Fase 1)
    # Isso evita consumo de memória RAM ilimitado antes de existir
    # persistência em banco de dados (que virá na Fase 3).
    max_session_history: int = 500

    # Traços de personalidade padrão, usados por core/personality.py
    default_traits: dict = field(
        default_factory=lambda: {
            "formalidade": 0.4,      # 0 = muito informal, 1 = muito formal
            "humor": 0.5,            # 0 = sério, 1 = bem-humorado
            "proatividade": 0.7,     # 0 = passivo, 1 = sugere ações sozinho
            "empatia": 0.8,          # 0 = frio, 1 = muito empático
        }
    )


# Instância única (singleton simples) usada por todo o projeto.
# Outras camadas devem importar esta instância em vez de criar
# suas próprias configurações, garantindo uma única fonte de verdade.
settings = Settings()
