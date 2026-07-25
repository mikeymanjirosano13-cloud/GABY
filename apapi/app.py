"""
api/app.py

Ponto de entrada da API da G.A.B.Y.: cria e configura a aplicação
FastAPI e registra as rotas disponíveis.

Escopo desta fase (Fase 2 - mínima):
    - Cria a instância do FastAPI.
    - Inclui o router de chat (api/routes.py).
    - Expõe uma rota raiz simples ("/") apenas como verificação de
      que o serviço está no ar (não é um "health check" completo -
      isso pode evoluir futuramente sem quebrar compatibilidade).

    Sem autenticação, sem banco de dados, sem integrações externas -
    conforme solicitado para esta fase.

Como executar (fora do escopo desta tarefa, apenas referência):
    uvicorn api.app:app --reload
"""

from fastapi import FastAPI

from config.settings import settings
from api.routes import router as chat_router

# Instância central da aplicação FastAPI. O nome e a versão exibidos
# na documentação automática (/docs) vêm da mesma fonte de verdade
# usada pelo restante do projeto (config/settings.py), evitando
# duplicar esses valores aqui.
app = FastAPI(
    title=settings.ai_name,
    description=f"API mínima da {settings.ai_full_name}.",
    version=settings.ai_version,
)

# Registra as rotas de chat definidas em api/routes.py.
# Mantemos a inclusão de routers centralizada aqui: quando novos
# grupos de rotas forem criados em fases futuras (ex: github, plugins),
# eles serão incluídos da mesma forma, sem alterar routes.py existente.
app.include_router(chat_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Rota raiz simples, usada apenas para confirmar que a API está
    respondendo. Não substitui um endpoint de status/saúde mais
    completo, que poderá ser adicionado em fases futuras.
    """
    return {"mensagem": f"{settings.ai_name} está online."}

