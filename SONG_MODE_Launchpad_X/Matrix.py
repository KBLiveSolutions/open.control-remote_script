from builtins import object
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import *
from . import consts_SM

MIDI_CHANNEL = consts_SM.CHANNEL
IS_MOMENTARY = True

class Matrix(object):

    def __init__(self, pad_matrix):
        self.pad_matrix = pad_matrix
        self.song_pad = []
        self.scene_pad = []
        self.matrix = [el for el in pad_matrix]

    def get_pad(self, pad_index):
        return self.matrix[pad_index]


class Buttons(object):

    def __init__(self, num, index):
        self.button = ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL, num)
        self.button.index = index
