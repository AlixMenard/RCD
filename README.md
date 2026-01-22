```
from Cube import Cube

cube = Cube()

cube.set_solved()

cube.red.rotate()
print(cube.red)
print(cube.white)
print(cube.green)

cube.white.rotate()
print(cube.red)
print(cube.white)
print(cube.green)
```