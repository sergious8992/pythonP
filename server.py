import socket
import subprocess
import os
import tkinter

class Server: 
    ''' Server class, controla el servidor y todas sus funciones '''

    def __init__(self) -> None:
        '''__init__ metodo inicia la clase con dos variables
        "server_start_bat" donde se guarda el nombre del archivo .bat
        "dir" donde se guarda el directorio actual'''
        self.server_start_bat = "start.bat" 
        '''Nombre del archivo .bat'''

        self.dir = os.getcwd()
        """Directorio actual """              
        
    def start_server(self) -> bool: 
        ''' Empieza el servidor devolviendo True '''
        self.server = subprocess.Popen(self.server_start_bat, cwd=self.dir, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,text=False)
        return True

    def stop_server(self) -> None:
        '''Para el servidor enviado el comando "stop"
        haciendo uso del metodo .communicate()'''

        self.command('stop\n'.encode('utf-8'))
        self.server.communicate()

    def command(self, comando: bytes ) -> None:
        ''' Mediante subprocess.stdin introduce el comando
            deseado. Despues mediante el metodo .flush libera 
            stdin'''

        self.server.stdin.write(command)
        self.server.stdin.flush()

    def output(self) -> bytes:
        '''Devuelve el output de la consola como
        bytes'''
        return self.server.stdout

class Window:
    '''TODO'''
    pass

if __name__ == "__main__":


    minecraft_comands = ('tp', 'gamemode', 'gamerule', 'summon','weahter', 
                        'toggledownfalse', 'locate','tell', 'time', 
                        'ban', 'ban-ip', 'kick','op', 'deop', 'pardon') 
    server = Server()
    Running = server.start_server()

    while Running:
        log = server.output().readline()                
        if type(log) != "_io.BufferedReader":           # _io.BufferedReader -> Todavia no hay ningun output del servidor
            print(log.decode(errors="ignore"), end="")  

        if "Done" in log.decode(errors="ignore"):
            server_is_up = True
            '''Mientras el servidor este activo esta variable sera True'''

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

                    for _ in range(2):
                        log = server.output().readline()
                        print(f'{log.decode(errors="ignore")}', end="")
                    
                    _ = input()
                elif comando[0] == '!':
                    print(f'Su comando ha sido: {comando}')
                    _ = input()
                else:
                    print(f'Comando incorrecto, debe empezar por "!"')
                    _ = input()

    lista = [1,2,3,4, "hola"]

    print("El servidor se ha cerrado correctamente!", end="")
    _ = input()