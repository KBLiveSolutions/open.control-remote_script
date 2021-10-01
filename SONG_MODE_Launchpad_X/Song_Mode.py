from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import range
from past.utils import old_div
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.ModesComponent import ModesComponent, LayerMode, AddLayerMode, ImmediateBehaviour, CancellableBehaviour
from _Framework.InputControlElement import *
from .Scenes import Session, SongList
from .Markers import Arrangement, MarkerList
from .Matrix import Matrix, Buttons
from .Loopers import LooperMode
from .LEDs import LEDs
from . import consts_SM

MATRIX_LENGTH = len(consts_SM.PAD_MATRIX)
HALF_MATRIX_LENGTH = old_div(MATRIX_LENGTH, 2)
BUTTON_LIST = {'UP_BUTTON': consts_SM.UP_BUTTON, 'DOWN_BUTTON': consts_SM.DOWN_BUTTON, 'LEFT_BUTTON': consts_SM.LEFT_BUTTON, 'RIGHT_BUTTON': consts_SM.RIGHT_BUTTON,
'SHIFT_BUTTON': consts_SM.SHIFT_BUTTON, 'STOP_ALL_CLIPS_BUTTON': consts_SM.STOP_ALL_CLIPS_BUTTON, 'LAYOUT_BUTTON': consts_SM.LAYOUT_BUTTON,
'PLAY_BUTTON': consts_SM.PLAY_BUTTON, 'RESTART_BUTTON': consts_SM.RESTART_BUTTON, 'MODE_BUTTON': consts_SM.MODE_BUTTON, 'NEW_BUTTON': consts_SM.NEW_BUTTON,
'DELETE_BUTTON': consts_SM.DELETE_BUTTON, 'RECORD_BUTTON': consts_SM.RECORD_BUTTON, 'LOOP_BUTTON': consts_SM.LOOP_BUTTON, 'UNDO_BUTTON': consts_SM.UNDO_BUTTON,
'NOTE_BUTTON': consts_SM.NOTE_BUTTON, 'SESSION_BUTTON': consts_SM.SESSION_BUTTON, 'NEXT_SCENE_BUTTON': consts_SM.NEXT_SCENE_BUTTON, 'PREV_SCENE_BUTTON': consts_SM.PREV_SCENE_BUTTON}

