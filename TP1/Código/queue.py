class Queue_imp:

    def __init__(self):
        self.items = []
    
    def put(self,item):
        self.items.append(item)
    
    def get(self):

        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def is_empty(self):
        return len(self.items) == 0

    def len(self):
        return len(self.items)