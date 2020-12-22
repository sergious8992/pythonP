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

    def recive_log(self) -> [str]:
        """ 
        if socket.recv-> str \n
        else -> None
        """
        try:
            log = self.sock.recv(1024)
            return log.decode(errors="ignore")
        except:
            return None

    def send_command(self, command):
        self.sock.send(command.encode("utf-8"))
        return True

    def connect(self, ip: str = socket.gethostname()) -> bool:
        """ 
        if connection succed -> True \n
        if connection does not succed -> False
        """
        if ip == "":
            ip = socket.gethostname()
        try:
            print(ip)
            self.sock.connect((ip, 1414))
            return True
        except:
            return False


class Window:

    def __init__(self, cliente: Client):
        self.__root = None
        self.__ip_list = set({})
        self.__cliente = cliente
        try:
            with open("ips.txt", "r+") as ip:
                for line in ip:
                    self.__ip_list.add(line.rstrip("\n"))
        except:
            pass

    def start_gui(self) -> None:
        """ -> None"""
        size = (800, 600)
        self.__root = tk.Tk()
        self.__root.geometry("800x600")
        self.__root.maxsize(size[0], size[1])
        self.__root.minsize(size[0], size[1])

        self.__build_minecraft_frame()
        self.__build_python_frame()
        self.__build_server_frame()
        reciving = threading.Thread(target=self.__recive_sminecraft_output,
                                    args=[self.__cliente])
        reciving.start()
        self.__root.mainloop()

    def __build_python_frame(self) -> None:
        """ -> None"""
        self.__python_frame = tk.Frame(self.__root, bg='grey', width=350, height=300)
        self.__python_frame.pack_propagate(False)
        self.__python_frame.place(x=10, y=5)

        self.__clear_minecraft_text_button = tk.Button(master=self.__python_frame,
                                                       text="Clear",
                                                       command=self.__clear_minecraft_console, )

        self.__clear_minecraft_text_button.place(x=0, y=1)

        self.__connect_button = tk.Button(master=self.__python_frame,
                                          text="Conenct",
                                          command=lambda: self.__cliente.connect(ip=self.__ip_choose.get()))
        self.__connect_button.place(x=0, y=40)

        self.__ip_status_label = tk.Label(self.__python_frame, text="....", bg="#a881cc")
        self.__ip_status_label.place(x=260, y=1)

        self.__ip_add = tk.Button(self.__python_frame,
                                  text="ADD IP",
                                  command=self.__save_ip)
        self.__ip_add.place(x=80, y=1)

        self.__ip_entry = tk.Entry(self.__python_frame)
        self.__ip_entry.place(x=130, y=1)

        self.__ip_entry.bind('<Return>', self.__save_ip)

        self.__remove_ip = ttk.Combobox(self.__python_frame, values=list(self.__ip_list))
        self.__remove_ip.place(x=65, y=80)

        self.__remove_ip_button = tk.Button(self.__python_frame,
                                            text="Remove",
                                            command=self.__delete_ip)
        self.__remove_ip_button.place(x=1, y=79)

    def __build_server_frame(self) -> None:
        """ -> None"""
        self.__server_frame = tk.Frame(self.__root, bg="#c881cc", width=300, height=300)
        self.__server_frame.place(x=490, y=5)

        self.__ip_label = tk.Label(self.__server_frame,
                                   text="IP ADRESS: ",
                                   bg="#c881cc")
        self.__ip_label.place(x=10, y=10)

        self.__ip_choose = ttk.Combobox(self.__server_frame,
                                        state="readonly", )
        print(self.__ip_list)
        self.__ip_choose["values"] = list(self.__ip_list)
        self.__ip_choose.place(x=80, y=10)

    def __build_minecraft_frame(self) -> None:
        """ -> None"""
        self.__minecraft_frame = tk.Frame(self.__root, bg='green', width=780, height=280)
        self.__minecraft_frame.pack_propagate(False)
        self.__minecraft_frame.place(x=10, y=310)

        self.__minecraft_text = tk.Text(self.__minecraft_frame,
                                        height=15,
                                        width=90,
                                        state=tk.DISABLED)  # caracter height size = 16.2
        self.__minecraft_scroll = tk.Scrollbar(self.__minecraft_frame, command=self.__minecraft_text.yview)
        self.__minecraft_text.configure(yscrollcommand=self.__minecraft_scroll.set)
        self.__minecraft_text.place(x=10, y=10)
        self.__minecraft_scroll.place(x=755, y=10, height=243, width=20)

        self.__minecraft_text.configure(state='disable')

        self.__minecraft_entry = tk.Entry(self.__minecraft_frame, textvariable="Minecraft Command")
        self.__minecraft_entry.place(x=10, y=257, height=20, width=725)

        self.__minecraft_entry.bind('<Return>', self.__send_minecraft_command)

    def __send_minecraft_command(self, _: str) -> None:
        """ -> None"""
        self.__minecraft_text.configure(state='normal')
        self.__minecraft_text.insert(tk.INSERT, ">>" + self.__minecraft_entry.get() + "\n")
        try:
            self.__cliente.send_command(self.__minecraft_entry.get()+"\n")
        except:
            pass
        self.__minecraft_entry.delete(0, tk.END)
        self.__minecraft_text.configure(state='disable')

    def __save_ip(self, _: str = None) -> bool:
        self.__ip_status_label.config(text="Saving...", fg="black")
        self.__server_frame.update()
        if not os.path.isfile("ips.txt"):
            with open("ips.txt", "w+") as ip:
                ip.close()
        with open("ips.txt", "r+") as ip:
            for line in ip:
                if line.rstrip("\n") == self.__ip_entry.get():
                    self.__ip_status_label.after(200, self.__ip_status_label.config(text="Saved!", fg="green"))
                    return False
            ip.write(self.__ip_entry.get() + "\n")
            self.__ip_list.add(str(self.__ip_entry.get()).strip())
            self.__combobox_updater()
            self.__ip_status_label.after(200, self.__ip_status_label.config(text="Saved!", fg="green"))
            return True

    def __delete_ip(self, ) -> None:
        with open("ips.txt", "r") as ip:
            lines = ip.readlines()
        with open("ips.txt", "w") as ip:
            for line in lines:
                if line.strip("\n") != self.__remove_ip.get():
                    ip.write(line)
        try:
            self.__ip_list.remove(self.__remove_ip.get())
            self.__combobox_updater()
        except:
            pass

    def __combobox_updater(self) -> None:
        self.__ip_choose["values"] = list(self.__ip_list)
        self.__remove_ip["values"] = list(self.__ip_list)
        self.__ip_choose.update()
        self.__remove_ip.update()
        return None

    def __clear_minecraft_console(self) -> None:
        """ -> None"""
        self.__minecraft_text.configure(state='normal')
        self.__minecraft_text.delete(1.0, tk.END)
        self.__minecraft_text.configure(state='disable')

    def __recive_sminecraft_output(self, client: Client) -> None:
        """ -> None"""
        while True:
            if (log := client.recive_log()) is not None and (log != ""):
                self.__minecraft_text.configure(state='normal')
                self.__minecraft_text.insert(tk.INSERT, ">>" + log)
                self.__minecraft_text.see('end')
                self.__minecraft_text.configure(state='disable')
            else:
                pass


if __name__ == "__main__":
    port: int
    server: str

    cliente = Client()
    client_gui = Window(cliente=cliente)
    client_gui.start_gui()
