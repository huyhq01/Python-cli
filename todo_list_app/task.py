from datetime import date
class Task:
    def __init__ (self, id: int, content: str = "", deadline: date | None = None, status: bool = False):
        self.id = id
        self.content = content
        self.deadline = deadline
        self.status = bool(status)  # 0 = False not completed, 1 = True completed