import socket
import threading

class Servidor:
    def __init__(self, host='localhost', port=12345):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((host, port))
        self.socket_servidor.listen()
        self.clientes = {}  # Armazena clientes com nome, IP e porta

    def tratar_cliente(self, socket_cliente, endereco_cliente):
        try:
            # Recebe o nome e a porta do cliente
            nome_cliente = socket_cliente.recv(1024).decode('utf-8')
            porta_cliente = socket_cliente.recv(1024).decode('utf-8')
            self.clientes[nome_cliente] = (endereco_cliente[0], porta_cliente)
            print(f"{nome_cliente} conectado de {endereco_cliente[0]}:{porta_cliente}")

            while True:
                requisicao = socket_cliente.recv(1024).decode('utf-8')
                if requisicao == "LIST":
                    lista_clientes = "\n".join([f"{nome}: {endereco[0]}:{endereco[1]}" for nome, endereco in self.clientes.items()])
                    socket_cliente.sendall(lista_clientes.encode('utf-8'))
                elif requisicao == "DISCONNECT":
                    print(f"{nome_cliente} se desconectou.")
                    del self.clientes[nome_cliente]
                    break
                else:
                    print(f"Comando não reconhecido: {requisicao}")

        except Exception as e:
            print(f"Erro ao conectar {endereco_cliente}: {e}")
        finally:
            socket_cliente.close()

    def iniciar(self):
        print("Servidor central iniciado...")
        while True:
            socket_cliente, endereco_cliente = self.socket_servidor.accept()
            handler_cliente = threading.Thread(target=self.tratar_cliente, args=(socket_cliente, endereco_cliente))
            handler_cliente.start()

if __name__ == "__main__":
    servidor = Servidor()
    servidor.iniciar()

