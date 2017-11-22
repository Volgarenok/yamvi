from image_window import ImageWindow
from mapviewer import TSMState, TSMStateMachine
import tkinter
root = tkinter.Tk()
basestate = TSMState(0, 0, 0)

# See TSMState.any_image(self) in mapviewe if you want customize dir with map
# Default @basedir is "map" and default @format is "png". Defined in mapviewer
if not basestate.any_image():
    print("::application::(Error. Image for base state does not exist)")
    exit(1)

# If you change default dir or image format
# don't forget tell state machine about it.
# Parameters are same: @basedir and @format
mapmachine = TSMStateMachine(basestate)
window = ImageWindow(root, "Map Viewer", mapmachine.image())

# Application interaction
# (7: zoom top left tile) (8: move uper tile onZ) (9: zoom top right tile)
# (4: move left tile onZ) (5: unzoom to par-tile) (6: move right tile onZ)
# (1: zoom bot left tile) (2: move down tile onZ) (3: zoom bot right tile)
def key(event):
    keylist = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    if not event.char in keylist:
        print("::key-func::(Check NUM-LOCK enable and use numpad)")
    if event.char == '5':
        mapmachine.pop()
        window.update(mapmachine.image())

    if event.char == '1':
        new_state = mapmachine.state().zoom(0, 0)
        if new_state.any_image():
            mapmachine.push(new_state)
            window.update(mapmachine.image())
        else:
            print("::key-func::(Zoom level does not exist)")

    if event.char == '7':
        new_state = mapmachine.state().zoom(0, 1)
        if new_state.any_image():
            mapmachine.push(new_state)
            window.update(mapmachine.image())
        else:
            print("::key-func::(Zoom level does not exist)")

    if event.char == '9':
        new_state = mapmachine.state().zoom(1, 1)
        if new_state.any_image():
            mapmachine.push(new_state)
            window.update(mapmachine.image())
        else:
            print("::key-func::(Zoom level does not exist)")

    if event.char == '3':
        new_state = mapmachine.state().zoom(1, 0)
        if new_state.any_image():
            mapmachine.push(new_state)
            window.update(mapmachine.image())
        else:
            print("::key-func::(Zoom level does not exist)")

    if event.char == '4':
        new_state = mapmachine.state().move(-1, 0)
        if new_state.any_image():
            mapmachine.update(new_state)
            window.update(mapmachine.image())
        else:
            print("key-func::(Tile's image does not exist)")

    if event.char == '8':
        new_state = mapmachine.state().move(0, 1)
        if new_state.any_image():
            mapmachine.update(new_state)
            window.update(mapmachine.image())
        else:
            print("key-func::(Tile's image does not exist)")

    if event.char == '6':
        new_state = mapmachine.state().move(1, 0)
        if new_state.any_image():
            mapmachine.update(new_state)
            window.update(mapmachine.image())
        else:
            print("key-func::(Tile's image does not exist)")

    if event.char == '2':
        new_state = mapmachine.state().move(0, -1)
        if new_state.any_image():
            mapmachine.update(new_state)
            window.update(mapmachine.image())
        else:
            print("key-func::(Tile's image does not exist)")

window.keybind(key)
window.start()
