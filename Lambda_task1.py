fib = lambda n :  fib(n-1) + fib(n-2) if n > 1 else 1
if __name__ == "__main__":
    amount = int(input("Enter number: "))
    print(fib(amount))
