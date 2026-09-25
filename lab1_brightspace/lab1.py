# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque
import numpy as np

class TextbookStack(object):
    """ A class that tracks the """
    def __init__(self, initial_order, initial_orientations):
        assert len(initial_order) == len(initial_orientations)
        self.num_books = len(initial_order)
        
        for i, a in enumerate(initial_orientations):
            assert i in initial_order
            assert a == 1 or a == 0

        self.order = np.array(initial_order)
        self.orientations = np.array(initial_orientations)

    def flip_stack(self, position):
        assert position <= self.num_books
        
        self.order[:position] = self.order[:position][::-1]
        self.orientations[:position] = np.abs(self.orientations[:position] - 1)[::-1]

    def check_ordered(self):
        for idx, front_matter in enumerate(self.orientations):
            if (idx != self.order[idx]) or (front_matter != 1):
                return False

        return True

    def copy(self):
        return TextbookStack(self.order, self.orientations)
    
    def __eq__(self, other):
        assert isinstance(other, TextbookStack), "equality comparison can only ba made with other __TextbookStacks__"
        return all(self.order == other.order) and all(self.orientations == other.orientations)

    def __str__(self):
        return f"TextbookStack:\n\torder: {self.order}\n\torientations:{self.orientations}"


def apply_sequence(stack, sequence):
    new_stack = stack.copy()
    for flip in sequence:
        new_stack.flip_stack(flip)
    return new_stack

def breadth_first_search(stack):
    flip_sequence = []

    # --- v ADD YOUR CODE HERE v --- #
    if stack.check_ordered():
        return flip_sequence

    # numpy arrays aren't hashable
    # and tuple them so they can go in a set
    # 튜플로 바꿔야 set 에 넣을 수 있음. 근데 헷갈리니까 이따 돌아오기
    # might need to come back later
    start_state = (tuple(stack.order), tuple(stack.orientations))
    been_there = {start_state}

    pending_tbd = deque()
    pending_tbd.append((stack, flip_sequence))

    while pending_tbd:
        stack_rightnow, path_sofar_used = pending_tbd.popleft()

        # position is 1-indexed here, not 0 -- forgot this at first and
        # kept hitting the assert in flip_stack
        for point_here in range(1, stack_rightnow.num_books + 1):
            new_stack = stack_rightnow.copy()
            new_stack.flip_stack(point_here)
            new_state = (tuple(new_stack.order), tuple(new_stack.orientations))

            # pass in here
            if new_state in been_there:
                continue
            been_there.add(new_state)

            # save the info here
            new_path = path_sofar_used + [point_here]

            if new_stack.check_ordered():
                return new_path

            pending_tbd.append((new_stack, new_path))

    return flip_sequence
    # ---------------------------- #


def depth_first_search(stack):
    flip_sequence = []

    # --- v ADD YOUR CODE HERE v --- #
    # should be in the order
    if stack.check_ordered():
        return flip_sequence

    # 돌아오기
    start_state = (tuple(stack.order), tuple(stack.orientations))
    been_there = {start_state}

    # same loop as BFS below
    # just a stack instead of a queue
    # the change (pop vs popleft) is what makes this DFS
    backup = [(stack, flip_sequence)]

    while backup:
        stack_rightnow, path_sofar_used = backup.pop()

        for point_here in range(1, stack_rightnow.num_books + 1):
            new_stack = stack_rightnow.copy()
            new_stack.flip_stack(point_here)
            new_state = (tuple(new_stack.order), tuple(new_stack.orientations))

            # let's pass
            if new_state in been_there:
                continue
            been_there.add(new_state)

            new_path = path_sofar_used + [point_here]

            # return here
            if new_stack.check_ordered():
                return new_path

            backup.append((new_stack, new_path))

    return flip_sequence
    # ---------------------------- #
