#!/usr/bin/env python3
"""
ETJCA Cloud Agent - Versione Semplificata per Railway
"""

import os
import asyncio
import logging
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETJCAAgent:
    def __init__(self):
        self.running = True
        
        # Verifica database
        db_url = os.environ.get('DATABASE_URL', 'sqlite:///etjca.db')
        self.db_type = "postgresql" if "postgresql" in db_url else "sqlite"
        
        logger.info("🚀 ETJCA Agent inizializzato")
        logger.info(f"🗄️ Database: {self.db_type}")
        
        # Configurazione base
        self.config = {
            "agent_name": "ETJCA-Cloud-Agent",
            "version": "1.0.0",
            "providers": ["aws", "azure", "gcp"],
            "monitoring_interval": 300  # 5 minuti
        }
        
    async def discover_resources(self):
        """Simula discovery risorse cloud"""
        logger.info("🔍 Discovering cloud resources...")
        await asyncio.sleep(1)
        
        # Simula discovery
        resources = [
            {
                "id": "aws-ec2-001", 
                "type": "instance", 
                "provider": "aws",
                "status": "running",
                "cpu_usage": 75.5,
                "memory_usage": 68.2
            },
            {
                "id": "azure-vm-002", 
                "type": "vm", 
                "provider": "azure",
                "status": "running",
                "cpu_usage": 45.1,
                "memory_usage": 52.3
            },
            {
                "id": "gcp-compute-003", 
                "type": "instance", 
                "provider": "gcp",
                "status": "running",
                "cpu_usage": 89.7,
                "memory_usage": 91.2
            }
        ]
        
        logger.info(f"📊 Scoperte {len(resources)} risorse cloud")
        return resources
        
    async def analyze_resources(self, resources):
        """Analizza risorse scoperte"""
        logger.info("🧠 Analizzando risorse...")
        await asyncio.sleep(1)
        
        critical_resources = []
        recommendations = []
        
        for resource in resources:
            # Controlla utilizzo critico
            if resource["cpu_usage"] > 85 or resource["memory_usage"] > 85:
                critical_resources.append(resource)
                recommendations.append({
                    "resource_id": resource["id"],
                    "action": "scale_up",
                    "reason": f"High usage: CPU {resource['cpu_usage']}%, Memory {resource['memory_usage']}%"
                })
        
        analysis = {
            "total_resources": len(resources),
            "critical_resources": len(critical_resources),
            "recommendations": recommendations,
            "avg_cpu": sum(r["cpu_usage"] for r in resources) / len(resources),
            "avg_memory": sum(r["memory_usage"] for r in resources) / len(resources)
        }
        
        logger.info(f"📈 Analisi completata: {analysis['critical_resources']} risorse critiche")
        return analysis
        
    async def optimize_resources(self, analysis):
        """Ottimizza risorse basandosi sull'analisi"""
        if analysis["recommendations"]:
            logger.info(f"⚡ Applicando {len(analysis['recommendations'])} ottimizzazioni...")
            await asyncio.sleep(1)
            
            for rec in analysis["recommendations"]:
                logger.info(f"  🔧 {rec['resource_id']}: {rec['action']} - {rec['reason']}")
            
            logger.info("✅ Ottimizzazioni applicate")
            return len(analysis["recommendations"])
        else:
            logger.info("✅ Nessuna ottimizzazione necessaria")
            return 0
        
    async def send_notifications(self, analysis):
        """Invia notifiche per situazioni critiche"""
        if analysis["critical_resources"] > 0:
            logger.info(f"📧 Invio notifiche per {analysis['critical_resources']} risorse critiche")
            # Qui potresti aggiungere invio email reale
            await asyncio.sleep(0.5)
            logger.info("📧 Notifiche inviate")
        
    async def run_cycle(self):
        """Esegue un ciclo completo di monitoraggio"""
        cycle_start = datetime.now()
        logger.info("🔄 Inizio ciclo di monitoraggio")
        
        try:
            # 1. Discovery
            resources = await self.discover_resources()
            
            # 2. Analisi
            analysis = await self.analyze_resources(resources)
            
            # 3. Ottimizzazione
            optimizations = await self.optimize_resources(analysis)
            
            # 4. Notifiche
            await self.send_notifications(analysis)
            
            # 5. Riepilogo
            cycle_duration = (datetime.now() - cycle_start).total_seconds()
            
            logger.info("✅ Ciclo completato con successo")
            logger.info(f"📊 Riepilogo: {analysis['total_resources']} risorse, {optimizations} ottimizzazioni, {cycle_duration:.1f}s")
            
            return {
                "success": True,
                "duration": cycle_duration,
                "resources": analysis["total_resources"],
                "optimizations": optimizations,
                "critical_resources": analysis["critical_resources"]
            }
            
        except Exception as e:
            logger.error(f"❌ Errore nel ciclo: {e}")
            return {"success": False, "error": str(e)}
            
    async def start(self):
        """Avvia l'agente in modalità continua"""
        logger.info("🚀 ETJCA Agent avviato - modalità continua")
        
        cycle_count = 0
        while self.running:
            try:
                cycle_count += 1
                logger.info(f"📊 Ciclo #{cycle_count}")
                
                # Esegui ciclo
                result = await self.run_cycle()
                
                if result["success"]:
                    logger.info(f"💤 Pausa {self.config['monitoring_interval']} secondi...")
                    await asyncio.sleep(self.config["monitoring_interval"])
                else:
                    logger.error("❌ Ciclo fallito, riprovo in 60 secondi...")
                    await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"❌ Errore critico: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        """Ferma l'agente"""
        self.running = False
