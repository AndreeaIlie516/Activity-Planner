def filter(iterable, accept):
    """
    Method for filtering different things
    """
    new_list = type(iterable)()
    for x in iterable:
        if accept(x):
            new_list.append(x)
    return new_list

class Container:
    def __init__(self, new_list=None):
        if new_list is None:
            new_list = []
        self._thing = new_list

    def __len__(self):
        return len(self._thing)

    def __setitem__(self, key, value):
        self._thing[key] = value

    def __getitem__(self, item):
        return self._thing[item]

    def __delitem__(self, key):
        del self._thing[key]

    def __iter__(self):
        self.key = -1
        return self

    def __next__(self):
        self.key += 1
        if self.key >= len(self._thing):
            raise StopIteration
        return self._thing[self.key]

    def append(self, item):
        self._thing.append(item)

    def remove(self, item):
        self._thing.remove(item)