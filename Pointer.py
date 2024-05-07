class Pointer:
    def __init__(self, pid, size, index):
        self.index = index
        self.page_list = []
        self.pid = pid
        self.size = size
        self.kill = False
        self.in_ram = False

    def Kill(self):
        self.page_list = []
        self.kill = True

