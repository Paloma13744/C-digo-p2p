# Código P2P

**Descrição:📜**

Este projeto é uma implementação de um sistema de comunicação cliente-servidor com um servidor central. A solução é dividida em duas partes principais:

## Cliente-Servidor P2P
Cada cliente funciona como um servidor e um cliente ao mesmo tempo, permitindo a comunicação direta entre pares.
Os clientes podem:
Enviar e receber mensagens.
Armazenar mensagens localmente.
Listar mensagens armazenadas.

**Servidor Central**
O servidor central é responsável apenas por listar os clientes conectados à rede. 
Ele: Não participa diretamente da troca de mensagens entre os clientes.
     Apenas gerencia a listagem de clientes conectados.
     
## Funcionalidades 🚀
**Cliente-Servidor P2P:**
Comunicação direta entre clientes.
Envio e recebimento de mensagens.
Armazenamento local das mensagens enviadas e recebidas.
Listagem de mensagens armazenadas.

**Servidor Central:**
Listagem de clientes conectados.
Não gerencia mensagens ou interações entre clientes.

## Estrutura do Projeto 📁
**Cliente-Servidor P2P:**
cliente_servidor_p2p.py: Código para a implementação do cliente-servidor, incluindo funcionalidades para envio, recebimento e armazenamento de mensagens.

**Servidor Central:**
servidor_central.py: Código para a implementação do servidor central, responsável por listar os clientes conectados.

## Requisitos 🛠️
Para executar este projeto, você precisará ter o Python instalado em seu sistema. Além disso, as seguintes bibliotecas devem ser instaladas:

   ```bash pip install socket```

## Como Executar 🔧
Inicie o Servidor Central:
**python servidor_central.py**

Inicie os Clientes:
Em cada cliente, execute:
**python cliente_servidor_p2p.py**

Os clientes se conectarão ao servidor central para listar outros clientes conectados e poderão se comunicar diretamente entre si.

## Uso 💬
Enviar Mensagem: No menu do cliente, selecione a opção para enviar uma mensagem e insira o destinatário e o texto da mensagem.
Listar Mensagens: No menu do cliente, selecione a opção para listar mensagens recebidas.
Listar Clientes: No menu do cliente, selecione a opção para listar clientes conectados.

