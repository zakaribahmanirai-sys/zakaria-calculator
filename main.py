
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window


Window.clearcolor = (0.025, 0.025, 0.03, 1)


class CircleButton(Button):
    def __init__(self, **kwargs):
        self.circle_color = kwargs.pop(
            "circle_color", (0.12, 0.12, 0.14, 1)
        )
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = "23sp"

        with self.canvas.before:
            self.bg_color = Color(*self.circle_color)
            self.circle = Ellipse(
                pos=self.pos, size=self.size
            )

        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size


class CalculatorApp(App):

    def build(self):
        self.expression = ""

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=12
        )

        self.display = Label(
            text="0",
            font_size="48sp",
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            size_hint=(1, 0.28)
        )
        self.display.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )
        root.add_widget(self.display)

        grid = GridLayout(
            cols=4,
            spacing=10,
            size_hint=(1, 0.72)
        )

        buttons = [
            "AC", "DEL", "sin", "cos",
            "tan", "√", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            ".", "00", "=", "0"
        ]

        for value in buttons:
            if value in ["÷", "×", "-", "+", "=", "sin", "tan"]:
                color = (1, 0.48, 0.12, 1)
            elif value == "cos":
                color = (0.95, 0.57, 0.24, 1)
            elif value in ["AC", "DEL", "√", "%"]:
                color = (0.27, 0.27, 0.30, 1)
            else:
                color = (0.12, 0.12, 0.14, 1)

            button = CircleButton(
                text=value,
                circle_color=color,
                font_size="29sp" if value == "=" else "23sp"
            )
            button.bind(
                on_release=lambda btn:
                self.press(btn.text)
            )
            grid.add_widget(button)

        root.add_widget(grid)
        return root

    def press(self, value):
        if value == "AC":
            self.expression = ""
            self.display.text = "0"
            return

        if value == "DEL":
            self.expression = self.expression[:-1]
            self.display.text = self.expression or "("
            return

        if value == "=":
            try:
                expression = self.expression
                expression = expression.replace("×", "*")
                expression = expression.replace("÷", "/")
                expression = expression.replace("√", "sqrt")

                allowed = {
                    "sqrt": math.sqrt,
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                }

                result = eval(
                    expression,
                    {"__builtins__": {}},
                    allowed
                )

                if not math.isfinite(float(result)):
                    raise ValueError

                self.expression = str(round(result, 10))
                self.display.text = self.expression

            except Exception:
                self.display.text = "Error"
                self.expression = ""

            return

        if value == "√":
            self.expression += "sqrt("
        elif value in ["sin", "cos", "tan"]:
            self.expression += value + "("
        else:
            self.expression += value

        self.display.text = self.expression


if __name__ == "__main__":
    CalculatorApp().run()
