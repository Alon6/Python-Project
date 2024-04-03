

if __name__ == "__main__":
    arr = [4,-5,2,1,-9,0,10,12]
    print(list(filter(lambda x : x > 0,arr)) + list(filter(lambda x : x <= 0,arr)))
    arr.sort(key = lambda x:x * -1)
    print(arr)