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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains some sample tests for Assignment 2.
Please use this as a starting point to check your work and write your own
tests!
"""
from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten, generate_goals, _grid
from player import Player, _get_block, create_players
from renderer import Renderer
from settings import COLOUR_LIST
from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE

def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)


@pytest.fixture
def renderer() -> Renderer:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    return Renderer(750)


@pytest.fixture
def child_block() -> Block:
    """Create a reference child block with a size of 750 and a max_depth of 0.
    """
    return Block((0, 0), 750, COLOUR_LIST[0], 0, 0)

@pytest.fixture
def board_no_children() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, COLOUR_LIST[1], 0, 2)
    return board

@pytest.fixture
def board_1x1() -> Block:
    """Create a reference board with a size of 750 that is at max_depth"""
    board = Block((0, 0), 375, COLOUR_LIST[1], 0, 0)
    return board

@pytest.fixture
def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def board_16x16_swap1() -> Block:
    """Create a reference board that is swapped along the vertical plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    return board


@pytest.fixture
def board_16x16_rotate1() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_rotate3() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated counter-clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_paint() -> Block:
    """Create a reference board where the top-right block on level 2 is painted.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_copy() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_combine() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    return board


@pytest.fixture
def flattened_board_16x16() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]

@pytest.fixture
def flattened_board_16x16_max() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    a, b, c, d = COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]
    return [
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [c, c, c, c, c, c, c, c, b, b, b, b, b, b, b, b],
        [b, b, b, b, b, b, b, b, d, d, d, d, d, d, d, d],
        [b, b, b, b, b, b, b, b, d, d, d, d, d, d, d, d],
        [b, b, b, b, b, b, b, b, d, d, d, d, d, d, d, d],
        [b, b, b, b, b, b, b, b, d, d, d, d, d, d, d, d],
        [a, a, a, a, d, d, d, d, d, d, d, d, d, d, d, d],
        [a, a, a, a, d, d, d, d, d, d, d, d, d, d, d, d],
        [a, a, a, a, d, d, d, d, d, d, d, d, d, d, d, d],
        [a, a, a, a, d, d, d, d, d, d, d, d, d, d, d, d]
    ]
@pytest.fixture
def visited_board_16x16() -> List[List[int]]:
    """Create a list of -1 parallel to a flattened board."""
    return [
        [-1, -1, -1, -1],
        [-1, -1, -1, -1],
        [-1, -1, -1, -1],
        [-1, -1, -1, -1]
    ]


@pytest.fixture
def board_16x16_perimeter() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, None, None, None]
    set_children(board, colours)

    # Level 2
    colours0 = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]]
    set_children(board.children[0], colours0)

    colours1 = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[0]]
    set_children(board.children[1], colours1)

    colours2 = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board.children[2], colours2)

    colours3 = [COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board.children[3], colours3)

    return board


@pytest.fixture
def board_16x16_blobby() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, None, None, None]
    set_children(board, colours)

    # Level 2
    colours0 = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board.children[0], colours0)

    colours1 = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board.children[1], colours1)

    colours2 = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]]
    set_children(board.children[2], colours2)

    colours3 = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[3], colours3)

    return board


# =============================================================================


def test_block_to_squares_leaf(child_block) -> None:
    """Test that a board with only one block can be correctly trasnlated into
    a square that would be rendered onto the screen.
    """
    squares = _block_to_squares(child_block)
    expected = [(COLOUR_LIST[0], (0, 0), 750)]

    assert squares == expected


def test_block_to_squares_reference(board_16x16) -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    squares = set(_block_to_squares(board_16x16))
    expected = {((1, 128, 181), (563, 0), 188),
                ((199, 44, 58), (375, 0), 188),
                ((199, 44, 58), (375, 188), 188),
                ((255, 211, 92), (563, 188), 188),
                ((138, 151, 71), (0, 0), 375),
                ((199, 44, 58), (0, 375), 375),
                ((255, 211, 92), (375, 375), 375)
                }

    assert squares == expected


# =============================================================================


class TestRender:
    """A collection of methods that show you a way to save the boards in your
    test cases to image (i.e., PNG) files.

    NOTE: this requires that your blocky._block_to_squares function is working
    correctly.
    """

    def test_render_reference_board(self, renderer, board_16x16) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('reference-board.png')

    def test_render_reference_board_swap0(self, renderer, board_16x16,
                                          board_16x16_swap0) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_swap0))
        renderer.save_to_file('reference-swap-0.png')

        # Render what your swap does to the reference board
        board_16x16.swap(0)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-swap-0.png')

    def test_render_reference_board_rotate1(self, renderer, board_16x16,
                                            board_16x16_rotate1) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_rotate1))
        renderer.save_to_file('reference-rotate-1.png')

        # Render what your swap does to the reference board
        board_16x16.children[0].rotate(1)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-rotate-1.png')


class TestBlock:
    """A collection of methods that test the Block class.

    NOTE: this is a small subset of tests - just because you pass them does NOT
    mean you have a fully working implementation of the Block class.
    """
    # Helper tests
    def test_child_size(self, board_1x1) -> None:
        """Tests that child size rounds size properly."""
        assert board_1x1._child_size() == 188

    def test_children_positions(self, board_1x1) -> None:
        """Tests that the correct children positions are returned."""
        assert board_1x1._children_positions() == [(188, 0), (0, 0),
                                                   (0, 188), (188, 188)]


    # Main methods
    def test_smashable(self, board_no_children) -> None:
        b = board_no_children.smashable()
        assert b

    def test_not_smashable(self, board_16x16) -> None:
        b = board_16x16.smashable()
        assert not b

    def test_smash_on_child(self, child_block) -> None:
        """Test that a child block cannot be smashed.
        """
        child_block.smash()

        assert len(child_block.children) == 0
        assert child_block.colour == COLOUR_LIST[0]

    def test_smash_on_parent_with_no_children(self, board_16x16) -> None:
        """Test that a block not at max_depth and with no children can be
        smashed.
        """
        block = board_16x16.children[1]
        block.smash()

        assert len(block.children) == 4
        assert block.colour is None

        for child in block.children:
            if len(child.children) == 0:
                # A leaf should have a colour
                assert child.colour is not None
                # Colours should come from COLOUR_LIST
                assert child.colour in COLOUR_LIST
            elif len(child.children) == 4:
                # A parent should not have a colour
                assert child.colour is None
            else:
                # There should only be either 0 or 4 children (RI)
                assert False

    def test_swap0(self, board_16x16, board_16x16_swap0) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        board_16x16.swap(0)
        assert board_16x16 == board_16x16_swap0

    def test_swap1(self, board_16x16, board_16x16_swap1) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        board_16x16.swap(1)
        assert board_16x16 == board_16x16_swap1

    def test_swap_no_children(self, board_no_children) -> None:
        """Test that swap does not work with no children.
        """
        b = board_no_children.swap(0)
        assert not b
        c = board_no_children.swap(1)
        assert not c

    def test_rotate1(self, board_16x16, board_16x16_rotate1) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly rotated clockwise.
        """
        board_16x16.children[0].rotate(1)
        assert board_16x16 == board_16x16_rotate1

    def test_rotate2(self, board_16x16, board_16x16_rotate3) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly rotated counter-clockwise.
        """
        board_16x16.children[0].rotate(3)
        assert board_16x16 == board_16x16_rotate3

    def test_rotate_no_children(self, board_no_children) -> None:
        """Test that rotate does not work without children.
        """
        b = board_no_children.rotate(3)
        assert not b
        c = board_no_children.rotate(1)
        assert not c

    def test_paint(self, board_16x16, board_16x16_paint) -> None:
        """Tests that paint works on the top right block of reference board on
        level 2.
        """
        board_16x16.children[0].children[0].paint(COLOUR_LIST[3])
        assert board_16x16 == board_16x16_paint

    def test_paint_false(self, board_16x16, board_16x16_paint) -> None:
        """Tests that paint works on the top right block of reference board on
        level 1.
        """
        board_16x16.children[0].paint(COLOUR_LIST[3])
        assert not board_16x16 == board_16x16_paint

    def test_combine(self, board_16x16, board_16x16_combine) -> None:
        """Tests that combine works on the top right block of reference bord on
        level 1. """
        board_16x16.children[0].combine()
        assert board_16x16 == board_16x16_combine

    def test_combine_no_children(self, board_no_children) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        b = board_no_children.combine()
        assert not b

    def test_combine_no_majority(self, board_16x16) -> None:
        """Tests that combine works on the top right block of reference bord on
        level 1. """
        b = board_16x16.combine()
        assert not b
        c =  board_16x16.children[1].combine()
        assert not c

    def test_create_copy(self, board_16x16, board_16x16_copy) -> None:
        """Tests if create_copy creates a deep copy of this block. This also
         checks that __eq__ works properly."""
        board_16x16.create_copy()
        assert board_16x16 == board_16x16_copy


class TestPlayer:
    """A collection of methods for testing the methods and functions in the
    player module.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation.
    """

    def test_get_block_top_left(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-left corner of the board.
        """
        top_left = (0, 0)
        assert _get_block(board_16x16, top_left, 0) == board_16x16
        assert _get_block(board_16x16, top_left, 1) == board_16x16.children[1]

    def test_get_block_top_right(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-right corner of the board.
        """
        top_right = (board_16x16.size - 1, 0)
        assert _get_block(board_16x16, top_right, 0) == board_16x16
        assert _get_block(board_16x16, top_right, 1) == board_16x16.children[0]
        assert _get_block(board_16x16, top_right, 2) == \
               board_16x16.children[0].children[0]

    def test_create_players(self) -> None:
        hp = create_players(3, 0, [])
        for player in hp:
            assert player.id in range(0, 3)
        hrp = create_players(1, 3, [])
        for player in hrp:
            assert player.id in range(0, 4)
        hrsp = create_players(1, 1, [3, 4])
        for player in hrsp:
            assert player.id in range(0, 4)
        assert hrsp[2]._difficulty == 3
        assert hrsp[3]._difficulty == 4

    def test_generate_move_mutate(self, board_16x16) -> None:
        """Tests the generate_move does not mutate the board"""
        playas = create_players(0, 1, [4])
        b = board_16x16.create_copy()

        # test the randie
        playas[0].generate_move(board_16x16)
        assert board_16x16 == b

        # test the nerd
        playas[1].generate_move(board_16x16)
        assert board_16x16 == b

class TestGoal:
    """A collection of methods for testing the sub-classes of Goal.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation of the Goal sub-classes.
    """

    def test_block_flatten(self, board_16x16, flattened_board_16x16) -> None:
        """Test that flattening the reference board results in the expected list
        of colours.
        """
        result = _flatten(board_16x16)

        # We are expected a "square" 2D list
        for sublist in result:
            assert len(result) == len(sublist)

        assert result == flattened_board_16x16

    def test_block_flatten_unit_cell(self, board_1x1) -> None:
        """Test that flatten correctly flattens a unit cell."""
        assert _flatten(board_1x1) == [[board_1x1.colour]]

    def test_block_flatten_max_depth_4(self, board_16x16,
                                       flattened_board_16x16_max) -> None:
        """Test that flattening the reference board with a max_depth of 4.
        """
        board = Block((0, 0), 750, None, 0, 4)

        # Level 1
        colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
        set_children(board, colours)

        # Level 2
        colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1],
                   COLOUR_LIST[3]]
        set_children(board.children[0], colours)

        result = _flatten(board)
        assert len(result) == 16

        # check if its a square
        for sublist in result:
            assert len(result) == len(sublist)

        assert result == flattened_board_16x16_max

    def test_blob_goal(self, board_16x16) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 4),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_16x16) == expected

    def test_blob_goal_only_middle(self, board_16x16_blobby) -> None:
        """Tests for only the middle of blob."""
        correct_scores = [
            (COLOUR_LIST[0], 0),
            (COLOUR_LIST[1], 1),
            (COLOUR_LIST[2], 12),
            (COLOUR_LIST[3], 1)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_16x16_blobby) == expected

    def test_blob_goal_sides(self, board_16x16_perimeter) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 1),
            (COLOUR_LIST[2], 12),
            (COLOUR_LIST[3], 1)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            score = goal.score(board_16x16_perimeter)
            # assert goal.score(board_16x16_perimeter) == expected

    def test_perimeter_goal(self, board_16x16):
        correct_scores = [
            (COLOUR_LIST[0], 2),
            (COLOUR_LIST[1], 5),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_16x16) == expected

    def test_perimeter_goal_1x1_block(self, board_1x1):
        goal = PerimeterGoal(COLOUR_LIST[1])
        assert goal.score(board_1x1) == 4

    def test_perimeter_goal_no_middle(self, board_16x16_perimeter):
        """Tests that the blobs in the middle are not counted to the score"""
        correct_scores = [
            (COLOUR_LIST[0], 0),
            (COLOUR_LIST[1], 0),
            (COLOUR_LIST[2], 16),
            (COLOUR_LIST[3], 0)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_16x16_perimeter) == expected

    def test_perimeter_goal_only_corners(self, board_16x16_blobby):
        """Tests that the blobs in the middle are not counted to the score"""
        correct_scores = [
            (COLOUR_LIST[0], 0),
            (COLOUR_LIST[1], 6),
            (COLOUR_LIST[2], 8),
            (COLOUR_LIST[3], 2)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_16x16_blobby) == expected

    def test_generate_goals(self) -> None:
        """Tests generate_goal, testing that there are no duplicates """
        goals = generate_goals(4)
        r = []
        for g in goals:
            if g not in r:
                r.append(g)
        assert len(r) == 4

    def test_generate_goals2(self) -> None:
        """Tests if generate_goals generates goals with the same type """
        goals = generate_goals(4)
        _type = type(goals[0])
        for g in goals:
            assert _type == type(g)

    def test__grid(self, flattened_board_16x16, visited_board_16x16) -> None:
        """Test that _grid works properly"""
        v = _grid(flattened_board_16x16)
        assert v == visited_board_16x16

    def test__undiscovered_blob_size(self, flattened_board_16x16,
                                     visited_board_16x16) -> None:
        """Tests _undiscovered_blob_size"""
        # Set up a goal for colour and check the results
        flattened = flattened_board_16x16
        visited = visited_board_16x16
        goal = BlobGoal(COLOUR_LIST[2])
        g = goal._undiscovered_blob_size((0, 0), flattened, visited)
        assert g == 4
        goal2 = BlobGoal(COLOUR_LIST[3])
        g2 = goal2._undiscovered_blob_size((0, 0), flattened, visited)
        assert g2 == 0


if __name__ == '__main__':
    pytest.main(['example_tests.py'])
