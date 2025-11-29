"""
Worker para processar filas SQS periodicamente
Simula o comportamento de Lambda triggers em SQS
"""
import time
import logging
from config.setup import processar_filas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_worker():
    """Executa worker que processa filas continuamente"""
    logger.info("Worker iniciado. Processando filas SQS...")
    
    while True:
        try:
            processar_filas()
            time.sleep(2)  # Polling a cada 2 segundos
        except KeyboardInterrupt:
            logger.info("Worker interrompido pelo usuário")
            break
        except Exception as e:
            logger.error(f"Erro no worker: {str(e)}")
            time.sleep(5)


if __name__ == '__main__':
    run_worker()

