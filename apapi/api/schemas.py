"""
api/schemas.py

Modelos de dados (DTOs - Data Transfer Objects) usados pela API.

Por que este arquivo existe:
    Em Clean Architecture, a camada HTTP nunca deve expor diretamente
    as classes do domínio (ex: core.brain.Brain ou core.memory.MemoryEntry)
    para o mundo externo. Em vez disso, usamos schemas próprios (aqui,
    com Pydantic) que definem exatamente o formato de entrada e saída
    da API - isso isola o núcleo de mudanças no contrato HTTP, e vice-versa.

Escopo desta fase:
    Apenas os schemas necessários para o endpoint mínimo de chat.
    Nada de autenticação, paginação, ou modelos de erro customizados
    ainda - isso será adicionado quando for realmente necessário.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Corpo da requisição enviada pelo cliente para conversar com a G.A.B.Y.

    Attributes:
        message: texto da mensagem do usuário. Não pode ser vazio.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="Mensagem de texto enviada pelo usuário para a G.A.B.Y.",
        examples=["Olá, GABY! Como você está?"],
    )


class ChatResponse(BaseModel):
    """
    Corpo da resposta devolvida ao cliente após o processamento.

    Attributes:
        response: texto de resposta gerado pela G.A.B.Y.
    """

    response: str = Field(
        ...,
        description="Texto de resposta gerado pela G.A.B.Y.",
    )
  
