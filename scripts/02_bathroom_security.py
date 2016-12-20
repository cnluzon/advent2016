import argparse
"""
--- Day 2: Bathroom Security ---

You arrive at Easter Bunny Headquarters under cover of darkness. However, you
left in such a rush that you forgot to use the bathroom! Fancy office buildings
like this one usually have keypad locks on their bathrooms, so you search the
front desk for the code.

"In order to improve security," the document you find says, "bathroom codes
will no longer be written down. Instead, please memorize and follow the
procedure below to access the bathrooms."

The document goes on to explain that each button to be pressed can be found by
starting on the previous button and moving to adjacent buttons on the keypad:
U moves up, D moves down, L moves left, and R moves right.
Each line of instructions corresponds to one button, starting at the previous
button (or, for the first line, the "5" button); press whatever button you're
on at the end of each line. If a move doesn't lead to a button, ignore it.

You can't hold it much longer, so you decide to figure out the code as you walk
to the bathroom. You picture a keypad like this:

1 2 3
4 5 6
7 8 9

Suppose your instructions are:

ULL
RRDDD
LURDL
UUUUD

    You start at "5" and move up (to "2"), left (to "1"), and left (you can't,
    and stay on "1"), so the first button is 1.
    Starting from the previous button ("1"), you move right twice (to "3") and
    then down three times (stopping at "9" after two moves and ignoring the
    third), ending up with 9.
    Continuing from "9", you move left, up, right, down, and left, ending with
    8.

    Finally, you move up four times (stopping at "2"), then down once, ending
    with 5.

So, in this example, the bathroom code is 1985.
"""


class SecurityCode:

    def __init__(self, code_board, finger_position):
        self.code_board = code_board
        self.code_board_shape = [len(code_board), len(code_board[0])]
        self.finger_position = finger_position

        ok_dims = self._validate_input_dimensions(self.code_board_shape,
                                                  finger_position)

        if not ok_dims:
            board_dims = [len(code_board[0]), len(code_board)]
            msg = "Board dimensions and finger position do not match."
            msg += "{} board, {} finger".format(str(board_dims),
                                                str(finger_position))
            raise ValueError(msg)

    def _validate_input_dimensions(self, board_dims, position):
        ok = True
        ok = self._validate_closed_interval([0, board_dims[0]-1], position[0])
        ok = self._validate_closed_interval([0, board_dims[1]-1], position[1])
        return ok

    def _validate_closed_interval(self, interval, position):
        ok = True
        if position < interval[0]:
            ok = False
        elif position > interval[1]:
            ok = False

        return ok

    def move_finger(self, code):
        next_position = self.finger_position[:]

        if code == 'U':
            if next_position[0] > 0:
                next_position[0] -= 1
        elif code == 'R':
            if next_position[1] < (self.code_board_shape[1]-1):
                next_position[1] += 1
        elif code == 'L':
            if next_position[1] > 0:
                next_position[1] -= 1
        elif code == 'D':
            if next_position[0] < (self.code_board_shape[0]-1):
                next_position[0] += 1

        if self._is_valid(next_position):
            self.finger_position = next_position

    def _is_valid(self, position):
        invalid_char = ' '
        if self.code_board[position[0]][position[1]] == invalid_char:
            return False
        else:
            return True

    def press_key(self):
        return self.code_board[self.finger_position[0]][self.finger_position[1]]

    def enter_code(self, moves_lines):
        result_code = ''
        for line in moves_lines:
            for direction in line:
                self.move_finger(direction)

            result_code += self.press_key()
        return result_code


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 02: Bathroom security')

    parser.add_argument('in_file', help='Input moves file')

    args = parser.parse_args()
    code_board = [['1', '2', '3'],
                  ['4', '5', '6'],
                  ['7', '8', '9']]

    finger_position = [1, 1]

    my_security_code = SecurityCode(code_board, finger_position)

    fi = open(args.in_file)
    moves_lines = fi.readlines()
    fi.close()

    result_code = my_security_code.enter_code(moves_lines)

    print "Result code first floor: {}".format(result_code)

    code_board_second_floor = [[' ', ' ', '1', ' ', ' '],
                               [' ', '2', '3', '4', ' '],
                               ['5', '6', '7', '8', '9'],
                               [' ', 'A', 'B', 'C', ' '],
                               [' ', ' ', 'D', ' ', ' ']]

    finger_position_second_floor = [2, 0]

    my_security_code_second_floor = SecurityCode(code_board_second_floor,
                                                 finger_position_second_floor)

    result_code_second_floor = my_security_code_second_floor.enter_code(moves_lines)

    print "Result code second floor: {}".format(result_code_second_floor)

