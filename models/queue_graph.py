class Queue_:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def clone(self):
        items = self.items[:]
        self.copy = Queue_()
        for item in items[::-1]:
            self.copy.enqueue(item)
        return self.copy

    def __eq__(self, other):
        return self.items == other.items

    def peek(self):
        return self.items[-1]
