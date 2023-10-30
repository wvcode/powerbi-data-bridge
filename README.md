# PowerBI Data Bridge

Uma API para acessar dados armazenados no Supabase no PowerBI.

## Objetivo

Esse código é um exemplo de um servidor web baseado no framework FastAPI que fornece uma API para acessar dados de uma fonte chamada Supabase. Vou explicar as principais partes do código:

## Solução Passo a Passo

1. Importações:

O código começa importando várias bibliotecas e módulos necessários para a execução do servidor: 
  - `os` (para acesso ao sistema operacional), 
  - `uvicorn` (para executar o servidor), 
  - `traceback` (para rastrear exceções), 
  - `math` (para funções matemáticas),
  - `dotenv` (para carregar variáveis do ambiente),
  - `supabase` (para connectar no banco de dados),
  - `fastapi` (para colocar o servidor no ar)


2. Configuração do ambiente:
   - O código carrega variáveis de ambiente usando a biblioteca `dotenv`, que permite configurar variáveis de ambiente a partir de um arquivo `.env`. Isso é útil para armazenar informações sensíveis, como chaves de API e URLs de banco de dados, fora do código fonte.


3. Middleware de CORS e GZip:
   - Além de inicializado o servidor FastAPI, são adicionados dois middlewares ao aplicativo:
     - `CORSMiddleware` é usado para habilitar o Cross-Origin Resource Sharing (CORS), permitindo que o servidor responda a solicitações de diferentes origens (navegadores da web, por exemplo).
     - `GZipMiddleware` é usado para comprimir as respostas do servidor usando o algoritmo GZip, economizando largura de banda e melhorando o desempenho.

4. Carregamento de variáveis de configuração:
   - As variáveis `valid_apikeys` e `keys` são carregadas do ambiente. Elas são interpretadas usando `eval`, o que significa que essas variáveis devem ser representadas em formato de lista ou dicionário válido no arquivo `.env`.

5. Função `stream_data`:
   - Essa função é definida para se conectar ao Supabase (um serviço de banco de dados) usando as informações de URL e chave API fornecidas e recuperar dados de uma tabela especificada. Ela pode recuperar todos os registros da tabela ou registros de uma página específica, dependendo do valor do parâmetro `page`.

6. Rotas da API:
   - O código define três rotas principais para a API:
     - A rota raiz ("/") apenas retorna uma mensagem indicando que a API está funcionando.
     - A rota "/retrieve_page/{tbl_name}" permite que os clientes solicitem dados de uma tabela específica e página. É necessário fornecer uma chave de API (`apikey`) que será verificada na lista de chaves válidas antes de permitir o acesso aos dados.
     - A rota "/retrieve/{tbl_name}" é semelhante à rota anterior, mas sempre retorna a primeira página de dados da tabela especificada.


Resumidamente, esse código cria um servidor web usando o FastAPI que fornece endpoints para acessar dados de uma fonte Supabase, com autenticação baseada em chaves de API e suporte a CORS e compressão GZip para melhor desempenho.
