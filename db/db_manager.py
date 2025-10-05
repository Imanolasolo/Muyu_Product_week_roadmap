import sqlite3

DB_PATH = "roadmap.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# ---- EPICS ----
def create_epic(name, description, week, status="Pendiente"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO epics (name, description, week, status) VALUES (?, ?, ?, ?)",
                   (name, description, week, status))
    conn.commit()
    conn.close()

def get_epics_by_week(week):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM epics WHERE week = ?", (week,))
    data = cursor.fetchall()
    conn.close()
    return data

def update_epic_status(epic_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE epics SET status = ? WHERE id = ?", (new_status, epic_id))
    conn.commit()
    conn.close()

def delete_epic(epic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM epics WHERE id = ?", (epic_id,))
    conn.commit()
    conn.close()

def get_all_epics():
    """Función de debug para ver todas las épicas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM epics ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def get_epic_count_by_week():
    """Función para contar épicas por semana"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT week, COUNT(*) as count FROM epics GROUP BY week")
    data = cursor.fetchall()
    conn.close()
    return data

# ---- TASKS ----
def create_task(title, description, epic_id, owner="", priority="Media"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, epic_id, owner, priority, status) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, description, epic_id, owner, priority, "Pendiente"))
    conn.commit()
    conn.close()

def get_tasks_by_epic(epic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE epic_id = ? ORDER BY priority DESC, id ASC", (epic_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def update_task_status(task_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_task_completion_status(epic_id):
    """Retorna el porcentaje de completación de tareas de una épica"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE epic_id = ?", (epic_id,))
    total = cursor.fetchone()[0]
    
    if total == 0:
        conn.close()
        return 0, 0, 0  # completed, total, percentage
    
    cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE epic_id = ? AND status = 'Completado'", (epic_id,))
    completed = cursor.fetchone()[0]
    conn.close()
    
    percentage = (completed / total) * 100
    return completed, total, percentage

def auto_complete_epic_if_tasks_done(epic_id):
    """Cambia automáticamente la épica a 'Hecho' si todas las tareas están completadas"""
    completed, total, percentage = get_task_completion_status(epic_id)
    if total > 0 and percentage == 100:
        update_epic_status(epic_id, "Hecho")
        return True
    return False
