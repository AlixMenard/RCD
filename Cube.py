import numpy as np
from typing import Optional

class Cube:
    def __init__(self):
        self.red    = Face("red")
        self.orange = Face("orange")
        self.yellow = Face("yellow")
        self.green  = Face("green")
        self.blue   = Face("blue")
        self.white  = Face("white")

        for c in Geometry.colors:
            self[c].top   = self[self[c].top]
            self[c].right = self[self[c].right]
            self[c].left  = self[self[c].left]
            self[c].down  = self[self[c].down]

    def __getitem__(self, color:str):
        match color:
            case "red"   : return self.red
            case "orange": return self.orange
            case "yellow": return self.yellow
            case "green" : return self.green
            case "blue"  : return self.blue
            case "white" : return self.white

    def set_solved(self):
        for pos in range(9):
            for color in Geometry.colors:
                self[color].assign(color, pos)

class Face:

    # For white/yellow : Looking facing white, red up
    # For rest, color facing, white top

    def __init__(self, color:Optional[str] = None):
        self.composition = np.full((3, 3), "", dtype="U10")
        self.composition[1, 1] = color
        self.color = color

        self.geometry = Geometry.map[color]
        self.top = self.geometry["top"]
        self.right = self.geometry["right"]
        self.down = self.geometry["down"]
        self.left = self.geometry["left"]
        self.sections = {
            self.top   : np.s_[0, :],
            self.right : np.s_[:, 2],
            self.down  : np.s_[2, :],
            self.left  : np.s_[:, 0]
        }

    def assign(self, color:str, position: int):
        """
            012
            345
            678

            5 forbidden
        """
        if position == 4: return
        row, column = divmod(position, 3)
        self.composition[row, column] = color

    def rotate(self, clockwise:bool = True):
        if clockwise:
            self.composition = np.rot90(self.composition, k=-1)
        else:
            self.composition = np.rot90(self.composition, k=1)

        top_section   = np.copy(self.top.composition[self.top.sections[self.color]])
        right_section = np.copy(self.right.composition[self.right.sections[self.color]])
        down_section  = np.copy(self.down.composition[self.down.sections[self.color]])
        left_section  = np.copy(self.left.composition[self.left.sections[self.color]])

        if clockwise:
            self.top.composition[self.top.sections[self.color]]     = left_section
            self.right.composition[self.right.sections[self.color]] = top_section
            self.down.composition[self.down.sections[self.color]]   = right_section
            self.left.composition[self.left.sections[self.color]]   = down_section
        else:
            self.top.composition[self.top.sections[self.color]]     = right_section
            self.right.composition[self.right.sections[self.color]] = down_section
            self.down.composition[self.down.sections[self.color]]   = left_section
            self.left.composition[self.left.sections[self.color]]   = top_section


    def __str__(self):
        return str(self.composition)

class Geometry:
    colors = ["white", "red", "orange", "yellow", "green", "blue"]

    # For white/yellow : Looking facing white, red up
    # For rest, color facing, white top

    white = {
        "top"   : "red",
        "right" : "green",
        "down"  : "orange",
        "left"  : "blue"
    }
    yellow = {
        "top"   : "red",
        "right" : "blue",
        "down"  : "orange",
        "left"  : "green"
    }
    red = {
        "top"   : "white",
        "right" : "blue",
        "down"  : "yellow",
        "left"  : "green"
    }
    green = {
        "top"   : "white",
        "right" : "red",
        "down"  : "yellow",
        "left"  : "orange"
    }
    orange = {
        "top"   : "white",
        "right" : "green",
        "down"  : "yellow",
        "left"  : "blue"
    }
    blue = {
        "top"   : "white",
        "right" : "orange",
        "down"  : "yellow",
        "left"  : "red"
    }

    map = {
        "white"  : white,
        "yellow" : yellow,
        "red"    : red,
        "green"  : green,
        "orange" : orange,
        "blue"   : blue}

if __name__ == "__main__":
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