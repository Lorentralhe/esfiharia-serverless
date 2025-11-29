"""
Simulação de Amazon SQS (Simple Queue Service)
Implementa filas de mensagens para processamento assíncrono
"""
from queue import Queue
from threading import Lock
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class SQSQueue:
    """Simula uma fila SQS"""
    
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.queue = Queue()
        self.lock = Lock()
        logger.info(f"Fila SQS criada: {queue_name}")
    
    def send_message(self, message_body: Dict[Any, Any]) -> Dict[str, str]:
        """
        Envia mensagem para a fila
        Retorna um dicionário com MessageId similar ao SQS real
        """
        with self.lock:
            message = {
                'Body': json.dumps(message_body),
                'MessageId': f"{self.queue_name}-{id(message_body)}"
            }
            self.queue.put(message)
            logger.info(f"Mensagem enviada para {self.queue_name}: {message['MessageId']}")
            return {
                'MessageId': message['MessageId'],
                'MD5OfBody': str(hash(json.dumps(message_body)))
            }
    
    def receive_message(self, max_number_of_messages: int = 1) -> list:
        """
        Recebe mensagens da fila
        Retorna lista de mensagens no formato SQS
        """
        messages = []
        with self.lock:
            for _ in range(max_number_of_messages):
                if not self.queue.empty():
                    message = self.queue.get()
                    messages.append(message)
                    logger.info(f"Mensagem recebida de {self.queue_name}: {message['MessageId']}")
        
        return messages
    
    def delete_message(self, receipt_handle: str):
        """Remove mensagem da fila (simulado)"""
        logger.info(f"Mensagem deletada de {self.queue_name}: {receipt_handle}")
        # Em uma implementação real, precisaríamos rastrear receipt_handles
    
    def get_queue_size(self) -> int:
        """Retorna o tamanho atual da fila"""
        return self.queue.qsize()


# Instâncias globais das filas
_filas = {}
_lock = Lock()


def get_queue(queue_name: str) -> SQSQueue:
    """Obtém ou cria uma fila SQS"""
    with _lock:
        if queue_name not in _filas:
            _filas[queue_name] = SQSQueue(queue_name)
        return _filas[queue_name]


def get_all_queues() -> Dict[str, SQSQueue]:
    """Retorna todas as filas criadas"""
    return _filas