#
# ### Launchpad MK2
#
# class Song_Mode():
#
#     def __init__(self, control_surface, *a, **k):
#         self.control_surface = control_surface
#         self.buttons = []
#         self.is_active = 0
#         self.shift_button = 0
#         self.controller = "Launchpad"
#         self.model = "MK2"
#         self.new_button = 0
#         self.delete_button = 0
#         self.old_beat = 0
#         self.mode_button = 0
#         self.stop_toggle = False
#         self.is_playing = False
#         self.temp_switch_on = False
#         self.color_mode_on = 0
#         self.matrix_length = len(consts_SM.PAD_MATRIX)/2
#         self.restart_position = self._song.current_song_time
#         self.active_view = 'arrangement'
#         with self.control_surface.component_guard():
#             version = Live.Application.get_application().get_major_version()
#             self.leds = LEDs(self.control_surface, version)
#             self.create_pads()
#             self.main_view = {'session': Session(self), 'arrangement': Arrangement(self), 'looper': LooperMode(self)}
#             if self.main_view['session'].song_amount > 0:
#                 self.active_view = 'session'
#             self.active_view = 'looper'
#             self.create_buttons()
#             self._song.add_current_song_time_listener(self.midi_clock)
#             self._song.add_is_playing_listener(self.on_is_playing_changed)
#             # self._song.add_record_mode_listener(self.on_is_recording_changed)
#             self._song.add_loop_listener(self.on_loop_changed)
#
#     def create_buttons(self):
#             self.pad_matrix_song = Matrix(consts_SM.PAD_MATRIX[:self.matrix_length])
#             self.pad_matrix_scene = Matrix(consts_SM.PAD_MATRIX[self.matrix_length:])
#             for i in range(self.matrix_length*2):
#                 self.buttons.append(Buttons(consts_SM.PAD_MATRIX[i], i))
#                 self.buttons[i].button.add_value_listener(self.on_pad_pressed, identify_sender= True)
#             self.up_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.UP_BUTTON['NUM'])
#             self.up_button.add_value_listener(self.on_up_button_pressed)
#             self.down_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.DOWN_BUTTON['NUM'])
#             self.down_button.add_value_listener(self.on_down_button_pressed)
#             self.left_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.LEFT_BUTTON['NUM'])
#             self.left_button.add_value_listener(self.on_left_button_pressed)
#             self.right_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.RIGHT_BUTTON['NUM'])
#             self.right_button.add_value_listener(self.on_right_button_pressed)
#             self.shift_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.SHIFT_BUTTON['NUM'])
#             self.shift_button.add_value_listener(self.on_shift_button_pressed)
#             self.stop_clips_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.STOP_ALL_CLIPS_BUTTON['NUM'])
#             self.stop_clips_button.add_value_listener(self.on_stop_clips_button_pressed)
#             self.play_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.PLAY_BUTTON['NUM'])
#             self.play_button.add_value_listener(self.on_play_button_pressed)
#             self.delete_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.DELETE_BUTTON['NUM'])
#             self.delete_button.add_value_listener(self.on_delete_button_pressed)
#             self.new_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.NEW_BUTTON['NUM'])
#             self.new_button.add_value_listener(self.on_new_button_pressed)
#             self.restart_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.RESTART_BUTTON['NUM'])
#             self.restart_button.add_value_listener(self.on_restart_button_pressed)
#             self.mode_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.MODE_BUTTON['NUM'])
#             self.mode_button.add_value_listener(self.on_mode_button_pressed)
#             self.loop_button = ButtonElement(True, MIDI_NOTE_TYPE, consts_SM.CHANNEL, consts_SM.LOOP_BUTTON['NUM'])
#             self.loop_button.add_value_listener(self.on_loop_button_pressed)
#             self._song.view.add_selected_scene_listener(self.main_view['session'].on_selected_scene_changed)
#             self.main_view['session'].on_selected_scene_changed()

### ALL but LP MK2

