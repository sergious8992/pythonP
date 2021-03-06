import socket
import subprocess
import os
import tkinter
import threading
import time
import select
from subprocess import Popen
from typing import Any, Union


class Server:
    """Server class"""

    def __init__(self, defaulttimeout: float = 0.5) -> None:
        """ -> None """
        socket.setdefaulttimeout(defaulttimeout)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((socket.gethostname(), 1414))
        self.clients: list[socket.socket] = []

    def __start_listening(self) -> None:
        """ -> None"""
        self.sock.listen(3)
        try:
            clientsocket, address = self.sock.accept()
            if clientsocket and (clientsocket not in self.clients):
                print(f'\n\nConnection from {address} has been stablished!\n\n')
                self.clients.append(clientsocket)
            else:
                return None
        except:
            return None

    def send_log(self, minecraft_server_log: bytes = "".encode("utf-8")) -> None:
        """ -> None"""
        for client in self.clients:
            client.send(minecraft_server_log)
        return None

    def recieve_comand(self) -> str:
        while True:
            try:
                for cliente in self.clients:
                    command = cliente.recv(1024).decode("utf-8", errors="ignore")
                return command
            except:
                pass

    def main(self, log: bytes = None) -> None:
        """ -> None"""
        self.__start_listening()
        if log:
            self.send_log(minecraft_server_log=log)
        return None


class Minecraft_Server:
    """ Server class, controla el servidor y todas sus funciones """

    def __init__(self) -> None:
        """__init__ method iniciates the class with two variabless
        "server_start_bat" where it saves the file's name .bat,
        "dir"  it saves to the current working directory."""
        self.mserver: subprocess.Popen
        self.server_start_bat = "start.bat"
        self.dir = os.getcwd()

    def stop_server(self) -> None:
        """Para el servidor enviado el comando "stop"
        haciendo uso del metodo .communicate()."""

        self.command('stop\n'.encode('utf-8'))
        self.mserver.communicate()

    def command(self, comando: bytes) -> None:
        """ Mediante subprocess.stdin introduce el comando
            deseado.
            Despues mediante el metodo .flush libera
            stdin y stdout.
        """

        self.mserver.stdin.write(comando)
        self.mserver.stdin.flush()
        self.mserver.stdout.flush()

    def start_server(self) -> bool:
        """ Empieza el servidor devolviendo True."""
        self.mserver = subprocess.Popen(self.server_start_bat,
                                        cwd=self.dir,
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        text=False)
        return True

    def output(self) -> subprocess.STDOUT:
        """Devuelve el output de la consola como bytes."""
        return self.mserver.stdout


class Window:
    """TODO"""
    pass


class Log:
    """ """

    def __init__(self) -> None:
        """ -> None"""
        self.message: bytes = bytes("", encoding="utf-8")
        self.__data: subprocess.STDOUT
        self.__fifo = []

    def __read_data(self, __data: subprocess.STDOUT) -> None:
        """ -> None"""
        for _ in range(2):                              # SI EL PROGRAMA NO FUNCIONA, ELIMINAR EL FOR           
            self.message = __data.readline()
            self.__fifo.append(self.message)

    def __process_output(self, server_output: subprocess.STDOUT) -> None:
        """ -> None"""
        time_to_wait = 0.2
        wait = threading.Thread(target=time.sleep, args=[time_to_wait])
        output = threading.Thread(target=self.__read_data, args=[server_output])
        wait.start()
        output.start()
        wait.join()

    def flush(self) -> True:
        """ -> bool"""
        self.message = bytes("")
        return True

    def main(self, minecraft_server: Minecraft_Server) -> list[bytes]:
        """Returns bytes"""
        self.__fifo = []
        for _ in range(3):
            self.__process_output(minecraft_server.output())
        return self.__fifo


if __name__ == "__main__":

    defaulttiemout = 0.5
    minecraft_comands = ('tp', 'gamemode', 'gamerule', 'summon', 'weather',
                         'toggledownfalse', 'locate', 'tell', 'time',
                         'ban', 'ban-ip', 'kick', 'op', 'deop', 'pardon')

    options = input("Quiere conocer los parametros (y/N)?")
    if options.lower() == "y":
        print(f'defaulttimeout = {defaulttiemout}\n'
              f'minecraft commands = {minecraft_comands}')

    sserver = Server(defaulttimeout=defaulttiemout,)
    sserver.main()
    mserver = Minecraft_Server()
    Running = mserver.start_server()
    minecraft_log = Log()
    message = bytes("", "utf-8")

    while Running:
        log = mserver.output().readline()
        if type(log) != "_io.BufferedReader":  # _io.BufferedReader -> Todavia no hay ningun output del servidor
            sserver.main(log=log)
            print(log.decode(errors="ignore"), end="")

        if "Done" in log.decode(errors="ignore"):
            server_is_up = True
            print(f'\n\n\nServidor abierto correctamente!\nEsperando comandos: ', end="")
            while server_is_up:
                # comando = str(input())
                comando = sserver.recieve_comand()
                if comando == 'stop\n' or comando == 'stop':
                    mserver.stop_server()
                    Running = False
                    server_is_up = False
                elif comando.split(" ")[0] in minecraft_comands:
                    message = ""
                    comando = comando.encode("utf-8")
                    print(f'{comando}')
                    mserver.command(comando)
                    fifo_log = minecraft_log.main(minecraft_server=mserver)
                    for log in fifo_log:
                        sserver.send_log(minecraft_server_log=log)
                    # _ = input()
                elif comando == "":
                    pass
                    # _ = input()
                elif comando[0] == '!':
                    print(f'Su comando ha sido: {comando}')
                    # _ = input()
                else:
                    print(f'Comando incorrecto, debe empezar por "!"')
                    # _ = input()

    print("El servidor se ha cerrado correctamente!", end="")
    _ = input()
