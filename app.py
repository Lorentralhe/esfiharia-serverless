"""
API Gateway Flask - Sistema de Pedidos Esfiharia
Simula o API Gateway da AWS
"""
from flask import Flask, request, jsonify, render_template
from lambda_functions.receber_pedido import receber_pedido_handler
import logging
import os

# Importa configuração para inicializar arquitetura
import config.setup

app = Flask(__name__, template_folder='templates')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def index():
    """Endpoint raiz - página inicial com menu e instruções"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({"status": "healthy", "service": "API Gateway"}), 200


@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    """
    Endpoint principal para receber pedidos
    Simula: User -> API Gateway -> Lambda (Receber_Pedido)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Dados do pedido não fornecidos"}), 400
        
        # Validação básica
        if 'cliente' not in data or 'itens' not in data:
            return jsonify({
                "erro": "Dados incompletos. Necessário: cliente, itens"
            }), 400
        
        # Invoca a função Lambda Receber_Pedido
        logger.info(f"Recebendo pedido: {data}")
        resultado = receber_pedido_handler(data, {})
        
        return jsonify(resultado), 201
        
    except Exception as e:
        logger.error(f"Erro ao processar pedido: {str(e)}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500


@app.route('/pedidos/<pedido_id>', methods=['GET'])
def consultar_pedido(pedido_id):
    """Consulta status de um pedido"""
    from database.db import get_pedido
    
    try:
        pedido = get_pedido(pedido_id)
        if pedido:
            return jsonify(pedido), 200
        return jsonify({"erro": "Pedido não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao consultar pedido: {str(e)}")
        return jsonify({"erro": str(e)}), 500


@app.route('/estoque', methods=['GET'])
def consultar_estoque():
    """Consulta estoque de esfihas"""
    from database.db import get_estoque
    
    try:
        estoque = get_estoque()
        return jsonify(estoque), 200
    except Exception as e:
        logger.error(f"Erro ao consultar estoque: {str(e)}")
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

