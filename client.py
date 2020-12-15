import socket
import tkinter as tk
import threading
import os
from tkinter import ttk

class Client:

    socket.setdefaulttimeout(0.5)

    def __init__(self):
        """-> None"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def recive_log(self) -> str:
        """ 
        if socket.recv-> str \n
        else -> None
        """
        try:
            log = self.sock.recv(1024)
            return log.decode(errors="ignore")
        except:
            return None

    def connect(self) -> bool:
        """ 
        if connection succed -> True \n
        if connection does not succed -> False
        """
        try:
            self.sock.connect((socket.gethostname(), 1414))
            return True
        except:
            return False

class Window:

    def __init__(self):
        self.root = None
        self.__ip_list = set({})
        try:
            with open("ips.txt", "r+") as ip:
                for line in ip:
                    self.__ip_list.add(line.rstrip("\n"))
        except:
            pass
    def start_gui(self, cliente: Client) -> None:
        """ -> None"""
        size = (800,600)
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.maxsize(size[0], size[1])
        self.root.minsize(size[0], size[1])
        
        self.__build_minecraft_frame()
        self.__build_python_frame(cliente)
        self.__build_server_frame()
        reciving = threading.Thread(target=self.__recive_sminecraft_output, 
                                    args=[cliente])
        reciving.start()
        self.root.mainloop()

    def __build_python_frame(self, client: Client) -> None:
        """ -> None"""
        self.python_frame = tk.Frame(self.root, bg='grey', width=350, height=300)
        self.python_frame.pack_propagate(False)
        self.python_frame.place(x=10, y=5)

        self.clear_minecraft_text_button = tk.Button(master=self.python_frame, 
                                                    text="Clear",
                                                    command = self.__clear_minecraft_console,)

        self.clear_minecraft_text_button.place(x = 0, y = 1)

        self.connect_button = tk.Button(master = self.python_frame, 
                                        text="Conenct",
                                        command = cliente.connect,)
        self.connect_button.place(x=0, y=40)

        self.ip_status_label = tk.Label(self.python_frame, text="....", bg="#a881cc")
        self.ip_status_label.place(x=260, y=1)

        self.ip_add = tk.Label(self.python_frame, 
                                text="ADD IP",
                                bg="grey",)
        self.ip_add.place(x=80, y=1)

        self.ip_entry = tk.Entry(self.python_frame)
        self.ip_entry.place(x=130, y=1)

        self.ip_entry.bind('<Return>', self.__save_ip)

        self.remove_ip = ttk.Combobox(self.python_frame, values=list(self.__ip_list))
        self.remove_ip.place(x=65, y=80)

        self.remove_ip_button = tk.Button(self.python_frame,
                                        text="Remove",
                                        command=self.__delete_ip)  
        self.remove_ip_button.place(x=1,y=79)                                        
 
    def __build_server_frame(self) -> None:
        """ -> None"""
        self.server_frame = tk.Frame(self.root, bg="#c881cc", width = 300, height= 300)
        self.server_frame.place(x=490, y=5)

        self.ip_label = tk.Label(self.server_frame, text="IP ADRESS: ", bg="#c881cc")
        self.ip_label.place(x=10, y=10)
        
        self.ip_choose = ttk.Combobox(self.server_frame,  
                                      state="readonly",)
        print(self.__ip_list)
        self.ip_choose["values"] = list(self.__ip_list)
        self.ip_choose.place(x=80,y=10)

    def __build_minecraft_frame(self) -> None:
        """ -> None"""
        self.minecraft_frame = tk.Frame(self.root, bg='green', width=780, height=280)
        self.minecraft_frame.pack_propagate(False)
        self.minecraft_frame.place(x=10, y=310)

        self.minecraft_text = tk.Text(self.minecraft_frame,height=15, width=90, state=tk.DISABLED) #caracter height size = 16.2
        self.minecraft_scroll = tk.Scrollbar(self.minecraft_frame, command=self.minecraft_text.yview)
        self.minecraft_text.configure(yscrollcommand=self.minecraft_scroll.set)
        self.minecraft_text.place(x=10,y=10)
        self.minecraft_scroll.place(x=755, y=10, height=243, width=20)

        self.minecraft_text.configure(state='disable')

        self.minecraft_entry = tk.Entry(self.minecraft_frame, textvariable = "Minecraft Command")
        self.minecraft_entry.place(x = 10, y = 257, height=20, width=725)

        self.minecraft_entry.bind('<Return>', self.__send_minecraft_command)

    def __send_minecraft_command(self, _: str) -> None:
        """ -> None"""
        self.minecraft_text.configure(state='normal')
        self.minecraft_text.insert(tk.INSERT, ">>" + self.minecraft_entry.get() + "\n")
        self.minecraft_entry.delete(0, tk.END)
        self.minecraft_text.configure(state='disable')

    def __save_ip(self, _: str) -> None:
        self.ip_status_label.config(text="Saving...", fg="black")
        self.server_frame.update()
        if not os.path.isfile("ips.txt"):
            with open("ips.txt", "w+") as ip:
                ip.close()
        with open("ips.txt", "r+") as ip:
            for line in ip:
                if line.rstrip("\n") == self.ip_entry.get():
                    return False
            ip.write(self.ip_entry.get()+"\n")
            self.__ip_list.add(str(self.ip_entry.get()))
            self.__combobox_updater()
            self.ip_status_label.after(200, self.ip_status_label.config(text="Saved!", fg="green"))
            return True

    def __delete_ip(self,) -> None:
        with open("ips.txt", "r") as ip:
            lines = ip.readlines()
        with open("ips.txt", "w") as ip:
            for line in lines:
                if line.strip("\n") != self.remove_ip.get():
                    ip.write(line)
        try:
            self.__ip_list.remove(self.remove_ip.get())
            self.__combobox_updater()
        except:
            pass
    
    def __combobox_updater(self) -> None:
            self.ip_choose["values"] = list(self.__ip_list)
            self.remove_ip["values"] = list(self.__ip_list)
            self.ip_choose.update()
            self.remove_ip.update()
            return None

    def __clear_minecraft_console(self) -> None:
        """ -> None"""
        self.minecraft_text.configure(state='normal')
        self.minecraft_text.delete(1.0, tk.END)
        self.minecraft_text.configure(state='disable')

    def __recive_sminecraft_output(self, cliente: Client) -> None:
        """ -> None"""
        while True:
            if (log:=cliente.recive_log()) != None and (log!=""):
                self.minecraft_text.configure(state='normal')
                self.minecraft_text.insert(tk.INSERT, ">>" + log + "\n")
                self.minecraft_text.see('end')
                self.minecraft_text.configure(state='disable')
            else:
                pass

if __name__ == "__main__":
    
    port: int
    server: str

    cliente = Client()
    client_gui = Window()
    client_gui.start_gui(cliente)

