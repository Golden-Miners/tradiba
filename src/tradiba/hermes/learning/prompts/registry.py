import sqlite3
import json
from typing import Dict, Any, Optional
from datetime import datetime

class PromptRegistry:
    """
    Tracks version history of prompts and models with rollback support.
    Backed by local SQLite for genuine persistence.
    """
    def __init__(self, db_path: str = "prompts.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    name TEXT,
                    version INTEGER,
                    template TEXT,
                    model_config TEXT,
                    created_at REAL,
                    status TEXT,
                    PRIMARY KEY (name, version)
                )
            ''')
            conn.commit()

    def register_prompt(self, name: str, template: str, model_config: Dict[str, Any]) -> int:
        now = datetime.now().timestamp()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(version) FROM prompts WHERE name = ?", (name,))
            row = cursor.fetchone()
            next_version = (row[0] or 0) + 1
            
            cursor.execute('''
                INSERT INTO prompts (name, version, template, model_config, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, next_version, template, json.dumps(model_config), now, "ACTIVE"))
            conn.commit()
            
        return next_version

    def get_prompt(self, name: str, version: Optional[int] = None) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if version:
                cursor.execute("SELECT version, template, model_config, status FROM prompts WHERE name = ? AND version = ?", (name, version))
            else:
                cursor.execute("SELECT version, template, model_config, status FROM prompts WHERE name = ? ORDER BY version DESC LIMIT 1", (name,))
                
            row = cursor.fetchone()
            if not row:
                return {}
                
        return {
            "version": row[0],
            "template": row[1],
            "model_config": json.loads(row[2]),
            "status": row[3]
        }

    def rollback_prompt(self, name: str, target_version: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Mark all newer versions as ROLLED_BACK
            cursor.execute("UPDATE prompts SET status = 'ROLLED_BACK' WHERE name = ? AND version > ?", (name, target_version))
            conn.commit()
            
    def clear_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("DROP TABLE IF EXISTS prompts")
            conn.commit()
        self._init_db()
