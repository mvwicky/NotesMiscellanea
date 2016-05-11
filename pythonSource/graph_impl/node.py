class Node(object):  # class node(pysfml.ellipse)
    def __init__(self, x, y, weight=0):
        self.x = x
        self.y = y
        self.weight = weight
        self.visited = False

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __getitem__(self, index):
        if index not in (0, 1):
            raise IndexError
        return self.y if index else self.x

    def __setitem__(self, index, val):
        if index not in (0, 1):
            raise IndexError
        if index:
            self.y = val
        else:
            self.x = val


def main():
    pass

if __name__ == '__main__':
    main()
