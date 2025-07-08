print("\n✅ Test MCP completato con successo!")
        print("🔗 Configurazione MCP salvata in: etjca_mcp_config.json")
        print(f"🗄️  Database: {agent.email_manager.rate_limiter.db_manager.db_type}")
        
        if agent.email_manager.rate_limiter.db_manager.db_type == "postgresql":
            print("📊 Database PostgreSQL attivo (perfetto per Railway!)")
        else:
            print("📊 Database SQLite attivo (ottimo per sviluppo locale)")
        
        print("\n📝 CONFIGURAZIONE EMAIL:")
        print("   Per attivare le notifiche email, modifica etjca_mcp_config.json:")
        print('   "email": {')
        print('     "enabled": true,')
        print('     "username": "your-email@gmail.com",')
        print('     "password": "your-app-password",')
        print('     "recipients": ["admin@company.com"]')
        print('   }')
        
        print("\n🚀 DEPLOY RAILWAY:")
        print("   1. Assicurati che PostgreSQL sia attivo su Railway")
        print("   2. Configura la variabile DATABASE_URL")
        print("   3. Installa: pip install psycopg2-binary")
        print("   4. Deploy: git push")
        
    except Exception as e:
        print(f"❌ Errore durante test MCP: {e}")
        import traceback
        traceback.print_exc()

