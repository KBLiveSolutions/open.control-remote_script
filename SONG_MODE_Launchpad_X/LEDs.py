from builtins import range
from builtins import object
from . import consts_SM

ARROW_BUTTONS = {
'up_button' : consts_SM.UP_BUTTON,
'down_button' : consts_SM.DOWN_BUTTON,
'left_button' : consts_SM.LEFT_BUTTON,
'right_button' : consts_SM.RIGHT_BUTTON,
}

class LEDs(object):
    def __init__(self, control_surface, version):
        self.control_surface = control_surface
        self.is_active = 0
        if version >= 10:
            self.color_index_table = consts_SM.COLOR_INDEX_L10
            self.slow = 10
            self.fast = 14
        else:
            self.color_index_table = consts_SM.COLOR_INDEX_L9
            self.slow = 10
            self.fast = 14

    def set_led_color(self, color_index, pad_num, blink_type):
        if consts_SM.CONTROLLER == 'LP':
            if blink_type == 'normal':
                message = (144 + consts_SM.CHANNEL, pad_num, self.color_index_table[color_index])
            if blink_type == 'slow_blink':
                self.send_midi((144 + consts_SM.CHANNEL, pad_num, self.color_index_table['black']))
                message = (144 + 2, pad_num, self.color_index_table[color_index])
            if blink_type == 'fast_blink':
                self.send_midi((144 + consts_SM.CHANNEL, pad_num, self.color_index_table['black']))
                message = (144 + 1, pad_num, self.color_index_table[color_index])
            if blink_type == 'fast_blink_yellow':
                self.send_midi((144 + consts_SM.CHANNEL, pad_num, self.color_index_table['yellow']))
                message = (144 + 1, pad_num, self.color_index_table[color_index])
            if self.is_active > 0 and message[1] != -1:
                self.send_midi(message)

        elif consts_SM.CONTROLLER == 'Push2':
            if blink_type == 'normal':
                self.send_midi((144, pad_num, self.color_index_table[color_index]))
            if blink_type == 'slow_blink':
                self.send_midi((144, pad_num, self.color_index_table['black']))
                self.send_midi((144 + self.slow, pad_num, self.color_index_table[color_index]))
            if blink_type == 'fast_blink':
                self.send_midi((144, pad_num, self.color_index_table['black']))
                self.send_midi((144 + self.fast, pad_num, self.color_index_table[color_index]))
            if blink_type == 'fast_blink_yellow':
                self.send_midi((144, pad_num, self.color_index_table['yellow']))
                self.send_midi((144 + self.fast, pad_num, self.color_index_table[color_index]))

    def set_arrow_color(self, button_name, state):
        if consts_SM.CONTROLLER == 'LP':
            val = 14
        if consts_SM.CONTROLLER == 'Push2':
            val = 127
        if state:
            midi_message = (176+ consts_SM.CHANNEL, ARROW_BUTTONS[button_name]['NUM'], val)
        else:
            midi_message = (176+ consts_SM.CHANNEL, ARROW_BUTTONS[button_name]['NUM'], 0)
        self.send_midi(midi_message)


    def clear(self):
        for pad_num in consts_SM.PAD_MATRIX:
            self.send_midi((144 + consts_SM.CHANNEL, pad_num, self.color_index_table['black']))
        for arrow_button in ARROW_BUTTONS:
            self.send_midi((176+ consts_SM.CHANNEL, ARROW_BUTTONS[arrow_button]['NUM'], 0))

    def set_zero(self, color):
        for i in range(len(consts_SM.PAD_MATRIX)):
            rgb = 'black'
            if consts_SM.zero[i] == 1:
                rgb = color
            self.send_midi((144 + consts_SM.CHANNEL, consts_SM.PAD_MATRIX[i], self.color_index_table[rgb]))

    def send_midi(self, midi_event_bytes):
        self.control_surface._send_midi(midi_event_bytes)
