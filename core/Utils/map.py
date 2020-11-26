import json

import arcade
import core.Errors as errs
from core.Utils.colors import bcolors as css


def map_parser(cmd, params):
    # TODO add funcs to this parser
    if '-h' in params:
        raise NotImplementedError

    # HELP
    if cmd=='help':
        if not len(params):
            print(css.HEADER+'[*]'+css.ENDC+' List of commands:')
            [print(command) for command in json.loads(open('core/commands.json').read())['commands']]
        else:
            # TODO add specific docs
            raise NotImplementedError
    
    # SHOW
    elif cmd=='show':
        # NO SELECT -> NO SHOW
        raise errs.DeprecationError()
        overrideshow=False
        if '-a' in params:
            overrideshow=True
        if 'id' in params or '-id' in params:
            showids=True
            showpos=False
        elif 'pos' in params or '-pos' in params:
            showids=False
            showpos=True
        elif 'null' in params or '-null' in params:
            showids=False
            showpos=False
        else:
            raise errs.ParamError(params)
        return ['showupdate', showids, showpos, overrideshow] # TODO use thuis in the map
    
    # SELECT
    elif cmd=='select':
        raise errs.DeprecationError('use mouse click instead')
        pass # now mouse click
    
    # EXIT && BYE
    elif cmd in ['bye', 'exit']:
        raise errs.DeprecationError()
        pass # now ESC key
    
    # SHOP
    elif cmd=='shop':
        # TODO add the shop
        raise NotImplementedError()
    
    # RECO
    elif cmd in ['reco', 'recognitors']:
        # TODO add recognition team
        raise NotImplementedError()

    # SMTP
    elif cmd in ['smtp', 'email']:
        # TODO add the graphic mail service
        raise NotImplementedError()

    return [None]

class HelpMainView(arcade.View):
    def __init__(self, you, mode, window=None):
        super().__init__(window=window)
        self.game=you
        self.path='core/commands.json'
        if mode=='bot':
            self.path='core/Characters/commands.json'
    
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "[*] List of commands:",
            320, 215+(20*len(json.loads(open(self.path).read())['commands'])),
            arcade.color.BLACK,
            anchor_x='center',
            font_size=21
        )
        [arcade.draw_text(
            command,
            320, 390-(30*json.loads(open(self.path).read())['commands'].index(command)),
            arcade.color.BLACK,
            anchor_x='center',
            font_size=18
        ) for command in json.loads(open(self.path).read())['commands']]
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(self.game)

    def on_key_press(self, symbol, modifiers):
        self.window.show_view(self.game)

class WinView(arcade.View):
    pass