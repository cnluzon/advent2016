import argparse
import re

"""
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small
microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two
microchips, and once it does, it gives each one to a different bot or puts it
in a marked "output" bin. Sometimes, bots take microchips from "input" bins,
too.

Inspecting one of the microchips, it seems like they each contain a single
number; the bots must use some logic to decide what to do with each chip.
You access the local control computer and download the bots' instructions
(your puzzle input).

Some of the instructions specify that a specific-valued microchip should be
given to a specific bot; the rest of the instructions indicate what a given
bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

    Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a
        value-2 chip and a value-5 chip.

    Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and
        its higher one (5) to bot 0.

    Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and
        gives the value-3 chip to bot 0.

    Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in
        output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a
    value-2 microchip, and output bin 2 contains a value-3 microchip. In this
    configuration, bot number 2 is responsible for comparing value-5 microchips
    with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible
    for comparing value-61 microchips with value-17 microchips?


"""

def parse_input(fi):
    result = []
    for line in fi.readlines():
        result.append(line.rstrip())

    return result


class Bot:
    def __init__(self, id_, values=None, instructions=None):
        self.id = id_
        self.values = []
        self.instructions = {}

        if values:
            self.values = values

        if instructions:
            self.instructions = instructions
            self._validate_instructions()

        self.instructions = instructions

    def __str__(self):
        result = 'Bot {} has values {} and intends to give {}'.format(
            self.id,
            self.values,
            str(self.instructions))
        return result

    def high(self):
        return max(self.values)

    def low(self):
        return min(self.values)

    def active(self):
        return ((len(self.values) == 2) and
                (set(self.instructions.keys()) == set(['high', 'low'])))

    def add_value(self, value):
        if len(self.values) < 2:
            self.values.append(value)
        else:
            print "Warning: Given a bot third value."
            print "{} was given {}, but had {}".format(self.id, value, self.values)

    def clear_values(self):
        self.values = []

    def set_instructions(self, instructions):
        self.instructions = instructions
        self._validate_instructions()

    def _validate_instructions(self,):
        if 'high' not in self.instructions.keys():
            msg = 'Missing "high" key in instructions'
            raise ValueError(msg)
        elif 'low' not in self.instructions.keys():
            msg = 'Missing "low" key in instructions'
            raise ValueError(msg)

        return True

    def give_high_value_to(self):
        return self.instructions['high']

    def give_low_value_to(self):
        return self.instructions['low']

    def give(self):
        if len(self.values) == 2:
            return {self.instructions['low']: self.low(),
                    self.self.instructions['high']: self.high()}
        else:
            return None


class BotSimulator:
    def __init__(self, instructions):
        self.bots = self.initialize_simulator(instructions)

    def initialize_simulator(self, instructions_list):
        """
        Initialize de bot list with the initial microchips and the whole set of bots
        """
        bots = {}

        classified_instructions = self.extract_instructions(instructions_list)

        for instruction in classified_instructions['initial']:
            (value, bot_id) = self.process_value_instruction(instruction)
            if bots.get(bot_id, None):
                bots[bot_id].add_value(value)
            else:
                bots[bot_id] = Bot(bot_id, values=[value])

        for instruction in classified_instructions['give']:
            (bot_id, instructions) = self.process_give_instruction(instruction)
            if bots.get(bot_id, None):
                bots[bot_id].set_instructions(instructions)
            else:
                bots[bot_id] = Bot(bot_id, values=[], instructions=instructions)

            if not bots.get(instructions['high'], None):
                bots[instructions['high']] = Bot(instructions['high'])

            if not bots.get(instructions['low'], None):
                bots[instructions['low']] = Bot(instructions['low'])

        return bots

    def process_value_instruction(self, instruction):
        # value 11 goes to bot 3
        words = instruction.split()
        value = int(words[1])
        bot_id = 'b{}'.format(words[-1])

        return (value, bot_id)

    def process_give_instruction(self, instruction):
        # bot 129 gives low to bot 52 and high to bot 57
        words = instruction.split()
        bot_id = 'b{}'.format(words[1])
        low_id = '{}{}'.format(words[5][0], words[6])
        high_id = '{}{}'.format(words[-2][0], words[-1])

        return (bot_id, {'high': high_id, 'low': low_id})

    def extract_instructions(self, instructions_list):
        result = {}
        result['initial'] = []
        result['give'] = []

        for instruction in instructions_list:
            words = instruction.split(' ')
            if words[0] == 'value':
                result['initial'].append(instruction)
            else:
                result['give'].append(instruction)

        return result

    def run(self, instructions_event=None):

        active_bot = self.get_next_active_bot()

        while(active_bot):
            if instructions_event:
                if (min(active_bot.values) == min(instructions_event.values()) and 
                    max(active_bot.values) == max(instructions_event.values())):
                    print "Bot found: ID {} gives high to {} and low to {}".format(
                        active_bot.id, active_bot.instructions['high'],
                        active_bot.instructions['low'])
                    print active_bot

            high_goes_to = active_bot.instructions['high']
            low_goes_to = active_bot.instructions['low']

            self.bots[high_goes_to].add_value(active_bot.high())
            self.bots[low_goes_to].add_value(active_bot.low())

            active_bot.clear_values()
            active_bot = self.get_next_active_bot()

        print "Run finished. Final status"
        self.show_status()

    def how_many_active_bots(self):
        result = 0
        for i in self.bots.keys():
            if self.bots[i].active():
                result += 1

        return result

    def get_next_active_bot(self):
        for i in self.bots.keys():
            if self.bots[i].active():
                return self.bots[i]

        return None

    def show_status(self):
        for k in sorted(self.bots.keys()):
            print self.bots[k]

    def show_microchips(self):
        for k in sorted(self.bots.keys()):
            if self.bots[k].values:
                print self.bots[k]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 09: Explosives in cyberspace')

    parser.add_argument('in_file', help='Input data')

    args = parser.parse_args()

    fi = open(args.in_file)
    instructions_list = parse_input(fi)
    fi.close()

    event = {'high': 61, 'low': 17}

    botsimulator = BotSimulator(instructions_list)
    botsimulator.run(instructions_event=event)
