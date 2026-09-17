def main():
    n = int(input())
    nLan = 0
    for _ in range(n):
        if input().split()[3].strip().lower() == "true":
            nLan += 1
    print(nLan, n-nLan, sep=' ')

if __name__ == "__main__":
    main()
