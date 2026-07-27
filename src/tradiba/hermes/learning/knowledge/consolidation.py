import sqlite3
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime

class KnowledgeConsolidator:
    """
    Handles persistence and consolidation of Hermes knowledge.
    Backed by a local SQLite database for genuine data persistence.
    """
    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id TEXT PRIMARY KEY,
                    topic TEXT,
                    content TEXT,
                    confidence REAL,
                    provenance TEXT,
                    status TEXT,
                    created_at REAL,
                    updated_at REAL
                )
            ''')
            conn.commit()

    def add_knowledge(self, topic: str, content: Dict[str, Any], confidence: float, provenance: str) -> str:
        item_id = str(uuid.uuid4())
        now = datetime.now().timestamp()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO knowledge_items (id, topic, content, confidence, provenance, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_id, topic, json.dumps(content), confidence, provenance, "DRAFT", now, now))
            conn.commit()
            
        return item_id

    def consolidate(self):
        """
        Merge duplicates and update confidences. (Simplified for Phase 5.3)
        """
        # In a real system, this would use LLM embeddings to find semantic duplicates
        # For this phase, we just mark old drafts as consolidated if there is a newer one for the same topic.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT topic, MAX(created_at) FROM knowledge_items GROUP BY topic")
            latest_topics = cursor.fetchall()
            
            for topic, max_time in latest_topics:
                # Mark older drafts as superseded
                cursor.execute('''
                    UPDATE knowledge_items 
                    SET status = 'SUPERSEDED' 
                    WHERE topic = ? AND created_at < ? AND status = 'DRAFT'
                ''', (topic, max_time))
            conn.commit()

    def get_knowledge(self, topic: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, content, confidence, status FROM knowledge_items WHERE topic = ?", (topic,))
            rows = cursor.fetchall()
            
        return [{"id": r[0], "content": json.loads(r[1]), "confidence": r[2], "status": r[3]} for r in rows]

    def clear_db(self):
        """For testing purposes"""
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("DROP TABLE IF EXISTS knowledge_items")
            conn.commit()
        self._init_db()
