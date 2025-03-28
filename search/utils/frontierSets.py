import heapq
from abc import ABC, abstractmethod
from collections import deque


class Collection(ABC):
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

class Queue(Collection):
    def __init__(self):
        self.items = deque()

    def add(self, item):
        self.items.append(item)

    def next(self):
        return self.items.popleft() if self.items else None

    def __len__(self):
        return len(self.items)


class Stack(Collection):
    def __init__(self):
        self.items = deque()

    def add(self, item):
        self.items.append(item)

    def next(self):
        return self.items.pop() if self.items else None

    def __len__(self):
        return len(self.items)


class Sorted(Collection):
    def __init__(self, key=lambda x: x):
        self.items = []
        self.key = key

    def add(self, item):
        key_value = self.key(item)
        heapq.heappush(self.items, (key_value, id(item), item))

    def next(self):
        return heapq.heappop(self.items)[2] if self.items else None

    def __len__(self):
        return len(self.items)
