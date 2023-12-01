import numpy as np
import matplotlib.pyplot as plt
from jupyter_ui_poll import ui_events
import time
import random
from IPython.display import clear_output

from ipywidgets import Button, widgets


class ButtonPoller:
    ui_choice = None
    ui_done = False

    @staticmethod
    def register(btn):
        btn.on_click(ButtonPoller.on_click)

    @staticmethod
    def on_click(btn):
        ButtonPoller.ui_done = True
        ButtonPoller.ui_choice = btn.description

    @staticmethod
    def get_press():
        ButtonPoller.ui_done = False
        with ui_events() as poll:
            while ButtonPoller.ui_done is False:
                poll(10)  # React to UI events (upto 10 at a time)
                time.sleep(0.1)
            ButtonPoller.ui_done = False  # Reset flag for next time

        return ButtonPoller.ui_choice


def annotate(x_data, y_data, filename):
    buttons = []
    n_pixels = int(np.sqrt(x_data.shape[1]))

    for directions in ["⬅️ Left", "⬆️ Up", "⬇️ Down", " ➡️ Right", "QUIT"]:
        button = Button(description=directions)
        buttons.append(button)
        ButtonPoller.register(button)

    direction_map = {
        "⬆️ Up": 0,
        "⬅️ Left": 1,
        "⬇️ Down": 2,
        " ➡️ Right": 3,
    }

    n_completed = 0
    while True:
        index = random.randint(0, len(x_data))
        image = x_data[index].reshape(n_pixels, n_pixels)
        g = plt.imshow(image, cmap="gray")

        display(widgets.HBox((buttons)))
        plt.show()
        print(f"Completed {n_completed}")
        x = ButtonPoller.get_press()
        clear_output(wait=True)
        if x == "QUIT":
            break

        with open(filename, "a") as f:
            f.write(f"{n_pixels}, {index}, {direction_map[x]}, {int(y_data[index])}\n")
        n_completed += 1
    return
