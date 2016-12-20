import argparse


def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


class Taxicab:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.directions = ['N', 'E', 'S', 'W']
        self.visited = set((x, y))

        self.first_repeated = None

    def turn(self, direction):
        if direction.lower() == 'r':
            self.orientation += 1
        elif direction.lower() == 'l':
            self.orientation -= 1
        else:
            msg = "Unknown direction: {}".format(direction)
            raise ValueError(msg)

        self.orientation = self.orientation % 4

    def move_step_forward(self):
        direction = self.directions[self.orientation]
        if direction == 'N':
            self.y += 1
        elif direction == 'S':
            self.y -= 1
        elif direction == 'W':
            self.x -= 1
        elif direction == 'E':
            self.x += 1

        print self.x, self.y

        if (self.x, self.y) in self.visited:
            if not self.first_repeated:
                self.first_repeated = (self.x, self.y)
        else:
            self.visited |= {(self.x, self.y)}

    def move_forward(self, steps):
        for i in range(steps):
            self.move_step_forward()

    def distance(self, other_x, other_y):
        return manhattan_distance((self.x, self.y), (other_x, other_y))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 01: Taxicab')

    parser.add_argument('in_file', help='Input moves file')

    args = parser.parse_args()

    fi = open(args.in_file)

    moves_line = fi.readline().rstrip()
    moves_list = moves_line.split(',')
    moves_list = [m.rstrip().lstrip() for m in moves_list]
    my_taxicab = Taxicab(0, 0, 0)

    for move in moves_list:
        direction = move[0]
        steps = int(move[1:])

        my_taxicab.turn(direction)
        my_taxicab.move_forward(steps)

    print "You are {} blocks away from where you started. ".format(
        my_taxicab.distance(0, 0))

    print "You are {} blocks away from {}, the first location you repeated".format(
        manhattan_distance((0, 0),
                            (my_taxicab.first_repeated[0], my_taxicab.first_repeated[1])),
        str(my_taxicab.first_repeated))
