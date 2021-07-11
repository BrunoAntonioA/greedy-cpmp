import pandas as pd

x = pd.read_csv('./datasets/xtest-bsg5x7-c.csv', header=None)
y = pd.read_csv('./datasets/ytest-bsg5x7-c.csv', header=None)

print(x)

print(y.shape)
print(x.shape)

