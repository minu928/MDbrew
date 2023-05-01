class ColorFont:
    _color_map = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    }

    def __init__(self) -> None:
        self.__font_shape__()
        self.__font_color__()
        self.__font_bright_color__()
        self.__background_color__()
        self.__background_color__()

    def pick_color(self, name, bright: bool = False, bg: str = False):
        color = self._color_map[name]
        color = color + 60 if bright else color
        color = color + 10 if bg else color
        return f"\033[{color}m"

    def __font_shape__(self):
        self.reset = "\033[0m"
        self.bold = "\033[1m"
        self.itatilc = "\033[3m"
        self.underline = "\033[4m"

    def __font_color__(self):
        self.font_black = self.pick_color("black", bright=False, bg=False)
        self.font_red = self.pick_color("red", bright=False, bg=False)
        self.font_green = self.pick_color("green", bright=False, bg=False)
        self.font_yellow = self.pick_color("yellow", bright=False, bg=False)
        self.font_blue = self.pick_color("blue", bright=False, bg=False)
        self.font_magenta = self.pick_color("magenta", bright=False, bg=False)
        self.font_cyan = self.pick_color("cyan", bright=False, bg=False)
        self.font_white = self.pick_color("white", bright=False, bg=False)

    def __font_bright_color__(self):
        self.font_bright_black = self.pick_color("black", bright=True, bg=False)
        self.font_bright_red = self.pick_color("red", bright=True, bg=False)
        self.font_bright_green = self.pick_color("green", bright=True, bg=False)
        self.font_bright_yellow = self.pick_color("yellow", bright=True, bg=False)
        self.font_bright_blue = self.pick_color("blue", bright=True, bg=False)
        self.font_bright_magenta = self.pick_color("magenta", bright=True, bg=False)
        self.font_bright_cyan = self.pick_color("cyan", bright=True, bg=False)
        self.font_bright_white = self.pick_color("white", bright=True, bg=False)

    def __background_color__(self):
        self.background_black = self.pick_color("black", bright=False, bg=True)
        self.background_red = self.pick_color("red", bright=False, bg=True)
        self.background_green = self.pick_color("green", bright=False, bg=True)
        self.background_yellow = self.pick_color("yellow", bright=False, bg=True)
        self.background_blue = self.pick_color("blue", bright=False, bg=True)
        self.background_magenta = self.pick_color("magenta", bright=False, bg=True)
        self.background_cyan = self.pick_color("cyan", bright=False, bg=True)
        self.background_white = self.pick_color("white", bright=False, bg=True)

    def __background_bright_color__(self):
        self.background_bright_black = self.pick_color("black", bright=True, bg=True)
        self.background_bright_red = self.pick_color("red", bright=True, bg=True)
        self.background_bright_green = self.pick_color("green", bright=True, bg=True)
        self.background_bright_yellow = self.pick_color("yellow", bright=True, bg=True)
        self.background_bright_blue = self.pick_color("blue", bright=True, bg=True)
        self.background_bright_magenta = self.pick_color("magenta", bright=True, bg=True)
        self.background_bright_cyan = self.pick_color("cyan", bright=True, bg=True)
        self.background_bright_white = self.pick_color("white", bright=True, bg=True)


if __name__ == "__main__":
    colorfont = ColorFont()
