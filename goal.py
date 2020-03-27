"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Optional, Union
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement Me
    colours, goals = COLOUR_LIST[:], [PerimeterGoal, BlobGoal]
    random.shuffle(colours)
    result = []

    # TT: colour list of identical colours
    for i in range(num_goals):
        # choose a random goal type
        chosen_g = random.choice(goals)
        if not result:
            if chosen_g == BlobGoal:
                chosen_g = BlobGoal(colours[i])
            else:
                chosen_g = PerimeterGoal(colours[i])
            # Goal.__init__(chosen_g, colours[i])
            result.append(chosen_g)

        # check if color already in list
        elif result[i - 1].colour != colours[i]:
            if chosen_g == BlobGoal:
                chosen_g = BlobGoal(colours[i])
            else:
                chosen_g = PerimeterGoal(colours[i])
            result.append(chosen_g)

    return result


def _grid(flattened: List[List[Tuple[int, int, int]]]) -> List[List[int]]:
    """Returns a flattened block with -1 in the position of each cell."""
    r = []
    for i in range(len(flattened)):
        column = []
        for j in range(len(flattened)):
            column.append(-1)
        r.append(column)
    return r


def _get_unchecked(visited: list) -> List[List[Optional[int]]]:
    """ Returns a list parallel to visited that contains the index of cells with
    -1 as its value. """
    r = []
    for i in range(len(visited)):
        column = []
        for j in range(len(visited)):
            if visited[i][j] == -1:
                column.append(j)
        r.append(column)
    return r


def _get_pos(index: List[List[Optional[int]]]) -> List[Tuple[int, int]]:
    """ Returns a list of tuples containing positions of parallel to visited that
    contains the value -1. """
    l = []
    for i in range(len(index)):
        for j in range(len(index)):
            if index[i] != []:
                l.append((i, j))
    return l


def _decolumnise(block: Union[List[Tuple],
                              List[List[Tuple]]]) -> List[Tuple[int, int, int]]:
    """Return a list representing the raw colours in this <block>, flattening
    the columns."""
    lst = []
    for b in block:
        if not isinstance(b, list):
            lst.append(b)
        else:
            lst.extend(_decolumnise(b))
    return lst


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement me
    # TT: Must test on board with depth >= 3 and diff depths
    if block.colour is not None:
        res = []
        for i in range(2 ** (block.max_depth - block.level)):
            cell = []
            for j in range(2 ** (block.max_depth - block.level)):
                cell.append(block.colour)
            res.append(cell)
        return res

    else:
        # Recursive case: block has children
        size, res = 2 ** (block.max_depth - block.level), []

        # Reorder them based on the order of the output
        blockies = block.children[1], block.children[2], \
                   block.children[0], block.children[3]

        i = 0
        # Make a column and append it to res
        while i < 4:
            # Flatten and take adjacent blockies out of their columns
            curr, next = _flatten(blockies[i]), _flatten(blockies[i + 1])
            c, n = _decolumnise(curr), _decolumnise(next)

            # Make columns with adjacent top and bottom blockies
            start, end = 0, size // 2
            while start < len(c):
                top, bottom = c[start:end], n[start:end]
                col = top + bottom
                res.append(col)
                start, end = start + size // 2, end + size // 2
            i += 2

        return res


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    def score(self, board: Block) -> int:
        """Returns the number of blocks of the target colour that are in the
        perimeter of the board."""
        # TODO: Implement me
        b = _flatten(board)
        score = 0
        for i in range(len(b)):
            # Check if colour is in a corner spot
            if i == 0 or i == len(b) - 1:
                score += b[i].count(self.colour)
                if b[i][0] == self.colour:
                    score += 1
                if b[i][-1] == self.colour:
                    score += 1

            else:
                # We are at a middle column
                if b[i][0] == self.colour:
                    score += 1
                if b[i][-1] == self.colour:
                    score += 1
        return score

    def description(self) -> str:
        # TODO: Implement me
        return f'Get as many blocks of colour {colour_name(self.colour)} on ' \
               f'the perimeter of the board'


