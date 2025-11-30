import subprocess
import threading
import time
from datetime import datetime
from collections import deque
from flask import Flask, Response, jsonify, request
import json

app = Flask(__name__)

# Configuration
MAX_LOG_LINES = 100000  # Keep last 100k lines in memory
ODOO_COMMAND = [
    "./odoo/odoo-bin",
    "-u", "my_hostel",
    "-d", "odoo_test"
]
ODOO_CWD = "/home/erp/odoo-dev"

# Global state
log_buffer = deque(maxlen=MAX_LOG_LINES)  # Efficient circular buffer
listeners = []
process = None
process_info = {
    "started_at": None,
    "status": "not_started",
    "total_lines": 0,
    "uptime_seconds": 0
}
lock = threading.Lock()


def add_log_entry(line):
    """Add a log entry with timestamp and metadata"""
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "line_number": process_info["total_lines"],
        "content": line
    }
    
    with lock:
        log_buffer.append(entry)
        process_info["total_lines"] += 1
        
        # Broadcast to all active listeners
        for queue in list(listeners):
            try:
                queue.append(entry)
            except:
                listeners.remove(queue)


def stream_process():
    """Launch Odoo and capture logs continuously"""
    global process, process_info
    
    try:
        process_info["started_at"] = datetime.now().isoformat()
        process_info["status"] = "running"
        
        process = subprocess.Popen(
            ODOO_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=ODOO_CWD
        )
        
        add_log_entry(f"=== Odoo process started (PID: {process.pid}) ===")
        
        for line in process.stdout:
            clean = line.rstrip()
            if clean:  # Skip empty lines
                add_log_entry(clean)
        
        # Process ended
        process_info["status"] = "stopped"
        add_log_entry(f"=== Odoo process ended with code {process.returncode} ===")
        
    except Exception as e:
        process_info["status"] = "error"
        add_log_entry(f"=== ERROR: {str(e)} ===")


def update_uptime():
    """Update uptime in background"""
    while True:
        if process_info["started_at"]:
            start = datetime.fromisoformat(process_info["started_at"])
            process_info["uptime_seconds"] = (datetime.now() - start).total_seconds()
        time.sleep(1)


# Start background threads
threading.Thread(target=stream_process, daemon=True).start()
threading.Thread(target=update_uptime, daemon=True).start()


@app.route("/logs")
def logs():
    """SSE endpoint for streaming logs"""
    def event_stream():
        # Send all historical logs first
        with lock:
            for entry in log_buffer:
                yield f"data: {json.dumps(entry)}\n\n"
        
        # Create queue for new logs
        queue = []
        listeners.append(queue)
        
        try:
            while True:
                if queue:
                    entry = queue.pop(0)
                    yield f"data: {json.dumps(entry)}\n\n"
                else:
                    time.sleep(0.1)  # Prevent busy waiting
        finally:
            if queue in listeners:
                listeners.remove(queue)
    
    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/api/stats")
def stats():
    """Get current statistics"""
    return jsonify({
        **process_info,
        "buffer_size": len(log_buffer),
        "max_buffer_size": MAX_LOG_LINES,
        "active_viewers": len(listeners),
        "process_pid": process.pid if process else None
    })


@app.route("/api/logs/export")
def export_logs():
    """Export all logs as JSON"""
    with lock:
        logs = list(log_buffer)
    return jsonify({
        "exported_at": datetime.now().isoformat(),
        "total_lines": len(logs),
        "logs": logs
    })


@app.route("/api/logs/search")
def search_logs():
    """Search logs by keyword"""
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    
    with lock:
        results = [
            entry for entry in log_buffer 
            if query in entry["content"].lower()
        ]
    
    return jsonify({
        "query": query,
        "matches": len(results),
        "results": results[:1000]  # Limit results
    })


@app.route("/api/webhook/n8n", methods=["POST"])
def webhook_n8n():
    """Webhook endpoint for n8n integration"""
    # Configure this URL in n8n as a webhook trigger
    # Sends recent logs on demand
    
    count = int(request.args.get("count", 100))
    level = request.args.get("level", "all")  # all, error, warning
    
    with lock:
        logs = list(log_buffer)[-count:]
    
    # Filter by level if needed
    if level != "all":
        logs = [
            log for log in logs 
            if level.upper() in log["content"].upper()
        ]
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "logs": logs,
        "stats": process_info
    })


