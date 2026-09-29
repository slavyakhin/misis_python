import sys


class FloatIntFormatted(float):
    '''float wrapper.
    
    Integer floats display without trailing zeroes.
    '''

    def __repr__(self):
        if self.is_integer():
            return str(int(self))
        return super().__repr__()


old_displayhook = sys.displayhook

def float_int_formatted_displayhook(value):
    '''Displayhook wrapper.

    Usage: "sys.displayhook = integer_float_displayhook"

    ! Works only with floats itself or 1-dimension lists.
    Recursive type check has been deemed unnecessary !
    '''

    # Func must not change value
    display_value = value

    if isinstance(value, float) and value.is_integer():
        display_value = int(value) # New object

    elif isinstance(value, list):
        display_value = [
            (FloatIntFormatted(elem) if isinstance(elem, float)
             else elem)
             for elem in value
        ]

    old_displayhook(display_value)
