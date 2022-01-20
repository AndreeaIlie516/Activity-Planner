from copy import deepcopy


def gnome_sort(list_, key=None, reverse=False):
    """
    Method for computing the gnome sort
    Implementation: Check each element along with the previous and the next element. If they are not in the correct
    order, it swaps the elements. If no previous element, step forward. If no next element, finish the sorting.
    Complexity: -time: O(n^2)
                -space: O(1)
    :param list_: list to be sorted
    :param key: object used for comparison
    :param reverse: bool parameter for reversing the string(descending order) or not
    :return: sorted list
    """

    def default_key(obj):
        return obj

    def compare(obj1, obj2):
        return obj1 < obj2

    new_list = deepcopy(list_)
    if key is None:
        key = default_key
    pos = 1
    while pos < len(new_list):
        if pos == 0 or not compare(key(new_list[pos]), key(new_list[pos - 1])):
            pos += 1
        else:
            new_list[pos - 1], new_list[pos] = new_list[pos], new_list[pos - 1]
            pos -= 1
    if reverse:
        i = 0
        j = len(new_list) - 1
        while i < j:
            new_list[i], new_list[j] = new_list[j], new_list[i]
            i += 1
            j -= 1
    return new_list


def custom_filter(iterable, accept):
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
