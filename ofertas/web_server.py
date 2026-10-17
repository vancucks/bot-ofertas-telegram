import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Força o Python a imprimir os logs imediatamente (sem buffer)
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

PORT = int(os.environ.get("PORT", 10000))

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Bot de Ofertas rodando 24/7!")

    def log_message(self, format, *args):
        pass

def iniciar_bot():
    print("🚀 Iniciando o bot de ofertas em segundo plano...", flush=True)
    # Executa o bot forçando a saída de logs para o terminal (sys.stdout / sys.stderr)
    subprocess.run(
        [sys.executable, "-u", "-m", "ofertas.main"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

if __name__ == "__main__":
    thread_bot = threading.Thread(target=iniciar_bot, daemon=True)
    thread_bot.start()

    print(f"🌐 Servidor Web ativo na porta {PORT}", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
    server.serve_forever()
