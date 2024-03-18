import json
import logging
import os

from PIL import Image

import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import Widget
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.faces as faces

MAPPING = [value for name, value in vars(faces).items() if not name.startswith('_') and isinstance(value, str)]

def load_sprite_sheet(path, sprite_size):
        with Image.open(path) as sheet:
            # Lots of processing to do.

            sheet = sheet.convert('RGBA')
            pixels = sheet.load()

            for y in range(sheet.size[1]):
                for x in range(sheet.size[0]):
                    if pixels[x,y][3] < 255:    # check alpha
                        pixels[x,y] = (255, 255, 255, 255)

            # Processing done, let's cut up this sprite sheet.

            sprite_sheet_width, sprite_sheet_height = sheet.size

            if not sprite_size:
                sprite_size = sprite_sheet_width

            sprite_count = sprite_sheet_height // sprite_size

            if sprite_sheet_width < sprite_size:
                raise ValueError('sprite sheet is smaller than sprite size')

            if sprite_count < len(MAPPING):
                raise ValueError('sprite sheet (%dx%d) has fewer sprites than defined faces: %d < %d', sprite_sheet_width, sprite_sheet_height, sprite_count, len(MAPPING))

            return [ sheet.crop((0, sprite_size * y, sprite_size, (sprite_size * y) + sprite_size)) for y in range(sprite_count) ]

class SpriteFace(Widget):
    def __init__(self, sprite, size, value="", position=(0, 0)):
        super().__init__(position)
        self.value = value

        self.sprites = load_sprite_sheet(sprite, size)

        logging.debug("loaded %d sprites from %s", len(self.sprites), sprite)

    def _get_active_sprite(self):
        try:
            index = MAPPING.index(self.value)
        except ValueError:
            logging.error('using unknown face: %s', self.value)
            index = MAPPING.index(faces.BROKEN)

        sprite = self.sprites[index]
        sprite_width, sprite_height = sprite.size

        logging.debug('loaded sprite %d (%dx%d) for value %s', index, sprite_width, sprite_height, self.value)

        return self.sprites[index]

    def draw(self, canvas, drawer):
        if self.value is None:
            return

        canvas.paste(self._get_active_sprite(), self.xy)

class SpriteFaces(plugins.Plugin):
    __author__ = 'james@notjam.es'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'Cute faces.'


    def __init__(self):
        self.running = True

    def _get_sprite(self, name):
        if 'sprites' not in self.options:
            raise ValueError('invalid config - missing sprites')

        sprites = self.options['sprites']

        if name not in sprites:
            raise ValueError('invalid config - missing sprite %s', name)

        sprite_size = sprites[name]['size']
        sprite_path = sprites[name]['path']

        return sprite_path, sprite_size

    def on_ui_setup(self, ui):
        face_sprite_path, face_sprite_size = self._get_sprite('face')

        try:
            friend_sprite_path, friend_sprite_size = self._get_sprite('friend')
        except:
            friend_sprite_path, friend_sprite_size = face_sprite_path, face_sprite_size

        # TODO: Something is wrong with this but I can't currently fix it
        face_position = ui._layout['face']
        friend_position = ui._layout['friend_face']

        ui.add_element('face', SpriteFace(face_sprite_path, face_sprite_size, value=faces.SLEEP, position=ui._layout['face']))
        ui.add_element('friend_face', SpriteFace(friend_sprite_path, friend_sprite_size, value=faces.SLEEP, position=friend_position))
