"""
Configuração inicial do sistema
Conecta SNS topics com SQS queues e Lambda functions
"""
import logging
from messaging.sns import get_topic
from messaging.sqs import get_queue
from lambda_functions.processar_pagamento import processar_pagamento_handler

logger = logging.getLogger(__name__)


def configurar_arquitetura():
    """
    Configura a arquitetura serverless:
    - SNS Topics com assinantes SQS
    - SQS Queues com handlers Lambda
    """
    logger.info("Configurando arquitetura serverless...")
    
    # 1. Tópico "Eventos_Pedidos" -> Fila_Pagamentos
    topic_eventos_pedidos = get_topic('Eventos_Pedidos')
    
    # Assina fila de pagamentos
    topic_eventos_pedidos.subscribe('sqs', 'Fila_Pagamentos')
    
    # 2. Tópico "Pagamento_Concluido" -> atualiza Tabela_Pedidos
    topic_pagamento_concluido = get_topic('Pagamento_Concluido')
    
    # Assina atualização de pedidos (via Lambda direto)
    def atualizar_pedido_handler(event, ctx):
        """Atualiza pedido quando pagamento é concluído"""
        from database.db import atualizar_pedido
        from datetime import datetime
        pedido_id = event.get('pedido_id')
        if pedido_id:
            atualizar_pedido(pedido_id, {
                'status': 'pago',
                'data_pagamento': datetime.now().isoformat()
            })
    
    topic_pagamento_concluido.subscribe('lambda', 'Atualizar_Pedido', atualizar_pedido_handler)
    
    logger.info("Arquitetura configurada com sucesso!")


def processar_filas():
    """
    Processa mensagens das filas SQS e invoca Lambda functions
    Deve ser chamado periodicamente (polling)
    """
    from messaging.sqs import get_queue
    
    # Processa Fila_Pagamentos
    fila_pagamentos = get_queue('Fila_Pagamentos')
    mensagens = fila_pagamentos.receive_message(max_number_of_messages=10)
    
    for msg in mensagens:
        import json
        body_data = json.loads(msg['Body'])
        if isinstance(body_data, dict) and 'Message' in body_data:
            event = json.loads(body_data['Message'])
        else:
            event = body_data
        processar_pagamento_handler(event, {})
        fila_pagamentos.delete_message(msg['MessageId'])


# Configura arquitetura ao importar
configurar_arquitetura()
