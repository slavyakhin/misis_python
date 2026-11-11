from collections import deque

class EmptyStackError(Exception):
    """Stack must not be empty"""

class EmptyQueueError(Exception):
    """Queue must not be empty"""


# --------------- STACK ---------------


def stack_create() -> list:
    """ Stack constructor """
    return list()


def stack_from_list(l: list) -> list:
    """ Construct stack from list. list[-1] becomes stack's top """
    st = stack_create()
    for value in l:
        stack_push(st, value)
    return st


def stack_to_list(st: list) -> list:
    """ Construct list from stack. stack's top becomes list[-1] """
    l = list()
    while not stack_is_empty(st):
        l.append(stack_pop(st))
    l.reverse()
    return l


def stack_push(st: list, item) -> None:
    """ Push an item to the top of the stack """
    st.append(item)


def stack_pop(st: list) -> object:
    """
    Return top element of the stack and remove it.

    If stack is empty raises EmptyStackError exception.
    """
    if len(st) == 0:
        raise EmptyStackError("Stack is empty")

    return st.pop()


def stack_peek(st: list) -> object:
    """
    Return top element of the stack.
    
    If stack is empty raises EmptyStackError  exception.
    """
    if stack_is_empty(st):
        raise EmptyStackError("Stack is empty")

    return st[-1]


def stack_is_empty(st: list) -> bool:
    """ Return whether stack has no elements """
    return not st


def is_balanced(s: str) -> bool:
    """
    Return whether s has a balanced bracket sequence.

    Other char are ignored.
    """
    st = stack_create()
    bracket_pair = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    for c in s:
        if c in '([{':
            stack_push(st, c)
        elif c in ')]}':
            if stack_is_empty(st) or stack_pop(st) != bracket_pair[c]:
                return False

    return stack_is_empty(st)


def rpn(expr: str) -> float:
    """
    Reverse Polish Notation calculator.

    Tokens must be separated by spaces.
    """

    unary_operators = ['~']
    binary_operators = ['+', '-', '*', '/', '%', '**', '//']

    values_st = stack_create()

    for token in expr.split():
        if token in unary_operators:

            try:
                a = stack_pop(values_st)
                assert isinstance(a, float)
            except EmptyStackError:
                raise ValueError(f"Invalid rpn: no operand for '{token}' operator")

            match token:
                case '~':
                    stack_push(values_st, -a)

        elif token in binary_operators:

            try:
                a = stack_pop(values_st)
                assert isinstance(a, float)
                b = stack_pop(values_st)
                assert isinstance(b, float)

            except EmptyStackError:
                raise ValueError(f"Invalid rpn: no operand for '{token}' operator")

            match token:
                case '+':
                    stack_push(values_st, a+b)
                case '-':
                    stack_push(values_st, a-b)
                case '*':
                    stack_push(values_st, a*b)
                case '/':
                    stack_push(values_st, a/b)
                case '%':
                    stack_push(values_st, a%b)
                case '**':
                    stack_push(values_st, a**b)
                case '//':
                    stack_push(values_st, a//b)
        else:
            try:
                stack_push(values_st, float(token))
            except ValueError:
                raise ValueError(f'Non-convertable to float token "{token}"')

    try:
        result = stack_pop(values_st)
        if not stack_is_empty(values_st):
            raise ValueError("Not all tokens used")

        assert isinstance(result, float)

        return result
    except EmptyStackError:
        raise ValueError("No values in the rpn")


# --------------- QUEUE ---------------


def queue_create() -> deque:
    """ Queue constructor """
    return deque()


def queue_from_list(l: list) -> deque:
    """ Construct queue from list. l[0] becomes q's front. """
    q = queue_create()
    for value in l:
        queue_enqueue(q, value)
    return q


def queue_to_list(q: deque) -> list:
    """ Construct list from queue. q front becomes l[0] """

    l = []
    while not queue_is_empty(q):
        l.append(queue_dequeue(q))

    return l


def queue_enqueue(q: deque, item) -> None:
    """ Push the item to the end of the queue """
    q.append(item)


def queue_dequeue(q: deque) -> None:
    """
    Pop an item from queue front

    If queue is empty raises EmptyQueueError exception.
    """
    if queue_is_empty(q):
        raise EmptyQueueError("Queue is empty")

    return q.popleft()


def queue_peek(q: deque) -> object | None:
    """
    Return front element of the queue.
    
    If queue is empty raises EmptyQueueError exception.
    """

    if queue_is_empty(q):
        raise EmptyQueueError("Queue is empty")

    return q[0]


def queue_is_empty(q: deque) -> bool:
    """ Return whether queue is empty """
    return not bool(q)
