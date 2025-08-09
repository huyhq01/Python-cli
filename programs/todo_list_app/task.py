class Task:
    def __init__ (self, id, content = "", deadline = None, status = False):
        self.id = id
        self.content = content
        self.deadline = deadline
        self.status = bool(status)  # 0 = False not completed, 1 = True completed