class Song_Mode(ControlSurface):

    def __init__(self, *a, **k):
        super(Song_Mode, self).__init__(*a, **k)
        self.control_surface = self
        self.buttons = []
        self.controller = "Launchpad"
        self.model = "X"
        self.is_active = 0
        self.shift_button = 0
        self.new_button = 0
        self.shift_button = 0
        self.delete_button = 0
        self.session_button_pressed = 0
        self.note_button_pressed = 0
        self.old_beat = 0
        self.mode_button = 0
        self.stop_toggle = False
        self.is_playing = False
        self.color_mode_on = 0
        self.tick = False
        self.matrix_length = old_div(len(consts_SM.PAD_MATRIX),2)
        self.restart_position = self._song.current_song_time
        self.active_view = 'arrangement'

        with self.control_surface.component_guard():
            version = Live.Application.get_application().get_major_version()
            self.view = Live.Application.get_application().view
            self.leds = LEDs(self.control_surface, version)
            self.create_pads()
            self._create_modes()
            self._create_buttons()
            self._create_song_listeners()


    def _create_modes(self):
        self.main_view = {'session': Session(self), 'arrangement': Arrangement(self), 'looper': LooperMode(self)}
        if self.main_view['session'].song_amount > 0:
            self.active_view = 'session'
        self.prev_active_view = self.active_view
        # self.active_view = 'looper'


    def _create_buttons(self):
        self.up_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.UP_BUTTON['NUM'])
        self.up_button.add_value_listener(self.on_up_button_pressed)
        self.down_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.DOWN_BUTTON['NUM'])
        self.down_button.add_value_listener(self.on_down_button_pressed)
        self.left_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.LEFT_BUTTON['NUM'])
        self.left_button.add_value_listener(self.on_left_button_pressed)
        self.right_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.RIGHT_BUTTON['NUM'])
        self.right_button.add_value_listener(self.on_right_button_pressed)
        self.shift_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.SHIFT_BUTTON['NUM'])
        self.shift_button.add_value_listener(self.on_shift_button_pressed)
        self.stop_clips_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.STOP_ALL_CLIPS_BUTTON['NUM'])
        self.stop_clips_button.add_value_listener(self.on_stop_clips_button_pressed)
        self.play_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.PLAY_BUTTON['NUM'])
        self.play_button.add_value_listener(self.on_play_button_pressed)
        self.delete_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.DELETE_BUTTON['NUM'])
        self.delete_button.add_value_listener(self.on_delete_button_pressed)
        self.new_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.NEW_BUTTON['NUM'])
        self.new_button.add_value_listener(self.on_new_button_pressed)
        self.restart_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.RESTART_BUTTON['NUM'])
        self.restart_button.add_value_listener(self.on_restart_button_pressed)
        self.loop_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.LOOP_BUTTON['NUM'])
        self.loop_button.add_value_listener(self.on_loop_button_pressed)
        if self.controller == "Launchpad":
            self.view_button_timer = Live.Base.Timer(callback=self._on_view_button_timer, interval=500, repeat=True)
            if self.model == "mini_MK3":
                self.mode_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.MODE_BUTTON['NUM'])
                self.mode_button.add_value_listener(self.on_mode_button_pressed)
                self.session_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 95)
                self.session_button.add_value_listener(self.on_session_pad_pressed)
                self.drums_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 96)
                self.drums_button.add_value_listener(self.on_drums_button_pressed)
                self.keys_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 97)
                self.keys_button.add_value_listener(self.on_keys_button_pressed)
                self.user_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 98)
                self.user_button.add_value_listener(self.on_user_button_pressed)
                for control_surface in Live.Application.get_application().control_surfaces:
                    name = str(control_surface)
                    if name.find('Launchpad_X_for_Song_Mode') > -1:
                        self.LP_X_DAW = control_surface
            elif self.model == "X":
                self.last_layout_byte = 4
                self.LP_sysex = 12
                self.mode_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.MODE_BUTTON['NUM'])
                self.mode_button.add_value_listener(self.on_mode_button_pressed)
                self.session__mode_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 95)
                self.session__mode_button.add_value_listener(self.on_session__mode_button_pressed)
                self.note_mode_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 96)
                self.note_mode_button.add_value_listener(self.on_note_mode_button_pressed)
                self.custom_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, 97)
                self.custom_button.add_value_listener(self.on_custom_button_pressed)
                self.record_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.RECORD_BUTTON['NUM'])
                self.record_button.add_value_listener(self.on_record_button_pressed)
                for control_surface in Live.Application.get_application().control_surfaces:
                    name = str(control_surface)
                    if name.find('Launchpad_X_for_Song_Mode') > -1:
                        self.LP_X_DAW = control_surface
        if self.controller == "Push":
            self.note_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.NOTE_BUTTON['NUM'])
            self.note_button.add_value_listener(self.on_note_button_pressed)
            self.session_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.SESSION_BUTTON['NUM'])
            self.session_button.add_value_listener(self.on_session_button_pressed)
            self.undo_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.UNDO_BUTTON['NUM'])
            self.undo_button.add_value_listener(self.on_undo_button_pressed)
            self.next_scene_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.NEXT_SCENE_BUTTON['NUM'])
            self.next_scene_button.add_value_listener(self.main_view['session'].on_next_scene_button_pressed)
            self.prev_scene_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.PREV_SCENE_BUTTON['NUM'])
            self.prev_scene_button.add_value_listener(self.main_view['session'].on_prev_scene_button_pressed)
            self.layout_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.LAYOUT_BUTTON['NUM'])
            self.layout_button.add_value_listener(self.on_layout_button_pressed)
            self.record_button = ButtonElement(True, MIDI_CC_TYPE, consts_SM.CHANNEL, consts_SM.RECORD_BUTTON['NUM'])
            self.record_button.add_value_listener(self.on_record_button_pressed)
            self.session_button_pressed = 0
            self.session_note_pressed = 0

    def _create_song_listeners(self):
        self._song.add_current_song_time_listener(self.midi_clock)
        self._song.add_is_playing_listener(self.on_is_playing_changed)
        self._song.add_record_mode_listener(self.on_is_recording_changed)
        self._song.add_loop_listener(self.on_loop_changed)
        self._song.view.add_selected_scene_listener(self.main_view['session'].on_selected_scene_changed)
        self.main_view['session'].on_selected_scene_changed()

    @property
    def _song(self):
        return self.control_surface.song()

    def create_pads(self):
            self.pad_matrix = Matrix(consts_SM.PAD_MATRIX)
            self.pad_matrix_song = Matrix(consts_SM.PAD_MATRIX[:HALF_MATRIX_LENGTH])
            self.pad_matrix_scene = Matrix(consts_SM.PAD_MATRIX[HALF_MATRIX_LENGTH:])
            for i in range(MATRIX_LENGTH):
                button = Buttons(consts_SM.PAD_MATRIX[i], i)
                button.button.add_value_listener(self.on_pad_pressed, identify_sender=True)
                self.buttons.append(button)

    def is_active_changed(self, num):
        self.is_active = num
        self.leds.is_active = num
        if num == 1:
            self.shift_button = 0
            self.delete_button = 0
            self.new_button = 0
            self.set_special_buttons()
            self.change_view(self.active_view)

    def set_song_pad_led_color(self, color_index, pad_index, blink_type):
        self.leds.set_led_color(color_index, self.pad_matrix_song.get_pad(pad_index), blink_type)

    def set_scene_pad_led_color(self, color_index, pad_index, blink_type):
        self.leds.set_led_color(color_index, self.pad_matrix_scene.get_pad(pad_index), blink_type)

    def set_pad_led_color(self, color_index, pad_index, blink_type):
        self.leds.set_led_color(color_index, self.pad_matrix.get_pad(pad_index), blink_type)

    def change_view(self, mode):
        self.shift_button = 0
        self.new_button = 0
        self.main_view[self.active_view].set_view_on()
        for view in self.main_view:
            self.main_view[view].is_active = False
        self.main_view[self.active_view].is_active = True
        self.set_view_buttons()
        self.on_is_playing_changed()
        self.on_is_recording_changed()
        self.on_loop_changed()

    def on_note_button_pressed(self, value):
        self.note_button_pressed = 1
        if value:
            if self.session_button_pressed == 1:
                self.active_view = 'looper'
            else:
                self.active_view = 'arrangement'
            Live.Application.get_application().view.focus_view("Arranger")
        else:
            self.note_button_pressed = 0
        self.change_view(self.active_view)
        self.check_layout()
        self.set_view_buttons()

    def on_session_button_pressed(self, value):
        self.session_button_pressed = 1
        if value:
            if self.note_button_pressed == 1:
                self.active_view = 'looper'
            else:
                self.active_view = 'session'
                Live.Application.get_application().view.focus_view("Session")
        else:
            self.session_button_pressed = 0
        self.change_view(self.active_view)
        self.check_layout()
        self.set_view_buttons()

    def on_is_playing_changed(self):
        state = 'half'
        # self.control_surface._do_send_midi((252, 0))
        if self._song.is_playing:
            self.is_playing = True
            state = 'on'
        else:
            self.is_playing = False
        self.set_button('PLAY_BUTTON', state)

    def on_is_recording_changed(self):
        state = 'half'
        if self._song.record_mode:
            self.is_recording = True
            state = 'on'
        else:
            self.is_recording = False
        if consts_SM.RECORD_BUTTON['NUM'] != -1:
            self.set_button('RECORD_BUTTON', state)

    def on_loop_changed(self):
        state = 'half'
        if self._song.loop:
            self.loop = True
            state = 'on'
        else:
            self.loop = False
        if self.active_view == "arrangement" and not self.main_view['arrangement'].no_marker:
            self.main_view['arrangement'].set_marker_buttons()
        self.set_button('LOOP_BUTTON', state)

    def set_button(self, button_name, state):
        midi_prefix = 144
        if BUTTON_LIST[button_name]['TYPE'] == 'MIDI_CC_TYPE':
            midi_prefix = 176
        color = BUTTON_LIST[button_name]['COLOR'][state]
        self.control_surface._send_midi((midi_prefix + consts_SM.CHANNEL, BUTTON_LIST[button_name]['NUM'],  self.leds.color_index_table[color]))

    def on_shift_button_pressed(self, value):

        self.main_view[self.active_view].on_shift_button_pressed(value)
        if value:
            color = 'on'
            self.shift_button = 1
        else:
            self.shift_button = 0
            color = 'half'
            if self.color_mode_on:
                self.exit_color_mode()
        self.set_button('SHIFT_BUTTON', color)

    def on_new_button_pressed(self, value):
        if value > 0:
            color = 'on'
            self.new_button = 1
        else:
            self.new_button = 0
            color = 'half'
        self.main_view[self.active_view].on_new_button_pressed(value)
        self.set_button('NEW_BUTTON', color)

    def on_restart_button_pressed(self, value):
        if self.active_view == 'arrangement':
            color = 'half'
            if value:
                color = 'on'
                self.restart_button = 1
                self._song.is_playing = 1
                self._song.current_song_time = self.restart_position
            self.restart_button = 0
        self.set_button('RESTART_BUTTON', color)

    def on_record_button_pressed(self, value):

        if value:
            self.record_button = 1
            self._song.record_mode = 1 if self._song.record_mode == 0 else 0
        else:
            self.record_button = 0

    def on_delete_button_pressed(self, value):
        color = 'half'
        if value:
            if self.active_view == 'session':
                color = 'on'
            else:
                color = 'off'
            self.delete_button = 1
        else:
            if self.active_view == 'session':
                color = 'half'
            else:
                color = 'off'
            self.delete_button = 0
        self.set_button('DELETE_BUTTON', color)

    def on_play_button_pressed(self, value):
        if value:
            if not self.is_playing:
                if self.shift_button:
                    self._song.continue_playing()
                else:
                    self._song.start_playing()
                    self._song.current_song_time = self.restart_position
            else:
                self._song.stop_playing()

    def on_loop_button_pressed(self, value):

        if value:
            if self.shift_button:
                self._song.play_selection()
                if self.is_playing == 0:
                    self._song.stop_playing()
                self._song.loop = 1

            else:
                if not self.loop:
                    self._song.loop = 1
                else:
                    self._song.loop = 0

    def on_stop_clips_button_pressed(self, value):
        color = 'half'
        if value:
            color = 'on'
            if self.shift_button:
                self._song.back_to_arranger = 0
            else:
                self._song.stop_all_clips()
                self.playing_scene_index = -1
                self.playing_song = -1
            # self.set_song_buttons()
        self.set_button('STOP_ALL_CLIPS_BUTTON', color)

    def on_pad_pressed(self, value, id):

        if self.shift_button and value:
            if self.color_mode_on:
                color = consts_SM.COLOR_GRID[id.index]
                if color != 'black':
                    self.main_view[self.active_view].change_launcher_color(color)
                    self.exit_color_mode()
            else:
                self.main_view[self.active_view].select_launcher(id)
                self.enter_color_mode()
        else:
            if not self.color_mode_on:
                self.main_view[self.active_view].on_pad_pressed(id, value)

    def on_left_button_pressed(self, value):
        if value:
            self.main_view[self.active_view].on_left_button_pressed()

    def on_right_button_pressed(self, value):
        if value:
            self.main_view[self.active_view].on_right_button_pressed()

    def on_up_button_pressed(self, value):
        if value:
            self.main_view[self.active_view].on_up_button_pressed()

    def on_down_button_pressed(self, value):
        if value:
            self.main_view[self.active_view].on_down_button_pressed()

    def enter_color_mode(self):

        self.leds.clear()
        self.color_mode_on = True
        self.set_function_buttons_off()
        for i in range(len(consts_SM.PAD_MATRIX)):
            self.leds.set_led_color(consts_SM.COLOR_GRID[i], consts_SM.PAD_MATRIX[i], 'normal')

    def exit_color_mode(self):
        self.color_mode_on = False
        self.set_view_buttons()
        self.change_view(self.active_view)

    def disconnect(self):
        #self.is_active_changed(0)
        super(Song_Mode, self).disconnect()

    def set_special_buttons(self):
        if self.controller == "Launchpad":
            self.looper_switching = False
            if self.model == "MK2":
                pass
            elif self.model == "mini_MK3":
                self.control_surface._send_midi((176, 95, 1))
                self.control_surface._send_midi((176, 96, 1))
                self.control_surface._send_midi((176, 97, 1))
                self.control_surface._send_midi((176, 98, 13))
            elif self.model == "X":
                self.control_surface._send_midi((176, 95, 2))
                self.control_surface._send_midi((176, 96, 2))
                self.control_surface._send_midi((176, 97, 13))
        else:
            # self.control_surface._do_send_midi((251, 0))
            # self.control_surface._do_send_midi((252, 0))
            self.set_button('UNDO_BUTTON', 'on')
            self.tick = False
            self.check_layout()
            self.set_view_buttons()

    def check_layout(self):
        if self.controller == "Launchpad":
            pass
        else:
            color = 'half'
            if self.main_view[self.active_view ].layout == "advanced":
                color = 'on'
            self.set_button('LAYOUT_BUTTON', color)

    def set_view_buttons(self):
        if self.controller == "Launchpad":
            self.set_button('MODE_BUTTON', self.active_view)
        else:
            self.set_button('UNDO_BUTTON', 'half')
            if self.active_view == 'session':
                self.set_button('NOTE_BUTTON', 'half')
                self.set_button('SESSION_BUTTON', 'on')
                self.set_button('NEXT_SCENE_BUTTON', 'half')
                self.set_button('PREV_SCENE_BUTTON', 'half')
            else:
                self.set_button('NOTE_BUTTON', 'on')
                self.set_button('SESSION_BUTTON', 'half')
                self.set_button('NEXT_SCENE_BUTTON', 'off')
                self.set_button('PREV_SCENE_BUTTON', 'off')
            self.check_layout()

    def set_function_buttons_off(self):
        if self.controller == "Launchpad":
            for but in ['MODE_BUTTON','DELETE_BUTTON','PLAY_BUTTON', 'RESTART_BUTTON', 'LOOP_BUTTON', \
            'NEW_BUTTON', 'STOP_ALL_CLIPS_BUTTON']:
                self.set_button(but, 'off')
        else:
            for but in ['NOTE_BUTTON','SESSION_BUTTON','LAYOUT_BUTTON', 'UNDO_BUTTON', 'DELETE_BUTTON', \
            'RESTART_BUTTON', 'LOOP_BUTTON', 'NEW_BUTTON', 'STOP_ALL_CLIPS_BUTTON', 'PLAY_BUTTON']:
                self.set_button(but, 'off')

    def midi_clock(self):
        self.beat = int(self._song.current_song_time)
        if self.beat != self.old_beat:
            self.main_view['arrangement'].compare_cue(self.beat)
            self.old_beat = self.beat
        if not self.is_playing:
            self.restart_position = self._song.current_song_time

