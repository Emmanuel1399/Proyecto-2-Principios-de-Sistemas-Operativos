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
            page.waste = 0
        self.page_list = []
        return waste
    def Kill(self):
        waste = self.delete()
        self.kill = True
        return waste
