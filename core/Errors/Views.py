import arcade

class ErrorView(arcade.View):
    def __init__(self, error, you, window=None):
        super().__init__(window=window)
        self.err=error
        self.game=you
    
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            str(self.err),
            400, 300,
            arcade.color.BLACK,
            font_size=20,
            anchor_x='center'
        )
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(self.game)

    def on_key_press(self, symbol, modifiers):
        self.window.show_view(self.game)