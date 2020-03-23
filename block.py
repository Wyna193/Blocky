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

This file contains the Block class, the main data structure used in the game.
"""
from __future__ import annotations

import random
from typing import List, Optional, Tuple

from math import exp
from settings import COLOUR_LIST, colour_name


def generate_board(max_depth: int, size: int) -> Block:
    """Return a new game board with a depth of <max_depth> and dimensions of
    <size> by <size>.

    >>> board = generate_board(3, 750)
    >>> board.max_depth
    3
    >>> board.size
    750
    >>> len(board.children) == 4
    True
    """
    board = Block((0, 0), size, random.choice(COLOUR_LIST), 0, max_depth)
    board.smash()

    return board


class Block:
    """A square Block in the Blocky game, represented as a tree.

    In addition to its tree-related attributes, a Block also contains attributes
    that describe how the Block appears on a Cartesian plane. All positions
    describe the upper left corner (x, y), and the origin is at (0, 0). All
    positions and sizes are in the unit of pixels.

    When a block has four children, the order of its children impacts each
    child's position. Indices 0, 1, 2, and 3 are the upper-right child,
    upper-left child, lower-left child, and lower-right child, respectively.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
    size:
        The height and width of this square Block.
    colour:
        If this block is not subdivided, <colour> stores its colour. Otherwise,
        <colour> is None.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero. If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    children:
        The blocks into which this block is subdivided. The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.

    === Representation Invariants===
    - len(children) == 0 or len(children) == 4
    - If this Block has children:
        - their max_depth is the same as that of this Block.
        - their size is half that of this Block.
        - their level is one greater than that of this Block.
        - their position is determined by the position and size of this Block,
          and their index in this Block's list of children.
        - this Block's colour is None.
    - If this Block has no children:
        - its colour is not None.
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    children: List[Block]

    def __init__(self, position: Tuple[int, int], size: int,
                 colour: Optional[Tuple[int, int, int]], level: int,
                 max_depth: int) -> None:
        """Initialize this block with <position>, dimensions <size> by <size>,
        the given <colour>, at <level>, and with no children.

        Preconditions:
            - position[0] >= 0 and position[1] >= 0
            - size > 0
            - level >= 0
            - max_depth >= level
        """
        self.position = position
        self.size = size
        self.colour = colour
        self.level = level
        self.max_depth = max_depth
        self.children = []

    def __str__(self) -> str:
        """Return this Block in a string format.
        """
        if len(self.children) == 0:
            indents = '\t' * self.level
            colour = colour_name(self.colour)
            return f'{indents}Leaf: colour={colour}, pos={self.position}, ' \
                   f'size={self.size}, level={self.level}\n'
        else:
            indents = '\t' * self.level
            result = f'{indents}Parent: pos={self.position},' \
                     f'size={self.size}, level={self.level}\n'

            for child in self.children:
                result += str(child)

            return result

    def __eq__(self, other: Block) -> bool:
        """Return True iff this Block and all its descendents are equivalent to
        the <other> Block and all its descendents.
        """
        if len(self.children) == 0 and len(other.children) == 0:
            # Both self and other are leaves.
            return self.position == other.position and \
                   self.size == other.size and \
                   self.colour == other.colour and \
                   self.level == other.level and \
                   self.max_depth == other.max_depth
        elif len(self.children) != len(other.children):
            # One of self or other is a leaf while the other is not.
            return False
        else:
            # Both self and other have four children.
            for i in range(4):
                # The != operator also uses the __eq__ special method.
                if self.children[i] != other.children[i]:
                    return False

            return True

    def _child_size(self) -> int:
        """Return the size of this Block's children.
        """
        return round(self.size / 2.0)

    def _children_positions(self) -> List[Tuple[int, int]]:
        """Return the positions of this Block's four children.

        The positions are returned in this order: upper-right child, upper-left
        child, lower-left child, lower-right child.
        """
        x = self.position[0]
        y = self.position[1]
        size = self._child_size()

        return [(x + size, y), (x, y), (x, y + size), (x + size, y + size)]

    def _update_children_positions(self, position: Tuple[int, int]) -> None:
        """Set the position of this Block to <position> and update all its
        descendants to have positions consistent with this Block's.

        <position> is the (x, y) coordinates of the upper-left corner of this
        Block.
        """
        # TODO: Implement me

        # use _children_position to get the positions of children
        child_pos = self._children_positions()
        self.position = position
        # set the children Blocks with positions as appropriate
        for i in range(len(self.children)):
            self.children[i].position = child_pos[i]

    def smashable(self) -> bool:
        """Return True iff this block can be smashed.

        A block can be smashed if it has no children and its level is not at
        max_depth.
        """
        return self.level != self.max_depth and len(self.children) == 0

    def smash(self) -> bool:
        """Sub-divide this block so that it has four randomly generated
        children.

        If this Block's level is <max_depth>, do nothing. If this block has
        children, do nothing.

        Return True iff the smash was performed.
        """

        # TODO: Implement me
        if not self.smashable():
            return False

        else:
            self.colour = None
            child_pos = self._children_positions()

            # Append self.children with 4 blocks
            for i in range(4):
                b = Block(child_pos[i], self._child_size(),
                          random.choice(COLOUR_LIST), self.level + 1,
                          self.max_depth)
                self.children.append(b)

            # Determine if each blocky can be smashed further
            num = random.random()
            for blocky in self.children:
                if num < exp(-0.25 * self.level):
                    # Subdivide this blocky
                    blocky.smash()

                else:
                    # Set this blocky's colour to a random one
                    self.colour = random.choice(COLOUR_LIST)
            return True

    def swap(self, direction: int) -> bool:
        """Swap the child Blocks of this Block.

        If this Block has no children, do nothing. Otherwise, if <direction> is
        1, swap vertically. If <direction> is 0, swap horizontally.

        Return True iff the swap was performed.

        Precondition: <direction> is either 0 or 1
        """
        # TODO: Implement me
        # Base case: Block has no children
        if self.children: # block has children and we're swapping them
            cp = self._children_positions() # a list of children's position
            tr, tl ,bl, br = cp[0], cp[1], cp[2], cp[3]
            # Swap Vertically
            if direction == 1:
                for block in self.children:
                    #Case: child has no children --> directly swap
                    if not block.children:
                        if block == self.children[0]:
                            block.position = br
                        elif block == self.children[1]:
                            block.position = bl
                        elif block == self.children[2]:
                            block.position = tl
                        else:
                            block.position = tr
                    else:
                        # we know that this block has children
                        if block == self.children[0]:
                            block.position = br
                            block._update_children_positions(br)
                        elif block == self.children[1]:
                            block.position = bl
                            block._update_children_positions(bl)
                        elif block == self.children[2]:
                            block.position = tl
                            block._update_children_positions(tl)
                        else:
                            block.position = tr
                            block._update_children_positions(tr)
                self.children = [self.children[3], self.children[2],
                                 self.children[1], self.children[0]]
                return True
            # Swap Horizontally
            else:
                for block in self.children:
                    #Case: child has no children --> directly swap
                    if not block.children:
                        if block == self.children[0]:
                            block.position = tl
                        elif block == self.children[1]:
                            block.position = tr
                        elif block == self.children[2]:
                            block.position = br
                        else:
                            block.position = bl
                    else:
                        # we know that this block has children
                        if block == self.children[0]:
                            block.position = tl
                            block._update_children_positions(tl)
                        elif block == self.children[1]:
                            block.position = tr
                            block._update_children_positions(tr)
                        elif block == self.children[2]:
                            block.position = br
                            block._update_children_positions(br)
                        else:
                            block.position = bl
                            block._update_children_positions(bl)
                self.children = [self.children[1], self.children[0],
                                 self.children[3], self.children[2]]
                return True
        else:
            return False

    def rotate(self, direction: int) -> bool:
        """Rotate this Block and all its descendants.

        If this Block has no children, do nothing. If <direction> is 1, rotate
        clockwise. If <direction> is 3, rotate counter-clockwise.

        Return True iff the rotate was performed.

        Precondition: <direction> is either 1 or 3.
        """
        # TODO: Implement me
        if self.children:
            cp = self._children_positions() # a list of children's position
            tr, tl ,bl, br = cp[0], cp[1], cp[2], cp[3]
            # Clockwise rotation
            if direction == 1:
                for block in self.children:
                    # Case 1: Block has no children
                    if block.colour:
                    # Directly move the block into position
                        if block == self.children[0]:
                            block.position = br
                        elif block == self.children[1]:
                            block.position = tr
                        elif block == self.children[2]:
                            block.position = tl
                        else:
                            block.position = bl
                    # Case 2: Block has children
                    else:
                        block.rotate(direction)
                self.children = [self.children[1], self.children[2],
                                 self.children[3], self.children[0]]
                return True

            # Counter-clockwise rotation
            else:
                for block in self.children:
                    # Case 1: Block has no children
                    if block.colour is not None:
                    # Directly move the block into position
                        for block in self.children:
                            if block == self.children[0]:
                                block.position = tr
                            elif block == self.children[1]:
                                block.position = bl
                            elif block == self.children[2]:
                                block.position = br
                            else:
                                block.position = tl
                    # Case 2: Block has children
                    else:
                        block.rotate(direction)
                self.children = [self.children[1], self.children[2],
                                 self.children[3], self.children[0]]
                return True
        else:
            # Block has no children so nothing is done
            return False

    def paint(self, colour: Tuple[int, int, int]) -> bool:
        """Change this Block's colour iff it is a leaf at a level of max_depth
        and its colour is different from <colour>.

        Return True iff this Block's colour was changed.
        """
        # TODO: Implement me
        # Base Case: Not at max_depth and not leaf
            # max_depth cannot have children; if has children, not max
        if self.level != self.max_depth or self.children:
            return False
        else:
            # We know that it has no children and is at max_depth
            # Case 1: is at colour
            if self.colour == colour:
                return False
            else:
                self.colour = colour
                return True

    def combine(self) -> bool:
        """Turn this Block into a leaf based on the majority colour of its
        children.

        The majority colour is the colour with the most child blocks of that
        colour. A tie does not constitute a majority (e.g., if there are two red
        children and two blue children, then there is no majority colour).

        If there is no majority colour, do nothing. If this block is not at a
        level of max_depth - 1, or this block has no children, do nothing.

        Return True iff this Block was turned into a leaf node.
        """
        # TODO: Implement me
        # Base Case: # not at max_depth -1 or has no children
        if self.level != self.max_depth - 1 or not self.children:
            return False
        # block must be at max_depth -1 and have children
        else:
            pass
            # We know this block is at max_depth -1 and has children
            # get colours and find majority
            colours = {}
            for child in self.children:
                if child.colour not in colours:
                    colours[child.colour] = 1
                else:
                    colours[child.colour] += 1
            # Case 1: All different colours or tied
            if len(colours) == 4 or len(colours) == 2:
                return False
            # Case 2: There is a majority
            else:
                colour = max(colours, key=colours.get())
                self.children = []
                self.colour = colour
                return True  # FIXME

    def create_copy(self) -> Block:
        """Return a new Block that is a deep copy of this Block.

        Remember that a deep copy has new blocks (not aliases) at every level.
        """
        # TODO: Implement me
        # no aliasing --> always make new blocks
        copy = Block()
        copy.position = self.position
        copy.size = self.size
        copy.level = self.level
        copy.max_depth = self.max_depth
        if self.children:
            for child in self.children:
                copy.children.append(child.create_copy())
        return copy


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', '__future__', 'math',
            'settings'
        ],
        'max-attributes': 15,
        'max-args': 6
    })

    # This is a board consisting of only one block.
    b1 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    print("=== tiny board ===")
    print(b1)

    # Now let's make a random board.
    b2 = generate_board(3, 750)
    print("\n=== random board ===")
    print(b2)
