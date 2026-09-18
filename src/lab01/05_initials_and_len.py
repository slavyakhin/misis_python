def main():
    nameList = input("ФИО: ").split()
    if (len(nameList) == 0):
        raise ValueError("Name is required")

    print(f'Инициалы: {"".join(map(lambda word: word[0], nameList))}.')
    print(f'Длина (символов): {sum(map(len, nameList)) + len(nameList) - 1}') # usually 2 additional spaces

if __name__ == "__main__":
    main()
