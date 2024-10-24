import math
class draw_graph():
    def __init__(self, display, x_pos, y_pos, width, height, y_max, y_min, data = []):
        self.display  = display
        self.x_pos    = x_pos
        self.y_pos    = y_pos
        self.width    = width
        self.height   = height
        self.y_max    = y_max
        self.y_min    = y_min
        # TODO: データ溢れ対応
        self.data     = data
        self.draw_box()
        self.display.show()

    def draw_box(self):
        self.display.hline(self.x_pos, self.y_pos, self.width,  1)
        self.display.vline(self.x_pos, self.y_pos, self.height, 1)
        self.display.hline(self.x_pos, self.y_pos + self.height - 1, self.width, 1)
        self.display.vline(self.x_pos + self.width - 1, self.y_pos, self.height, 1)

    def add_data(self, new_data):
        self.data.append(new_data)
        if self.width - 2 < len(self.data):
            del self.data[0]

    def draw_graph(self):
        self.display.fill_rect(self.x_pos + 1, self.y_pos  + 1, self.width - 2, self.height - 2, 0)
        for c, i in enumerate(self.data):
            if self.y_max <= i:
              continue
            value = self.height - (math.ceil(i) - self.y_min) * self.height // ( self.y_max - self.y_min ) + self.y_pos
            self.display.pixel(self.x_pos + 1 + c, value, 1)
            previous = value
        self.display.show()