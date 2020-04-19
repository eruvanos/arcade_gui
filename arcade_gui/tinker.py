import arcade


class View(arcade.View):
    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol, modifiers)
        print(chr(symbol))

    def update(self, delta_time: float):
        print('update')

    def on_update(self, delta_time: float):
        print('on_update')


arcade.Window().show_view(View())

arcade.run()