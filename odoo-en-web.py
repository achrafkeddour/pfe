import subprocess
from flask import Flask, Response

app = Flask(__name__)

def stream_logs():

    # Lancement EXACT de ta commande Odoo dans le venv
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
        cwd="/home/erp/odoo-dev"   # <-- IMPORTANT : dossier où se trouve odoo-bin
    )

    for line in process.stdout:
        yield f"data: {line.rstrip()}\n\n"

@app.route("/logs")
def logs():
    return Response(stream_logs(), mimetype="text/event-stream")

@app.route("/")
def home():
    return """
    <h2>Live Odoo Logs</h2>
    <pre id="log"></pre>
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
