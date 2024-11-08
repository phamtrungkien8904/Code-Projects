import time
start = time.time()

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


print("Fibonacci sequence")
n = int(input("Enter the numbers of terms: "))

fib = []
for i in range(n):
    fib.append(fibonacci(i))
print(fib)

end = time.time()
print("---",
      (end-start) * 10**3, "ms")