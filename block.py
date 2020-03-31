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


def _update_descendents(block: Block) -> None:
    """Update position of block's descendants, given that blocky has kids. """
    # blocky's position is already changed in the methods
    for blocky in block.children:
        if blocky.children:
            blocky._update_children_positions(blocky.position)


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

    def _swap_vertical(self) -> None:
        """Swaps the contents of block by reflecting on the x axis."""
        cp = self._children_positions()  # a list of children's position
        tr, tl, bl, br = cp[0], cp[1], cp[2], cp[3]
        for block in self.children:
            # Case: child has no children --> directly swap
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
                    _update_descendents(block)
                elif block == self.children[1]:
                    block.position = bl
                    block._update_children_positions(bl)
                    _update_descendents(block)
                elif block == self.children[2]:
                    block.position = tl
                    block._update_children_positions(tl)
                    _update_descendents(block)
                else:
                    block.position = tr
                    block._update_children_positions(tr)
                    _update_descendents(block)

        # once all the blockies' position are changed, put them in right order
        self.children = [self.children[3], self.children[2],
                         self.children[1], self.children[0]]

    def _swap_horizontal(self) -> None:
        """Swaps the contents of block by reflecting on the y axis."""
        cp = self._children_positions()  # a list of children's position
        tr, tl, bl, br = cp[0], cp[1], cp[2], cp[3]
        for block in self.children:
            # Case: child has no children --> directly swap
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
                    _update_descendents(block)
                elif block == self.children[1]:
                    block.position = tr
                    block._update_children_positions(tr)
                    _update_descendents(block)
                elif block == self.children[2]:
                    block.position = br
                    block._update_children_positions(br)
                    _update_descendents(block)
                else:
                    block.position = bl
                    block._update_children_positions(bl)
                    _update_descendents(block)

        self.children = [self.children[1], self.children[0],
                         self.children[3], self.children[2]]

    def swap(self, direction: int) -> bool:
        """Swap the child Blocks of this Block.

        If this Block has no children, do nothing. Otherwise, if <direction> is
        1, swap vertically. If <direction> is 0, swap horizontally.

        Return True iff the swap was performed.

        Precondition: <direction> is either 0 or 1
        """
        # TODO: Implement me
        # Base case: Block has no children
        if not self.children:
            return False
        else:
            # block has children and we're swapping them
            if direction == 0:
                pos = self._children_positions()

                self.children[0].position, \
                self.children[1].position, \
                self.children[2].position, \
                self.children[3].position = pos[1], pos[0], pos[3], pos[2]

                self.children = [self.children[1], self.children[0],
                                 self.children[3], self.children[2]]
            else:
                # direction == 1

                pos = self._children_positions()

                self.children[0].position, \
                self.children[1].position, \
                self.children[2].position, \
                self.children[3].position = pos[3], pos[2], pos[1], pos[0]

                self.children = [self.children[3], self.children[2],
                                 self.children[1], self.children[0]]

            for block in self.children:
                block.swap(direction)
                # block._update_children_positions(block.position)

            return True

            # # Swap Vertically
            # if direction == 1:
            #     self._swap_vertical()
            #     return True
            # # Swap Horizontally
            # else:
            #     self._swap_horizontal()
            #     return True

    def _cw_rotation(self, direction) -> None:
        """The clockwise rotation of blocks and its descendants"""
        # We know that block must have children in order to be rotated
        cp = self._children_positions()  # a list of children's position
        tr, tl, bl, br = cp[0], cp[1], cp[2], cp[3]
        for block in self.children:
            # need to change position of block before recursing into children
            if block == self.children[0]:
                block.position = br
                _update_descendents(block)
            elif block == self.children[1]:
                block.position = tr
                _update_descendents(block)
            elif block == self.children[2]:
                block.position = tl
                _update_descendents(block)
            else:
                block.position = bl
                _update_descendents(block)
            # recurse to rotate little blockies
            block.rotate(direction)

        # once all blockies' are in right position, set right order
        self.children = [self.children[1], self.children[2],
                         self.children[3], self.children[0]]

    def _ccw_rotation(self, direction) -> None:
        """The counterclockwise rotation of block and its descendants."""
        # We know that block must have children in order to be rotated
        cp = self._children_positions()  # a list of children's position
        tr, tl, bl, br = cp[0], cp[1], cp[2], cp[3]
        for block in self.children:
            if block == self.children[0]:
                block.position = tr
                _update_descendents(block)
            elif block == self.children[1]:
                block.position = bl
                _update_descendents(block)
            elif block == self.children[2]:
                block.position = br
                _update_descendents(block)
            else:
                block.position = tl
                _update_descendents(block)
            # recurse through little blockies
            block.rotate(direction)

        self.children = [self.children[1], self.children[2],
                         self.children[3], self.children[0]]

    def rotate(self, direction: int) -> bool:
        """Rotate this Block and all its descendants.

        If this Block has no children, do nothing. If <direction> is 1, rotate
        clockwise. If <direction> is 3, rotate counter-clockwise.

        Return True iff the rotate was performed.

        Precondition: <direction> is either 1 or 3.
        """
        # TODO: Implement me
        # Case 1: Blocky has no children
        if not self.children:
            return False

        # Case 2: Blocky has children
        else:
            # if direction == 1:
            #     self._cw_rotation(direction)
            #     return True
            # # direction == 3
            # else:
            #     self._ccw_rotation(direction)
            #     return True

            if direction == 1:
                pos = self._children_positions()
                self.children[0].position, \
                self.children[1].position, \
                self.children[2].position, \
                self.children[3].position = pos[3], pos[0], pos[1], pos[2]

                self.children = [self.children[1], self.children[2],
                                 self.children[3], self.children[0]]

            else:
                # direction == 3
                pos = self._children_positions()
                self.children[0].position, \
                self.children[1].position, \
                self.children[2].position, \
                self.children[3].position = pos[0], pos[2], pos[3], pos[1]

                self.children = [self.children[3], self.children[0],
                                 self.children[1], self.children[2]]

            for block in self.children:
                block.rotate(direction)

            return True

    def paint(self, colour: Tuple[int, int, int]) -> bool:
        """Change this Block's colour iff it is a leaf at a level of max_depth
        and its colour is different from <colour>.

        Return True iff this Block's colour was changed.
        """
        # TODO: Implement me
        if self.level == self.max_depth and not self.children:
            if self.colour == colour:
                return False
            else:
                self.colour = colour
                return True
        else:
            return False

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

        if self.level == self.max_depth - 1 and self.children:
            colours = {}

            for block in self.children:
                if block.colour not in colours:
                    colours[block.colour] = 1
                else:
                    colours[block.colour] += 1

            if max(colours.values()) > 2:
                colour = max(colours, key=colours.get)
                self.children = []
                self.colour = colour
                return True
            return False
        else:
            return False

    def create_copy(self) -> Block:
        """Return a new Block that is a deep copy of this Block.

        Remember that a deep copy has new blocks (not aliases) at every level.
        """
        # TODO: Implement me
        if not self.children:
            return Block(self.position, self.size, self.colour, self.level,
                         self.max_depth)

        else:
            b = Block(self.position, self.size, self.colour, self.level,
                      self.max_depth)

            for bby in self.children:
                b.children.append(bby.create_copy())

            return b


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