class BlobGoal(Goal):
    def score(self, board: Block) -> int:
        """Returns the score of the number of target coloured blocks in larger
        connected blocks of the same colour."""
        # TODO: Implement me
        b = _flatten(board)

        # Make parallel structure for visited
        visited = _grid(b)
        _max = []

        # Start with top left
        for i in range(len(b)):
            for j in range(len(b)):
                pos = i, j
                # Get the largest blob starting from pos
                if visited[i][j] == -1:
                    _max.append(self._undiscovered_blob_size(pos, b, visited))

        return max(_max)

        # visited = _grid(b)
        # count = 0
        # index = _get_unchecked(visited)
        # pos = _get_pos(index)
        # while pos:
        #     count += self._undiscovered_blob_size(pos[0], b, visited)
        #     index = _get_unchecked(visited)
        #     pos = _get_pos(index)
        # return count

    def _go_left(self, pos: Tuple[int, int],
                 board: List[List[Tuple[int, int, int]]],
                 visited: List[List[int]], size: int) -> bool:
        """ Returns True if you are able to go left from pos and updates
        size"""
        i, j = pos[0], pos[1]
        if j + 1 not in range(len(board)):
            return False
        elif board[i][j + 1] in range(len(board)) and visited[i][j + 1] == -1:
            if board[i][j + 1] == self.colour:
                visited[i][j + 1] = 1
                size += 1
                return True
            else:
                visited[i][j + 1] = 0
                return False

    def _go_down(self, pos: Tuple[int, int],
                 board: List[List[Tuple[int, int, int]]],
                 visited: List[List[int]], size: int) -> bool:
        """ Returns True if you are able to go down from pos and updates
        size"""
        i, j = pos[0], pos[1]
        if i + 1 not in range(len(board)):
            return False

        elif board[i + 1][j] in range(len(board)) and visited[i + 1][j] == -1:
            if board[i + 1][j] == self.colour:
                visited[i + 1][j] = 1
                size += 1
                return True
            else:
                visited[i + 1][j] = 0
                return False

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # TODO: Implement me
        i, j = pos[0], pos[1]
        if i not in range(len(board)) or j not in range(len(board)):
            return 0

        elif board[i][j] != self.colour:
            visited[i][j] = 0
            return 0

        elif visited[i][j] == 0 or visited[i][j] == 1:
            return 0


        else:
            # We know that pos is of target colour
            visited[i][j] = 1
            return 1 + self._undiscovered_blob_size((i+1, j), board, visited) +\
                self._undiscovered_blob_size((i-1, j), board, visited) + \
                self._undiscovered_blob_size((i, j+1), board, visited) + \
                self._undiscovered_blob_size((i, j-1), board, visited)

            # i1, j1 = i, j
            # while i1 < len(board) and j1 < len(board):
            #     # If the adjacent cell is of colour and not visited
            #     if self._go_left((i1, j1+1), board, visited, size) or \
            #             i1 + 1 == len(board):
            #         size += self._undiscovered_blob_size((i1, j1 + 1),
            #                                              board, visited)
            #         j1 += 1
            #
            #     if self._go_down((i1 + 1, j1), board, visited, size) or \
            #             j1 + 1 == len(board):
            #         size += self._undiscovered_blob_size((i1 + 1, j1), board,
            #                                              visited)
            #         i1 += 1
            #
            # return size
            # if board[i1+1][j1] == self.colour and \
            #         visited[i1+1][j1] == -1:
            #     size += self._undiscovered_blob_size((i1, j1+1),
            #                                          board, visited)
            #     visited[i1 + 1][j1] = 1
            #     i1 += 1
            #
            # if board[i1][j1+1] == self.colour and \
            #         visited[i1][j1+1] == -1:
            #     size += self._undiscovered_blob_size((i1, j1+1),
            #                                          board, visited)
            #     visited[i1][j1 + 1] = 1
            #     j1 += 1
            #
            # else:
            #     # We know we have to go down a column
            #     i1 += 1

    # # use this helper to check the surroundings of pos and whether in blob
    # i, j = pos[0], pos[1]
    # _max = len(board) - 1
    # colour = board[i][j]
    # # check if cell at pos is out of range
    # if i not in range(len(board)) or j not in range(len(board)):
    #     return 0
    # # check if pos in colour
    # else:
    #     count = 0
    #     count += self._check_surroundings(count, pos, board, visited)
    # return count

    # if self._undiscovered_blob_size((pos), board, visited) == 0:
    #     pass
    #     # stop
    # # if undiscovered blob at j+ 1 == 0: stop
    # else:
    #     # undiscovered blob at i + 1 == 1:
    #     count += self._undiscovered_blob_size((pos), board, visited)
    #     # count += undiscovered blob i + 1

    # def _visit(self, i: int, j: int, board: List[List[Tuple[int, int, int]]],
    #            visited: List[List[int]]) ->  int:
    #     """ Updates visited as it is used in _undiscovered_blob."""
    #     p = visited[i][j]
    #     colour = board[i][j]
    #     if p == - 1 and self.colour == colour:
    #         visited[i][j] = 1
    #         return 1
    #     else:
    #         visited[i][j] = 0
    #         return 0
    #
    # def _corner_check(self, total: int, pos: Tuple[int, int],
    #                   board: List[List[Tuple[int, int, int]]],
    #                   visited: List[List[int]]) -> Tuple[bool, int]:
    #     """Checks the left, right, above and bottom cell from cell based on
    #     its position to check if it is of the target colour and returns
    #     the value."""
    #
    #     i, j = pos[0], pos[1]
    #     _max = len(board) - 1
    #     count = total
    #     a = self._visit(i, j-1, board, visited)
    #     r = self._visit(i + 1, j, board, visited)
    #     b = self._visit(i, j + 1, board, visited)
    #     l = self._visit(i - 1 , j, board, visited)
    #
    #     # Top left corner --> check right and bottom
    #     if i == 0 and j == 0:
    #         if r and b == 0:
    #             return False, count
    #         else:
    #             count += r
    #             count += b
    #             return True, count
    #
    #     #Top right corner --> check left and bottom
    #     elif i == _max and j == 0:
    #         if l and b == 0:
    #             return False, count
    #         else:
    #             count += l
    #             count += b
    #             return True, count
    #
    #     # Bottom left corner --> check above and right
    #     elif i == 0 and j == _max:
    #         if a and r == 0:
    #             return False, count
    #         else:
    #             count += a
    #             count += r
    #             return True, count
    #
    #     # Bottom right corner --> check left and above
    #     elif i == _max and j == _max:
    #         if a and l == 0:
    #             return (False, count)
    #         else:
    #             count += l
    #             count += a
    #             return True, count
    #     else:
    #         return (False, count)
    #
    #
    # def _side_check(self, total: int, pos: Tuple[int, int],
    #                 board: List[List[Tuple[int, int, int]]],
    #                 visited: List[List[int]]) -> Tuple[bool, int]:
    #     """Checks the left, right, above and bottom cell from cell based on
    #     its position to check if it is of the target colour and returns
    #     the value."""
    #
    #     i, j = pos[0], pos[1]
    #     _max = len(board) - 1
    #     count = total
    #     a = self._visit(i, j-1, board, visited)
    #     r = self._visit(i + 1, j, board, visited)
    #     b = self._visit(i, j + 1, board, visited)
    #     l = self._visit(i - 1 , j, board, visited)
    #
    #     # Left side, no corner --> r, b, a
    #     if i == 0 and (j != 0 and j!= _max):
    #         if r and b  and a == 0:
    #             return (False, count)
    #         else:
    #             count += r
    #             count += b
    #             count += a
    #             return (True, count)
    #
    #     #Right side no corner --> l, b, a
    #     elif i == _max and (j != 0 and j!= _max):
    #         if l and b  and a== 0:
    #             return (False, count)
    #         else:
    #             count += l
    #             count += b
    #             count += a
    #             return (True, count)
    #
    #     # Bottom side no corner --> a, r, l
    #     elif j == _max and (i != 0 and i != _max):
    #         if a and r and l == 0:
    #             return (False, count)
    #         else:
    #             count += a
    #             count += r
    #             count += l
    #             return (True, count)
    #
    #     # Top side no corner --> b, r, l
    #     elif j == 0 and (i != 0 and i != _max):
    #         if a and l == 0:
    #             return (False, count)
    #         else:
    #             count += r
    #             count += b
    #             count += l
    #             return (True, count)
    #     else:
    #         return (False, count)
    #
    # def _mid_check(self, total: int, pos: Tuple[int, int],
    #                board: List[List[Tuple[int, int, int]]],
    #                visited: List[List[int]]) -> int:
    #     """Checks the left, right, above and bottom cell from cell if it is of
    #     the target colour and returns the value."""
    #     i, j = pos[0], pos[1]
    #     _max = len(board) - 1
    #     count = total
    #     a = self._visit(i, j-1, board, visited)
    #     r = self._visit(i + 1, j, board, visited)
    #     b = self._visit(i, j + 1, board, visited)
    #     l = self._visit(i - 1 , j, board, visited)
    #
    #     # We know that checking if the pos is in middle is last option
    #     count += r
    #     count += b
    #     count += a
    #     count += l
    #     return count
    #
    #
    # def _check_surroundings(self, total: int, pos: Tuple[int, int],
    #                         board: List[List[Tuple[int, int, int]]],
    #                         visited: List[List[int]]) -> int:
    #     """Checks the surrounding cells if it is of the target colour."""
    #     c = self._corner_check(total, pos, board, visited)
    #     s = self._side_check(total, pos, board, visited)
    #     m = self._mid_check(total, pos, board, visited)
    #     total = total
    #     # if not corner: check side
    #         # else total += corner
    #     # if not side check mid
    #         #else total += side
    #     if not c[0]:
    #         if not s[0]:
    #             total += m
    #         else:
    #             total += s[1]
    #     else:
    #         total += c[1]
    #     return total

    def description(self) -> str:
        # TODO: Implement me
        return f'Get the largest *connected* blob of colour ' \
               f'{colour_name(self.colour)}'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
