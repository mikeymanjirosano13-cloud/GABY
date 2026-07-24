"""
core/memory.py

Sistema de memória DE SESSÃO (curto prazo) da G.A.B.Y.

IMPORTANTE - Escopo desta fase:
    Esta é a memória "de trabalho", guardada apenas em RAM, que existe
    durante a execução do programa. Ela é suficiente para a IA lembrar
    o histórico da conversa atual.

    A memória PERSISTENTE (banco de dados, lembranças de longo prazo
    entre sessões diferentes) será construída na FASE 3, em um módulo
    próprio (provavelmente database/ + uma nova camada em core/memory.py
    ou um novo arquivo core/long_term_memory.py). Esta classe atual
    não será apagada - será estendida.
"""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryEntry:
    """
    Representa uma única entrada de memória (uma interação).

    Attributes:
        role: quem "falou" - "user" ou "gaby".
        content: o conteúdo textual da interação.
        timestamp: momento em que a entrada foi registrada.
    """

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Converte a entrada em dicionário (útil para APIs/serialização)."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


class SessionMemory:
    """
    Memória de curto prazo, mantida apenas durante a execução do processo.

    Esta classe é intencionalmente simples e desacoplada: ela não sabe
    nada sobre banco de dados, API ou personalidade. Apenas armazena e
    devolve o histórico de interações.
    """

    def __init__(self, max_entries: int = 500) -> None:
        """
        Args:
            max_entries: número máximo de entradas guardadas.
                Isso evita crescimento infinito de memória RAM.
        """
        self._max_entries = max_entries

        # Usamos deque(maxlen=...) em vez de list: quando o limite é
        # atingido, a entrada mais antiga é descartada automaticamente
        # em tempo O(1). Antes, com list + pop(0), a remoção do
        # primeiro elemento era O(n) a cada nova entrada - o que
        # deixaria de escalar bem se max_entries crescesse muito
        # (ex: quando a memória de longo prazo da Fase 3 reaproveitar
        # este padrão). A API pública (get_history, add, clear, len)
        # permanece idêntica; só a implementação interna melhorou.
        self._history: deque[MemoryEntry] = deque(maxlen=max_entries)

    def add(self, role: str, content: str) -> None:
        """
        Adiciona uma nova entrada ao histórico.

        Graças ao `deque(maxlen=...)`, se o limite máximo for atingido,
        a entrada mais antiga é descartada automaticamente pela própria
        estrutura de dados (comportamento de fila - FIFO), sem custo
        extra de verificação manual de tamanho.
        """
        self._history.append(MemoryEntry(role=role, content=content))

    def get_history(self, last_n: int | None = None) -> list[MemoryEntry]:
        """
        Retorna o histórico de interações.

        Args:
            last_n: se fornecido, retorna apenas as últimas N entradas.
                Se None, retorna o histórico completo.

        Nota de implementação:
            `deque` não suporta slicing (`[-n:]`) diretamente, por isso
            convertemos para lista antes de fatiar. O contrato público
            do método (retorna sempre uma `list[MemoryEntry]`) não muda.
        """
        historico_completo = list(self._history)
        if last_n is None:
            return historico_completo
        return historico_completo[-last_n:]

    def clear(self) -> None:
        """Limpa todo o histórico da sessão atual."""
        self._history.clear()

    def __len__(self) -> int:
        """Permite usar len(memoria) para saber quantas entradas existem."""
        return len(self._history)
      
