import subprocess
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
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
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
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(57, 255, 20, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(57, 255, 20, 0); }
            100% { box-shadow: 0 0 0 0 rgba(57, 255, 20, 0); }
        }
        .refresh-btn {
            display: block;
            margin: 40px auto;
            padding: 12px 35px;
            background: rgba(0, 243, 255, 0.1);
            color: var(--neon-blue);
            border: 1px solid var(--neon-blue);
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        .refresh-btn:hover {
            background: var(--neon-blue);
            color: #000;
            box-shadow: 0 0 20px var(--neon-blue);
        }
    </style>
</head>
<body>
    <h1><span class="live-indicator"></span> NaaS Control Center - Grupo 01</h1>
    
    <div class="container">
        <div class="card">
            <h2>🖥️ Compute Plane (KVM VMs)</h2>
            <pre>{vms}</pre>
        </div>

        <div class="card">
            <h2>🖧 Data Plane (Open vSwitch)</h2>
            <pre>{ovs}</pre>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">Atualizar Dados</button>
</body>
</html>
"""

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        try:
            vms = subprocess.check_output(['sudo', 'virsh', 'list', '--all'], text=True)
            ovs = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'], text=True)
        except Exception as e:
            vms = "Erro ao carregar VMs: " + str(e)
            ovs = "Erro ao carregar OVS: " + str(e)
            
        html = HTML_TEMPLATE.replace("{vms}", vms).replace("{ovs}", ovs)
        self.wfile.write(html.encode("utf-8"))

    # Desativa logs no console para manter o terminal limpo
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    porta = 8080
    server = HTTPServer(('0.0.0.0', porta), DashboardHandler)
    print("\033[0;32m[SUCESSO] Dashboard NaaS rodando!\033[0m")
    print(f"Abra o seu navegador no Windows e acesse: \033[1;36mhttp://localhost:{porta}\033[0m")
    print("Pressione Ctrl+C para desligar o servidor.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor desligado.")
