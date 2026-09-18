def main():
    n = int(input('in_1: '))
    nLan = 0
    for i in range(2, n + 2):
        if input(f'in_{i}: ').split()[3].strip().lower() == "true":
            nLan += 1
    print(f'out: {nLan} {n-nLan}')

if __name__ == "__main__":
    main()
