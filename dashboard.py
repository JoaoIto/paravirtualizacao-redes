import subprocess
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaaS Dashboard - Provedor Regional</title>
    <style>
        :root {
            --neon-blue: #00f3ff;
            --neon-green: #39ff14;
            --neon-purple: #b026ff;
            --bg-color: #0b0f19;
            --card-bg: rgba(20, 25, 40, 0.7);
        }
        body { 
            background-color: var(--bg-color); 
            color: #fff; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            padding: 40px; 
            background-image: radial-gradient(circle at 50% 0%, #1a233a 0%, transparent 50%);
            min-height: 100vh;
            margin: 0;
        }
        h1 { 
            color: var(--neon-blue); 
            text-align: center; 
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            margin-bottom: 40px;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        @media (max-width: 1024px) {
            .container { grid-template-columns: 1fr 1fr; }
        }
        @media (max-width: 768px) {
            .container { grid-template-columns: 1fr; }
        }
        .card { 
            background: var(--card-bg); 
            border: 1px solid rgba(0, 243, 255, 0.2); 
            border-radius: 15px; 
            padding: 25px; 
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            border-color: var(--neon-blue);
            box-shadow: 0 8px 32px 0 rgba(0, 243, 255, 0.1);
        }
        .card.purple:hover {
            border-color: var(--neon-purple);
            box-shadow: 0 8px 32px 0 rgba(176, 38, 255, 0.1);
        }
        h2 { 
            color: #fff; 
            font-size: 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        pre { 
            background: rgba(0,0,0,0.5); 
            padding: 15px; 
            border-radius: 8px; 
            color: #a5d6ff; 
            overflow-x: auto; 
            font-size: 0.95rem;
            line-height: 1.5;
            border-left: 3px solid var(--neon-blue);
        }
        .card.purple pre { border-left-color: var(--neon-purple); }
        .live-indicator {
            width: 12px;
            height: 12px;
            background-color: var(--neon-green);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px var(--neon-green);
            animation: pulse 1.5s infinite;
            margin-right: 10px;
        }
        .status-badge {
            background-color: rgba(57, 255, 20, 0.2);
            color: var(--neon-green);
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            border: 1px solid var(--neon-green);
            margin-bottom: 20px;
            display: inline-block;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(57, 255, 20, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(57, 255, 20, 0); }
            100% { box-shadow: 0 0 0 0 rgba(57, 255, 20, 0); }
        }
    </style>
</head>
<body>
    <h1><span class="live-indicator"></span> NaaS Control Center - Grupo 01</h1>
    
    <div style="text-align: center;">
        <div class="status-badge">AUTO-REFRESH: ATIVO (2s)</div>
    </div>

    <div class="container">
        <div class="card purple">
            <h2>⚙️ Bare Metal Host (Recursos do KVM)</h2>
            <pre id="nodeinfo">Carregando...</pre>
        </div>

        <div class="card">
            <h2>🖥️ Compute Plane (Status das VMs)</h2>
            <pre id="vms">Carregando...</pre>
        </div>

        <div class="card">
            <h2>🖧 Data Plane (Open vSwitch)</h2>
            <pre id="ovs">Carregando...</pre>
        </div>
    </div>
    
    <script>
        function fetchData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('vms').textContent = data.vms;
                    document.getElementById('ovs').textContent = data.ovs;
                    document.getElementById('nodeinfo').textContent = data.nodeinfo;
                })
                .catch(err => console.error("Erro ao buscar dados:", err));
        }
        
        // Busca os dados imediatamente ao carregar a página
        fetchData();
        
        // Atualiza os dados a cada 2 segundos magicamente em background
        setInterval(fetchData, 2000);
    </script>
</body>
</html>
"""

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            try:
                vms = subprocess.check_output(['sudo', 'virsh', 'list', '--all'], text=True)
                ovs = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'], text=True)
                nodeinfo = subprocess.check_output(['sudo', 'virsh', 'nodeinfo'], text=True)
            except Exception as e:
                vms = "Erro ao carregar VMs: " + str(e)
                ovs = "Erro ao carregar OVS: " + str(e)
                nodeinfo = "Erro ao carregar Host: " + str(e)
                
            data = {
                "vms": vms,
                "ovs": ovs,
                "nodeinfo": nodeinfo
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

    # Desativa logs no console para manter o terminal limpo
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    porta = 8080
    server = HTTPServer(('0.0.0.0', porta), DashboardHandler)
    print("\033[0;32m[SUCESSO] Dashboard NaaS rodando em TEMPO REAL!\033[0m")
    print(f"Abra o seu navegador no Windows e acesse: \033[1;36mhttp://localhost:{porta}\033[0m")
    print("Pressione Ctrl+C para desligar o servidor.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor desligado.")