# Utility per verificare la configurazione del database
def check_database_config():
    """Verifica la configurazione del database"""
    print("🔍 VERIFICA CONFIGURAZIONE DATABASE")
    print("="*40)
    
    db_manager = DatabaseManager()
    print(f"Database rilevato: {db_manager.db_type}")
    
    if db_manager.db_type == "postgresql":
        print("✅ PostgreSQL configurato correttamente")
        print(f"Parametri di connessione: {list(db_manager.connection_params.keys())}")
        
        try:
            # Test connessione
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                print(f"✅ Connessione riuscita: {version}")
        except Exception as e:
            print(f"❌ Errore connessione PostgreSQL: {e}")
            print("💡 Suggerimenti:")
            print("   - Verifica che DATABASE_URL sia configurato")
            print("   - Installa psycopg2-binary: pip install psycopg2-binary")
            print("   - Controlla che il database sia attivo su Railway")
    
    else:
        print("📁 SQLite configurato per sviluppo locale")
        print(f"Database path: {db_manager.connection_params['database_path']}")
        
        try:
            # Test connessione SQLite
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sqlite_version()")
                version = cursor.fetchone()[0]
                print(f"✅ SQLite version: {version}")
        except Exception as e:
            print(f"❌ Errore SQLite: {e}")
    
    print("\n🔧 VARIABILI AMBIENTE:")
    env_vars = ['DATABASE_URL', 'POSTGRES_HOST', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var or 'URL' in var:
                print(f"   {var}: {'*' * min(len(value), 10)}")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: NON CONFIGURATO")

# Utility per configurare email facilmente
def setup_email_config():
    """Utility per configurare facilmente le email"""
    print("🔧 CONFIGURAZIONE EMAIL ETJCA")
    print("="*40)
    
    config_path = "etjca_mcp_config.json"
    
    # Carica config esistente
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        print("❌ Config file non trovato. Eseguire prima main().")
        return
    
    print("📧 Configurazione email attuale:")
    email_config = config.get("email", {})
    print(f"  Abilitato: {email_config.get('enabled', False)}")
    print(f"  Username: {email_config.get('username', 'NON CONFIGURATO')}")
    print(f"  Destinatari: {len(email_config.get('recipients', []))}")
    
    # Chiedi se modificare
    if input("\nVuoi modificare la configurazione email? (s/n): ").lower() == 's':
        
        # Configura SMTP
        email_config["enabled"] = input("Abilitare email? (s/n): ").lower() == 's'
        
        if email_config["enabled"]:
            email_config["username"] = input("Email username (es. youremail@gmail.com): ").strip()
            email_config["password"] = input("App password (non la password normale!): ").strip()
            
            # Configura destinatari
            recipients = []
            print("\nAggiungi destinatari (premi invio per finire):")
            while True:
                recipient = input(f"Destinatario {len(recipients)+1}: ").strip()
                if not recipient:
                    break
                recipients.append(recipient)
            
            email_config["recipients"] = recipients
            
            # Configura rate limits
            print(f"\nRate limits attuali:")
            limits = email_config.get("rate_limits", {})
            print(f"  Settimanale: {limits.get('weekly_limit', 10)}")
            print(f"  Giornaliero: {limits.get('daily_limit', 3)}")
            print(f"  Orario: {limits.get('hourly_limit', 1)}")
            
            if input("Modificare rate limits? (s/n): ").lower() == 's':
                try:
                    limits["weekly_limit"] = int(input(f"Limite settimanale [{limits.get('weekly_limit', 10)}]: ") or limits.get('weekly_limit', 10))
                    limits["daily_limit"] = int(input(f"Limite giornaliero [{limits.get('daily_limit', 3)}]: ") or limits.get('daily_limit', 3))
                    limits["hourly_limit"] = int(input(f"Limite orario [{limits.get('hourly_limit', 1)}]: ") or limits.get('hourly_limit', 1))
                    email_config["rate_limits"] = limits
                except ValueError:
                    print("⚠️ Valori non validi, mantengo quelli attuali")
        
        # Salva configurazione
        config["email"] = email_config
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("\n✅ Configurazione email salvata!")
        print(f"📧 Email abilitate: {email_config.get('enabled', False)}")
        print(f"📬 Destinatari: {len(email_config.get('recipients', []))}")
        print(f"⏱️ Limite settimanale: {email_config.get('rate_limits', {}).get('weekly_limit', 10)} email")
    
    else:
        print("📧 Configurazione email non modificata")

# Test specifico per rate limiting email
async def test_email_rate_limiting():
    """Test specifico per il rate limiting delle email"""
    print("🧪 TEST RATE LIMITING EMAIL")
    print("="*30)
    
    # Crea agent con config di test
    agent = ETJCAMCPAgent()
    
    # Mostra tipo database
    print(f"🗄️  Database: {agent.email_manager.rate_limiter.db_manager.db_type}")
    
    # Configura un destinatario di test
    agent.config["email"]["enabled"] = True
    agent.config["email"]["recipients"] = ["test@example.com"]
    agent.config["email"]["rate_limits"]["weekly_limit"] = 3  # Limite basso per test
    agent.config["email"]["rate_limits"]["daily_limit"] = 2
    agent.config["email"]["rate_limits"]["hourly_limit"] = 1
    
    print("📧 Configurazione test:")
    print(f"  Limite settimanale: {agent.config['email']['rate_limits']['weekly_limit']}")
    print(f"  Limite giornaliero: {agent.config['email']['rate_limits']['daily_limit']}")
    print(f"  Limite orario: {agent.config['email']['rate_limits']['hourly_limit']}")
    
    # Test invio multiple email
    print("\n🔄 Test invio email multiple...")
    
    for i in range(5):
        priority = EmailPriority.MEDIUM if i < 3 else EmailPriority.CRITICAL
        
        result = await agent.send_smart_notification(
            subject=f"Test Email {i+1}",
            content=f"Contenuto email di test numero {i+1}",
            priority=priority,
            resource_uri=f"test://resource-{i+1}"
        )
        
        print(f"  Email {i+1} ({priority.value}): {result['queue_results']['sent']} inviata, {len([r for r in result['individual_results'] if r.get('status') == 'skipped'])} saltata")
    
    # Mostra statistiche finali
    stats = agent.get_email_statistics()
    recipient_stats = list(stats["recipient_statistics"].values())[0]
    limits_status = recipient_stats["current_limits_status"]
    
    print(f"\n📊 RISULTATI TEST:")
    print(f"  Database: {recipient_stats['database_type']}")
    print(f"  Email inviate oggi: {limits_status['daily']['count']}/{limits_status['daily']['limit']}")
    print(f"  Email inviate questa settimana: {limits_status['weekly']['count']}/{limits_status['weekly']['limit']}")
    print(f"  Email inviate quest'ora: {limits_status['hourly']['count']}/{limits_status['hourly']['limit']}")
    
    total_emails = recipient_stats["total_emails"]
    print(f"  Totale inviato: {total_emails.get('sent', 0)}")
    print(f"  Totale saltato: {total_emails.get('skipped', 0)}")
    
    print("\n✅ Test rate limiting completato!")

# Crea requirements.txt per Railway
def create_requirements_file():
    """Crea requirements.txt per Railway"""
    requirements = [
        "psycopg2-binary>=2.9.0",  # PostgreSQL adapter
        "asyncio",  # Async support
        "aiohttp",  # HTTP client (se necessario)
        "python-dotenv",  # Environment variables
    ]
    
    with open("requirements.txt", "w") as f:
        for req in requirements:
            f.write(req + "\n")
    
    print("✅ requirements.txt creato per Railway")
    print("📦 Dipendenze incluse:")
    for req in requirements:
        print(f"  - {req}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            setup_email_config()
        elif sys.argv[1] == "test-email":
            asyncio.run(test_email_rate_limiting())
        elif sys.argv[1] == "check-db":
            check_database_config()
        elif sys.argv[1] == "requirements":
            create_requirements_file()
        else:
            print("Comandi disponibili:")
            print("  python etjca_mcp_agent.py              # Test completo")
            print("  python etjca_mcp_agent.py config       # Configura email")
            print("  python etjca_mcp_agent.py test-email   # Test rate limiting")
            print("  python etjca_mcp_agent.py check-db     # Verifica database")
            print("  python etjca_mcp_agent.py requirements # Crea requirements.txt")
    else:
        asyncio.run(main())        print(f"\n📊 RISULTATI CICLO:")
        print(f"  • Risorse totali scoperte: {result['total_resources']}")
        print(f"  • Ottimizzazioni applicate: {result['total_optimizations']}")
        
        # Mostra statistiche email
        email_stats = dashboard.get("email_statistics", {})
        if email_stats.get("email_config", {}).get("enabled"):
            print(f"\n📧 STATISTICHE EMAIL:")
            queue = email_stats.get("queue_status", {})
            print(f"  • Coda email: {queue.get('queue_length', 0)} in attesa")
            
            config = email_stats.get("email_config", {})
            limits = config.get("rate_limits", {})
            print(f"  • Rate limits: {limits.get('weekly_limit', 'N/A')}/settimana, {limits.get('daily_limit', 'N/A')}/giorno")
            
            # Mostra stats per primo destinatario
            recipient_stats = email_stats.get("recipient_statistics", {})
            if recipient_stats:
                first_recipient = list(recipient_stats.keys())[0]
                stats = recipient_stats[first_recipient]
                current_limits = stats.get("current_limits_status", {})
                weekly = current_limits.get("weekly", {})
                print(f"  • Utilizzo settimana: {weekly.get('count', 0)}/{weekly.get('limit', 0)} email")
        else:
            print(f"\n📧 EMAIL: Disabilitate (configurare per attivare notifiche)")
        
        if result.get('#!/usr/bin/env python3
"""
ETJCA Cloud Agent con Model Context Protocol (MCP)
Agente AI nativo per gestione intelligente del cloud
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database imports - supporta sia PostgreSQL che SQLite
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

import sqlite3

# MCP Protocol Implementation
from abc import ABC, abstractmethod

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailPriority(Enum):
    """Livelli di priorità per le email"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class EmailNotification:
    """Rappresenta una notifica email"""
    id: str
    recipient: str
    subject: str
    content: str
    priority: EmailPriority
    created_at: datetime
    sent_at: Optional[datetime] = None
    status: str = "pending"  # pending, sent, failed, skipped
    resource_uri: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "recipient": self.recipient,
            "subject": self.subject,
            "content": self.content,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "status": self.status,
            "resource_uri": self.resource_uri
        }

class DatabaseManager:
    """Gestore database unificato per PostgreSQL e SQLite"""
    
    def __init__(self):
        self.db_type = self._detect_database_type()
        self.connection_params = self._get_connection_params()
        
        logger.info(f"🗄️  Database: {self.db_type}")
        self.init_database()
    
    def _detect_database_type(self) -> str:
        """Rileva il tipo di database da usare"""
        # Controlla se c'è DATABASE_URL (Railway PostgreSQL)
        if os.environ.get('DATABASE_URL') and POSTGRESQL_AVAILABLE:
            return "postgresql"
        
        # Controlla se c'è configurazione PostgreSQL manuale
        if (os.environ.get('POSTGRES_HOST') and 
            os.environ.get('POSTGRES_DB') and 
            POSTGRESQL_AVAILABLE):
            return "postgresql"
        
        # Fallback a SQLite
        return "sqlite"
    
    def _get_connection_params(self) -> Dict:
        """Ottiene parametri di connessione per il database"""
        if self.db_type == "postgresql":
            # Railway format: postgres://user:password@host:port/dbname
            database_url = os.environ.get('DATABASE_URL')
            if database_url:
                return {"database_url": database_url}
            
            # Configurazione manuale
            return {
                "host": os.environ.get('POSTGRES_HOST', 'localhost'),
                "database": os.environ.get('POSTGRES_DB', 'etjca'),
                "user": os.environ.get('POSTGRES_USER', 'postgres'),
                "password": os.environ.get('POSTGRES_PASSWORD', ''),
                "port": int(os.environ.get('POSTGRES_PORT', '5432'))
            }
        
        # SQLite
        return {"database_path": "etjca_mcp.db"}
    
    def get_connection(self):
        """Ottiene una connessione al database"""
        if self.db_type == "postgresql":
            if "database_url" in self.connection_params:
                return psycopg2.connect(
                    self.connection_params["database_url"],
                    cursor_factory=RealDictCursor
                )
            else:
                return psycopg2.connect(
                    host=self.connection_params["host"],
                    database=self.connection_params["database"],
                    user=self.connection_params["user"],
                    password=self.connection_params["password"],
                    port=self.connection_params["port"],
                    cursor_factory=RealDictCursor
                )
        else:
            conn = sqlite3.connect(self.connection_params["database_path"])
            conn.row_factory = sqlite3.Row
            return conn
    
    def init_database(self):
        """Inizializza le tabelle del database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if self.db_type == "postgresql":
                # Tabelle PostgreSQL
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS email_log (
                        id VARCHAR(255) PRIMARY KEY,
                        recipient VARCHAR(255) NOT NULL,
                        subject TEXT NOT NULL,
                        content TEXT NOT NULL,
                        priority VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        sent_at TIMESTAMP,
                        status VARCHAR(50) NOT NULL,
                        resource_uri TEXT,
                        week_key VARCHAR(20) NOT NULL,
                        day_key VARCHAR(20) NOT NULL,
                        hour_key VARCHAR(20) NOT NULL
                    )
                ''')
                
                # Indici PostgreSQL
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_email_week 
                    ON email_log(week_key, recipient)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_email_day 
                    ON email_log(day_key, recipient)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_email_hour 
                    ON email_log(hour_key, recipient)
                ''')
                
                # Tabella risorse MCP
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mcp_resources (
                        uri VARCHAR(500) PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        mime_type VARCHAR(100),
                        resource_type VARCHAR(100),
                        metadata JSONB,
                        last_updated TIMESTAMP NOT NULL
                    )
                ''')
                
                # Tabella messaggi MCP
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mcp_messages (
                        id VARCHAR(255) PRIMARY KEY,
                        message_type VARCHAR(50) NOT NULL,
                        method VARCHAR(100) NOT NULL,
                        params JSONB,
                        timestamp TIMESTAMP NOT NULL,
                        source VARCHAR(100),
                        target VARCHAR(100)
                    )
                ''')
                
            else:
                # Tabelle SQLite (come prima)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS email_log (
                        id TEXT PRIMARY KEY,
                        recipient TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        content TEXT NOT NULL,
                        priority TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        sent_at TEXT,
                        status TEXT NOT NULL,
                        resource_uri TEXT,
                        week_key TEXT NOT NULL,
                        day_key TEXT NOT NULL,
                        hour_key TEXT NOT NULL
                    )
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_email_week 
                    ON email_log(week_key, recipient)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_email_day 
                    ON email_log(day_key, recipient)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_email_hour 
                    ON email_log(hour_key, recipient)
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mcp_resources (
                        uri TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        mime_type TEXT,
                        resource_type TEXT,
                        metadata TEXT,
                        last_updated TEXT NOT NULL
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mcp_messages (
                        id TEXT PRIMARY KEY,
                        message_type TEXT NOT NULL,
                        method TEXT NOT NULL,
                        params TEXT,
                        timestamp TEXT NOT NULL,
                        source TEXT,
                        target TEXT
                    )
                ''')
            
            conn.commit()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """Esegue una query con gestione unificata"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                return cursor.fetchall()
            
            conn.commit()
            return cursor.rowcount

class EmailRateLimiter:
    """Gestore del rate limiting per le email con supporto multi-database"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        
        # Configurazione rate limits
        self.limits = {
            "weekly_limit": 10,  # Massimo 10 email a settimana
            "daily_limit": 3,    # Massimo 3 email al giorno
            "hourly_limit": 1,   # Massimo 1 email all'ora
            "critical_bypass": True  # Le email critiche bypassano i limiti
        }
    
    def init_database(self):
        """Database già inizializzato dal DatabaseManager"""
        pass
    
    def _get_time_keys(self, dt: datetime) -> tuple:
        """Genera chiavi temporali per rate limiting"""
        # Chiave settimana (anno-settimana)
        year, week, _ = dt.isocalendar()
        week_key = f"{year}-W{week:02d}"
        
        # Chiave giorno
        day_key = dt.strftime("%Y-%m-%d")
        
        # Chiave ora
        hour_key = dt.strftime("%Y-%m-%d-%H")
        
        return week_key, day_key, hour_key
    
    def check_rate_limit(self, recipient: str, priority: EmailPriority) -> Dict[str, Any]:
        """Controlla se l'email può essere inviata rispettando i rate limits"""
        now = datetime.now()
        week_key, day_key, hour_key = self._get_time_keys(now)
        
        # Le email critiche bypassano sempre i limiti
        if priority == EmailPriority.CRITICAL and self.limits["critical_bypass"]:
            return {
                "allowed": True,
                "reason": "critical_bypass",
                "limits_status": self._get_limits_status(recipient, week_key, day_key, hour_key)
            }
        
        # Conta email inviate nei vari periodi
        weekly_count = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM email_log WHERE recipient = %s AND week_key = %s AND status = 'sent'" 
            if self.db_manager.db_type == "postgresql" else
            "SELECT COUNT(*) FROM email_log WHERE recipient = ? AND week_key = ? AND status = 'sent'",
            (recipient, week_key),
            fetch=True
        )[0][0]
        
        daily_count = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM email_log WHERE recipient = %s AND day_key = %s AND status = 'sent'"
            if self.db_manager.db_type == "postgresql" else
            "SELECT COUNT(*) FROM email_log WHERE recipient = ? AND day_key = ? AND status = 'sent'",
            (recipient, day_key),
            fetch=True
        )[0][0]
        
        hourly_count = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM email_log WHERE recipient = %s AND hour_key = %s AND status = 'sent'"
            if self.db_manager.db_type == "postgresql" else
            "SELECT COUNT(*) FROM email_log WHERE recipient = ? AND hour_key = ? AND status = 'sent'",
            (recipient, hour_key),
            fetch=True
        )[0][0]
        
        # Controlla limiti
        limits_status = {
            "weekly": {"count": weekly_count, "limit": self.limits["weekly_limit"]},
            "daily": {"count": daily_count, "limit": self.limits["daily_limit"]},
            "hourly": {"count": hourly_count, "limit": self.limits["hourly_limit"]}
        }
        
        # Verifica se qualche limite è superato
        if weekly_count >= self.limits["weekly_limit"]:
            return {
                "allowed": False,
                "reason": "weekly_limit_exceeded",
                "limits_status": limits_status
            }
        
        if daily_count >= self.limits["daily_limit"]:
            return {
                "allowed": False,
                "reason": "daily_limit_exceeded",
                "limits_status": limits_status
            }
        
        if hourly_count >= self.limits["hourly_limit"]:
            return {
                "allowed": False,
                "reason": "hourly_limit_exceeded",
                "limits_status": limits_status
            }
        
        return {
            "allowed": True,
            "reason": "within_limits",
            "limits_status": limits_status
        }
    
    def _get_limits_status(self, recipient: str, week_key: str, day_key: str, hour_key: str) -> Dict:
        """Ottiene lo stato attuale dei limiti"""
        weekly_count = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM email_log WHERE recipient = %s AND week_key = %s AND status = 'sent'"
            if self.db_manager.db_type == "postgresql" else
            "SELECT COUNT(*) FROM email_log WHERE recipient = ? AND week_key = ? AND status = 'sent'",
            (recipient, week_key),
            fetch=True
        )[0][0]
        
        daily_count = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM email_log WHERE recipient = %s AND day_key = %s AND status = 'sent'"
            if self.db_manager.db_type == "postgresql" else
            "SELECT COUNT(*) FROM email_log WHERE recipient = ? AND day_key = ? AND status = 'sent'",
            (recipient, day_key),
            fetch=True
        )[0][0]
        
        hourly_count = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM email_log WHERE recipient = %s AND hour_key = %s AND status = 'sent'"
            if self.db_manager.db_type == "postgresql" else
            "SELECT COUNT(*) FROM email_log WHERE recipient = ? AND hour_key = ? AND status = 'sent'",
            (recipient, hour_key),
            fetch=True
        )[0][0]
        
        return {
            "weekly": {"count": weekly_count, "limit": self.limits["weekly_limit"]},
            "daily": {"count": daily_count, "limit": self.limits["daily_limit"]},
            "hourly": {"count": hourly_count, "limit": self.limits["hourly_limit"]}
        }
    
    def log_email(self, email: EmailNotification) -> bool:
        """Registra l'email nel database"""
        week_key, day_key, hour_key = self._get_time_keys(email.created_at)
        
        if self.db_manager.db_type == "postgresql":
            query = '''
                INSERT INTO email_log 
                (id, recipient, subject, content, priority, created_at, sent_at, 
                 status, resource_uri, week_key, day_key, hour_key)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    sent_at = EXCLUDED.sent_at,
                    status = EXCLUDED.status
            '''
            params = (
                email.id, email.recipient, email.subject, email.content,
                email.priority.value, email.created_at,
                email.sent_at if email.sent_at else None,
                email.status, email.resource_uri,
                week_key, day_key, hour_key
            )
        else:
            query = '''
                INSERT OR REPLACE INTO email_log 
                (id, recipient, subject, content, priority, created_at, sent_at, 
                 status, resource_uri, week_key, day_key, hour_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                email.id, email.recipient, email.subject, email.content,
                email.priority.value, email.created_at.isoformat(),
                email.sent_at.isoformat() if email.sent_at else None,
                email.status, email.resource_uri,
                week_key, day_key, hour_key
            )
        
        self.db_manager.execute_query(query, params)
        return True
    
    def get_email_statistics(self, recipient: str) -> Dict:
        """Ottiene statistiche dettagliate delle email"""
        now = datetime.now()
        week_key, day_key, hour_key = self._get_time_keys(now)
        
        # Statistiche generali
        status_counts = {}
        if self.db_manager.db_type == "postgresql":
            results = self.db_manager.execute_query(
                "SELECT status, COUNT(*) FROM email_log WHERE recipient = %s GROUP BY status",
                (recipient,),
                fetch=True
            )
        else:
            results = self.db_manager.execute_query(
                "SELECT status, COUNT(*) FROM email_log WHERE recipient = ? GROUP BY status",
                (recipient,),
                fetch=True
            )
        
        for row in results:
            status_counts[row[0]] = row[1]
        
        # Email per priorità questa settimana
        priority_counts = {}
        if self.db_manager.db_type == "postgresql":
            results = self.db_manager.execute_query(
                "SELECT priority, COUNT(*) FROM email_log WHERE recipient = %s AND week_key = %s GROUP BY priority",
                (recipient, week_key),
                fetch=True
            )
        else:
            results = self.db_manager.execute_query(
                "SELECT priority, COUNT(*) FROM email_log WHERE recipient = ? AND week_key = ? GROUP BY priority",
                (recipient, week_key),
                fetch=True
            )
        
        for row in results:
            priority_counts[row[0]] = row[1]
        
        # Ultime email inviate
        if self.db_manager.db_type == "postgresql":
            recent_results = self.db_manager.execute_query(
                "SELECT subject, priority, sent_at, status FROM email_log WHERE recipient = %s ORDER BY created_at DESC LIMIT 5",
                (recipient,),
                fetch=True
            )
        else:
            recent_results = self.db_manager.execute_query(
                "SELECT subject, priority, sent_at, status FROM email_log WHERE recipient = ? ORDER BY created_at DESC LIMIT 5",
                (recipient,),
                fetch=True
            )
        
        recent_emails = [
            {
                "subject": row[0],
                "priority": row[1],
                "sent_at": row[2],
                "status": row[3]
            }
            for row in recent_results
        ]
        
        return {
            "recipient": recipient,
            "database_type": self.db_manager.db_type,
            "limits": self.limits,
            "current_limits_status": self._get_limits_status(recipient, week_key, day_key, hour_key),
            "total_emails": status_counts,
            "this_week_by_priority": priority_counts,
            "recent_emails": recent_emails
        }

class EmailNotificationManager:
    """Gestore intelligente delle notifiche email con rate limiting"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.rate_limiter = EmailRateLimiter()
        self.email_queue = []
        self.smtp_config = config.get("email", {})
        
        logger.info("📧 Email Manager inizializzato con rate limiting")
    
    async def queue_notification(self, recipient: str, subject: str, content: str, 
                                priority: EmailPriority, resource_uri: str = None) -> Dict:
        """Aggiunge una notifica alla coda con controllo rate limiting"""
        
        # Crea notifica
        notification = EmailNotification(
            id=f"email-{uuid.uuid4().hex[:8]}",
            recipient=recipient,
            subject=subject,
            content=content,
            priority=priority,
            created_at=datetime.now(),
            resource_uri=resource_uri
        )
        
        # Controlla rate limiting
        rate_check = self.rate_limiter.check_rate_limit(recipient, priority)
        
        if rate_check["allowed"]:
            # Aggiungi alla coda
            self.email_queue.append(notification)
            logger.info(f"📧 Email accodata: {subject} (Priorità: {priority.value})")
            
            return {
                "status": "queued",
                "notification_id": notification.id,
                "rate_check": rate_check
            }
        else:
            # Rate limit superato - segna come skipped
            notification.status = "skipped"
            self.rate_limiter.log_email(notification)
            
            logger.warning(f"⚠️ Email saltata per rate limiting: {rate_check['reason']}")
            
            return {
                "status": "skipped",
                "notification_id": notification.id,
                "rate_check": rate_check,
                "reason": rate_check["reason"]
            }
    
    async def process_email_queue(self) -> Dict:
        """Processa la coda delle email"""
        if not self.email_queue:
            return {"processed": 0, "sent": 0, "failed": 0}
        
        results = {"processed": 0, "sent": 0, "failed": 0}
        
        # Ordina per priorità (critiche prima)
        priority_order = {
            EmailPriority.CRITICAL: 4,
            EmailPriority.HIGH: 3,
            EmailPriority.MEDIUM: 2,
            EmailPriority.LOW: 1
        }
        
        sorted_queue = sorted(
            self.email_queue, 
            key=lambda x: priority_order[x.priority], 
            reverse=True
        )
        
        for notification in sorted_queue:
            results["processed"] += 1
            
            try:
                # Invia email (simulato o reale)
                if self.smtp_config.get("enabled", False):
                    success = await self._send_real_email(notification)
                else:
                    success = await self._simulate_email_send(notification)
                
                if success:
                    notification.status = "sent"
                    notification.sent_at = datetime.now()
                    results["sent"] += 1
                    logger.info(f"✅ Email inviata: {notification.subject}")
                else:
                    notification.status = "failed"
                    results["failed"] += 1
                    logger.error(f"❌ Invio email fallito: {notification.subject}")
                
            except Exception as e:
                notification.status = "failed"
                results["failed"] += 1
                logger.error(f"❌ Errore invio email: {e}")
            
            # Registra nel database
            self.rate_limiter.log_email(notification)
        
        # Svuota la coda
        self.email_queue.clear()
        
        return results
    
    async def _simulate_email_send(self, notification: EmailNotification) -> bool:
        """Simula l'invio di un'email"""
        await asyncio.sleep(0.1)  # Simula latenza
        return True  # Simulazione sempre success
    
    async def _send_real_email(self, notification: EmailNotification) -> bool:
        """Invia email reale tramite SMTP"""
        try:
            smtp_host = self.smtp_config.get("smtp_host", "smtp.gmail.com")
            smtp_port = self.smtp_config.get("smtp_port", 587)
            username = self.smtp_config.get("username")
            password = self.smtp_config.get("password")
            
            if not username or not password:
                logger.warning("Credenziali SMTP non configurate")
                return False
            
            # Crea messaggio
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = notification.recipient
            msg['Subject'] = f"[ETJCA-{notification.priority.value.upper()}] {notification.subject}"
            
            # Contenuto HTML migliorato
            html_content = f"""
            <html>
            <body>
                <h2>🚀 ETJCA Cloud Agent Notification</h2>
                <p><strong>Priorità:</strong> {notification.priority.value.upper()}</p>
                <p><strong>Timestamp:</strong> {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                {f'<p><strong>Risorsa:</strong> {notification.resource_uri}</p>' if notification.resource_uri else ''}
                <hr>
                <div>
                    {notification.content.replace('\n', '<br>')}
                </div>
                <hr>
                <p><small>Inviato automaticamente da ETJCA MCP Agent</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Invia email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logger.error(f"Errore invio email SMTP: {e}")
            return False
    
    def get_queue_status(self) -> Dict:
        """Ritorna lo stato della coda email"""
        priority_counts = {}
        for notification in self.email_queue:
            priority = notification.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        return {
            "queue_length": len(self.email_queue),
            "by_priority": priority_counts,
            "rate_limiter_status": "active"
        }
    """Tipi di messaggi MCP"""
    INITIALIZE = "initialize"
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"

class MCPResourceType(Enum):
    """Tipi di risorse MCP"""
    CLOUD_INSTANCE = "cloud_instance"
    DATABASE = "database"
    STORAGE = "storage"
    NETWORK = "network"
    MONITORING = "monitoring"

@dataclass
class MCPMessage:
    """Messaggio del Model Context Protocol"""
    id: str
    type: MCPMessageType
    method: str
    params: Dict[str, Any]
    timestamp: datetime
    source: str
    target: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "target": self.target
        }

@dataclass
class MCPResource:
    """Risorsa gestita tramite MCP"""
    uri: str
    name: str
    description: str
    mime_type: str
    resource_type: MCPResourceType
    metadata: Dict[str, Any]
    last_updated: datetime
    
    def to_dict(self) -> Dict:
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type,
            "type": self.resource_type.value,
            "metadata": self.metadata,
            "lastUpdated": self.last_updated.isoformat()
        }

class MCPServer(ABC):
    """Interfaccia base per server MCP"""
    
    @abstractmethod
    async def handle_request(self, message: MCPMessage) -> MCPMessage:
        """Gestisce una richiesta MCP"""
        pass
    
    @abstractmethod
    async def list_resources(self) -> List[MCPResource]:
        """Lista le risorse disponibili"""
        pass
    
    @abstractmethod
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Legge una risorsa specifica"""
        pass

class CloudMCPServer(MCPServer):
    """Server MCP per risorse cloud"""
    
    def __init__(self, provider: str, config: Dict):
        self.provider = provider
        self.config = config
        self.resources = {}
        self.tools = self._init_tools()
    
    def _init_tools(self) -> Dict[str, Dict]:
        """Inizializza gli strumenti MCP disponibili"""
        return {
            "etjca_discover": {
                "description": "Scopre risorse cloud automaticamente",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "provider": {"type": "string"},
                        "region": {"type": "string"},
                        "resource_types": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            "email": {
                "enabled": False,  # Disabilitato di default per sicurezza
                "smtp_host": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",  # Da configurare
                "password": "",  # Da configurare (usa app password)
                "recipients": [],  # Lista email destinatari
                "rate_limits": {
                    "weekly_limit": 10,
                    "daily_limit": 3,
                    "hourly_limit": 1,
                    "critical_bypass": True
                }
            },
            "etjca_analyze": {
                "description": "Analizza utilizzo e performance delle risorse",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource_uri": {"type": "string"},
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "time_range": {"type": "string"}
                    }
                }
            },
            "etjca_optimize": {
                "description": "Ottimizza automaticamente le risorse cloud",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource_uri": {"type": "string"},
                        "optimization_type": {
                            "type": "string",
                            "enum": ["cost", "performance", "availability"]
                        },
                        "constraints": {"type": "object"}
                    }
                }
            },
            "etjca_scale": {
                "description": "Scala automaticamente le risorse",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource_uri": {"type": "string"},
                        "scale_direction": {
                            "type": "string",
                            "enum": ["up", "down", "auto"]
                        },
                        "scale_factor": {"type": "number"}
                    }
                }
            },
            "etjca_monitor": {
                "description": "Configura monitoraggio intelligente",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource_uri": {"type": "string"},
                        "alerts": {"type": "array"},
                        "thresholds": {"type": "object"}
                    }
                }
            }
        }
    
    async def handle_request(self, message: MCPMessage) -> MCPMessage:
        """Gestisce richieste MCP per risorse cloud"""
        try:
            method = message.method
            params = message.params
            
            if method == "tools/list":
                return self._create_response(message, {"tools": list(self.tools.values())})
            
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result = await self._execute_tool(tool_name, tool_args)
                return self._create_response(message, {"result": result})
            
            elif method == "resources/list":
                resources = await self.list_resources()
                return self._create_response(message, {
                    "resources": [r.to_dict() for r in resources]
                })
            
            elif method == "resources/read":
                uri = params.get("uri")
                content = await self.read_resource(uri)
                return self._create_response(message, {"contents": [content]})
            
            else:
                raise ValueError(f"Metodo non supportato: {method}")
                
        except Exception as e:
            return self._create_error_response(message, str(e))
    
    async def _execute_tool(self, tool_name: str, args: Dict) -> Dict:
        """Esegue uno strumento ETJCA"""
        if tool_name == "etjca_discover":
            return await self._discover_resources(args)
        elif tool_name == "etjca_analyze":
            return await self._analyze_resource(args)
        elif tool_name == "etjca_optimize":
            return await self._optimize_resource(args)
        elif tool_name == "etjca_scale":
            return await self._scale_resource(args)
        elif tool_name == "etjca_monitor":
            return await self._setup_monitoring(args)
        else:
            raise ValueError(f"Strumento non riconosciuto: {tool_name}")
    
    async def _discover_resources(self, args: Dict) -> Dict:
        """Scopre risorse cloud tramite MCP"""
        provider = args.get("provider", self.provider)
        region = args.get("region", "us-east-1")
        resource_types = args.get("resource_types", ["instances", "storage", "databases"])
        
        # Simulazione discovery intelligente
        discovered = []
        import random
        
        for resource_type in resource_types:
            for i in range(random.randint(1, 3)):
                resource_id = f"{provider}-{resource_type}-{uuid.uuid4().hex[:8]}"
                resource = MCPResource(
                    uri=f"cloud://{provider}/{region}/{resource_type}/{resource_id}",
                    name=f"{resource_type.title()} {i+1}",
                    description=f"Risorsa {resource_type} su {provider}",
                    mime_type="application/json",
                    resource_type=MCPResourceType.CLOUD_INSTANCE,
                    metadata={
                        "provider": provider,
                        "region": region,
                        "type": resource_type,
                        "cpu_usage": random.uniform(20.0, 95.0),
                        "memory_usage": random.uniform(30.0, 90.0),
                        "cost_per_hour": random.uniform(0.05, 0.20),
                        "status": "running"
                    },
                    last_updated=datetime.now()
                )
                self.resources[resource.uri] = resource
                discovered.append(resource.to_dict())
        
        return {
            "discovered_count": len(discovered),
            "resources": discovered,
            "provider": provider,
            "region": region
        }
    
    async def _analyze_resource(self, args: Dict) -> Dict:
        """Analizza una risorsa tramite MCP"""
        uri = args.get("resource_uri")
        metrics = args.get("metrics", ["cpu", "memory", "network"])
        
        if uri not in self.resources:
            raise ValueError(f"Risorsa non trovata: {uri}")
        
        resource = self.resources[uri]
        analysis = {
            "resource_uri": uri,
            "analysis_timestamp": datetime.now().isoformat(),
            "metrics": {},
            "recommendations": [],
            "risk_level": "low"
        }
        
        # Analisi intelligente basata sui metadata
        metadata = resource.metadata
        cpu_usage = metadata.get("cpu_usage", 0)
        memory_usage = metadata.get("memory_usage", 0)
        
        analysis["metrics"] = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "efficiency_score": 100 - max(cpu_usage, memory_usage),
            "cost_optimization_potential": max(0, 80 - cpu_usage) * 0.01
        }
        
        # Raccomandazioni intelligenti
        if cpu_usage > 90:
            analysis["recommendations"].append({
                "type": "scale_up",
                "priority": "high",
                "description": "CPU utilizzo critico - scala immediatamente",
                "estimated_cost_impact": metadata.get("cost_per_hour", 0) * 0.5
            })
            analysis["risk_level"] = "high"
        elif cpu_usage < 30:
            analysis["recommendations"].append({
                "type": "scale_down",
                "priority": "medium",
                "description": "CPU sottoutilizzato - considera riduzione",
                "estimated_cost_saving": metadata.get("cost_per_hour", 0) * 0.3
            })
        
        if memory_usage > 85:
            analysis["recommendations"].append({
                "type": "memory_optimization",
                "priority": "high",
                "description": "Memoria critica - ottimizzazione necessaria"
            })
        
        return analysis
    
    async def _optimize_resource(self, args: Dict) -> Dict:
        """Ottimizza una risorsa tramite MCP"""
        uri = args.get("resource_uri")
        optimization_type = args.get("optimization_type", "cost")
        
        if uri not in self.resources:
            raise ValueError(f"Risorsa non trovata: {uri}")
        
        # Simula ottimizzazione
        await asyncio.sleep(1)  # Simula tempo di elaborazione
        
        optimization_result = {
            "resource_uri": uri,
            "optimization_type": optimization_type,
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "changes_applied": [],
            "metrics_improvement": {}
        }
        
        if optimization_type == "cost":
            optimization_result["changes_applied"] = [
                "Resized instance to optimal size",
                "Configured auto-scaling policies",
                "Optimized storage allocation"
            ]
            optimization_result["metrics_improvement"] = {
                "cost_reduction": "25%",
                "efficiency_gain": "15%"
            }
        elif optimization_type == "performance":
            optimization_result["changes_applied"] = [
                "Upgraded instance type",
                "Optimized memory allocation",
                "Enhanced network configuration"
            ]
            optimization_result["metrics_improvement"] = {
                "performance_gain": "30%",
                "response_time_improvement": "40%"
            }
        
        return optimization_result
    
    async def _scale_resource(self, args: Dict) -> Dict:
        """Scala una risorsa tramite MCP"""
        uri = args.get("resource_uri")
        direction = args.get("scale_direction", "auto")
        factor = args.get("scale_factor", 1.5)
        
        if uri not in self.resources:
            raise ValueError(f"Risorsa non trovata: {uri}")
        
        resource = self.resources[uri]
        
        # Simula scaling
        await asyncio.sleep(2)  # Simula tempo di scaling
        
        return {
            "resource_uri": uri,
            "scale_direction": direction,
            "scale_factor": factor,
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "new_capacity": f"{int(100 * factor)}%",
            "estimated_cost_change": resource.metadata.get("cost_per_hour", 0) * (factor - 1)
        }
    
    async def _setup_monitoring(self, args: Dict) -> Dict:
        """Configura monitoraggio tramite MCP"""
        uri = args.get("resource_uri")
        alerts = args.get("alerts", [])
        thresholds = args.get("thresholds", {})
        
        return {
            "resource_uri": uri,
            "monitoring_status": "active",
            "alerts_configured": len(alerts),
            "thresholds": thresholds,
            "monitoring_id": f"monitor-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat()
        }
    
    async def list_resources(self) -> List[MCPResource]:
        """Lista tutte le risorse disponibili"""
        return list(self.resources.values())
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Legge i dettagli di una risorsa"""
        if uri not in self.resources:
            raise ValueError(f"Risorsa non trovata: {uri}")
        
        resource = self.resources[uri]
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(resource.to_dict(), indent=2)
        }
    
    def _create_response(self, request: MCPMessage, result: Dict) -> MCPMessage:
        """Crea una risposta MCP"""
        return MCPMessage(
            id=uuid.uuid4().hex,
            type=MCPMessageType.RESPONSE,
            method="response",
            params={
                "id": request.id,
                "result": result
            },
            timestamp=datetime.now(),
            source=f"etjca-{self.provider}",
            target=request.source
        )
    
    def _create_error_response(self, request: MCPMessage, error: str) -> MCPMessage:
        """Crea una risposta di errore MCP"""
        return MCPMessage(
            id=uuid.uuid4().hex,
            type=MCPMessageType.ERROR,
            method="error",
            params={
                "id": request.id,
                "error": {
                    "code": -1,
                    "message": error
                }
            },
            timestamp=datetime.now(),
            source=f"etjca-{self.provider}",
            target=request.source
        )

class ETJCAMCPAgent:
    """Agente ETJCA basato su Model Context Protocol"""
    
    def __init__(self, config_path: str = "etjca_mcp_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.servers = {}
        self.message_history = []
        self.running = False
        
        # Inizializza il gestore email con rate limiting
        self.email_manager = EmailNotificationManager(self.config)
        
        self._init_mcp_servers()
        logger.info("🚀 ETJCA MCP Agent inizializzato")
        logger.info(f"📧 Rate limiting email: {self.config['email']['rate_limits']['weekly_limit']}/settimana")
    
    def load_config(self) -> Dict:
        """Carica la configurazione MCP"""
        default_config = {
            "mcp_version": "0.1.0",
            "agent_name": "ETJCA-MCP-Agent",
            "providers": {
                "aws": {
                    "enabled": True,
                    "regions": ["us-east-1", "eu-west-1"],
                    "endpoint": "mcp://aws.cloud.etjca.com"
                },
                "azure": {
                    "enabled": True,
                    "regions": ["eastus", "westeurope"],
                    "endpoint": "mcp://azure.cloud.etjca.com"
                },
                "gcp": {
                    "enabled": True,
                    "regions": ["us-central1", "europe-west1"],
                    "endpoint": "mcp://gcp.cloud.etjca.com"
                }
            },
            "monitoring": {
                "auto_discovery_interval": 300,
                "auto_optimization": True,
                "alert_thresholds": {
                    "cpu_critical": 90,
                    "memory_critical": 85,
                    "cost_threshold": 100.0
                }
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                logger.warning(f"Errore nel caricamento config MCP: {e}")
        
        # Salva config di default
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict = None):
        """Salva la configurazione MCP"""
        config_to_save = config or self.config
        with open(self.config_path, 'w') as f:
            json.dump(config_to_save, f, indent=2)
    
    def _init_mcp_servers(self):
        """Inizializza i server MCP per ogni provider"""
        for provider_name, provider_config in self.config["providers"].items():
            if provider_config.get("enabled", False):
                self.servers[provider_name] = CloudMCPServer(
                    provider_name, 
                    provider_config
                )
                logger.info(f"📡 Server MCP {provider_name} inizializzato")
    
    async def send_mcp_request(self, provider: str, method: str, params: Dict) -> Dict:
        """Invia una richiesta MCP a un provider"""
        if provider not in self.servers:
            raise ValueError(f"Provider {provider} non configurato")
        
        server = self.servers[provider]
        
        # Crea messaggio MCP
        request = MCPMessage(
            id=uuid.uuid4().hex,
            type=MCPMessageType.REQUEST,
            method=method,
            params=params,
            timestamp=datetime.now(),
            source="etjca-agent",
            target=provider
        )
        
        # Salva nella cronologia
        self.message_history.append(request)
        
        # Invia richiesta
        response = await server.handle_request(request)
        self.message_history.append(response)
        
        return response.params.get("result", {})
    
    async def discover_all_resources(self) -> Dict:
        """Scopre tutte le risorse da tutti i provider tramite MCP"""
        all_resources = {}
        
        for provider_name in self.servers.keys():
            try:
                result = await self.send_mcp_request(
                    provider_name,
                    "tools/call",
                    {
                        "name": "etjca_discover",
                        "arguments": {
                            "provider": provider_name,
                            "resource_types": ["instances", "databases", "storage"]
                        }
                    }
                )
                all_resources[provider_name] = result
                logger.info(f"📊 {provider_name}: {result.get('discovered_count', 0)} risorse")
                
            except Exception as e:
                logger.error(f"Errore discovery {provider_name}: {e}")
        
        return all_resources
    
    async def analyze_all_resources(self) -> Dict:
        """Analizza tutte le risorse scoperte"""
        analysis_results = {}
        
        for provider_name, server in self.servers.items():
            try:
                resources = await server.list_resources()
                provider_analysis = []
                
                for resource in resources:
                    analysis = await self.send_mcp_request(
                        provider_name,
                        "tools/call",
                        {
                            "name": "etjca_analyze",
                            "arguments": {
                                "resource_uri": resource.uri,
                                "metrics": ["cpu", "memory", "cost"]
                            }
                        }
                    )
                    provider_analysis.append(analysis)
                
                analysis_results[provider_name] = provider_analysis
                
            except Exception as e:
                logger.error(f"Errore analisi {provider_name}: {e}")
        
        return analysis_results
    
    async def send_smart_notification(self, subject: str, content: str, 
                                     priority: EmailPriority, resource_uri: str = None) -> Dict:
        """Invia notifiche intelligenti con rate limiting"""
        recipients = self.config.get("email", {}).get("recipients", [])
        
        if not recipients:
            logger.warning("📧 Nessun destinatario email configurato")
            return {"status": "no_recipients", "notifications_sent": 0}
        
        results = []
        
        for recipient in recipients:
            result = await self.email_manager.queue_notification(
                recipient=recipient,
                subject=subject,
                content=content,
                priority=priority,
                resource_uri=resource_uri
            )
            results.append({
                "recipient": recipient,
                **result
            })
        
        # Processa la coda email
        queue_results = await self.email_manager.process_email_queue()
        
        return {
            "status": "processed",
            "recipients_processed": len(recipients),
            "queue_results": queue_results,
            "individual_results": results
        }
    
    async def send_critical_alert(self, resource_uri: str, alert_message: str) -> Dict:
        """Invia alert critico bypassando alcuni rate limits"""
        return await self.send_smart_notification(
            subject=f"🚨 ALERT CRITICO - Risorsa {resource_uri}",
            content=f"""
ALERT CRITICO RILEVATO:

Risorsa: {resource_uri}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Dettagli:
{alert_message}

Azione richiesta: Verificare immediatamente la risorsa.

---
ETJCA MCP Agent
            """,
            priority=EmailPriority.CRITICAL,
            resource_uri=resource_uri
        )
    
    async def send_optimization_report(self, optimization_results: Dict) -> Dict:
        """Invia report di ottimizzazione"""
        total_optimizations = sum(len(opts) for opts in optimization_results.values())
        
        content = f"""
REPORT OTTIMIZZAZIONI ETJCA

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Ottimizzazioni applicate: {total_optimizations}

"""
        
        for provider, optimizations in optimization_results.items():
            if optimizations:
                content += f"\n🔧 {provider.upper()}:\n"
                for opt in optimizations:
                    content += f"  • {opt.get('optimization_type', 'N/A')}: {opt.get('status', 'N/A')}\n"
        
        content += "\n---\nETJCA MCP Agent"
        
        return await self.send_smart_notification(
            subject=f"📊 Report Ottimizzazioni - {total_optimizations} completate",
            content=content,
            priority=EmailPriority.MEDIUM
        )
        """Ottimizzazione automatica basata su MCP"""
        optimization_results = {}
        
        # Prima analizza tutte le risorse
        analysis_results = await self.analyze_all_resources()
        
        for provider_name, analyses in analysis_results.items():
            provider_optimizations = []
            
            for analysis in analyses:
                recommendations = analysis.get("recommendations", [])
                
                for rec in recommendations:
                    if rec.get("priority") in ["high", "critical"]:
                        try:
                            # Esegui ottimizzazione automatica
                            optimization = await self.send_mcp_request(
                                provider_name,
                                "tools/call",
                                {
                                    "name": "etjca_optimize",
                                    "arguments": {
                                        "resource_uri": analysis["resource_uri"],
                                        "optimization_type": rec["type"].replace("_", "")
                                    }
                                }
                            )
                            provider_optimizations.append(optimization)
                            
                        except Exception as e:
                            logger.error(f"Errore ottimizzazione: {e}")
            
            optimization_results[provider_name] = provider_optimizations
        
        return optimization_results
    
    async def _check_critical_alerts(self, analysis_results: Dict):
        """Controlla e invia alert per situazioni critiche"""
        thresholds = self.config.get("monitoring", {}).get("alert_thresholds", {})
        
        for provider_name, analyses in analysis_results.items():
            for analysis in analyses:
                metrics = analysis.get("metrics", {})
                resource_uri = analysis.get("resource_uri")
                
                # Controlla CPU critico
                cpu_usage = metrics.get("cpu_usage", 0)
                if cpu_usage > thresholds.get("cpu_critical", 90):
                    await self.send_critical_alert(
                        resource_uri,
                        f"CPU utilizzo critico: {cpu_usage:.1f}% (soglia: {thresholds.get('cpu_critical', 90)}%)"
                    )
                
                # Controlla memoria critica
                memory_usage = metrics.get("memory_usage", 0)
                if memory_usage > thresholds.get("memory_critical", 85):
                    await self.send_critical_alert(
                        resource_uri,
                        f"Memoria utilizzo critico: {memory_usage:.1f}% (soglia: {thresholds.get('memory_critical', 85)}%)"
                    )
    
    def get_email_statistics(self) -> Dict:
        """Ottiene statistiche complete delle email"""
        recipients = self.config.get("email", {}).get("recipients", [])
        
        if not recipients:
            return {"status": "no_recipients_configured"}
        
        all_stats = {}
        for recipient in recipients:
            all_stats[recipient] = self.email_manager.rate_limiter.get_email_statistics(recipient)
        
        return {
            "email_config": {
                "enabled": self.config.get("email", {}).get("enabled", False),
                "recipients_count": len(recipients),
                "rate_limits": self.config.get("email", {}).get("rate_limits", {})
            },
            "queue_status": self.email_manager.get_queue_status(),
            "recipient_statistics": all_stats
        }
    
    async def run_mcp_cycle(self):
        """Esegue un ciclo completo di gestione tramite MCP"""
        logger.info("🔍 Inizio ciclo MCP ETJCA")
        
        try:
            # 1. Discovery
            discovery_results = await self.discover_all_resources()
            
            # 2. Analisi
            analysis_results = await self.analyze_all_resources()
            
                # 3. Ottimizzazione automatica se abilitata
            optimization_results = {}
            if self.config.get("monitoring", {}).get("auto_optimization", False):
                optimization_results = await self.auto_optimize()
                
                # Invia report se ci sono ottimizzazioni
                if optimization_results and any(optimization_results.values()):
                    await self.send_optimization_report(optimization_results)
            
            # 4. Controlla per alert critici
            await self._check_critical_alerts(analysis_results)
            
            # 4. Riepilogo
            summary = {
                "timestamp": datetime.now().isoformat(),
                "total_providers": len(self.servers),
                "total_resources": sum(r.get("discovered_count", 0) for r in discovery_results.values()),
                "total_optimizations": sum(len(opts) for opts in optimization_results.values()),
                "discovery": discovery_results,
                "analysis": analysis_results,
                "optimizations": optimization_results
            }
            
            logger.info("✅ Ciclo MCP completato")
            return summary
            
        except Exception as e:
            logger.error(f"Errore nel ciclo MCP: {e}")
            raise
    
    async def start(self):
        """Avvia l'agente MCP"""
        self.running = True
        logger.info("🚀 ETJCA MCP Agent avviato")
        
        while self.running:
            try:
                cycle_result = await self.run_mcp_cycle()
                
                # Attendi prima del prossimo ciclo
                interval = self.config.get("monitoring", {}).get("auto_discovery_interval", 300)
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Errore nel ciclo MCP: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        """Ferma l'agente MCP"""
        self.running = False
        logger.info("⏹️  ETJCA MCP Agent fermato")
    
    def get_mcp_dashboard(self) -> Dict:
        """Ritorna dati dashboard in formato MCP"""
        return {
            "agent_info": {
                "name": self.config.get("agent_name"),
                "version": self.config.get("mcp_version"),
                "status": "running" if self.running else "stopped",
                "providers_count": len(self.servers),
                "messages_processed": len(self.message_history)
            },
            "providers": {
                name: {
                    "status": "active",
                    "resources_managed": len(await server.list_resources()) if hasattr(server, 'resources') else 0,
                    "tools_available": len(server.tools)
                }
                for name, server in self.servers.items()
            },
            "recent_messages": [
                {
                    "id": msg.id,
                    "method": msg.method,
                    "timestamp": msg.timestamp.isoformat(),
                    "source": msg.source,
                    "target": msg.target
                }
                for msg in self.message_history[-10:]  # Ultimi 10 messaggi
            ],
            "email_statistics": self.get_email_statistics()
        }

# Funzione principale per test MCP
async def main():
    """Test dell'agente ETJCA con MCP"""
    print("🚀 Avvio ETJCA MCP Agent...")
    
    agent = ETJCAMCPAgent()
    
    try:
        # Esegui un ciclo completo
        print("📡 Eseguendo ciclo MCP...")
        result = await agent.run_mcp_cycle()
        
        # Mostra dashboard MCP
        dashboard = agent.get_mcp_dashboard()
        
        print("\n" + "="*60)
        print("📡 ETJCA MCP AGENT DASHBOARD")
        print("="*60)
        print(f"Agent: {dashboard['agent_info']['name']} v{dashboard['agent_info']['version']}")
        print(f"Status: {dashboard['agent_info']['status']}")
        print(f"Provider attivi: {dashboard['agent_info']['providers_count']}")
        print(f"Messaggi processati: {dashboard['agent_info']['messages_processed']}")
        
        print("\n🌐 PROVIDER MCP:")
        for name, info in dashboard['providers'].items():
            print(f"  📡 {name.upper()}: {info['resources_managed']} risorse, {info['tools_available']} strumenti")
        
        print(f"\n📊 RISULTATI CICLO:")
        print(f"  • Risorse totali scoperte: {result['total_resources']}")
        print(f"  • Ottimizzazioni applicate: {result['total_optimizations']}")
        
        if result.get('optimizations'):
            print("\n🔧 OTTIMIZZAZIONI MCP:")
            for provider, opts in result['optimizations'].items():
                for opt in opts[:3]:  # Mostra prime 3
                    print(f"  ⚡ {provider}: {opt.get('optimization_type', 'N/A')} completata")
        
        print("\n✅ Test MCP completato con successo!")
        print("🔗 Configurazione MCP salvata in: etjca_mcp_config.json")
        print("📧 Database email rate limiting: etjca_mcp.db")
        print("\n📝 CONFIGURAZIONE EMAIL:")
        print("   Per attivare le notifiche email, modifica etjca_mcp_config.json:")
        print('   "email": {')
        print('     "enabled": true,')
        print('     "username": "your-email@gmail.com",')
        print('     "password": "your-app-password",')
        print('     "recipients": ["admin@company.com"]')
        print('   }')
        
    except Exception as e:
        print(f"❌ Errore durante test MCP: {e}")
        import traceback
        traceback.print_exc()

# Utility per configurare email facilmente
def setup_email_config():
    """Utility per configurare facilmente le email"""
    print("🔧 CONFIGURAZIONE EMAIL ETJCA")
    print("="*40)
    
    config_path = "etjca_mcp_config.json"
    
    # Carica config esistente
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        print("❌ Config file non trovato. Eseguire prima main().")
        return
    
    print("📧 Configurazione email attuale:")
    email_config = config.get("email", {})
    print(f"  Abilitato: {email_config.get('enabled', False)}")
    print(f"  Username: {email_config.get('username', 'NON CONFIGURATO')}")
    print(f"  Destinatari: {len(email_config.get('recipients', []))}")
    
    # Chiedi se modificare
    if input("\nVuoi modificare la configurazione email? (s/n): ").lower() == 's':
        
        # Configura SMTP
        email_config["enabled"] = input("Abilitare email? (s/n): ").lower() == 's'
        
        if email_config["enabled"]:
            email_config["username"] = input("Email username (es. youremail@gmail.com): ").strip()
            email_config["password"] = input("App password (non la password normale!): ").strip()
            
            # Configura destinatari
            recipients = []
            print("\nAggiungi destinatari (premi invio per finire):")
            while True:
                recipient = input(f"Destinatario {len(recipients)+1}: ").strip()
                if not recipient:
                    break
                recipients.append(recipient)
            
            email_config["recipients"] = recipients
            
            # Configura rate limits
            print(f"\nRate limits attuali:")
            limits = email_config.get("rate_limits", {})
            print(f"  Settimanale: {limits.get('weekly_limit', 10)}")
            print(f"  Giornaliero: {limits.get('daily_limit', 3)}")
            print(f"  Orario: {limits.get('hourly_limit', 1)}")
            
            if input("Modificare rate limits? (s/n): ").lower() == 's':
                try:
                    limits["weekly_limit"] = int(input(f"Limite settimanale [{limits.get('weekly_limit', 10)}]: ") or limits.get('weekly_limit', 10))
                    limits["daily_limit"] = int(input(f"Limite giornaliero [{limits.get('daily_limit', 3)}]: ") or limits.get('daily_limit', 3))
                    limits["hourly_limit"] = int(input(f"Limite orario [{limits.get('hourly_limit', 1)}]: ") or limits.get('hourly_limit', 1))
                    email_config["rate_limits"] = limits
                except ValueError:
                    print("⚠️ Valori non validi, mantengo quelli attuali")
        
        # Salva configurazione
        config["email"] = email_config
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("\n✅ Configurazione email salvata!")
        print(f"📧 Email abilitate: {email_config.get('enabled', False)}")
        print(f"📬 Destinatari: {len(email_config.get('recipients', []))}")
        print(f"⏱️ Limite settimanale: {email_config.get('rate_limits', {}).get('weekly_limit', 10)} email")
    
    else:
        print("📧 Configurazione email non modificata")

# Test specifico per rate limiting email
async def test_email_rate_limiting():
    """Test specifico per il rate limiting delle email"""
    print("🧪 TEST RATE LIMITING EMAIL")
    print("="*30)
    
    # Crea agent con config di test
    agent = ETJCAMCPAgent()
    
    # Configura un destinatario di test
    agent.config["email"]["enabled"] = True
    agent.config["email"]["recipients"] = ["test@example.com"]
    agent.config["email"]["rate_limits"]["weekly_limit"] = 3  # Limite basso per test
    agent.config["email"]["rate_limits"]["daily_limit"] = 2
    agent.config["email"]["rate_limits"]["hourly_limit"] = 1
    
    print("📧 Configurazione test:")
    print(f"  Limite settimanale: {agent.config['email']['rate_limits']['weekly_limit']}")
    print(f"  Limite giornaliero: {agent.config['email']['rate_limits']['daily_limit']}")
    print(f"  Limite orario: {agent.config['email']['rate_limits']['hourly_limit']}")
    
    # Test invio multiple email
    print("\n🔄 Test invio email multiple...")
    
    for i in range(5):
        priority = EmailPriority.MEDIUM if i < 3 else EmailPriority.CRITICAL
        
        result = await agent.send_smart_notification(
            subject=f"Test Email {i+1}",
            content=f"Contenuto email di test numero {i+1}",
            priority=priority,
            resource_uri=f"test://resource-{i+1}"
        )
        
        print(f"  Email {i+1} ({priority.value}): {result['queue_results']['sent']} inviata, {len([r for r in result['individual_results'] if r.get('status') == 'skipped'])} saltata")
    
    # Mostra statistiche finali
    stats = agent.get_email_statistics()
    recipient_stats = list(stats["recipient_statistics"].values())[0]
    limits_status = recipient_stats["current_limits_status"]
    
    print(f"\n📊 RISULTATI TEST:")
    print(f"  Email inviate oggi: {limits_status['daily']['count']}/{limits_status['daily']['limit']}")
    print(f"  Email inviate questa settimana: {limits_status['weekly']['count']}/{limits_status['weekly']['limit']}")
    print(f"  Email inviate quest'ora: {limits_status['hourly']['count']}/{limits_status['hourly']['limit']}")
    
    total_emails = recipient_stats["total_emails"]
    print(f"  Totale inviato: {total_emails.get('sent', 0)}")
    print(f"  Totale saltato: {total_emails.get('skipped', 0)}")
    
    print("\n✅ Test rate limiting completato!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            setup_email_config()
        elif sys.argv[1] == "test-email":
            asyncio.run(test_email_rate_limiting())
        else:
            print("Comandi disponibili:")
            print("  python etjca_mcp_agent.py          # Test completo")
            print("  python etjca_mcp_agent.py config   # Configura email")
            print("  python etjca_mcp_agent.py test-email # Test rate limiting")
    else:
        asyncio.run(main())
