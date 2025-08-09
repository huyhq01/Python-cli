import sqlite3
from task import Task

DATABASE_NAME = "tasks.db"
_task_cache: list[Task] = []

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    connect = connect_db() # tạo kết nối đến cơ sở dữ liệu
    cursor = connect.cursor() # tạo con trỏ để thực hiện các câu lệnh SQL
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            deadline DATE,
            status BOOLEAN DEFAULT 0
            )"""
        )
    connect.commit() # lưu các thay đổi vào cơ sở dữ liệu
    connect.close() # đóng kết nối đến cơ sở dữ liệu 

def add_task(content, deadline):
    cursor = None
    try:
        with connect_db() as connect:
            cursor = connect.cursor()
            cursor.execute("INSERT INTO tasks (content, deadline, status) VALUES (?, ?, ?)",
                    (content, deadline, False))
            connect.commit()
            print("Thêm task thành công!")
    except sqlite3.Error as e:
        print(f"Rồi xong có lỗi: {e}")
    finally:
        if cursor: cursor.close()

def query_all_tasks():
    rows = []
    try:
        with connect_db() as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = [Task(*row) for row in cursor.fetchall()]  # Chuyển đổi mỗi hàng thành đối tượng Task
    except sqlite3.Error as e:
        print(f"Rồi xong có lỗi: {e}")
    finally:
        if cursor: cursor.close()
    
    return rows

def update_task(task_id, content=None, deadline=None, status=None):
    cursor = None
    success = False
    set_clauses = []
    values = []
    if content is not None: 
        set_clauses.append("content = ?")
        values.append(content)
    if deadline is not None:
        set_clauses.append("deadline = ?")
        values.append(deadline)
    if status is not None:
        set_clauses.append("status = ?")
        values.append(status)
    if not set_clauses:
        print("Không có gì để update!")
        return False
    
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ?"

    try:
        with connect_db() as connect:
            cursor = connect.cursor()
            cursor.execute(query, values)
            connect.commit()
            success = cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Rồi xong có lỗi: {e}")
    finally:
        if cursor: cursor.close()
    return success

def delete_task(task_id):
    pass

def update_list_task():
    global _task_cache
    _task_cache = query_all_tasks() 

def get_all_tasks():
    return _task_cache

def get_list_task_ids():
    return {i :task.id for i,task in enumerate(get_all_tasks(), start=1)}