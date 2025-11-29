"""
Script de exemplo para testar o sistema
Execute após iniciar o worker e a API
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def testar_sistema():
    """Testa o fluxo completo do sistema"""
    
    print("=" * 50)
    print("TESTE DO SISTEMA DE PEDIDOS - ESFIHARIA")
    print("=" * 50)
    
    # 1. Health Check
    print("\n1. Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 2. Consultar Estoque
    print("\n2. Consultando Estoque...")
    response = requests.get(f"{BASE_URL}/estoque")
    print(f"Status: {response.status_code}")
    estoque = response.json()
    print(f"Esfihas disponíveis: {len(estoque)} tipos")
    for item in estoque:
        print(f"  - {item['tipo']}: {item['quantidade']} unidades")
    
    # 3. Criar Pedido
    print("\n3. Criando Pedido...")
    pedido = {
        "cliente": {
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "telefone": "11987654321"
        },
        "itens": [
            {
                "tipo": "esfiha_carne",
                "quantidade": 2
            },
            {
                "tipo": "esfiha_queijo",
                "quantidade": 3
            },
            {
                "tipo": "esfiha_4_queijos",
                "quantidade": 1
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/pedidos",
        json=pedido,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    resultado = response.json()
    print(f"Resposta: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        pedido_id = resultado['body']['pedido_id']
        print(f"\n✅ Pedido criado com ID: {pedido_id}")
        
        # 4. Aguardar processamento
        print("\n4. Aguardando processamento (10 segundos)...")
        print("   (O worker está processando as filas SQS)")
        time.sleep(10)
        
        # 5. Consultar Pedido
        print(f"\n5. Consultando Pedido {pedido_id}...")
        response = requests.get(f"{BASE_URL}/pedidos/{pedido_id}")
        print(f"Status: {response.status_code}")
        pedido_completo = response.json()
        print(f"Pedido completo: {json.dumps(pedido_completo, indent=2, ensure_ascii=False)}")
        
        print("\n" + "=" * 50)
        print("TESTE CONCLUÍDO!")
        print("=" * 50)
        print("\nVerifique os logs do worker e da API para ver o fluxo completo:")
        print("  - Receber_Pedido")
        print("  - Processar_Pagamento")
    else:
        print(f"\n❌ Erro ao criar pedido: {resultado}")


if __name__ == '__main__':
    try:
        testar_sistema()
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar à API.")
        print("   Certifique-se de que a API está rodando em http://localhost:5000")
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")

