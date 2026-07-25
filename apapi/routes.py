"""
api/routes.py

Define os endpoints HTTP da G.A.B.Y. e conecta a camada web ao
núcleo (core/), sem que o núcleo precise saber nada sobre HTTP.

Escopo desta fase (Fase 2 - mínima):
    Apenas um endpoint funcional: POST /chat.
    Sem autenticação, sem banco de dados, sem memória persistente,
    sem integrações externas - conforme solicitado.

Como a instância de Brain é gerenciada:
    Usamos uma função `get_brain()` como "provider" (padrão de
    Dependency Injection do FastAPI, via `Depends`). Isso mantém uma
    única instância de Brain viva durante a vida do processo (memória
    de sessão compartilhada entre requisições), e evita que a lógica
    de negócio (Brain) seja instanciada diretamente dentro da rota -
    o que facilitaria trocar essa estratégia no futuro (ex: uma
    instância por usuário autenticado) sem alterar a assinatura da rota.
"""

from fastapi import APIRouter, Depends

from config.settings import settings
from core.brain import Brain
from api.schemas import ChatRequest, ChatResponse

# Router dedicado aos endpoints relacionados à conversa com a G.A.B.Y.
# Futuramente, outros routers (ex: github_router, plugins_router) podem
# ser criados e incluídos separadamente em api/app.py, mantendo cada
# grupo de rotas organizado por responsabilidade.
router = APIRouter()

# Instância única de Brain, compartilhada entre requisições enquanto
# o processo da API estiver de pé. Isso é intencionalmente simples
# nesta fase: não há persistência em disco/banco - se o processo for
# reiniciado, a memória de sessão é perdida (comportamento esperado,
# já que "memória persistente" está fora do escopo desta fase).
_brain_instance: Brain | None = None


def get_brain() -> Brain:
    """
    Provider de dependência do FastAPI: devolve a instância única
    do Brain, criando-a na primeira chamada (lazy initialization).

    Usar `Depends(get_brain)` nas rotas, em vez de importar uma
    instância global diretamente, mantém as rotas testáveis (é
    possível substituir esse provider por um Brain de teste/mock
    usando `app.dependency_overrides` do FastAPI).
    """
    global _brain_instance

    if _brain_instance is None:
        _brain_instance = Brain(
            name=settings.ai_name,
            version=settings.ai_version,
            default_traits=settings.default_traits,
        )

    return _brain_instance


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, brain: Brain = Depends(get_brain)) -> ChatResponse:
    """
    Endpoint principal de conversa com a G.A.B.Y.

    Fluxo:
        1. Recebe a mensagem do usuário (validada pelo schema ChatRequest).
        2. Delega todo o processamento para Brain.think(), que já cuida
           de memória, estado emocional e raciocínio (lógica de negócio
           definida inteiramente em core/, não aqui).
        3. Empacota a resposta no schema ChatResponse e devolve ao cliente.

    Esta rota não contém nenhuma regra de negócio - apenas traduz
    HTTP <-> domínio, respeitando Clean Architecture.
    """
    texto_resposta = brain.think(request.message)
    return ChatResponse(response=texto_resposta)
  
