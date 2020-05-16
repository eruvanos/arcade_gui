import arcade

from arcade_gui import UIView, UILabel, UIButton, UIInputBox, UIEvent, UI3DButton


class MyView(UIView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup()

    def setup(self):
        self.purge_ui_elements()

        self.add_ui_element(UILabel(
            'Username:',
            center_x=100,
            center_y=self.window.height // 2,
            width=300,
            height=40,
        ))
        self.add_ui_element(UIInputBox(
            center_x=350,
            center_y=self.window.height // 2,
            width=300,
            height=40,
            id='username'
        ))
        self.add_ui_element(UI3DButton(
            'Login',
            center_x=650,
            center_y=self.window.height // 2,
            width=200,
            height=40,
            id='submit_button'
        ))

        self.add_ui_element(UILabel(
            '',
            center_x=self.window.width // 2,
            center_y=self.window.height // 2 - 100,
            width=600,
            height=40,
            id='login_message'
        ))

    def on_event(self, event: UIEvent):
        super(MyView, self).on_event(event)

        if event.type == UIButton.CLICKED and event.ui_element.id == 'submit_button':
            # Trigger action if 'submit_button' was clicked
            self.submit()
        elif event.type == UIInputBox.ENTER and event.ui_element.id == 'username':
            # Trigger action if ENTER pressed in 'username'-UIInputBox
            self.submit()

    # noinspection PyTypeChecker
    def submit(self):
        username_input: UIInputBox = self.find_by_id('username')
        username = username_input.text

        login_message: UILabel = self.find_by_id('login_message')
        login_message.text = f'Welcome {username}, you are my first player.'


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