############################################
######## Controler Specific
############################################

# Launchpads

    def _on_view_button_timer(self):
        self.looper_switching = True
        self.prev_active_view = self.active_view
        self.active_view = 'looper'
        self.change_view(self.active_view)
        self.view_button_timer.stop()

    def on_mode_button_pressed(self, value):
        if value == 127:
            if self.shift_button and self.active_view != 'looper':
                self.main_view[self.active_view].switch_layout()
            # else:
            #     self.view_button_timer.stop()
            #     self.view_button_timer.start()
        else:
            if not self.shift_button:
                if self.looper_switching:
                    self.looper_switching = False
                else:
                    if self.active_view == 'session' :
                        self.on_note_button_pressed(127)
                        self.on_note_button_pressed(0)
                    else:
                        self.on_session_button_pressed(127)
                        self.on_session_button_pressed(0)
                self.looper_switching = False
                # self.view_button_timer.stop()

            # self.view_button_timer.stop()

# LP Mini MK3:
    def on_user_button_pressed(self, value):
        if value:
            self.is_active_changed(0)
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 14, 0, 247))
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 0, 6, 247))

    def on_drums_button_pressed(self, value):
        if value:
            self.is_active_changed(0)
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 14, 0, 247))
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 0, 4, 247))

    def on_keys_button_pressed(self, value):
        if value:
            self.is_active_changed(0)
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 14, 0, 247))
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 0, 5, 247))

    def on_session_pad_pressed(self, value):
        if value:
            self.is_active_changed(0)
            self.control_surface._send_midi((240, 0, 32, 41, 2, 13, 14, 0, 247))
            self.LP_X_DAW._main_modes.selected_mode = 'session'

