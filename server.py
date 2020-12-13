import socket
import subprocess
import os
import tkinter
import threading
import time

class Server:

    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), 1414))

    def start_listening(self):

        while True:
            clientsocket, address = self.sock.accept()
            print(f'Connection from {address} has been stablished!')

    def send_log(self, clientsocket: socket.socket):
        clientsocket.send(minecraft_server_log)

class Minecraft_Server: 
    ''' Server class, controla el servidor y todas sus funciones '''

    def __init__(self) -> None:
        '''__init__ metodo inicia la clase con dos variables
        "server_start_bat" donde se guarda el nombre del archivo .bat,
        "dir" donde se guarda el directorio actual.'''
        self.server_start_bat = "start.bat" 
        self.dir = os.getcwd()        

    def stop_server(self) -> None:
        '''Para el servidor enviado el comando "stop"
        haciendo uso del metodo .communicate().'''

        self.command('stop\n'.encode('utf-8'))
        self.server.communicate()

    def command(self, comando: bytes ) -> None:
        ''' Mediante subprocess.stdin introduce el comando
            deseado. Despues mediante el metodo .flush libera 
            stdin.'''

        self.server.stdin.write(comando)
        self.server.stdin.flush()
   
    def start_server(self) -> bool: 
        ''' Empieza el servidor devolviendo True.'''
        self.server = subprocess.Popen(self.server_start_bat, 
                                        cwd=self.dir, 
                                        shell=True, 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE,
                                        text=False)
        return True
   
    def output(self) -> bytes:
        '''Devuelve el output de la consola como bytes.'''
        return self.server.stdout

class Window:
    '''TODO'''
    pass

class Log:
    """ """
    def __init__(self) -> None:
        self.__message: str
        self.__data: subprocess.STDOUT

    def __read_data(self, __data) -> None:
        self.__message = __data.readline()
    
    def __process_output(self, server_output: subprocess.STDOUT) -> None:
        wait = threading.Thread(target=time.sleep, args=[0.5])
        output = threading.Thread(target=self.__read_data, args=[server_output])
        wait.start()
        output.start()
        wait.join()   
    def flush(self) -> True:
        self.__message = ""
        return True

    def main(self, minecraft_server: Minecraft_Server) -> bytes:
        """Returns bytes"""
        self.__process_output(minecraft_server.output())
        return self.__message

if __name__ == "__main__":

    minecraft_comands = ('tp', 'gamemode', 'gamerule', 'summon','weahter', 
                        'toggledownfalse', 'locate','tell', 'time', 
                        'ban', 'ban-ip', 'kick','op', 'deop', 'pardon') 
    server = Minecraft_Server()
    Running = server.start_server()
    minecraft_log = Log()

    while Running:
        log = server.output().readline()                
        if type(log) != "_io.BufferedReader":           # _io.BufferedReader -> Todavia no hay ningun output del servidor
            print(log.decode(errors="ignore"), end="")  

        if "Done" in log.decode(errors="ignore"):
            server_is_up = True

            while server_is_up:
                os.system("cls")
                print(f'Servidor abierto correctamente!\nEsperando comandos: ', end="")
                comando = str(input())

                if comando == 'stop':
                    server.stop_server()
                    Running = False
                    server_is_up = False

                elif comando.split(" ")[0] in minecraft_comands:
                    comando = (comando+"\n").encode("utf-8")
                    print(f'{comando}')
                    server.command(comando)
                    message = bytes("", "utf-8")
                    for _ in range(3):
                        if message != (new:=minecraft_log.main(minecraft_server= server)):
                            message = new
                            del(new)
                        else:
                            message = bytes("", "utf-8")
                        print(f'{message.decode(errors="ignore")}', end="")
                    _ = input()
                elif comando == "":
                    _ = input()
                elif comando[0] == '!':
                    print(f'Su comando ha sido: {comando}')
                    _ = input()
                else:
                    print(f'Comando incorrecto, debe empezar por "!"')
                    _ = input()

    print("El servidor se ha cerrado correctamente!", end="")
    _ = input()