logger.info("⏹️ ETJCA Agent fermato")
    
    def get_status(self):
        """Ritorna lo status dell'agente"""
        return {
            "agent_name": self.config["agent_name"],
            "version": self.config["version"],
            "database": self.db_type,
            "status": "running" if self.running else "stopped",
            "timestamp": datetime.now().isoformat()
        }

# Istanza globale per Railway
agent = ETJCAAgent()

async def main():
    """Funzione principale con web server semplice"""
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class ETJCAHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                status = agent.get_status()
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>ETJCA Cloud Agent</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                        .status {{ color: #28a745; font-weight: bold; }}
                        .metric {{ background: #e9ecef; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🚀 ETJCA Cloud Agent</h1>
                        <p class="status">Status: {status['status'].upper()}</p>
                        <div class="metric">
                            <strong>Agent:</strong> {status['agent_name']} v{status['version']}
                        </div>
                        <div class="metric">
                            <strong>Database:</strong> {status['database']}
                        </div>
                        <div class="metric">
                            <strong>Last Update:</strong> {status['timestamp']}
                        </div>
                        <div class="metric">
                            <strong>Monitoring:</strong> Cicli automatici ogni 5 minuti
                        </div>
                        <h3>📊 Funzionalità Attive</h3>
                        <ul>
                            <li>🔍 Discovery risorse cloud</li>
                            <li>🧠 Analisi intelligente</li>
                            <li>⚡ Ottimizzazioni automatiche</li>
                            <li>📧 Notifiche smart</li>
                        </ul>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
            elif self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                import json
                status = agent.get_status()
                self.wfile.write(json.dumps(status).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not Found')
    
    # Avvia web server in thread separato
    port = int(os.environ.get('PORT', 8000))
    httpd = HTTPServer(('0.0.0.0', port), ETJCAHandler)
    
    def start_web_server():
        logger.info(f"🌐 Web server avviato su porta {port}")
        httpd.serve_forever()
    
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    try:
        logger.info("🚀 Avvio ETJCA Cloud Agent...")
        
        # Mostra status
        status = agent.get_status()
        logger.info(f"📊 {status['agent_name']} v{status['version']}")
        logger.info(f"🗄️ Database: {status['database']}")
        logger.info(f"🌐 Web interface disponibile")
        
        # Esegui un ciclo di test
        logger.info("🧪 Eseguendo ciclo di test...")
        test_result = await agent.run_cycle()
        
        if test_result["success"]:
            logger.info("✅ Test completato con successo!")
            logger.info("🔄 Avvio modalità continua...")
            
            # Avvia modalità continua
            await agent.start()
        else:
            logger.error(f"❌ Test fallito: {test_result.get('error')}")
            # Mantieni il web server attivo anche se il test fallisce
            while True:
                await asyncio.sleep(60)
                
    except Exception as e:
        logger.error(f"❌ Errore fatale: {e}")
        # Mantieni il web server attivo anche con errori
        while True:
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
