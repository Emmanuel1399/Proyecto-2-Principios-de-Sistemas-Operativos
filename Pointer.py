class Pointer:
    def __init__(self,pid,size):
        self.page_list=[]
        self.pid = pid
        self.size = size
        self.kill = False
    def delete(self):
        self.page_list=[]
