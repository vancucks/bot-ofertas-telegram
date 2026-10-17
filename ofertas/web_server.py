import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Lê a porta que o Render atribui dinamicamente (padrão 10000)
PORT = int(os.environ.get("PORT", 10000))

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Responde HTTP 200 OK para o Render saber que o serviço está vivo
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Bot de Ofertas rodando 24/7!")

    def log_message(self, format, *args):
        pass  # Silencia os logs do servidor HTTP

def iniciar_bot():
    """Inicia o loop principal do bot de ofertas em segundo plano."""
    print("🚀 Iniciando o bot de ofertas em segundo plano...")
    # Aponta diretamente para o main.py dentro da pasta ofertas
    subprocess.run([sys.executable, "-m", "ofertas.main"])

if __name__ == "__main__":
    # 1. Inicia o bot numa thread separada
    thread_bot = threading.Thread(target=iniciar_bot, daemon=True)
    thread_bot.start()

    # 2. Inicia o servidor HTTP em 0.0.0.0 para atender o Render
    print(f"🌐 Servidor Web ativo na porta {PORT}")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
    server.serve_forever()
