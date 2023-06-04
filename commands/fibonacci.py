def fibonacci_generator(num):
  fib = [0, 1]
  returnValue = []

  # generate the rest of the sequence
  for i in range(num-2):
    fib.append(fib[-1] + fib[-2])

  # print the sequence
  print("The first", num, "Fibonacci numbers are:")
  for num in fib:
    print(num)
    returnValue.append(num)
  return returnValue