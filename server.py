import socket
import subprocess
import os
import tkinter
import threading
import time

class Server:

    socket.setdefaulttimeout(0.5)

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), 1414))
        print(socket.gethostname())
        self.clients = []

    def __start_listening(self) -> None:
        """ -> None"""
        self.sock.listen(5)
        try:
            clientsocket, address = self.sock.accept()
            if (clientsocket) and (clientsocket not in self.clients):
                print(f'\n\nConnection from {address} has been stablished!\n\n')
                self.clients.append(clientsocket)
            else:
                return None
        except:
            return None

    def __send_log(self, minecraft_server_log: bytes ="".encode("utf-8")) -> None:
        """ -> None"""
        for client in self.clients:
            client.send(minecraft_server_log)
        return None

    def main(self, log: bytes = None) -> None:
        """ -> None"""
        self.__start_listening()
        if log:
            self.__send_log(minecraft_server_log=log)
        return None

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
        self.mserver.communicate()

    def command(self, comando: bytes ) -> None:
        ''' Mediante subprocess.stdin introduce el comando
            deseado. Despues mediante el metodo .flush libera 
            stdin.'''

        self.mserver.stdin.write(comando)
        self.mserver.stdin.flush()
   
    def start_server(self) -> bool: 
        ''' Empieza el servidor devolviendo True.'''
        self.mserver = subprocess.Popen(self.server_start_bat, 
                                        cwd=self.dir, 
                                        shell=True, 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE,
                                        text=False)
        return True
   
    def output(self) -> bytes:
        '''Devuelve el output de la consola como bytes.'''
        return self.mserver.stdout

class Window:
    '''TODO'''
    pass

class Log:
    """ """
    def __init__(self) -> None:
        """ -> None"""
        self.message: str = ""
        self.__data: subprocess.STDOUT

    def __read_data(self, __data) -> None:
        """ -> None"""
        self.message = __data.readline()
    
    def __process_output(self, server_output: subprocess.STDOUT) -> None:
        """ -> None"""
        wait = threading.Thread(target=time.sleep, args=[0.5])
        output = threading.Thread(target=self.__read_data, args=[server_output])
        wait.start()
        output.start()
        wait.join()   

    def flush(self) -> True:
        """ -> bool"""
        self.message = ""
        return True

    def main(self, minecraft_server: Minecraft_Server) -> bytes:
        """Returns bytes"""
        self.__process_output(minecraft_server.output())
        return self.message

if __name__ == "__main__":

    minecraft_comands = ('tp', 'gamemode', 'gamerule', 'summon','weather', 
                        'toggledownfalse', 'locate','tell', 'time', 
                        'ban', 'ban-ip', 'kick','op', 'deop', 'pardon') 
    mserver = Minecraft_Server()
    sserver = Server()
    sserver.main()
    Running = mserver.start_server()
    minecraft_log = Log()
    message = bytes("", "utf-8")

    while Running:
        log = mserver.output().readline()                
        if type(log) != "_io.BufferedReader":           # _io.BufferedReader -> Todavia no hay ningun output del servidor
            sserver.main(log=log)
            print(log.decode(errors="ignore"), end="")  

        if "Done" in log.decode(errors="ignore"):
            sserver.main(log=log)
            server_is_up = True

            while server_is_up:
                os.system("cls")
                print(f'Servidor abierto correctamente!\nEsperando comandos: ', end="")
                comando = str(input())

                if comando == 'stop':
                    mserver.stop_server()
                    Running = False
                    server_is_up = False

                elif comando.split(" ")[0] in minecraft_comands:
                    comando = (comando+"\n").encode("utf-8")
                    print(f'{comando}')
                    mserver.command(comando)
                    for _ in range(3):
                        if message != (new:=minecraft_log.main(minecraft_server= mserver)):
                            message = new
                            del(new)
                            sserver.main(log=message)
                            
                        else:
                            pass
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









