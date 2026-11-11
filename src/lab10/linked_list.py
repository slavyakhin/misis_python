# --------------- LINKED LIST ---------------

class Node:
    def __init__(self, value, next: Node | None=None):
        self.value = value
        self.next = next

    def __reduce__(self):
        """ Serialize and deserialize """
        return ll_from_list, (ll_to_list(self),)


def ll_copy(head: Node | None) -> Node | None:
    """ Copies linked list. """

    if head is None:
        return None

    if not isinstance(head, Node):
        raise TypeError("head must be Node")

    new_head = Node(head.value, None)
    cur = new_head
    while head.next is not None:
        cur.next = Node(head.next.value, None)
        cur = cur.next
        head = head.next

    return new_head


def ll_from_list(values: list) -> Node | None:
    """ Construct linked list from list. """

    if not isinstance(values, list):
        raise TypeError("values must be list")

    if not values:
        return None

    head = Node(values[0], None)
    cur = head
    for value in values[1:]:
        cur.next = Node(value, None)
        cur = cur.next

    return head


def ll_to_list(head: Node | None) -> list:
    """ Make list from linked list """

    l = list()
    while head is not None:
        l.append(head.value)
        head = head.next

    return l


def ll_length(head: Node | None) -> int:
    """ Node count by traversal O(n) """

    counter = 0
    
    while head is not None:
        counter += 1
        head = head.next

    return counter


def ll_prepend(head: Node | None, value) -> Node:
    """ Add Node to the beggining O(1) """

    return Node(value, head)


def ll_append(head: Node | None, value) -> Node:
    """ Add Node to the end O(n) """

    if head is None:
        return Node(value)

    cur = head

    while cur.next is not None:
        cur = cur.next

    cur.next = Node(value)

    return head


def ll_insert(head: Node | None, idx: int, value) -> Node:
    """ Insert Node by index """

    if idx == 0:
        return ll_prepend(head, value)

    if head is None:
        raise IndexError("index out of range")

    i, cur = 1, head

    while cur.next is not None and i != idx:
        cur = cur.next
        i += 1

    if i != idx:
        raise IndexError("index out of range")

    cur.next = Node(value, cur.next)

    return head


def ll_remove(head: Node | None, value) -> Node | None:
    """
    Remove first occurence of value.

    If Not Found do nothing.
    """
# 
    if head is None:
        return None

    if head.value == value:
        return head.next

    cur = head

    while cur.next is not None and cur.next.value != value:
        cur = cur.next

    if cur.next is not None:
        cur.next = cur.next.next

    return head


def ll_remove_at(head: Node | None, idx: int) -> Node | None:
    """ Remove Node at index idx """

    if head is None:
        raise IndexError("the linked list is empty")

    if idx == 0:
        return head.next

    i, cur = 1, head

    while cur.next is not None and i != idx:
        cur = cur.next
        i += 1

    if i != idx:
        raise IndexError("index out of range")

    # Deletion
    if cur.next is not None:
        cur.next = cur.next.next

    return head


def ll_reverse(head: Node | None) -> Node | None:
    """ Reverse the list inplace """

    if head is None:
        return None

    prev = None
    cur = head
    nxt = head.next

    while nxt is not None:
        cur.next = prev

        prev = cur
        cur = nxt
        nxt = cur.next

    return cur


def ll_repr(head: Node | None) -> str:
    """ Represent linked list as string """

    l = [ f"[{v}]" for v in ll_to_list(head) ]
    l.append("None")
    return ' -> '.join(l)


def ll_middle(head: Node | None) -> Node | None:
    """ Middle Node by one traverse O(n) """

    if head is None:
        return None

    slow, fast = head, head

    while fast.next is not None and fast.next.next is not None:
        slow = slow.next # type: ignore
        fast = fast.next.next

    return slow


def ll_has_cycle(head: Node | None) -> bool:
    """ Floyd's algorithm """

    slow, fast = head, head

    while fast is not None and fast.next is not None:
        slow = slow.next # type: ignore
        fast = fast.next.next
        
        if fast == slow:
            return True

    return False
