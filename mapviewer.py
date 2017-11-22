from pathlib import Path
from PIL import Image, ImageTk
__name__ = "mapviewer"
mapbasedir = "map"
fileformat = "png"
class TMSState:
    #Using Z, X, Y as same as tile's direct links
    def __init__(self, z_, x_, y_):
        self.z = z_
        self.x = x_
        self.y = y_

    #Machine-readable format
    def __str__(self):
        return "(:Z " + str(self.z) + ":X " + str(self.x) + ":Y " + str(self.y) + ")"

    def __ne__(self, other):
        return self.z != other.z or self.x != other.x or self.y != other.y

    # Tile zoom navigation: NZ <=> not a zero
    # (0, NZ) (NZ, NZ)
    # (0,  0) (NZ,  0)
    def zoom(self, lhs, rhs):
        x = 2*self.x + int(bool(lhs))
        y = 2*self.y + int(bool(rhs))
        z = self.z + 1
        return TMSState(z, x, y)

    # In-tile navigation on zoom level Z
    # left = bot = 0
    # right = top = 2 ** Z - 1
    # Tile:
    # (left, top) ... (right, top)
    # ...                      ...
    # (left, bot) ... (right, bot)
    def move(self, lhs, rhs):
        z = self.z
        x = self.x + lhs
        y = self.y + rhs
        right = 2 ** z - 1
        left = 0
        x = x if x <= right else right
        x = x if x >= left else left
        y = y if y <= right else right
        y = y if y >= left else left
        return TMSState(z, x, y)

    #Get parent tile-state
    def parent(self):
        return TMSState(self.z - 1, self.x // 2, self.y // 2)

    #Get path in TMS-style coordinates. Files are stored in BASEDIR with specified FORMAT
    def to_path(self, basedir = mapbasedir, format = fileformat):
        return basedir + "/" + str(self.z) + "/" + str(self.x) + "/" + str(self.y) + "." + format

    #Check existing image with FORMAT for state instance in BASEDIR
    def any_image(self, basedir = mapbasedir, format = fileformat):
        curr_path = self.to_path(basedir, format)
        return Path(curr_path).is_file()


class TMSStateMachine:
    def __init__(self, basestate, basedir = mapbasedir, format = fileformat):
        self.states = [basestate]
        self.mapdir = basedir
        self.format = format
        if Path(self.mapdir).is_dir():
            print("::TMS-SM::(State machine ready)")
        else:
            print("::TMS-SM::(Base dir does not exist or it is not a dir)")

    def state(self):
        return self.states[-1]

    #Add new state in list
    def push(self, newstate):
        print("::TMS-SM::(New state", newstate, ")")
        self.states.append(newstate)

    #Update state list for newstate
    def update(self, newstate):
        if self.state() == newstate:
            print("::TMS-SM::(Same state)")
        else:
            old_state = self.state()
            new_state = newstate
            sub_states = [new_state]
            while old_state.parent() != new_state.parent() :
                old_state = old_state.parent()
                new_state = new_state.parent()
                sub_states.append(new_state)
            old_states = self.states[-1:-(len(sub_states) + 1):-1]
            old_states.reverse()
            self.states = self.states[:len(self.states) - len(sub_states)]
            sub_states.reverse()
            self.states.extend(sub_states)
            print("::TMS-SM::(Up states", *old_states, ":=", *sub_states, ")")

    #Remoe last not base state
    def pop(self):
        if len(self.states) <= 1:
            print("::TMS-SM::(Current state is base:", self.state(), ")")
        else:
            oldstate = self.state()
            self.states.pop()
            print("::TMS-SM::(Back from", oldstate, "to", self.state(), ")")

    #Get image reference for last state. Image existing for state must be checked before "push"
    def image(self):
        if not self.state().any_image(self.mapdir, self.format):
            print("::TMS-SM::(Fatal error. Image does not exist for current state", self.state(), ")")
        else:
            curr_path = self.state().to_path(self.mapdir, self.format)
            return ImageTk.PhotoImage(Image.open(curr_path))