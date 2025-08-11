from datetime import datetime, date
class Task:
    def __init__ (self, id: int, content: str = "", deadline: date | None = None, status: bool = False):
        self.id = id
        self.content = content
        self.deadline = (datetime.strptime(deadline, "%Y-%m-%d").date()
                         if deadline and isinstance(deadline, str) else deadline) # str -> date
        self.status = bool(status)  # 0 = False not completed, 1 = True completed