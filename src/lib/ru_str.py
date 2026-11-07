def age_ru_word(age: int) -> str:
    """
    Russian words for different age.
    """
    if not (0 < age % 10 < 5) or (10 < age < 15):
        return "лет"

    if age % 10 == 1:
        return "год"

    return "года"
