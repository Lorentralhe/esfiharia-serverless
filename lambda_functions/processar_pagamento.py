"""
Lambda Function: Processar_Pagamento
Processa pagamentos e publica evento de conclusão
"""
import logging
from messaging.sns import get_topic
from database.db import atualizar_pedido
from datetime import datetime
import random

logger = logging.getLogger(__name__)


def processar_pagamento_handler(event: dict, context: dict) -> dict:
    """
    Handler da função Lambda Processar_Pagamento
    Simula processamento de pagamento e publica evento de conclusão
    """
    try:
        logger.info(f"Processando pagamento: {event}")
        
        pedido_id = event.get('pedido_id')
        total = event.get('total', 0)
        # Campo opcional vindo do pedido original para forçar o resultado
        # Valores esperados: "aprovado" ou "recusado"
        forcar_status = event.get('forcar_status_pagamento')
        
        if not pedido_id:
            raise ValueError("pedido_id não fornecido")
        
        # Simula chamada ao gateway de pagamentos
        # Em produção, aqui seria uma chamada HTTP real
        resultado_pagamento = simular_gateway_pagamentos(total, forcar_status)
        
        if resultado_pagamento['status'] == 'aprovado':
            # Atualiza status do pedido
            atualizar_pedido(pedido_id, {
                'status': 'pago',
                'pagamento_id': resultado_pagamento['transacao_id'],
                'data_pagamento': datetime.now().isoformat()
            })
            
            # Publica evento no tópico "Pagamento_Concluido"
            topic = get_topic('Pagamento_Concluido')
            evento = {
                'tipo': 'pagamento_concluido',
                'pedido_id': pedido_id,
                'transacao_id': resultado_pagamento['transacao_id'],
                'total': total,
                'status': 'aprovado',
                'timestamp': datetime.now().isoformat()
            }
            
            topic.publish(evento)
            
            logger.info(f"Pagamento aprovado para pedido {pedido_id}")
            
            return {
                'statusCode': 200,
                'body': {
                    'mensagem': 'Pagamento processado com sucesso',
                    'pedido_id': pedido_id,
                    'status': 'aprovado',
                    'transacao_id': resultado_pagamento['transacao_id']
                }
            }
        else:
            # Pagamento recusado
            atualizar_pedido(pedido_id, {
                'status': 'pagamento_recusado',
                'data_pagamento': datetime.now().isoformat()
            })
            
            logger.warning(f"Pagamento recusado para pedido {pedido_id}")
            
            return {
                'statusCode': 402,
                'body': {
                    'mensagem': 'Pagamento recusado',
                    'pedido_id': pedido_id,
                    'status': 'recusado'
                }
            }
            
    except Exception as e:
        logger.error(f"Erro ao processar pagamento: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'erro': f'Erro ao processar pagamento: {str(e)}'
            }
        }


def simular_gateway_pagamentos(valor: float, forcar_status: str | None = None) -> dict:
    """
    Simula chamada ao gateway de pagamentos
    Em produção, seria uma chamada HTTP real
    """
    # Se o status foi forçado (para fins de demonstração/teste), respeita-o
    if forcar_status == 'aprovado':
        aprovado = True
    elif forcar_status == 'recusado':
        aprovado = False
    else:
        # Caso não tenha sido forçado, simula 95% de aprovação
        aprovado = random.random() > 0.05
    
    if aprovado:
        return {
            'status': 'aprovado',
            'transacao_id': f"TXN-{random.randint(100000, 999999)}",
            'valor': valor,
            'metodo': 'cartao_credito'
        }
    else:
        return {
            'status': 'recusado',
            'motivo': 'Saldo insuficiente ou cartão inválido'
        }

