"""
Lambda Function: Receber_Pedido
Recebe pedidos e publica evento no SNS
"""
import logging
from messaging.sns import get_topic
from database.db import criar_pedido
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


def receber_pedido_handler(event: dict, context: dict) -> dict:
    """
    Handler da função Lambda Receber_Pedido
    Recebe o pedido, salva no banco e publica evento no SNS
    """
    try:
        logger.info(f"Processando pedido recebido: {event}")
        
        # Gera ID único para o pedido
        pedido_id = str(uuid.uuid4())
        
        # Prepara dados do pedido
        pedido_data = {
            'pedido_id': pedido_id,
            'cliente': event.get('cliente'),
            'itens': event.get('itens', []),
            'status': 'recebido',
            'data_criacao': datetime.now().isoformat(),
            'total': calcular_total(event.get('itens', []))
        }
        
        # Salva pedido no banco (status inicial)
        criar_pedido(pedido_data)
        
        # Publica evento no tópico SNS "Eventos_Pedidos"
        topic = get_topic('Eventos_Pedidos')
        evento = {
            'tipo': 'pedido_recebido',
            'pedido_id': pedido_id,
            'cliente': event.get('cliente'),
            'itens': event.get('itens', []),
            'total': pedido_data['total'],
            'timestamp': datetime.now().isoformat()
        }
        
        topic.publish(evento)
        
        logger.info(f"Pedido {pedido_id} processado e evento publicado")
        
        return {
            'statusCode': 201,
            'body': {
                'mensagem': 'Pedido recebido com sucesso',
                'pedido_id': pedido_id,
                'status': 'recebido'
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar pedido: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'erro': f'Erro ao processar pedido: {str(e)}'
            }
        }


def calcular_total(itens: list) -> float:
    """Calcula o total do pedido"""
    total = 0.0
    precos = {
        'esfiha_carne': 3.50,
        'esfiha_frango': 3.50,
        'esfiha_queijo': 3.00,
        'esfiha_espinafre': 3.00,
        'esfiha_pizza': 3.50,
        'esfiha_4_queijos': 4.00
    }
    
    for item in itens:
        tipo = item.get('tipo')
        quantidade = item.get('quantidade', 1)
        preco = precos.get(tipo, 3.00)
        total += preco * quantidade
    
    return round(total, 2)

