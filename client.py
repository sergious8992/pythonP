import socket
import tkinter as tk
import threading
class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def recive_log(self) -> str:
        try:
            log = self.sock.recv(1024)
            return log.decode(errors="ignore")
        except:
            return None

    def connect(self):
        try:
            self.sock.connect((socket.gethostname(), 1414))
            return True
        except:
            return False

class Window:

    def __init__(self):
        self.root = None

    def start_gui(self, cliente) -> None:
        size = (800,600)
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.maxsize(size[0], size[1])
        self.root.minsize(size[0], size[1])
        
        self.__build_minecraft_frame()
        self.__build_python_frame(cliente)

        reciving = threading.Thread(target=self.__recive_sminecraft_output, args=[cliente])
        reciving.start()
        self.root.mainloop()

    def __build_python_frame(self, client) -> None:
        self.python_frame = tk.Frame(self.root, bg='grey', width=350, height=575)
        self.python_frame.pack_propagate(False)
        self.python_frame.pack(side=tk.LEFT)

        self.clear_minecraft_text_button = tk.Button(master=self.python_frame, 
                                                    text="Clear",
                                                    command = self.__clear_minecraft_console,)

        self.clear_minecraft_text_button.place(x = 0, y = 0)

        self.connect_button = tk.Button(master = self.python_frame, 
                                        text="Conenct",
                                        command = cliente.connect,)
        self.connect_button.place(x=0, y=40)

    def __build_minecraft_frame(self) -> None:
        self.minecraft_frame = tk.Frame(self.root, bg='green', width=350, height=575)
        self.minecraft_frame.pack_propagate(False)
        self.minecraft_frame.pack(side='right')


        self.minecraft_text = tk.Text(self.minecraft_frame,height=33, width=38, state=tk.DISABLED) #caracter height size = 16.2
        self.minecraft_scroll = tk.Scrollbar(self.minecraft_frame, command=self.minecraft_text.yview)
        self.minecraft_text.configure(yscrollcommand=self.minecraft_scroll.set)
        self.minecraft_text.place(x=10,y=10)
        self.minecraft_scroll.place(x=330, y=10, height=324, width=20)

        self.minecraft_text.configure(state='normal')
        # self.minecraft_text.insert(tk.INSERT, ">>Hello this is a line\n")
        # self.minecraft_text.insert(tk.INSERT, ">>Hello this is another line\n")
        # self.minecraft_text.insert(tk.INSERT, ">>Hello this is another very very very long line\n")
        self.minecraft_text.configure(state='disable')

        self.minecraft_entry = tk.Entry(self.minecraft_frame, textvariable = "Minecraft Command")
        self.minecraft_entry.place(x = 10, y = 550, height=20, width=308)

        self.minecraft_entry.bind('<Return>', self.__send_minecraft_command)

    def __send_minecraft_command(self, _: str) -> None:
        self.minecraft_text.configure(state='normal')
        self.minecraft_text.insert(tk.INSERT, ">>" + self.minecraft_entry.get() + "\n")
        self.minecraft_entry.delete(0, tk.END)
        self.minecraft_text.configure(state='disable')

    def __clear_minecraft_console(self) -> None:
        self.minecraft_text.configure(state='normal')
        self.minecraft_text.delete(1.0, tk.END)
        self.minecraft_text.configure(state='disable')

    def __recive_sminecraft_output(self, cliente: Client) -> None:
        while True:
            if (log:=cliente.recive_log()) != None and (log!=""):
                self.minecraft_text.configure(state='normal')
                self.minecraft_text.insert(tk.INSERT, ">>" + log + "\n")
                self.minecraft_text.configure(state='disable')
            else:
                pass

        



if __name__ == "__main__":
    
    port: int
    server: str

    cliente = Client()
    client_gui = Window()
    client_gui.start_gui(cliente)

