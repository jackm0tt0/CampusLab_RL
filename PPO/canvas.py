import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import TextBox

class show_canvas:
    def __init__(self):
        self.figure2, self.ax2 = plt.subplots()
        self.ax2.axis('off')  # Turn off the axis

        # Dimensions of the black rectangular window
        rect_width = 0.8
        rect_height = 0.6

        # Dimensions of the white window on the black rectangular window
        window_width = 0.6
        window_height = 0.1

        # Position of the black rectangular window
        rect_position = ((1 - rect_width) / 2, (1 - rect_height) / 2)

        # Position of the white window at the center of the black rectangular window
        window_position = (rect_position[0] + (rect_width - window_width) / 2,
                           rect_position[1] + (rect_height - window_height) / 2)

        self.black_rect = Rectangle(rect_position, rect_width, rect_height, color='black')
        self.ax2.add_patch(self.black_rect)

        self.white_window = Rectangle(window_position, window_width, window_height, color='white')
        self.ax2.add_patch(self.white_window)

        self.text_inside = TextBox(plt.axes([0.7, 0.9, 0.2, 0.05]), 'T-inside', initial='0.0')
        self.text_outside = TextBox(plt.axes([0.7, 0.85, 0.2, 0.05]), 'T-outside', initial='0.0')
        self.text_action = TextBox(plt.axes([0.7, 0.8, 0.2, 0.05]), 'T-Action', initial='0')
        self.text_step = TextBox(plt.axes([0.7, 0.75, 0.2, 0.05]), 'T-Step', initial='0')

    def update(self, action, T_inside, T_outside,step):
        if action == 1:
            self.white_window.set_color('white')
        elif action == 0:
            self.white_window.set_color('black')

        self.text_inside.set_val('%.2f' % T_inside)
        self.text_outside.set_val('%.2f' % T_outside)
        self.text_action.set_val(str(action))
        self.text_step.set_val(str(step))

        self.figure2.canvas.draw()
        plt.pause(0.01)