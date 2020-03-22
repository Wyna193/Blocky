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
from typing import List, Tuple
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
            # * incorrect instantiation?
            Goal.__init__(chosen_g, colours[i])
            result.append(chosen_g)

        # check if color already in list
        elif result[i - 1].colour != colours[i]:
            Goal.__init__(chosen_g, colours[i])
            result.append(chosen_g)

    return result

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
        for i in range(2**(block.max_depth - block.level)):
            cell = []
            for j in range(2**(block.max_depth - block.level)):
                cell.append(block.colour)
            res.append(cell)
        return res

    else:
        # Recursive case: block has children
        size, res = 2**(block.max_depth - block.level), []

        # Reorder them based on the order of the output
        blockies = block.children[1], block.children[2],\
                   block.children[0], block.children[3]

        i = 0
        # Make a column and append it to res
        while i < 4:
            # Flatten and take adjacent blockies out of their columns
            curr, next = _flatten(blockies[i]), _flatten(blockies[i+1])
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
        # TODO: Implement me
        b = _flatten(board)

    def description(self) -> str:
        # TODO: Implement me
        return f'Get as many blocks of colour {self.colour} on the perimeter' \
               f'of the board'


class BlobGoal(Goal):
    def score(self, board: Block) -> int:
        # TODO: Implement me
        b = _flatten(board)

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
        pass  # FIXME

    def description(self) -> str:
        # TODO: Implement me
        return f'Get the largest *connected* blob of colour {self.colour}'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
