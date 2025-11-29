"""
Simulação de Amazon SNS (Simple Notification Service)
Implementa tópicos para publicação/assinatura de eventos
"""
from typing import Dict, List, Callable, Any
from threading import Lock
import json
import logging

logger = logging.getLogger(__name__)


class SNSTopic:
    """Simula um tópico SNS"""
    
    def __init__(self, topic_name: str):
        self.topic_name = topic_name
        self.subscribers: List[Dict[str, Any]] = []  # Lista de assinantes (filas SQS ou funções)
        self.lock = Lock()
        logger.info(f"Tópico SNS criado: {topic_name}")
    
    def publish(self, message: Dict[Any, Any]) -> Dict[str, str]:
        """
        Publica mensagem no tópico
        Envia para todos os assinantes (fan-out)
        """
        with self.lock:
            message_id = f"{self.topic_name}-{id(message)}"
            message_body = {
                'Message': json.dumps(message),
                'MessageId': message_id,
                'TopicArn': f"arn:aws:sns:us-east-1:123456789012:{self.topic_name}"
            }
            
            logger.info(f"Mensagem publicada no tópico {self.topic_name}: {message_id}")
            
            # Fan-out: envia para todos os assinantes
            for subscriber in self.subscribers:
                try:
                    if subscriber['type'] == 'sqs':
                        # Envia para fila SQS
                        # SNS envia mensagens para SQS no formato: {"Message": "...", "MessageId": "...", ...}
                        from messaging.sqs import get_queue
                        queue = get_queue(subscriber['target'])
                        # Envia o envelope SNS completo (como AWS faz)
                        queue.send_message(message_body)
                        logger.info(f"Mensagem enviada para fila SQS: {subscriber['target']}")
                    
                    elif subscriber['type'] == 'lambda':
                        # Invoca função Lambda diretamente
                        handler = subscriber['handler']
                        # Passa o conteúdo da mensagem, não o envelope SNS
                        handler(message, {})
                        logger.info(f"Função Lambda invocada: {subscriber['target']}")
                    
                except Exception as e:
                    logger.error(f"Erro ao enviar mensagem para {subscriber['target']}: {str(e)}")
            
            return {
                'MessageId': message_id
            }
    
    def subscribe(self, subscriber_type: str, target: str, handler: Callable = None):
        """
        Adiciona um assinante ao tópico
        subscriber_type: 'sqs' ou 'lambda'
        target: nome da fila ou função
        handler: função Lambda (se tipo for 'lambda')
        """
        with self.lock:
            subscriber = {
                'type': subscriber_type,
                'target': target,
                'handler': handler
            }
            self.subscribers.append(subscriber)
            logger.info(f"Assinante adicionado ao tópico {self.topic_name}: {target} ({subscriber_type})")


# Instâncias globais dos tópicos
_topicos = {}
_lock = Lock()


def get_topic(topic_name: str) -> SNSTopic:
    """Obtém ou cria um tópico SNS"""
    with _lock:
        if topic_name not in _topicos:
            _topicos[topic_name] = SNSTopic(topic_name)
        return _topicos[topic_name]


def get_all_topics() -> Dict[str, SNSTopic]:
    """Retorna todos os tópicos criados"""
    return _topicos