@app.route("/")
def home():
    """Enhanced web interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Odoo Live Logs</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Consolas', 'Monaco', monospace; 
                background: #1e1e1e; 
                color: #d4d4d4;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            .header {
                background: #2d2d30;
                padding: 15px 20px;
                border-bottom: 2px solid #007acc;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 {
                font-size: 18px;
                color: #007acc;
            }
            .stats {
                display: flex;
                gap: 20px;
                font-size: 12px;
            }
            .stat {
                display: flex;
                flex-direction: column;
            }
            .stat-label { color: #858585; }
            .stat-value { color: #4ec9b0; font-weight: bold; }
            .controls {
                background: #252526;
                padding: 10px 20px;
                display: flex;
                gap: 10px;
                align-items: center;
                border-bottom: 1px solid #3e3e42;
            }
            button {
                background: #0e639c;
                color: white;
                border: none;
                padding: 8px 16px;
                cursor: pointer;
                border-radius: 3px;
                font-size: 12px;
            }
            button:hover { background: #1177bb; }
            input[type="text"] {
                background: #3c3c3c;
                border: 1px solid #5e5e5e;
                color: #d4d4d4;
                padding: 8px;
                border-radius: 3px;
                flex: 1;
                max-width: 300px;
            }
            .log-container {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }
            .log-entry {
                margin-bottom: 2px;
                font-size: 13px;
                line-height: 1.5;
                display: flex;
                gap: 10px;
            }
            .log-timestamp {
                color: #858585;
                min-width: 180px;
            }
            .log-content {
                flex: 1;
                white-space: pre-wrap;
                word-break: break-word;
            }
            .log-content.error { color: #f48771; }
            .log-content.warning { color: #dcdcaa; }
            .log-content.info { color: #4ec9b0; }
            #status {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #4ec9b0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .status-offline { background: #f48771 !important; }
        </style>
    </head>
    <body>
        <div class="header">
            <div style="display: flex; align-items: center; gap: 15px;">
                <h1>🔍 Odoo Live Logs Monitor</h1>
                <div id="status"></div>
            </div>
            <div class="stats">
                <div class="stat">
                    <span class="stat-label">Total Lines</span>
                    <span class="stat-value" id="total-lines">0</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Uptime</span>
                    <span class="stat-value" id="uptime">00:00:00</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Viewers</span>
                    <span class="stat-value" id="viewers">0</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Status</span>
                    <span class="stat-value" id="status-text">Connecting...</span>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <input type="text" id="search" placeholder="Search logs..." />
            <button onclick="clearLogs()">Clear Display</button>
            <button onclick="scrollToBottom()">Scroll to Bottom</button>
            <button onclick="exportLogs()">Export JSON</button>
            <label>
                <input type="checkbox" id="autoscroll" checked> Auto-scroll
            </label>
        </div>
        
        <div class="log-container" id="log"></div>
        
        <script>
            const logElement = document.getElementById("log");
            const statusIndicator = document.getElementById("status");
            const searchInput = document.getElementById("search");
            const autoscrollCheck = document.getElementById("autoscroll");
            
            let allLogs = [];
            let searchTerm = "";
            
            // Connect to SSE
            const source = new EventSource("/logs");
            
            source.onopen = function() {
                statusIndicator.classList.remove("status-offline");
                document.getElementById("status-text").textContent = "Connected";
            };
            
            source.onerror = function() {
                statusIndicator.classList.add("status-offline");
                document.getElementById("status-text").textContent = "Disconnected";
            };
            
            source.onmessage = function(event) {
                const entry = JSON.parse(event.data);
                allLogs.push(entry);
                
                if (matchesSearch(entry)) {
                    addLogToDOM(entry);
                }
            };
            
            function matchesSearch(entry) {
                if (!searchTerm) return true;
                return entry.content.toLowerCase().includes(searchTerm);
            }
            
            function addLogToDOM(entry) {
                const div = document.createElement("div");
                div.className = "log-entry";
                
                const timestamp = document.createElement("span");
                timestamp.className = "log-timestamp";
                timestamp.textContent = entry.timestamp;
                
                const content = document.createElement("span");
                content.className = "log-content";
                
                // Colorize based on content
                if (entry.content.includes("ERROR") || entry.content.includes("error")) {
                    content.classList.add("error");
                } else if (entry.content.includes("WARNING") || entry.content.includes("warning")) {
                    content.classList.add("warning");
                } else if (entry.content.includes("INFO")) {
                    content.classList.add("info");
                }
                
                content.textContent = entry.content;
                
                div.appendChild(timestamp);
                div.appendChild(content);
                logElement.appendChild(div);
                
                if (autoscrollCheck.checked) {
                    window.scrollTo(0, document.body.scrollHeight);
                }
            }
            
            // Search functionality
            searchInput.addEventListener("input", function() {
                searchTerm = this.value.toLowerCase();
                logElement.innerHTML = "";
                allLogs.filter(matchesSearch).forEach(addLogToDOM);
            });
            
            function clearLogs() {
                logElement.innerHTML = "";
            }
            
            function scrollToBottom() {
                window.scrollTo(0, document.body.scrollHeight);
            }
            
            function exportLogs() {
                window.open("/api/logs/export", "_blank");
            }
            
            // Update stats every second
            setInterval(async () => {
                try {
                    const res = await fetch("/api/stats");
                    const stats = await res.json();
                    
                    document.getElementById("total-lines").textContent = 
                        stats.total_lines.toLocaleString();
                    document.getElementById("viewers").textContent = stats.active_viewers;
                    
                    const hours = Math.floor(stats.uptime_seconds / 3600);
                    const minutes = Math.floor((stats.uptime_seconds % 3600) / 60);
                    const seconds = Math.floor(stats.uptime_seconds % 60);
                    document.getElementById("uptime").textContent = 
                        `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
                } catch (e) {
                    console.error("Failed to fetch stats:", e);
                }
            }, 1000);
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Odoo Log Streaming Server")
    print("=" * 60)
    print(f"📍 Access the web interface at: http://0.0.0.0:5000")
    print(f"📊 API Stats endpoint: http://0.0.0.0:5000/api/stats")
    print(f"🔍 Search logs: http://0.0.0.0:5000/api/logs/search?q=error")
    print(f"📤 Export logs: http://0.0.0.0:5000/api/logs/export")
    print(f"🔗 n8n webhook: http://0.0.0.0:5000/api/webhook/n8n")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5000, threaded=True)
