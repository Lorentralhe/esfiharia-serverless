# 🚀 Guia: Enviar Projeto para GitHub

## Passo a Passo Completo

### 1. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha:
   - **Repository name**: `esfiharia-serverless` (ou outro nome de sua preferência)
   - **Description**: "Sistema de pedidos para esfiharia com arquitetura serverless"
   - **Visibility**: Escolha Public ou Private
   - **NÃO marque** "Initialize this repository with a README"
5. Clique em **"Create repository"**

### 2. Inicializar Git no Projeto Local

Abra o terminal na pasta do projeto e execute:

```bash
# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Initial commit: Sistema de pedidos esfiharia serverless"
```

### 3. Conectar ao Repositório Remoto

No GitHub, após criar o repositório, você verá uma página com instruções. Use o comando:

```bash
# Adicionar repositório remoto (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/esfiharia-serverless.git

# Ou se preferir usar SSH:
# git remote add origin git@github.com:SEU_USUARIO/esfiharia-serverless.git
```

### 4. Enviar para o GitHub

```bash
# Renomear branch principal para 'main' (se necessário)
git branch -M main

# Enviar código para o GitHub
git push -u origin main
```

### 5. Verificar no GitHub

Acesse seu repositório no GitHub e verifique se todos os arquivos foram enviados corretamente.

---

## Comandos Rápidos (Copy & Paste)

Se você já tem o repositório criado no GitHub, execute estes comandos em sequência:

```bash
git init
git add .
git commit -m "Initial commit: Sistema de pedidos esfiharia serverless"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/esfiharia-serverless.git
git push -u origin main
```

**⚠️ Lembre-se de substituir `SEU_USUARIO` pelo seu username do GitHub!**

---

## Próximos Passos (Atualizações Futuras)

Quando fizer alterações no código, use:

```bash
# Ver o que mudou
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push
```

---

## Arquivos que NÃO serão enviados

Graças ao `.gitignore`, estes arquivos **NÃO** serão enviados:
- Arquivos Python compilados (`__pycache__/`)
- Ambientes virtuais (`venv/`, `env/`)
- Dados do TinyDB (`data/*.json`)
- Configurações de IDE (`.vscode/`, `.idea/`)

Isso mantém o repositório limpo e seguro! 🎉

