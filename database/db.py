"""
Gerenciamento de banco de dados usando TinyDB
Substitui DynamoDB da arquitetura AWS
"""
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import os
from pathlib import Path

# Cria diretório de dados se não existir
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Inicializa TinyDB com cache
db_pedidos = TinyDB('data/pedidos.json', storage=CachingMiddleware(JSONStorage))
db_estoque = TinyDB('data/estoque.json', storage=CachingMiddleware(JSONStorage))

Pedido = Query()
Estoque = Query()
Reserva = Query()


def inicializar_estoque():
    """Inicializa estoque com esfihas disponíveis"""
    if not db_estoque.all():
        esfihas_iniciais = [
            {'tipo': 'esfiha_carne', 'quantidade': 100, 'preco': 3.50},
            {'tipo': 'esfiha_frango', 'quantidade': 100, 'preco': 3.50},
            {'tipo': 'esfiha_queijo', 'quantidade': 100, 'preco': 3.00},
            {'tipo': 'esfiha_espinafre', 'quantidade': 80, 'preco': 3.00},
            {'tipo': 'esfiha_pizza', 'quantidade': 90, 'preco': 3.50},
            {'tipo': 'esfiha_4_queijos', 'quantidade': 70, 'preco': 4.00}
        ]
        
        for esfiha in esfihas_iniciais:
            db_estoque.insert(esfiha)
        
        print("Estoque inicializado com sucesso")


# Operações de Pedidos
def criar_pedido(pedido_data: dict):
    """Cria um novo pedido"""
    return db_pedidos.insert(pedido_data)


def get_pedido(pedido_id: str) -> dict:
    """Busca um pedido por ID"""
    resultado = db_pedidos.search(Pedido.pedido_id == pedido_id)
    return resultado[0] if resultado else None


def atualizar_pedido(pedido_id: str, atualizacoes: dict):
    """Atualiza um pedido"""
    db_pedidos.update(atualizacoes, Pedido.pedido_id == pedido_id)


def listar_pedidos() -> list:
    """Lista todos os pedidos"""
    return db_pedidos.all()


# Operações de Estoque
def get_estoque() -> list:
    """Retorna todo o estoque"""
    return db_estoque.all()


def get_estoque_item(tipo: str) -> dict:
    """Busca um item específico do estoque"""
    resultado = db_estoque.search(Estoque.tipo == tipo)
    return resultado[0] if resultado else None


def reservar_estoque(tipo: str, quantidade: int, pedido_id: str):
    """Reserva esfihas do estoque"""
    item = get_estoque_item(tipo)
    
    if item:
        nova_quantidade = item['quantidade'] - quantidade
        db_estoque.update(
            {'quantidade': nova_quantidade},
            Estoque.tipo == tipo
        )
        
        # Registra a reserva
        db_reservas.insert({
            'pedido_id': pedido_id,
            'tipo': tipo,
            'quantidade': quantidade,
            'data_reserva': item.get('data_reserva', '')
        })


def adicionar_estoque(tipo: str, quantidade: int):
    """Adiciona esfihas ao estoque"""
    item = get_estoque_item(tipo)
    
    if item:
        nova_quantidade = item['quantidade'] + quantidade
        db_estoque.update(
            {'quantidade': nova_quantidade},
            Estoque.tipo == tipo
        )
    else:
        db_estoque.insert({
            'tipo': tipo,
            'quantidade': quantidade,
            'preco': 3.00
        })


# Inicializa estoque ao importar
inicializar_estoque()

