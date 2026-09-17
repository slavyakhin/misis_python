def main():
    s = input()
    result = ''

    i = 0
    # Find first uppercase letter
    while i < len(s) and not s[i].isupper():
        i += 1
    if i < len(s):
        firstInd = i
        result = s[i] # single character string
    else:
        raise ValueError("No first uppercase letter")
    i += 1

    # Find first digit occurrence after
    while i < len(s) and s[i] != '.' and not s[i].isdigit():
        i += 1
    if i >= len(s):
        raise ValueError("No period and no digit")
    if s[i] == '.':
        print(result + '.')
        return

    # Digit occurs at ith position
    i += 1
    step = i - firstInd
    curStep = 0
    while i < len(s):
        if s[i] == '.':
            result += '.'
            break
        if curStep == 0:
            result += s[i]

        i += 1
        curStep = (curStep + 1) % step
    if result[len(result)-1] != '.':
        raise ValueError("No period")

    print(result)

if __name__ == "__main__":
    main()
