import base64
import random
import time

import arcade
from core.Errors import *

random.seed(time.time())

class Kernel():
    def __init__(self):
        self.is_locked=True
        self.is_active=True
        self.ports={'80':1, '443':1}
        self.hashes={}
        [self.hashes.update({port:base64.b64encode(''.join([chr(random.randint(97,122)) for _ in range(5)]).encode()).decode()}) for port in self.ports.keys()]

class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.BLUE)
    
    def on_tap(self):
        return 'cant select urself!'


class Robot(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.RED)
        self.id=random.randint(10, 1000)
        self.kernel=Kernel()
    
    def on_tap(self):
        return 'helo im'+str(self.id)


class Tile(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.WHITE)
        self.isplayer=False
        self.isrobot=False
        self.level=1
    
    def to_robot(self):
        self.id=random.randint(10, 1000)
        self.color=arcade.color.RED
        self.kernel=Kernel()
        self.isrobot=True
        self.isplayer=False
        self.level=random.randint(1,3)
    
    def to_player(self):
        self.color=arcade.color.GREEN
        self.isplayer=True
        self.isrobot=False
    
    def on_tap(self):
        if self.isrobot:
            print('helo im '+str(self.id))
        elif self.isplayer:
            print('cant select yourself')
    
    def parser_inner(self, cmd, params, view=None):
        # TODO add the bot parser
        print('bot parser w/:',cmd,params)
        if cmd == 'hack':
            if (not ('-p' in params or '--port' in params)):
                raise SyntaxError()
                return 'Invalid Syntax, check "'+cmd+' -h"'
            else:
                if '-p' in params:
                    kw='-p'
                else: 
                    kw='--port'
            if bool(int(self.kernel.ports[str(params[params.index(kw)+1])])):
                return 'Unable to hack, this port is locked.'
            else:
                self.kernel.is_locked=False
                return 'Kernel successfully unlocked' # FIXME ma ndo cazzo lo scrive wtf è tutto a sinistra
        elif cmd == 'scan':
            res=[
                "[*] Scanning:"
            ]
            for key in self.kernel.hashes.keys():
                res.append(str(key)+': '+str(self.kernel.hashes[key]))
            return '\n\n'.join(res)
        elif cmd in ['destroy', 'shutdown']:
            if self.kernel.is_locked:
                return 'Unable to shutdown, kernel is locked.'
            else:
                self.color=arcade.color.WHITE # nella mappa basta il colore
                #view.window.show_view() # TODO trova il modo di passare game a show_view per tornare alla mappa dopo la kill
                # TODO increment score
                return 'Bot killed.'
        elif cmd == 'hash':
            if (not ('-t' in params)) and (not ('--text' in params)) or (not ('-p' in params or '--port' in params)):
                raise SyntaxError(); return 'Invalid syntax, check "'+cmd+' -h"'
            if '-t' in params:
                kw='-t'
            else:
                kw='--text' 
            if '-p' in params:
                pkw='-p'
            else:
                pkw='--port'
            if params[params.index(kw)+1]==base64.b64decode(self.kernel.hashes[params[params.index(pkw)+1]]).decode():
                self.kernel.ports[params[params.index(pkw)+1]]=0
                return 'Port '+str(params[params.index(pkw)+1])+' successfully bypassed.'
            else:
                return 'Invalid Hash given.'
            
        elif cmd in ['translater', 'decoder', 'encode']:
            # TODO add decoder.
            pass

        return None
    
    def parser(self, cmd, params, view):
        try:
            view.outs.append(str(self.parser_inner(cmd, params, view))) # TODO add animations during command execution!
        except Exception as e:
            print('an error as occured on line 70 while parsing the command (or updating view.outs)\nerror:',e,type(e))
            raise e
