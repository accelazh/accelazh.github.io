x = linspace(1,100,10)
y = linspace(1,20,20)

def f(x, y):
  return x + y

X, Y = np.meshgrid(x, y)
Z = f(X, Y)


assert len(X) == len(Y)
Z2 = []
for row in range(0, len(X)):
  assert len(X[row]) == len(Y[row])
  Z2.append([f(X[row][col], Y[row][col]) 
    for col in range(0, len(X[row]))])

Z2 = np.array(Z2)
