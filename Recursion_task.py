# Disks are numbered from smallest to largest and towers are numbered from left to right
def hanoiTowers(amount, source, aux, dest):
    if amount <= 0:
        return
    hanoiTowers(amount-1,source,dest,aux)
    print("move disk " + str(amount) + " to tower " + str(dest))
    hanoiTowers(amount-1,aux,source,dest)
if __name__ == "__main__":
    amount = int(input("Enter number: "))
    hanoiTowers(amount, 1, 2, 3)