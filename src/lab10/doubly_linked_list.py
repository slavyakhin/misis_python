# --------------- DOUBLE LINKED LIST ---------------

class DoublyNode:
    def __init__(self, value, prev: DoublyNode | None=None, next: DoublyNode | None=None):
        self.value = value
        self.prev = prev
        self.next = next


def ll_copy(head: DoublyNode | None) -> DoublyNode | None:
    """ Copies doubly linked list. """

    if head is None:
        return None

    if not isinstance(head, DoublyNode):
        raise TypeError("head must be DoublyNode")

    new_head = DoublyNode(head.value, None, None)
    cur = new_head
    while head.next is not None:
        cur.next = DoublyNode(head.next.value, prev=cur, next=None)
        cur = cur.next
        head = head.next

    return new_head


def dll_from_list(values: list) -> DoublyNode | None:
    """ Construct doubly linked list from list """

    if not isinstance(values, list):
        raise TypeError("values must be list")

    if not values:
        return None

    head = DoublyNode(values[0])
    cur = head
    for value in values[1:]:
        cur.next = DoublyNode(value, prev=cur)
        cur = cur.next

    return head


def dll_to_list(head: DoublyNode | None) -> list:
    """ Make list from doubly linked list """

    l = list()
    while head is not None:
        l.append(head.value)
        head = head.next

    return l


def dll_length(head: DoublyNode | None) -> int:
    """ Node count by traversal O(n) """

    counter = 0

    while head is not None:
        counter += 1
        head = head.next

    return counter


def dll_prepend(head: DoublyNode | None, value) -> DoublyNode:
    """ Add Doubly Node to the beggining O(1) """

    new_head = DoublyNode(value, next=head)
    if head is not None:
        head.prev = new_head

    return new_head


def dll_append(head: DoublyNode | None, value) -> DoublyNode:
    """ Add Doubly Node to the end O(n) """

    if head is None:
        return DoublyNode(value)

    cur = head

    while cur.next is not None:
        cur = cur.next

    cur.next = DoublyNode(value, prev=cur)

    return head


def dll_insert(head: DoublyNode | None, idx: int, value) -> DoublyNode:
    """ Insert Doubly Node by index """

    if idx == 0:
        return dll_prepend(head, value)

    if head is None:
        raise IndexError("index out of range")

    i, cur = 1, head

    while cur.next is not None and i != idx:
        cur = cur.next
        i += 1

    if i != idx:
        raise IndexError("index out of range")

    new_node = DoublyNode(value, cur, cur.next)
    cur.next = new_node

    if new_node.next is not None:
        new_node.next.prev = new_node

    return head


def dll_remove(head: DoublyNode | None, value) -> DoublyNode | None:
    """
    Remove first occurence of value.

    If Not Found do nothing.
    """

    if head is None:
        return None

    if head.value == value:
        new_head = head.next
        if new_head is not None:
            new_head.prev = None
        return new_head

    cur = head

    while cur.next is not None and cur.next.value != value:
        cur = cur.next

    if cur.next is not None:
        cur.next = cur.next.next
        if cur.next is not None:
            cur.next.prev = cur

    return head


def dll_remove_at(head: DoublyNode | None, idx: int) -> DoublyNode | None:
    """ Remove Doubly Node at index idx """

    if head is None:
        raise IndexError("the doubly linked list is empty")

    if idx == 0:
        new_head = head.next
        if new_head is not None:
            new_head.prev = None
        return new_head

    i, cur = 1, head

    while cur.next is not None and i != idx:
        cur = cur.next
        i += 1

    if i != idx:
        raise IndexError("index out of range")

    # Deletion
    if cur.next is not None:
        cur.next = cur.next.next
        if cur.next is not None:
            cur.next.prev = cur

    return head


def dll_reverse(head: DoublyNode | None) -> DoublyNode | None:
    """ Reverse the doubly linked list inplace """

    if head is None:
        return None

    prev = None
    cur = head
    nxt = head.next

    while nxt is not None:
        cur.next = prev
        cur.prev = nxt

        prev = cur
        cur = nxt
        nxt = cur.next

    return cur


def dll_repr(head: DoublyNode | None) -> str:
    """ Represent doubly linked list as string """

    if head is None:
        return "None"

    l = [ f"[{v}]" for v in dll_to_list(head) ]
    return "None <- " + '<->'.join(l) + " -> None"


def dll_middle(head: DoublyNode | None) -> DoublyNode | None:
    """ Middle DoublyNode by one traverse O(n) """

    if head is None:
        return None

    slow, fast = head, head

    while fast.next is not None and fast.next.next is not None:
        slow = slow.next # type: ignore
        fast = fast.next.next

    return slow


def dll_has_cycle(head: DoublyNode | None) -> bool:
    """ Floyd's algorithm """

    slow, fast = head, head

    while fast is not None and fast.next is not None:
        slow = slow.next # type: ignore
        fast = fast.next.next
        
        if fast == slow:
            return True

    return False
