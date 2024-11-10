import board

class pcd8544_config:
    def __init__(self, mode):
        self.mode = mode
        if self.mode == "rpi":
            self.__set_gpio_rpi()
        elif self.mode == "uhp":
            self.__set_gpio_uhp()
        elif self.mode == "uhp_r2":
            self.__set_gpio_uhp_r2()

    def __set_gpio_rpi(self):
        self.sck     = board.D11
        self.mosi    = board.D10
        self.dc      = board.D25
        self.cs      = board.D8
        self.rst     = board.D24
        self.light   = board.D23
        self.buttons = (board.D27, board.D22, board.D6, board.D5)
        self.int_pin = board.D4

    def __set_gpio_uhp(self):
        self.sck     = board.GP18
        self.mosi    = board.GP19
        self.dc      = board.GP10
        self.cs      = board.GP22
        self.rst     = board.GP6
        self.light   = board.GP7
        self.buttons = (board.GP9, board.GP8, board.GP12, board.GP11)
        self.int_pin = board.GP3

    def __set_gpio_uhp_r2(self):
        self.sck     = board.GP18
        self.mosi    = board.GP19
        self.dc      = board.GP10
        self.cs      = board.GP22
        self.rst     = board.GP9
        self.light   = board.GP8
        self.buttons = (board.GP6, board.GP7, board.GP12, board.GP11)
        self.int_pin = board.GP3
