import socket
import threading

class ClienteServidor:
    def __init__(self, host='localhost', server_port=12345):
        self.endereco_servidor = (host, server_port)
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect(self.endereco_servidor)

        self.nome_cliente = input("Digite seu nome: ")
        self.socket_cliente.sendall(self.nome_cliente.encode('utf-8'))

        # Solicita a porta ao usuário para evitar conflitos
        porta_cliente = int(input("Digite a porta para o seu cliente: "))
        self.socket_cliente.sendall(str(porta_cliente).encode('utf-8'))  # Envia a porta para o servidor

        self.mensagens = []
        self.chat_all = []

        # Cliente servidor para receber mensagens
        self.socket_ouvir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_ouvir.bind(('localhost', porta_cliente))
        self.socket_ouvir.listen()

        threading.Thread(target=self.ouvir_mensagens).start()

    def ouvir_mensagens(self):
        while True:
            conn, _ = self.socket_ouvir.accept()
            mensagem = conn.recv(1024).decode('utf-8')
            if mensagem.startswith("CONFIRM:"):
                # Mensagem de confirmação recebida
                nome_remetente = mensagem[9:]
                print(f"Mensagem recebida com sucesso por {nome_remetente}")
            else:
                self.mensagens.append(mensagem)
                self.chat_all.append(mensagem)
                conn.sendall(f"CONFIRM:{self.nome_cliente}".encode('utf-8'))  # Envia confirmação de recebimento
            conn.close()

    def enviar_mensagem(self, ip_destinatario, porta_destinatario, mensagem):
        socket_destinatario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_destinatario.connect((ip_destinatario, porta_destinatario))
        socket_destinatario.sendall(f"{self.nome_cliente}: {mensagem}".encode('utf-8'))

        # Espera por uma confirmação
        socket_destinatario.settimeout(5.0)  # Define um tempo limite para receber a confirmação
        try:
            confirmacao = socket_destinatario.recv(1024).decode('utf-8')
            if confirmacao.startswith("CONFIRM:"):
                nome_remetente = confirmacao[9:]
                print(f"Mensagem enviada com sucesso para destinatário")
            else:
                print("Não recebeu confirmação do destinatário.")
        except socket.timeout:
            print("Tempo de espera pela confirmação expirou.")

        socket_destinatario.close()

    def enviar_mensagem_para_todos(self, mensagem):
        # Adiciona a mensagem à lista local para que o próprio cliente veja a mensagem
        mensagem_enviada = f"{self.nome_cliente}: {mensagem}"
        self.mensagens.append(mensagem_enviada)
        self.chat_all.append(mensagem_enviada)

        # Envia a mensagem para todos os clientes conectados
        clientes = self.listar_clientes_conectados()
        for cliente in clientes:
            ip_porta_destinatario = cliente.split(": ")[1]  # Formato é "nome: IP:PORTA"
            ip_destinatario, porta_destinatario = ip_porta_destinatario.split(":")
            self.enviar_mensagem(ip_destinatario, int(porta_destinatario), mensagem_enviada)

    def listar_mensagens(self):
        if self.mensagens:
            print("Mensagens recebidas:")
            for msg in self.mensagens:
                print(msg)
        else:
            print("Nenhuma mensagem recebida.")

    def listar_chat_all(self):
        if self.chat_all:
            print("Chat All:")
            for msg in self.chat_all:
                # Filtra mensagens para todos (sem destinatário específico)
                if "Para todos:" in msg:
                    print(msg)
        else:
            print("Nenhuma mensagem no chat all.")

    def listar_clientes_conectados(self):
        self.socket_cliente.sendall("LIST".encode('utf-8'))
        lista_clientes = self.socket_cliente.recv(4096).decode('utf-8')
        clientes = lista_clientes.splitlines()
        clientes = [cliente for cliente in clientes if not cliente.startswith(self.nome_cliente)]
        return clientes

    def selecionar_destinatario(self):
        clientes = self.listar_clientes_conectados()
        if not clientes:
            print("Nenhum cliente conectado.")
            return None, None

        print("Clientes conectados:")
        for i, cliente in enumerate(clientes):
            print(f"{i + 1}. {cliente}")

        try:
            escolha = int(input("Escolha o número do destinatário: ")) - 1
            if 0 <= escolha < len(clientes):
                cliente_selecionado = clientes[escolha]
                ip_porta_destinatario = cliente_selecionado.split(": ")[1]  # Formato é "nome: IP:PORTA"
                ip_destinatario, porta_destinatario = ip_porta_destinatario.split(":")
                return ip_destinatario, int(porta_destinatario)
            else:
                print("Escolha inválida.")
                return None, None
        except (ValueError, IndexError):
            print("Escolha inválida.")
            return None, None

    def iniciar(self):
        while True:
            print("\nMenu:")
            print("1. Enviar mensagem")
            print("2. Listar mensagens recebidas")
            print("3. Listar mensagens do chat all")
            print("4. Listar clientes conectados")
            print("5. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                print("1. Enviar mensagem para um cliente")
                print("2. Enviar mensagem para todos os clientes")
                sub_opcao = input("Escolha uma opção: ")

                if sub_opcao == '1':
                    ip_destinatario, porta_destinatario = self.selecionar_destinatario()
                    if ip_destinatario and porta_destinatario:
                        mensagem = input("Digite a mensagem: ")
                        self.enviar_mensagem(ip_destinatario, porta_destinatario, mensagem)

                elif sub_opcao == '2':
                    mensagem = input("Digite a mensagem para todos: ")
                    self.enviar_mensagem_para_todos(f"Para todos: {mensagem}")

                else:
                    print("Opção inválida.")

            elif opcao == '2':
                self.listar_mensagens()

            elif opcao == '3':
                self.listar_chat_all()

            elif opcao == '4':
                clientes = self.listar_clientes_conectados()
                if clientes:
                    print("Clientes conectados:")
                    for cliente in clientes:
                        print(cliente)
                else:
                    print("Nenhum cliente conectado.")

            elif opcao == '5':
                self.socket_cliente.sendall("DISCONNECT".encode('utf-8'))  # Notifica o servidor da desconexão
                self.socket_cliente.close()
                print("Conexão fechada.")
                break

            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    cliente = ClienteServidor()
    cliente.iniciar()

