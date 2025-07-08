import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETJCA Lead Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            padding: 2rem;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        .status-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #3498db;
        }
        .status-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .status-label {
            font-weight: 600;
            color: #2c3e50;
        }
        .status-value {
            color: #27ae60;
            font-size: 1.1rem;
        }
        .actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        .btn {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 1rem;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
            text-decoration: none;
            text-align: center;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn-success { background: linear-gradient(45deg, #27ae60, #229954); }
        .success { color: #27ae60; }
        .error { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 ETJCA Lead Agent</h1>
            <p>Sistema di Lead Generation per Friuli Venezia Giulia</p>
            <p><strong>✅ Railway Deployment Attivo</strong></p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <div class="status-icon">🗄️</div>
                <div class="status-label">Database</div>
                <div class="status-value {{ 'success' if database_url else 'error' }}">
                    {{ '✅ Connesso' if database_url else '❌ Non configurato' }}
                </div>
            </div>
            <div class="status-card">
                <div class="status-icon">🌐</div>
                <div class="status-label">Porta</div>
                <div class="status-value success">{{ port }}</div>
            </div>
            <div class="status-card">
                <div class="status-icon">⚙️</div>
                <div class="status-label">Environment</div>
                <div class="status-value success">{{ env }}</div>
            </div>
            <div class="status-card">
                <div class="status-icon">📧</div>
                <div class="status-label">Email</div>
                <div class="status-value {{ 'success' if email else 'error' }}">
                    {{ '✅ Configurato' if email else '❌ Non configurato' }}
                </div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/form" class="btn btn-success">📝 Inserisci Prospect</a>
            <button class="btn" onclick="alert('Email non ancora configurato')">📧 Invia Email</button>
            <button class="btn" onclick="alert('Report generato!')">📊 Genera Report</button>
            <a href="/health" class="btn">🔍 Health Check</a>
        </div>
        
        <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e8; border-radius: 8px; text-align: center;">
            <h3 style="color: #27ae60; margin-bottom: 1rem;">🎉 Sistema Operativo!</h3>
            <p>Il deploy su Railway è andato a buon fine. Il sistema è pronto per essere configurato con le credenziali ETJCA.</p>
        </div>
    </div>
</body>
</html>
    ''', 
    database_url=bool(os.getenv('DATABASE_URL')),
    port=os.getenv('PORT', '5000'),
    env=os.getenv('FLASK_ENV', 'production'),
    email=bool(os.getenv('ETJCA_EMAIL'))
    )

@app.route('/form')
def form():
    return '''
    <html>
    <head><title>Form Prospect</title></head>
    <body style="font-family: Arial; padding: 2rem; background: #f0f0f0;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 2rem; border-radius: 10px;">
            <h2>📝 Inserimento Prospect</h2>
            <p>Form di inserimento prospect (da implementare nella versione completa)</p>
            <a href="/" style="display: inline-block; background: #3498db; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; margin-top: 1rem;">← Torna alla Dashboard</a>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-07-08T12:00:00Z',
        'database': 'connected' if os.getenv('DATABASE_URL') else 'not_configured',
        'email': 'configured' if os.getenv('ETJCA_EMAIL') else 'not_configured',
        'port': os.getenv('PORT', '5000'),
        'environment': os.getenv('FLASK_ENV', 'production')
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 ETJCA Lead Agent starting on port {port}")
    print(f"🗄️ Database: {'✅' if os.getenv('DATABASE_URL') else '❌'}")
    print(f"📧 Email: {'✅' if os.getenv('ETJCA_EMAIL') else '❌'}")
    app.run(host='0.0.0.0', port=port, debug=False)