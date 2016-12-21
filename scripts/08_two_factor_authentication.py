"""
.. module:: 08_two_factor_authentication.py
.. moduleauthor:: cnluzon

Script to solve Advent of Code 2016's problem 08. Two-factor authentication.
"""

import argparse

"""
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an
implementation of two-factor authentication after a long game of requirements
telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a
nearby desk). Then, it displays a code on a little screen, and you type that
code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken
everything apart and figured out how it works. Now you just have to work out
what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for
the screen; these instructions are your puzzle input. The screen is 50 pixels
wide and 6 pixels tall, all of which start off, and is capable of three
somewhat peculiar operations:

    rect AxB turns on all of the pixels in a rectangle at the top-left of the
    screen which is A wide and B tall.

    rotate row y=A by B shifts all of the pixels in row A (0 is the top row)
    right by B pixels. Pixels that would fall off the right end appear at the
    left end of the row.

    rotate column x=A by B shifts all of the pixels in column A (0 is the left
    column) down by B pixels. Pixels that would fall off the bottom appear at
    the top of the column.

For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel,
    causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

As you can see, this display technology is extremely powerful, and will soon
dominate the tiny-code-displaying-screen market. That's what the advertisement
on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display:
after you swipe your card, if the screen did work, how many pixels should be
lit?


"""


def parse_input(fi):
    result = [line.rstrip() for line in fi.readlines()]
    return result


class PasswordScreen:
    def __init__(self, nrows, ncols, empty='.', filler='#'):
        if nrows > 0 and ncols > 0:
            self.screen = self._build_screen(nrows, ncols, empty)
            self.dimensions = (nrows, ncols)

            self.off_filler = empty
            self.on_filler = filler
        else:
            msg = "Invalid dimensions, must be positive integers."
            raise ValueError(msg)

    def _build_screen(self, nrows, ncols, filler):
        result = []
        for i in range(nrows):
            result.append([filler]*ncols)
        return result

    def show(self):
        for row in self.screen:
            print ''.join(row)

    def process_instruction(self, instruction):
        instruction_function = self.parse_function(instruction)
        instruction_parameters = self.parse_parameters(instruction)

        instruction_function(*instruction_parameters)

    def count_lights_on(self):
        count = 0
        for i in range(len(self.screen)):
            for j in range(len(self.screen[0])):
                if self.screen[i][j] == self.on_filler:
                    count += 1

        return count

    def rectangle(self, width, height):
        for i in range(width):
            for j in range(height):
                self.screen[j][i] = self.on_filler


    def rotate_row(self, row, shift):
        for i in range(shift):
            self.rotate_row_once(row)


    def rotate_list_once_right(self, list_):
        return [list_[-1]] + list_[0:-1]

    def rotate_list_once_left(self, list_):
        return list_[1:] + [list_[0]]

    def rotate_row_once(self, row):
        new_row = self.rotate_list_once_right(self.screen[row])
        self.screen[row] = new_row

    def rotate_column(self, column, shift):
        for i in range(shift):
            self.rotate_column_once(column)

    def rotate_column_once(self, column):
        column_list = [self.screen[i][column] for i in range(len(self.screen))]
        rotated_column = self.rotate_list_once_right(column_list)

        for i in range(len(self.screen)):
            self.screen[i][column] = rotated_column[i]

    def parse_function(self, instruction):
        words = instruction.split(' ')
        if words[0] == 'rect':
            function = getattr(self, 'rectangle')
        elif words[0] == 'rotate':
            if words[1] == 'row':
                function = getattr(self, 'rotate_row')
            elif words[1] == 'column':
                function = getattr(self, 'rotate_column')
        return function 

    def parse_parameters(self, instruction):
        words = instruction.split(' ')
        if words[0] == 'rect':
            parsing_function = getattr(self, 'parse_rectangle')

        elif words[0] == 'rotate':
            # if words[1] == 'row':
            parsing_function = getattr(self, 'parse_rotate')

        parameters = parsing_function(instruction)
        return parameters

    def parse_rectangle(self, instruction):
        words = instruction.split(' ')
        dims = words[1].split('x')
        return [int(d) for d in dims]

    def parse_rotate(self, instruction):
        words = instruction.split(' ')
        axis = words[2].split('=')[1]
        shift = words[-1]
        return [int(axis), int(shift)]



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 08: Two-factor authentication')

    parser.add_argument('-f', '--file', help='Input codes', required=True)

    args = parser.parse_args()

    fi = open(args.file)
    instructions_list = parse_input(fi)
    fi.close()

    screen = PasswordScreen(6, 50)

    for instruction in instructions_list:
        screen.process_instruction(instruction)

    screen.show()

    print ""
    print "The screen has {} lights on". format(screen.count_lights_on())