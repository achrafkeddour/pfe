import subprocess
from flask import Flask, Response
import threading

app = Flask(__name__)

log_buffer = []       # <-- stocke tout l’historique des logs
listeners = []        # <-- connexions actives SSE

def stream_process():
    """Lance Odoo et capture les logs en continu"""
    process = subprocess.Popen(
        [
            "./odoo/odoo-bin",
            "-u", "my_hostel",
            "-d", "odoo_test"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd="/home/erp/odoo-dev"
    )

    for line in process.stdout:
        clean = line.rstrip()

        # Ajouter dans le buffer
        log_buffer.append(clean)

        # Envoyer à tous les clients connectés
        for queue in list(listeners):
            queue.append(clean)

# Lancer odoo dans un thread séparé
threading.Thread(target=stream_process, daemon=True).start()

@app.route("/logs")
def logs():
    def event_stream():
        # 1️⃣ envoyer tout l'historique
        for old in log_buffer:
            yield f"data: {old}\n\n"

        # 2️⃣ écouter les nouvelles lignes
        queue = []
        listeners.append(queue)

        while True:
            if queue:
                item = queue.pop(0)
                yield f"data: {item}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/")
def home():
    return """
    <h2>Live Odoo Logs (with history)</h2>
    <pre id="log" style="white-space: pre-wrap;"></pre>
    <script>
        const logElement = document.getElementById("log");
        const source = new EventSource("/logs");

        source.onmessage = function(event) {
            logElement.textContent += event.data + "\\n";
            window.scrollTo(0, document.body.scrollHeight);
        };
    </script>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
