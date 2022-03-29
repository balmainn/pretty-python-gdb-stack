h = 0.1
x = 0 
y = -1
maxVal = 0.5

r = int(maxVal/h)

print(f"r = {r}")
print("n   x   y")

for i in range(0, r):
    print(f"{i}, {x}, {y}")
    function = -x / y 
    y = y + h*function
    x = x + h