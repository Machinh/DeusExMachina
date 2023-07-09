import os
import subprocess
import psutil
import tkinter as tk
import webbrowser
from threading import Thread
import time

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server App")
        self.root.geometry("300x300")

        self.status_label = tk.Label(root, text="MachinaServer Inativo", fg="red")
        self.status_label.pack(pady=10)

        start_button = tk.Button(root, text="Iniciar Servidor", command=self.start_server)
        start_button.pack(pady=10)

        stop_button = tk.Button(root, text="Parar Servidor", command=self.stop_server)
        stop_button.pack(pady=10)

        # Get the script's directory path
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load the image from the app's directory
        image_path = os.path.join(script_dir, "404.png")
        self.image = tk.PhotoImage(file=image_path)

        # Create a label to display the image
        self.image_label = tk.Label(root, image=self.image)
        self.image_label.pack(pady=10)

        self.server_process = None
        self.check_server_thread = Thread(target=self.check_server_status)
        self.check_server_thread.start()

    def start_server(self):
        if self.server_process is None or self.server_process.poll() is not None:
            # Get the script's directory path
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Inicia o servidor em um processo separado
            self.server_process = subprocess.Popen(["python", "-m", "http.server", "9999"], cwd=script_dir)
            self.open_browser("http://localhost:9999/index.html")

    def stop_server(self):
        if self.server_process is not None and self.server_process.poll() is None:
            # Encerra o processo do servidor
            self.server_process.terminate()
            self.server_process.wait()

    def check_server_status(self):
        while True:
            # Verifica se o servidor está em execução
            if self.server_process is not None and self.server_process.poll() is None:
                self.update_status_label("MachinaServer Ativo", "green")
            else:
                self.update_status_label("MachinaServer Inativo", "red")

            # Aguarda um segundo antes de verificar novamente
            time.sleep(1)

    def update_status_label(self, text, color):
        self.status_label.config(text=text, fg=color)

    def open_browser(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    # Cria a janela principal do aplicativo
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
