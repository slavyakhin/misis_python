def main():
    price = float(input("price="))
    discount = float(input("discount="))
    vat = float(input("vat="))

    base = price * (1 - discount/100)
    vat_amount = base * (vat / 100)
    total = base + vat_amount

    table = [
        ['База после скидки', base],
        ['НДС', vat_amount],
        ['Итого к оплате', total],
    ]

    maxTitleLen = max(map(lambda row: len(row[0]), table)) # row[0] is str

    for row in table:
        print(f'{row[0]+":":<{maxTitleLen+1}} {row[1]:.2f} ₽') # len + 1 for ":" char

if __name__ == '__main__':
    main()
