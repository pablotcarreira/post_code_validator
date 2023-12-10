
def three_five_counter():
    """Simple, clear and fast."""
    for i in range(1, 101):
        is_divisible_by_3 = i % 3 == 0
        is_divisible_by_5 = i % 5 == 0

        if is_divisible_by_3 and is_divisible_by_5:
            print("ThreeFive")
        elif is_divisible_by_3:
            print("Three")
        elif is_divisible_by_5:
            print("Five")
        else:
            print(i)


if __name__ == '__main__':
    three_five_counter()
