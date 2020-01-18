x = 123456789012
for i in range(30):
    x = x**2
    x = x % 1000000000
    x = x // 1000
    print(x)