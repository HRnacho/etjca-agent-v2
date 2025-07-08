#!/usr/bin/env python3
"""
ETJCA Cloud Agent - Versione Completa con Database
Agente AI per la gestione intelligente del cloud con persistenza dati
"""

import os
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import aiohttp
from pathlib import Path

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActionType(Enum):
    """Tipi di azioni supportate dall'agente"""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    OPTIMIZE = "optimize"
    MIGRATE = "migrate"
    BACKUP = "backup"
    MONITOR = "monitor"
    ALERT = "alert"

class Priority(Enum):
    """Livelli di priorità per le azioni"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CloudResource:
    """Rappresenta una risorsa cloud"""
    id: str
    name: str
    type: str
    provider: str
    region: str
    status: str
    cpu_usage: float
    memory_usage: float
    storage_usage: float
    cost_per_hour: float
    created_at: datetime
    last_updated: datetime
    
    def to_dict(self) -> Dict:
        """Converte in dizionario per serializzazione"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_updated'] = self.last_updated.isoformat()
        return data

@dataclass
class ETJCAAction:
    """Rappresenta un'azione dell'agente ETJCA"""
    id: str
    resource_id: str
    action_type: ActionType
    priority: Priority
    description: str
    parameters: Dict[str, Any]
    estimated_cost_impact: float
    estimated_time_minutes: int
    created_at: datetime
    scheduled_for: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    status: str = "pending"
    result: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Converte in dizionario per serializzazione"""
        data = asdict(self)
        data['action_type'] = self.action_type.value
        data['priority'] = self.priority.value
        data['created_at'] = self.created_at.isoformat()
        if self.scheduled_for:
            data['scheduled_for'] = self.scheduled_for.isoformat()
        if self.executed_at:
            data['executed_at'] = self.executed_at.isoformat()
        return data

class ETJCADatabase:
    """Gestore del database per l'agente ETJCA"""
    
    def __init__(self, db_path: str = "etjca_agent.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inizializza il database con le tabelle necessarie"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabella risorse
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resources (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    region TEXT NOT NULL,
                    status TEXT NOT NULL,
                    cpu_usage REAL NOT NULL,
                    memory_usage REAL NOT NULL,
                    storage_usage REAL NOT NULL,
                    cost_per_hour REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Tabella azioni
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actions (
                    id TEXT PRIMARY KEY,
                    resource_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    description TEXT NOT NULL,
                    parameters TEXT NOT NULL,
                    estimated_cost_impact REAL NOT NULL,
                    estimated_time_minutes INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    scheduled_for TEXT,
                    executed_at TEXT,
                    status TEXT NOT NULL,
                    result TEXT,
                    FOREIGN KEY (resource_id) REFERENCES resources (id)
                )
            ''')
            
            # Tabella metriche
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resource_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    cpu_usage REAL NOT NULL,
                    memory_usage REAL NOT NULL,
                    storage_usage REAL NOT NULL,
                    network_in REAL NOT NULL,
                    network_out REAL NOT NULL,
                    FOREIGN KEY (resource_id) REFERENCES resources (id)
                )
            ''')
            
            # Tabella configurazione
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def save_resource(self, resource: CloudResource):
        """Salva una risorsa nel database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO resources 
                (id, name, type, provider, region, status, cpu_usage, memory_usage, 
                 storage_usage, cost_per_hour, created_at, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                resource.id, resource.name, resource.type, resource.provider,
                resource.region, resource.status, resource.cpu_usage,
                resource.memory_usage, resource.storage_usage,
                resource.cost_per_hour, resource.created_at.isoformat(),
                resource.last_updated.isoformat()
            ))
            conn.commit()
    
    def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Recupera una risorsa dal database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM resources WHERE id = ?', (resource_id,))
            row = cursor.fetchone()
            if row:
                return CloudResource(
                    id=row[0], name=row[1], type=row[2], provider=row[3],
                    region=row[4], status=row[5], cpu_usage=row[6],
                    memory_usage=row[7], storage_usage=row[8],
                    cost_per_hour=row[9],
                    created_at=datetime.fromisoformat(row[10]),
                    last_updated=datetime.fromisoformat(row[11])
                )
        return None
    
    def get_all_resources(self) -> List[CloudResource]:
        """Recupera tutte le risorse dal database"""
        resources = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM resources ORDER BY last_updated DESC')
            for row in cursor.fetchall():
                resources.append(CloudResource(
                    id=row[0], name=row[1], type=row[2], provider=row[3],
                    region=row[4], status=row[5], cpu_usage=row[6],
                    memory_usage=row[7], storage_usage=row[8],
                    cost_per_hour=row[9],
                    created_at=datetime.fromisoformat(row[10]),
                    last_updated=datetime.fromisoformat(row[11])
                ))
        return resources
    
    def save_action(self, action: ETJCAAction):
        """Salva un'azione nel database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO actions 
                (id, resource_id, action_type, priority, description, parameters,
                 estimated_cost_impact, estimated_time_minutes, created_at,
                 scheduled_for, executed_at, status, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                action.id, action.resource_id, action.action_type.value,
                action.priority.value, action.description,
                json.dumps(action.parameters), action.estimated_cost_impact,
                action.estimated_time_minutes, action.created_at.isoformat(),
                action.scheduled_for.isoformat() if action.scheduled_for else None,
                action.executed_at.isoformat() if action.executed_at else None,
                action.status, action.result
            ))
            conn.commit()
    
    def get_pending_actions(self) -> List[ETJCAAction]:
        """Recupera tutte le azioni pending"""
        actions = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM actions 
                WHERE status = 'pending' 
                ORDER BY priority DESC, created_at ASC
            ''')
            for row in cursor.fetchall():
                actions.append(ETJCAAction(
                    id=row[0], resource_id=row[1],
                    action_type=ActionType(row[2]),
                    priority=Priority(row[3]),
                    description=row[4],
                    parameters=json.loads(row[5]),
                    estimated_cost_impact=row[6],
                    estimated_time_minutes=row[7],
                    created_at=datetime.fromisoformat(row[8]),
                    scheduled_for=datetime.fromisoformat(row[9]) if row[9] else None,
                    executed_at=datetime.fromisoformat(row[10]) if row[10] else None,
                    status=row[11],
                    result=row[12]
                ))
        return actions

class ETJCAIntelligenceEngine:
    """Motore di intelligenza artificiale per l'agente ETJCA"""
    
    def __init__(self, db: ETJCADatabase):
        self.db = db
        self.thresholds = {
            'cpu_high': 80.0,
            'cpu_critical': 95.0,
            'memory_high': 85.0,
            'memory_critical': 95.0,
            'storage_high': 80.0,
            'storage_critical': 90.0
        }
    
    def analyze_resource(self, resource: CloudResource) -> List[ETJCAAction]:
        """Analizza una risorsa e genera azioni intelligenti"""
        actions = []
        now = datetime.now()
        
        # Analisi CPU
        if resource.cpu_usage > self.thresholds['cpu_critical']:
            actions.append(ETJCAAction(
                id=f"cpu_scale_{resource.id}_{int(now.timestamp())}",
                resource_id=resource.id,
                action_type=ActionType.SCALE_UP,
                priority=Priority.CRITICAL,
                description=f"CPU critico al {resource.cpu_usage:.1f}% - Scale up immediato",
                parameters={"scale_factor": 2, "reason": "cpu_critical"},
                estimated_cost_impact=resource.cost_per_hour * 1.5,
                estimated_time_minutes=5,
                created_at=now
            ))
        elif resource.cpu_usage > self.thresholds['cpu_high']:
            actions.append(ETJCAAction(
                id=f"cpu_optimize_{resource.id}_{int(now.timestamp())}",
                resource_id=resource.id,
                action_type=ActionType.OPTIMIZE,
                priority=Priority.HIGH,
                description=f"CPU elevato al {resource.cpu_usage:.1f}% - Ottimizzazione necessaria",
                parameters={"optimization_type": "cpu", "target_usage": 70.0},
                estimated_cost_impact=0.0,
                estimated_time_minutes=10,
                created_at=now
            ))
        
        # Analisi Memoria
        if resource.memory_usage > self.thresholds['memory_critical']:
            actions.append(ETJCAAction(
                id=f"memory_scale_{resource.id}_{int(now.timestamp())}",
                resource_id=resource.id,
                action_type=ActionType.SCALE_UP,
                priority=Priority.CRITICAL,
                description=f"Memoria critica al {resource.memory_usage:.1f}% - Scale up immediato",
                parameters={"scale_factor": 1.5, "reason": "memory_critical"},
                estimated_cost_impact=resource.cost_per_hour * 1.3,
                estimated_time_minutes=3,
                created_at=now
            ))
        
        # Analisi Storage
        if resource.storage_usage > self.thresholds['storage_critical']:
            actions.append(ETJCAAction(
                id=f"storage_expand_{resource.id}_{int(now.timestamp())}",
                resource_id=resource.id,
                action_type=ActionType.SCALE_UP,
                priority=Priority.HIGH,
                description=f"Storage critico al {resource.storage_usage:.1f}% - Espansione necessaria",
                parameters={"expansion_gb": 100, "reason": "storage_critical"},
                estimated_cost_impact=0.1,
                estimated_time_minutes=15,
                created_at=now
            ))
        
        # Analisi costi (se utilizzo basso, suggerisci scale down)
        if (resource.cpu_usage < 30.0 and resource.memory_usage < 40.0 and
            resource.status == "running"):
            actions.append(ETJCAAction(
                id=f"cost_optimize_{resource.id}_{int(now.timestamp())}",
                resource_id=resource.id,
                action_type=ActionType.SCALE_DOWN,
                priority=Priority.LOW,
                description=f"Utilizzo basso - Possibile riduzione costi",
                parameters={"scale_factor": 0.8, "reason": "low_utilization"},
                estimated_cost_impact=-resource.cost_per_hour * 0.2,
                estimated_time_minutes=5,
                created_at=now,
                scheduled_for=now + timedelta(hours=1)  # Ritarda per evitare scale down troppo rapidi
            ))
        
        return actions
    
    def prioritize_actions(self, actions: List[ETJCAAction]) -> List[ETJCAAction]:
        """Ordina le azioni per priorità e impatto"""
        priority_order = {
            Priority.CRITICAL: 4,
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1
        }
        
        return sorted(actions, key=lambda x: (
            priority_order[x.priority],
            -x.estimated_cost_impact,  # Negative per dare priorità ai risparmi
            x.estimated_time_minutes
        ), reverse=True)

class ETJCACloudAgent:
    """Agente ETJCA principale per la gestione intelligente del cloud"""
    
    def __init__(self, config_path: str = "etjca_config.json"):
        self.config_path = config_path
        self.db = ETJCADatabase()
        self.intelligence = ETJCAIntelligenceEngine(self.db)
        self.config = self.load_config()
        self.running = False
        logger.info("🚀 ETJCA Cloud Agent inizializzato")
    
    def load_config(self) -> Dict:
        """Carica la configurazione dell'agente"""
        default_config = {
            "monitoring_interval": 300,  # 5 minuti
            "auto_execute": False,
            "max_concurrent_actions": 3,
            "cloud_providers": {
                "aws": {"enabled": True, "regions": ["us-east-1", "eu-west-1"]},
                "azure": {"enabled": True, "regions": ["eastus", "westeurope"]},
                "gcp": {"enabled": True, "regions": ["us-central1", "europe-west1"]}
            },
            "notifications": {
                "email": {"enabled": False, "recipients": []},
                "slack": {"enabled": False, "webhook_url": ""}
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                logger.warning(f"Errore nel caricamento config: {e}")
        
        return default_config
    
    def save_config(self):
        """Salva la configurazione corrente"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    async def discover_resources(self) -> List[CloudResource]:
        """Simula la scoperta di risorse cloud"""
        # In un'implementazione reale, qui ci sarebbero le chiamate API ai provider
        mock_resources = [
            CloudResource(
                id="aws-ec2-i-1234567890abcdef0",
                name="web-server-prod",
                type="ec2_instance",
                provider="aws",
                region="us-east-1",
                status="running",
                cpu_usage=75.5,
                memory_usage=82.3,
                storage_usage=65.8,
                cost_per_hour=0.096,
                created_at=datetime.now() - timedelta(days=30),
                last_updated=datetime.now()
            ),
            CloudResource(
                id="azure-vm-vm-5678901234567890",
                name="api-server-staging",
                type="virtual_machine",
                provider="azure",
                region="eastus",
                status="running",
                cpu_usage=45.2,
                memory_usage=38.7,
                storage_usage=42.1,
                cost_per_hour=0.054,
                created_at=datetime.now() - timedelta(days=15),
                last_updated=datetime.now()
            ),
            CloudResource(
                id="gcp-compute-vm-abcdef1234567890",
                name="db-server-prod",
                type="compute_instance",
                provider="gcp",
                region="us-central1",
                status="running",
                cpu_usage=92.1,
                memory_usage=94.5,
                storage_usage=78.3,
                cost_per_hour=0.142,
                created_at=datetime.now() - timedelta(days=45),
                last_updated=datetime.now()
            )
        ]
        
        # Salva le risorse nel database
        for resource in mock_resources:
            self.db.save_resource(resource)
        
        logger.info(f"📊 Scoperte {len(mock_resources)} risorse cloud")
        return mock_resources
    
    async def analyze_and_plan(self) -> List[ETJCAAction]:
        """Analizza le risorse e pianifica le azioni"""
        resources = self.db.get_all_resources()
        all_actions = []
        
        for resource in resources:
            actions = self.intelligence.analyze_resource(resource)
            all_actions.extend(actions)
        
        # Prioritizza le azioni
        prioritized_actions = self.intelligence.prioritize_actions(all_actions)
        
        # Salva le azioni nel database
        for action in prioritized_actions:
            self.db.save_action(action)
        
        logger.info(f"🧠 Pianificate {len(prioritized_actions)} azioni")
        return prioritized_actions
    
    async def execute_action(self, action: ETJCAAction) -> bool:
        """Esegue un'azione specifica"""
        try:
            logger.info(f"🔧 Eseguendo: {action.description}")
            
            # Simula l'esecuzione dell'azione
            await asyncio.sleep(1)  # Simula tempo di esecuzione
            
            # Aggiorna lo stato dell'azione
            action.status = "completed"
            action.executed_at = datetime.now()
            action.result = f"Azione {action.action_type.value} completata con successo"
            
            self.db.save_action(action)
            logger.info(f"✅ Completata: {action.description}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore nell'esecuzione: {e}")
            action.status = "failed"
            action.result = f"Errore: {str(e)}"
            self.db.save_action(action)
            return False
    
    async def run_monitoring_cycle(self):
        """Esegue un ciclo completo di monitoraggio"""
        logger.info("🔍 Inizio ciclo di monitoraggio")
        
        # Scopri risorse
        await self.discover_resources()
        
        # Analizza e pianifica
        actions = await self.analyze_and_plan()
        
        # Esegui azioni se auto_execute è abilitato
        if self.config.get("auto_execute", False):
            pending_actions = self.db.get_pending_actions()
            max_concurrent = self.config.get("max_concurrent_actions", 3)
            
            for action in pending_actions[:max_concurrent]:
                if action.priority in [Priority.CRITICAL, Priority.HIGH]:
                    await self.execute_action(action)
        
        logger.info("✅ Ciclo di monitoraggio completato")
    
    async def start(self):
        """Avvia l'agente ETJCA"""
        self.running = True
        logger.info("🚀 ETJCA Agent avviato")
        
        while self.running:
            try:
                await self.run_monitoring_cycle()
                
                # Attendi prima del prossimo ciclo
                interval = self.config.get("monitoring_interval", 300)
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Errore nel ciclo di monitoraggio: {e}")
                await asyncio.sleep(60)  # Attendi 1 minuto prima di riprovare
    
    def stop(self):
        """Ferma l'agente ETJCA"""
        self.running = False
        logger.info("⏹️  ETJCA Agent fermato")
    
    def get_dashboard_data(self) -> Dict:
        """Restituisce i dati per la dashboard"""
        resources = self.db.get_all_resources()
        pending_actions = self.db.get_pending_actions()
        
        # Calcola statistiche
        total_cost = sum(r.cost_per_hour for r in resources)
        avg_cpu = sum(r.cpu_usage for r in resources) / len(resources) if resources else 0
        avg_memory = sum(r.memory_usage for r in resources) / len(resources) if resources else 0
        
        critical_resources = [r for r in resources if r.cpu_usage > 90 or r.memory_usage > 90]
        
        return {
            "summary": {
                "total_resources": len(resources),
                "total_cost_per_hour": round(total_cost, 2),
                "avg_cpu_usage": round(avg_cpu, 1),
                "avg_memory_usage": round(avg_memory, 1),
                "critical_resources": len(critical_resources),
                "pending_actions": len(pending_actions)
            },
            "resources": [r.to_dict() for r in resources],
            "actions": [a.to_dict() for a in pending_actions],
            "critical_resources": [r.to_dict() for r in critical_resources]
        }

# Funzione principale per test
async def main():
    """Funzione principale per test dell'agente"""
    agent = ETJCACloudAgent()
    
    try:
        # Avvia un ciclo di monitoraggio singolo per test
        await agent.run_monitoring_cycle()
        
        # Mostra i dati della dashboard
        dashboard_data = agent.get_dashboard_data()
        print("\n" + "="*60)
        print("📊 ETJCA CLOUD AGENT DASHBOARD")
        print("="*60)
        print(f"Risorse totali: {dashboard_data['summary']['total_resources']}")
        print(f"Costo orario totale: ${dashboard_data['summary']['total_cost_per_hour']}")
        print(f"Utilizzo CPU medio: {dashboard_data['summary']['avg_cpu_usage']}%")
        print(f"Utilizzo memoria medio: {dashboard_data['summary']['avg_memory_usage']}%")
        print(f"Risorse critiche: {dashboard_data['summary']['critical_resources']}")
        print(f"Azioni pendenti: {dashboard_data['summary']['pending_actions']}")
        
        if dashboard_data['actions']:
            print("\n🔧 AZIONI PIANIFICATE:")
            for action in dashboard_data['actions'][:5]:  # Mostra solo le prime 5
                print(f"  • {action['description']} (Priorità: {action['priority']})")
        
        print("\n✅ Test completato con successo!")
        
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")

if __name__ == "__main__":
    asyncio.run(main())
