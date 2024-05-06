class Pointer:
    def __init__(self, pid, size):
        self.page_list = []
        self.pid = pid
        self.size = size
        self.kill = False

    def delete(self):
        waste = 0
        for page in self.page_list:
            waste += page.waste
        self.page_list = []
        return waste
