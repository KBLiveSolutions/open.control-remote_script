from __future__ import absolute_import, print_function, unicode_literals
from .miditouchbar import MidiTouchbar

def create_instance(c_instance):
    return MidiTouchbar(c_instance=c_instance)
