import argparse
"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways
and office furniture that makes up this part of Easter Bunny HQ. This must be a
graphic design department; the walls are covered in specifications for
triangles.

Or are they?

The design document gives the side lengths of each triangle it describes,
but... 5 10 25? Some of these aren't triangles. You can't help but mark the
impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining
side. For example, the "triangle" given above is impossible, because 5 + 10 is
not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

"""


class TriangleValidator:

    def validate_side_list(self, sides):
        result = True
        if sides[0] + sides[1] <= sides[2]:
            result = False
        elif sides[1] + sides[2] <= sides[0]:
            result = False
        elif sides[0] + sides[2] <= sides[1]:
            result = False

        return result

    def count_good_triangles(self, triangle_list):
        good_triangle_count = 0

        for triangle in triangle_list:
            if self.validate_side_list(triangle):
                good_triangle_count += 1

        return good_triangle_count


def parse_input_horizontal(fi):
    lines = fi.readlines()
    triangles_list = []
    for line in lines:
        values = line.rstrip().split()
        values = [int(v) for v in values]
        triangles_list.append(values)

    return triangles_list

def parse_input_vertical(fi):
    triangle_list = []
    transposed_matrix = []

    lines = fi.readlines()
    for line in lines:
        line = line.rstrip()
        values = line.split()
        values = [int(v) for v in values]
        transposed_matrix.append(values)

    for j in range(0, len(transposed_matrix[0])):
        value_list = [transposed_matrix[i][j] for i in range(len(transposed_matrix))]

        for i in range(0, len(value_list), 3):
            triangle_list.append(value_list[i:i+3])
        
    return triangle_list

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 03: Squares with three sides')

    parser.add_argument('in_file', help='Input triangles file')

    args = parser.parse_args()

    validator = TriangleValidator()

    fi = open(args.in_file)
    triangle_list_horizontal = parse_input_horizontal(fi)
    fi.close()

    fi = open(args.in_file)
    triangle_list_vertical = parse_input_vertical(fi)
    fi.close()

    good_triangles_horizontal = validator.count_good_triangles(triangle_list_horizontal)
    good_triangles_vertical = validator.count_good_triangles(triangle_list_vertical)

    print "In the list, there are {} good triangles".format(good_triangles_horizontal)
    print "In the list (vertically), there are {} good triangles".format(good_triangles_vertical)

