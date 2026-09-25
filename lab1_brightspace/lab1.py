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
    # already sorted, nothing to do
    if stack.check_ordered():
        return flip_sequence

    # state = order + orientations, as tuple
    # 튜플로 바꿔야 set 에 저장 가능함 (numpy 배열은 안됨)
    start_state = (tuple(stack.order), tuple(stack.orientations))
    # set of states already seen
    been_there = {start_state}

    # queue holds (stack, path so far)
    # 큐(FIFO): 먼저 넣은 게 먼저 나옴 -> 제일 짧은 경로부터 찾게 됨
    pending_tbd = deque()
    pending_tbd.append((stack, flip_sequence))

    while pending_tbd:
        # pop oldest item from front
        stack_rightnow, path_sofar_used = pending_tbd.popleft()

        # try flipping every possible position
        # 1번부터 맨 아래 책까지 다 시도
        for point_here in range(1, stack_rightnow.num_books + 1):
            new_stack = stack_rightnow.copy()
            new_stack.flip_stack(point_here)
            new_state = (tuple(new_stack.order), tuple(new_stack.orientations))

            # skip if seen this state before
            if new_state in been_there:
                continue
            been_there.add(new_state)

            # + makes a new list (원본 안 건드림)
            new_path = path_sofar_used + [point_here]

            # sorted now, we are done
            if new_stack.check_ordered():
                return new_path

            # not sorted yet, keep exploring
            pending_tbd.append((new_stack, new_path))

    return flip_sequence
    # ---------------------------- #


def depth_first_search(stack):
    flip_sequence = []

    # --- v ADD YOUR CODE HERE v --- #
    # already sorted, nothing to do
    if stack.check_ordered():
        return flip_sequence

    # state = order + orientations, as tuple
    start_state = (tuple(stack.order), tuple(stack.orientations))
    # set of states already seen
    been_there = {start_state}

    # backup is a stack (LIFO), not a queue
    # 나중에 넣은 게 먼저 나옴 -> 한쪽 길로 끝까지 감
    backup = [(stack, flip_sequence)]

    while backup:
        # pop most recently added item
        stack_rightnow, path_sofar_used = backup.pop()

        # try flipping every possible position
        for point_here in range(1, stack_rightnow.num_books + 1):
            new_stack = stack_rightnow.copy()
            new_stack.flip_stack(point_here)
            new_state = (tuple(new_stack.order), tuple(new_stack.orientations))

            # skip if seen this state before
            if new_state in been_there:
                continue
            been_there.add(new_state)

            # + makes a new list (원본 안 건드림)
            new_path = path_sofar_used + [point_here]

            # sorted now, we are done
            if new_stack.check_ordered():
                return new_path

            # not sorted yet, keep exploring
            backup.append((new_stack, new_path))

    return flip_sequence
    # ---------------------------- #