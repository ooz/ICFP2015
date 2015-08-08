#!/usr/bin/python
# coding: utf-8

import copy
import json

from lcg import LCG

class Game(object):
    def __init__(self, json_file):
        super(Game, self).__init__()
        with open(json_file) as f:
            json_data = json.load(f)
            self.ID = json_data["id"]
            self.units = [Unit(json_unit) for json_unit in json_data["units"]]
            self.width = json_data["width"]
            self.height = json_data["height"]
            self.filled = [json_cell2tuple(json_c) for json_c in json_data["filled"]]
            self.sourceLength = json_data["sourceLength"]
            self.sourceSeeds = json_data["sourceSeeds"]
            self.solutions = []

    def solve(self, ss_nr=0):
        for ss in self.sourceSeeds:
            commands = ""
            board = Board(self.width, self.height, self.filled)
            source = self.generate_source(ss, self.sourceLength)
            while not board.is_finished() and len(source) > 0:
                unit = source.pop(0)
                board.spawn(unit)
                if not board.is_finished():
                    while board.unit is not None:
                        commands += board.move_e()
                        commands += board.move_sw()
                        commands += board.move_w()
                        state = 0
                        while board.unit is not None:
                            if state % 2 == 0:
                                commands += board.move_se()
                            else:
                                commands += board.move_sw()
                            state += 1

            solution = {}
            solution["problemId"] = self.ID
            solution["seed"] = ss
            solution["tag"] = "Algo v2.2 with board update, fix 1"
            solution["solution"] = commands
            self.solutions.append(solution)
        return json.dumps(self.solutions)

    def generate_source(self, seed, sourceLength):
        source = []
        rng = LCG(seed)
        for i in range(sourceLength):
            unit_nr = rng.next() % len(self.units)
            unit = copy.deepcopy(self.units[unit_nr])
            source.append(unit)
        return source

    def __str__(self):
        return "Game(ID:%s)" % self.ID

class Unit(object):
    def __init__(self, json_unit):
        super(Unit, self).__init__()
        self.pivot = json_cell2tuple(json_unit["pivot"])
        self.members = [json_cell2tuple(json_m) for json_m in json_unit["members"]]
        self.pos = Cell(0, 0)

    def get_topmost(self):
        tm = self.members[0]
        for m in self.members:
            if m.y < tm.y:
                tm = m
        return tm

    def get_leftmost(self):
        lm = self.members[0]
        for m in self.members:
            if m.x < lm.x:
                lm = m
        return lm

    def get_rightmost(self):
        rm = self.members[0]
        for m in self.members:
            if m.x > rm.x:
                rm = m
        return rm

    def can_be_placed(self, board):
        for m in self.members:
            try:
                if board.get(self.pos.x + m.x, self.pos.y + m.y) in [1, 2, 3]:
                    return False
            except IndexError:
                return False
        return True

    def move_e(self):
        self.pos.x = self.pos.x - 1

    def move_w(self):
        self.pos.x = self.pos.x + 1

    def move_se(self):
        if self.pos.y % 2 == 0:
            self.pos.x = self.pos.x - 1
        self.pos.y = self.pos.y + 1

    def move_sw(self):
        if self.pos.y % 2 == 1:
            self.pos.x = self.pos.x + 1
        self.pos.y = self.pos.y + 1

    def turn_cw(self):
        pass

    def turn_ccw(self):
        pass

    def __str__(self):
        return "Unit(pivot:%s, members:%s)" % (self.pivot, self.members)

class Cell(object):
    def __init__(self, x, y):
        super(Cell, self).__init__()
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

def json_cell2tuple(json_cell):
    return Cell(json_cell["x"], json_cell["y"])

class Board(object):
    def __init__(self, width, height, filled):
        super(Board, self).__init__()
        self.width = width
        self.height = height
        self._board = [[0] * height for x in range(width)]
        for full in filled:
            self._board[full.x][full.y] = 1
        self.unit = None
        self.finished = False

    def spawn(self, unit):
        tm = unit.get_topmost()
        lm = unit.get_leftmost()
        rm = unit.get_rightmost()
        pad_top = 0
        pad_left = (self.width - (rm.x - lm.x + 1)) / 2
        unit.pos = Cell(pad_left, pad_top)

        if unit.can_be_placed(self):
            self.unit = unit
        else:
            self.finished = True

    def lock(self):
        if self.unit:
            for m in self.unit.members:
                self._board[m.x + self.unit.pos.x][m.y + self.unit.pos.y] = 1
            self.unit = None
            self.clear_rows()

    def clear_rows(self):
        # UGLY AS HELL
        for y in range(self.height)[::-1]:
            while self.row_is_filled(y):
                for x in range(self.width):
                    self._board[x][y] = 0
                for yy in range(y)[::-1]:
                    for x in range(self.width):
                        self._board[x][yy + 1] = self.get(x, yy)

    def row_is_filled(self, row):
        summ = 0
        for x in range(self.width):
            summ += self.get(x, row)
        if summ >= self.width:
            return True
        return False


    def is_finished(self):
        return self.finished

    def get_adjacent(self, x, y):
        return []

    def move_e(self):
        if self.unit is None:
            return ""
        unit_copy = copy.deepcopy(self.unit)
        unit_copy.move_e()
        if unit_copy.can_be_placed(self):
            self.unit.move_e()
            return "e"
        else:
            self.lock()
            return "c"

    def move_w(self):
        if self.unit is None:
            return ""
        unit_copy = copy.deepcopy(self.unit)
        unit_copy.move_w()
        if unit_copy.can_be_placed(self):
            self.unit.move_w()
            return "!"
        else:
            self.lock()
            return "!"

    def move_se(self):
        if self.unit is None:
            return ""
        unit_copy = copy.deepcopy(self.unit)
        unit_copy.move_se()
        if unit_copy.can_be_placed(self):
            self.unit.move_se()
            return "m"
        else:
            self.lock()
            return "n"

    def move_sw(self):
        if self.unit is None:
            return ""
        unit_copy = copy.deepcopy(self.unit)
        unit_copy.move_sw()
        if unit_copy.can_be_placed(self):
            self.unit.move_sw()
            return "i"
        else:
            self.lock()
            return "j"

    def get(self, x, y):
        return self._board[x][y]

    def __str__(self):
        board_copy = copy.deepcopy(self._board)
        if self.unit:
            for m in self.unit.members:
                board_copy[m.x + self.unit.pos.x][m.y + self.unit.pos.y] = 2
        buf = []
        for y in range(self.height):
            line = ""
            if y % 2 == 1:
                line = " "
            for x in range(self.width):
                line = line + str(board_copy[x][y]) + " "
            buf.append(line)
        return "\n".join(buf)

