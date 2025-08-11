import sqlite3
from typing import TypedDict
from task import Task
from datetime import date

DATABASE_NAME = "tasks.db"
_task_cache: list[Task] = []

class Response(TypedDict):
    status: bool
    message: str

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
    update_list_task()

def add_task(content: str, deadline: date | None):
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
        update_list_task()
        if cursor: cursor.close()

def query_all_tasks():
    rows = []
    cursor = None
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

def update_task(
        task_id: int, 
        content: str | None = None, 
        deadline: date|None = None, 
        status: bool | None = None
        ) -> Response:
    cursor = None
    set_clauses: list[str] = []
    values: list[str|date|bool|int] = []
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
        return {'status': False, 'message': "Không có gì để update!"}
    
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ?"

    try:
        with connect_db() as connect:
            cursor = connect.cursor()
            cursor.execute(query, values)
            connect.commit() # lưu các thay đổi vào cơ sở dữ liệu
            success = cursor.rowcount > 0 # xem số row đã bị thao tác thay đổi
            message = f"{'Cập nhật thành công!' if success else 'Không tìm thấy task để cập nhật!'}"
            return {'status': success, 'message': message}
    except sqlite3.Error as e:
        return {'status': False, 'message': f"Rồi xong lỗi database: {e}"}
    finally:
        update_list_task()
        if cursor: cursor.close()    

def delete_task(task_id: int) -> Response :
    cursor = None
    try:
        with connect_db() as connect:
            cursor = connect.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            connect.commit() # lưu các thay đổi vào cơ sở dữ liệu
            success = cursor.rowcount > 0 # xem số row đã bị thao tác thay đổi
            message = f"{'Xóa thành công!' if success else 'Không tìm thấy task để xóa!'}"
            return {'status': success, 'message': message}
    except sqlite3.Error as e:
        return {'status': False, 'message': f"Rồi xong lỗi database: {e}"}
    finally:
        update_list_task()
        if cursor: cursor.close()

def update_list_task():
    global _task_cache
    _task_cache = query_all_tasks() 

def get_all_tasks():
    return _task_cache

def get_list_task_ids() -> dict[int, int]:
    return {i :task.id for i,task in enumerate(get_all_tasks(), start=1)}

def get_task_by_id(task_id: int) -> Task | None:
    return next((task for task in _task_cache if task.id == task_id), None)