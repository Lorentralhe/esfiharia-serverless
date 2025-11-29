# Sistema de Pedidos - Esfiharia Serverless

Sistema de pedidos para esfiharia implementado com arquitetura serverless inspirada na AWS, utilizando Flask, TinyDB, e simulação de SQS/SNS.

## 📋 Arquitetura

O sistema segue a arquitetura serverless simplificada:

1. **API Gateway (Flask)** → Recebe requisições HTTP
2. **Lambda: Receber_Pedido** → Processa pedido e publica no SNS
3. **SNS: Eventos_Pedidos** → Distribui eventos para:
   - **SQS: Fila_Pagamentos** → Lambda: Processar_Pagamento
4. **SNS: Pagamento_Concluido** → Atualiza:
   - **DynamoDB: Tabela_Pedidos** (TinyDB) - Atualiza status do pedido

**Nota sobre Gateway_Pagamentos:** No diagrama original, o Gateway_Pagamentos representa um serviço externo de pagamento (como Stripe, PagSeguro, etc.), não um API Gateway da AWS. No nosso sistema, a Lambda Processar_Pagamento chama diretamente a função `simular_gateway_pagamentos()`, que simula essa integração. Em produção, essa função faria uma chamada HTTP real ao gateway de pagamento escolhido.

## 🚀 Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🏃 Executando o Sistema

### 1. Inicie o Worker (processa filas SQS)
Em um terminal, execute:
```bash
python worker.py
```

### 2. Inicie a API Flask
Em outro terminal, execute:
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## 📡 Endpoints da API

### POST /pedidos
Cria um novo pedido.

**Exemplo de requisição:**
```json
{
  "cliente": {
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999"
  },
  "itens": [
    {
      "tipo": "esfiha_carne",
      "quantidade": 2
    },
    {
      "tipo": "esfiha_queijo",
      "quantidade": 3
    }
  ]
}
```

**Resposta:**
```json
{
  "statusCode": 201,
  "body": {
    "mensagem": "Pedido recebido com sucesso",
    "pedido_id": "uuid-do-pedido",
    "status": "recebido"
  }
}
```

### GET /pedidos/<pedido_id>
Consulta um pedido específico.

### GET /estoque
Consulta o estoque de esfihas disponíveis.

### GET /health
Health check da API.

## 🧪 Testando com Postman

### 1. Criar um Pedido
- **Método:** POST
- **URL:** `http://localhost:5000/pedidos`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON) – exemplo simples:**
```json
{
  "cliente": {
    "nome": "Maria Santos",
    "email": "maria@example.com",
    "telefone": "11888888888"
  },
  "itens": [
    {
      "tipo": "esfiha_frango",
      "quantidade": 5
    },
    {
      "tipo": "esfiha_4_queijos",
      "quantidade": 2
    }
  ]
}
```

Se quiser **forçar o resultado do pagamento** (útil para demonstração):

- Atributo opcional: `forcar_status_pagamento`
- Valores aceitos:
  - `"aprovado"` → pagamento sempre aprovado
  - `"recusado"` → pagamento sempre recusado

Exemplo forçando pagamento aprovado:

```json
{
  "cliente": {
    "nome": "Maria Santos",
    "email": "maria@example.com",
    "telefone": "11888888888"
  },
  "itens": [
    {
      "tipo": "esfiha_frango",
      "quantidade": 5
    },
    {
      "tipo": "esfiha_4_queijos",
      "quantidade": 2
    }
  ],
  "forcar_status_pagamento": "aprovado"
}
```

### 2. Consultar Pedido
- **Método:** GET
- **URL:** `http://localhost:5000/pedidos/<pedido_id>`
- Substitua `<pedido_id>` pelo ID retornado na criação do pedido

### 3. Consultar Estoque
- **Método:** GET
- **URL:** `http://localhost:5000/estoque`

## 📦 Tipos de Esfihas Disponíveis

- `esfiha_carne` - R$ 3,50
- `esfiha_frango` - R$ 3,50
- `esfiha_queijo` - R$ 3,00
- `esfiha_espinafre` - R$ 3,00
- `esfiha_pizza` - R$ 3,50
- `esfiha_4_queijos` - R$ 4,00

## 🔄 Fluxo do Sistema

1. **Cliente faz pedido** → API Gateway recebe
2. **Receber_Pedido** → Salva no banco e publica no SNS "Eventos_Pedidos"
3. **Eventos_Pedidos** → Distribui para:
   - **Fila_Pagamentos** → Worker processa → **Processar_Pagamento**
4. **Processar_Pagamento** → Chama gateway de pagamentos (simulado) e publica no SNS "Pagamento_Concluido"
5. **Pagamento_Concluido** → Atualiza status do pedido em **Tabela_Pedidos** (TinyDB)

## 📁 Estrutura do Projeto

```
.
├── app.py                 # API Gateway Flask
├── worker.py              # Worker para processar filas SQS
├── requirements.txt       # Dependências
├── README.md             # Este arquivo
├── lambda_functions/     # Funções Lambda
│   ├── receber_pedido.py
│   └── processar_pagamento.py
├── messaging/            # SQS e SNS
│   ├── sqs.py
│   └── sns.py
├── database/             # TinyDB
│   └── db.py
├── config/               # Configuração
│   └── setup.py
└── data/                 # Dados do TinyDB (criado automaticamente)
    ├── pedidos.json
    ├── estoque.json
    └── reservas.json
```

## 📝 Notas

- O sistema simula uma arquitetura serverless AWS localmente
- O worker processa filas a cada 2 segundos (polling)
- Pagamentos são simulados (95% de aprovação)
- Emails são simulados (logs no console)
- Dados são persistidos em arquivos JSON via TinyDB

## 🐛 Troubleshooting

- Certifique-se de que o worker está rodando antes de fazer pedidos
- Verifique os logs no console para acompanhar o fluxo
- Os dados são salvos em `data/*.json`

