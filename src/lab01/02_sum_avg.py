def main():
    a = float(input("a: ").replace(',', '.'))
    b = float(input("b: ").replace(',', '.'))
    print(f'sum={a + b:.2f}; avg={(a + b) / 2:.2f}')


if __name__ == '__main__':
    main()
