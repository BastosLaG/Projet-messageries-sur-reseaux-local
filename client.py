import socket
import threading
import tkinter as tk
from datetime import datetime

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def send(self, msg):
        self.sock.send(msg.encode("utf-8"))

    def receive(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if msg == "l'utilisateur à quitté la conversation":
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.gui.chat_box.config(state=tk.NORMAL)
                    self.gui.chat_box.insert(tk.END, f"{msg} - {timestamp}\n")
                    self.gui.chat_box.config(state=tk.DISABLED)
                    self.gui.chat_box.yview(tk.END)
                elif (msg == ""):
                    pass
                else:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.gui.chat_box.config(state=tk.NORMAL)
                    self.gui.chat_box.insert(tk.END, f"{msg} - {timestamp}\n")
                    self.gui.chat_box.config(state=tk.DISABLED)
                    self.gui.chat_box.yview(tk.END)
            except socket.error:
                self.sock.close()
                
class GUI:
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
        self.root.title("La messagerie de l'avenir...")

        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        self.chat_box = tk.Text(chat_frame, state=tk.DISABLED)
        self.chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.chat_box.yview)
        self.chat_box.config(yscrollcommand=scrollbar.set)

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.input_box = tk.Entry(input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.send_button = tk.Button(input_frame, text="Envoyer", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        self.quit_button = tk.Button(self.root, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.BOTTOM, pady=5)

        self.root.bind('<Return>', lambda event: self.send_button.invoke())

        self.quit_event = threading.Event()

    def send_message(self):
        msg = self.input_box.get()
        if msg.lower() == "l'utilisateur à quitté la conversation":
            self.quit()
        else:
            self.client.send(msg)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, f"<<<<{msg} - {timestamp}\n")
            self.chat_box.config(state=tk.DISABLED)
            self.chat_box.yview(tk.END)
            self.input_box.delete(0, tk.END)

    def quit(self):
        self.quit_event.set()
        self.client.send("l'utilisateur à quitté la conversation")
        self.input_box.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.DISABLED)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.chat_box.insert(tk.END, f"Vous avez quitté la discussion. - {timestamp}\n")
        self.chat_box.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    HOST = "localhost"
    PORT = 6543
    client = Client(HOST, PORT)
    gui = GUI(client)
    client.gui = gui
    gui.run()
