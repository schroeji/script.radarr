#!/usr/bin/env python3

import sqlite3
import json
PATH = "tasks.db"

def create_task(action, **kwargs):
    kwargs["action"] = action
    return kwargs

class TaskQueue:
    def __init__(self):
        self.conn = sqlite3.connect(PATH)
        self.conn.execute('CREATE TABLE IF NOT EXISTS tasks (task json)')

    def push(self, task):
        self.conn.execute('INSERT INTO tasks (task) VALUES (?)', (json.dumps(task),))
        self.conn.commit()

    def pop(self):
        cursor = self.conn.execute('SELECT task FROM tasks ORDER BY rowid ASC LIMIT 1')
        task = cursor.fetchone()
        if task is not None:
            self.conn.execute('DELETE FROM tasks WHERE rowid = (SELECT min(rowid) FROM tasks)')
            self.conn.commit()
            return json.loads(task[0])
        else:
            return None
