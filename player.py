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

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    # TODO: Implement Me
    result = []
    # temporary goals to put into players
    goals = generate_goals(num_random + num_human + len(smart_players))

    # make human players
    if num_human != 0:
        for i in range(num_human):
            result.append(HumanPlayer(i, goals[i]))

    # make random players
    total = num_human
    if num_random != 0:
        for i in range(num_random):
            # use id as num_humans + i
            result.append(RandomPlayer(total + i, goals[total + i]))

    # make smart players
    total = total + num_random
    if len(smart_players) != 0:
        for i in range(len(smart_players)):
            # use id as num_humans + num_random + i
            result.append(SmartPlayer(total + i, goals[total + i],
                                      smart_players[i]))
    return result


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    # TODO: Implement me
    x, y = location[0], location[1]

    if block.level == level or (block.level < level and not block.children):
        if x in range(block.position[0], block.position[0] + block.size) and \
                y in range(block.position[1], block.position[1] + block.size):
            return block
        return None

    else:
        # We know that block.level < level and block.children
        for blocky in block.children:
            if _get_block(blocky, location, level) is not None:
                return _get_block(blocky, location, level)
        return None

def _get_random_blocky(copy: Block) -> Block:
    """Returns a random block from a copied board. """
    rx = random.randrange(0, copy.size)
    ry = random.randrange(0, copy.size)
    rl = random.randrange(0, copy.max_depth)
    block = _get_block(copy, (rx, ry), rl)
    return block

def _get_random_action(lst: list) -> Tuple[str, int]:
    """ Returns a random action from list. """
    ra = lst[random.randrange(len(lst))]
    return ra

def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    return action[0], action[1], block


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError

    def _check_action_validity(self, action: Tuple[str, int],
                               block: Block) -> bool:
        if action[0] == 'rotate':
            if action[1] == 1:
                return block.rotate(1)
            else:
                return block.rotate(3)
        elif action[0] == 'swap':
            if action[1] == 0:
                return block.swap(0)
            else:
                return block.swap(1)
        elif action[0] == 'smash':
            return block.smash()
        elif action[0] == 'combine':
            return block.combine()
        else:
            return block.paint(self.goal.colour)

class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        # block = _get_block(board, mouse_pos, self._level)
        block = _get_block(board, mouse_pos, min(self._level, board.max_depth))
        # this is the proposed change by Mario in Piazza to counter the bug
        # https://piazza.com/class/k4x6fyq98ktyv?cid=1750
        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    """Computer player that chooses moves at random."""
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        # TODO: Implement Me
        else:
            # create copy of the board
            copy = board.create_copy()
            # randomly choose block and level in  board
            block = _get_random_blocky(copy)
            # randomly choose action
            actions = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                       SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, COMBINE, PAINT]
            m = _get_random_action(actions)
            if self._check_action_validity(m, block):
                move = _create_move(m, block)
                self._proceed = False  # Must set to False before returning!
                return move
            else:
                return self.generate_move(board)


class SmartPlayer(Player):
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    # _difficulty:
    #   The number of randomly generated valid moves the player selects the
    #   highest scoring move from.
    # ==================== Representation Invariants =====================
    # _difficulty >= 0
    """ Computer player that chooses a random move that makes the highest
    increase score. """
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        else:
            # TODO: Implement Me
            curr = self.goal.score(board)
            possible_actions = []
            possible_scores = []
            actions = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                       SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, COMBINE, PAINT]

            # get self._difficulty number of random moves
            while len(possible_actions) - 1 < self._difficulty:
                m = _get_random_action(actions)
                blocky = _get_random_blocky(board)
                if self._check_action_validity(m, blocky):
                    possible_actions.append((m, blocky))

            # get score
            for i in range(len(possible_actions)):
                blocky = possible_actions[i][-1]
                possible_scores.append(self.goal.score(blocky))

            # get max score
            _max = max(possible_scores)
            index = possible_scores.index(_max)

            # if max score == current score: pass
            if curr == _max:
                self._proceed = False  # Must set to False before returning!
                return _create_move(PASS, board)

            # else return action with max score
            else:
                self._proceed = False  # Must set to False before returning!
                return _create_move(possible_actions[index][0], board)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