#### LP X

    def on_custom_button_pressed(self, value):
        if value:
            if self.is_active == 0:
                self.is_active_changed(1)
            else:
                self.is_active_changed(0)
                self.control_surface._send_midi((240, 0, 32, 41, 2, 12, 14, 0, 247))
                self.control_surface._send_midi((240, 0, 32, 41, 2, 12, 0, self.last_layout_byte[0], 247))

    def on_note_mode_button_pressed(self, value):
        if value:
            self.is_active_changed(0)
            self.control_surface._send_midi((240, 0, 32, 41, 2, 12, 14, 0, 247))
            self.control_surface._send_midi((240, 0, 32, 41, 2, 12, 0, 1, 247))

    def on_session__mode_button_pressed(self, value):
        if value:
            self.is_active_changed(0)
            self.LP_X_DAW._send_midi((240, 0, 32, 41, 2, 12, 14, 0, 247))
            self.LP_X_DAW._main_modes.selected_mode = 'session'

    def LP_last_layout_byte(self, value):
        self.last_layout_byte = value

#### Push

    def on_undo_button_pressed(self, value):
        color = self.leds.color_index_table['high']
        if value:
            color = self.leds.color_index_table['high']
            self._song.undo()
        self.control_surface._send_midi((176 + consts_SM.CHANNEL, consts_SM.UNDO_BUTTON, color))

    def on_layout_button_pressed(self, value):
        if value:
            self.main_view[self.active_view].switch_layout()
        self.check_layout()

    def handle_sysex(self, midi_bytes):
        if self.model == "Push2":
            if midi_bytes == (240, 0, 33, 29, 1, 1, 10, 1, 247):
                self.is_active_changed(1)

            if midi_bytes == (240, 0, 33, 29, 1, 1, 10, 0, 247):
                self.is_active_changed(0)
        if self.model == "Push1":
            if midi_bytes == (240, 71, 127, 21, 98, 0, 1, 1, 247):
                self.is_active_changed(1)

            if midi_bytes == (240, 71, 127, 21, 98, 0, 1, 0, 247):
                self.is_active_changed(0)
