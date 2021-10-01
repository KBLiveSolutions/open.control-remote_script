from __future__ import division
from builtins import str
from builtins import object
from past.utils import old_div
import Live
import time
from . import consts_SM

MATRIX_LENGTH = len(consts_SM.PAD_MATRIX)
HALF_MATRIX_LENGTH = old_div(MATRIX_LENGTH, 2)

class LooperMode(object):
    def __init__(self, song_mode, *a, **k):
        self.song_mode = song_mode
        self._song_view = self.song_mode._song.view
        self.state_color = {0: 'white', 1: 'red', 2: 'green', 3: 'marine', 'black': 'black'}
        self._selected_device = None
        self.global_looper_list = {}
        self._song.add_tracks_listener(self.rebuild_tracks_list)
        self._song.add_exclusive_arm_listener(self.check_exclusive_arm)
        self.check_exclusive_arm()
        self.rebuild_tracks_list()
        self.on_selected_track_changed()

    def _looper(self, num):
        return self.global_looper_list[num]

    def _pad(self, num):
        return num % 8 + (num - num % 8) * 4

    @property
    def _leds(self):
        return self.song_mode.leds

    def _print(self, *args):
        self.song_mode.control_surface.log_message(args)

    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def rebuild_tracks_list(self):
        try:
            self._selected_track.view.remove_selected_device_listener(self.on_selected_device_changed)
        except:
            pass
        try:
            self._song.view.remove_selected_track_listener(self.on_selected_track_changed)
        except:
            pass
        self._selected_device = None
        for i in self.global_looper_list:
            self.remove_looper(i)
        self.global_looper_list = {}
        self.track_list = []
        for track in self._song.tracks:
            self.track_list.append(TrackInstance(track, self))
        self._song.view.add_selected_track_listener(self.on_selected_track_changed)
        self.refresh_loopers()

    def on_selected_track_changed(self):
        try:
            self._selected_track.view.remove_selected_device_listener(self.on_selected_device_changed)
        except:
            pass
        try:
            self._selected_track.remove_devices_listener(self.on_selected_track_changed)
        except:
            pass
        self._selected_track = self._song_view.selected_track
        self._selected_track.add_devices_listener(self.on_selected_track_changed)
        self._selected_track.view.add_selected_device_listener(self.on_selected_device_changed)
        self.on_selected_device_changed()

    def on_selected_device_changed(self):
        try:
            self._selected_device.remove_name_listener(self.on_selected_device_name_changed)
        except:
            pass
        self._selected_device = self._selected_track.view.selected_device
        if self._selected_device and self._selected_device.class_display_name == "Looper":
            self._selected_device.add_name_listener(self.on_selected_device_name_changed)

    def check_exclusive_arm(self):
        self.exclusive_arm = self._song.exclusive_arm

    def add_looper(self, looper_instance):
        self.global_looper_list[looper_instance.num] = looper_instance

    def on_selected_device_name_changed(self):
        num = self.get_looper_number(self._selected_track.view.selected_device.name)
        if num > -1:
            self.check_duplicate(num)
            self.rebuild_tracks_list()

    def add_first_number_available(self, name):
        new_name = name
        num = 0
        while num in self.global_looper_list: num += 1
        new_name = new_name + " (LOOPER%s)" % str(num+1)
        return new_name.replace("  ", " ")

    def remove_looper_name(self):
        new_name = self._selected_device.name
        num1 = new_name.find("(LOOPER")
        if num1 > -1:
            num2 = new_name.find(")", num1) + 1
            new_name = new_name[:num1] + new_name[num2:]
        return new_name

    def check_duplicate(self, num):
        if num in self.global_looper_list:
            self.song_mode.control_surface.show_message("(LOOPER%s) already exists, please rename." % str(num + 1))

    def get_looper_number(self, name):
        num1 = name.find("(LOOPER")
        num3 = 0
        if num1 > -1:
            num3 = name[num1+7:name.find(")", num1)]
        return int(num3)-1

    def set_view_on(self):
        self.song_mode.set_button('SHIFT_BUTTON', 'half')
        self.song_mode.set_button('RESTART_BUTTON', 'off')
        self.song_mode.set_button('STOP_ALL_CLIPS_BUTTON', 'half')
        self.song_mode.set_button('NEW_BUTTON', 'half')
        self.song_mode.leds.clear()
        self.refresh_loopers()

    def refresh_loopers(self):
        if len(self.global_looper_list) == 0:
            self._leds.set_zero('half_yellow')
        else:
            self._leds.clear()
        for i in self.global_looper_list:
            self._looper(i).show_looper()

    def remove_looper(self, num):
        try:
            self.global_looper_list[num].state_param.remove_value_listener(self.global_looper_list[num].on_looper_state_changed)
        except:
            pass
        self.update_looper_state_button("black", num)
        self.update_track_color_button("black", num)
        self.update_track_mute_button("black", num)
        self.update_track_arm_button("black", num, 'normal')

    def on_shift_button_pressed(self, value):
        pass

    def on_pad_pressed(self, id, value):
        if value:
            button_num = id.index
            looper_num = button_num % 8
            if id.index > 31:
                button_num = id.index - 32
                looper_num = button_num % 8 + 8
            if 0 <= button_num < 8:
                self._looper(looper_num).change_looper_state()
            if 8 <= button_num < 16:
                self._looper(looper_num).select_looper_device()
            elif 16 <= button_num < 24:
                self._looper(looper_num).track_instance.mute_track()
            elif 24 <= button_num < 32:
                self._looper(looper_num).track_instance.arm_track()

    def on_new_button_pressed(self, value):
        self._selected_track = self._song_view.selected_track
        self._selected_device = self._song_view.selected_track.view.selected_device
        if value and self._selected_device.class_display_name == "Looper":
            if self.get_looper_number(self._selected_device.name) == -1:
                self._selected_device.name = self.add_first_number_available(self._selected_device.name)

    def update_looper_state_button(self, state, num):
        self.song_mode.set_pad_led_color(self.state_color[state], self._pad(num), 'normal')

    def update_track_color_button(self, color, num):
        self.song_mode.set_pad_led_color(color, self._pad(num) + 8, 'normal')

    def update_track_mute_button(self, color, num):
        self.song_mode.set_pad_led_color(color, self._pad(num) + 16, 'normal')

    def update_track_arm_button(self, color, num, blink_type):
        self.song_mode.set_pad_led_color(color, self._pad(num) + 24, blink_type)

class TrackInstance(object):
    def __init__(self, track, looper_mode):
        self.track = track
        self.looper_mode = looper_mode
        self.loopers_list = []
        self.devices_list = []
        self.prev_loopers_list = []
        self.track.add_devices_listener(self._on_devices_changed)
        self.track.add_color_listener(self.on_track_color_changed)
        try:
            self.track.add_mute_listener(self.on_track_mute_changed)
            self.track.add_arm_listener(self.on_track_arm_changed)
            self.track.add_current_monitoring_state_listener(self.on_monitoring_changed)
        except:
            pass
        self.on_track_color_changed()
        self.build_loopers_list()

    def _on_devices_changed(self):
        self.looper_mode.rebuild_tracks_list()

    def build_loopers_list(self):
        for dev in self.track.devices:
            if dev.class_display_name == "Looper":
                num = self.looper_mode.get_looper_number(dev.name)
                if dev not in [self._looper_instance(l).looper for l in self.looper_mode.global_looper_list] and num > -1:
                    self.looper_mode.check_duplicate(num)
                    looper_instance = LooperInstance(dev, num, self, self.looper_mode)
                    self.loopers_list.append(looper_instance)
                    self.looper_mode.add_looper(looper_instance)

    def on_track_color_changed(self):
        for l in self.looper_mode.global_looper_list:
            if self._looper_instance(l).track_instance == self:
                self.looper_mode.update_track_color_button(self.track.color_index, self._looper_instance(l).num)

    def on_track_mute_changed(self):
        for l in self.looper_mode.global_looper_list:
            if self._looper_instance(l).track_instance == self:
                self.looper_mode.update_track_mute_button("half_yellow" if self.track.mute else "yellow", self._looper_instance(l).num)

    def on_track_arm_changed(self):
        for l in self.looper_mode.global_looper_list:
            if self._looper_instance(l).track_instance == self and self.track.current_monitoring_state == 1:
                self.looper_mode.update_track_arm_button("red" if self.track.arm else "black", self._looper_instance(l).num, 'normal')

    def on_monitoring_changed(self):
        for l in self.looper_mode.global_looper_list:
            if self._looper_instance(l).track_instance == self:
                if self.track.current_monitoring_state == 0:
                    self.looper_mode.update_track_arm_button('marine', self._looper_instance(l).num, 'normal')
                elif self.track.current_monitoring_state == 1:
                    self.looper_mode.update_track_arm_button("red" if self.track.arm else "black", self._looper_instance(l).num, 'normal')
                else:
                    self.looper_mode.update_track_arm_button("half_red", self._looper_instance(l).num, 'fast_blink')

    def mute_track(self):
        self.track.mute = 1 if self.track.mute == 0 else 0

    def arm_track(self):
        if self.looper_mode.exclusive_arm:
            for track in self.looper_mode._song.tracks:
                track.arm = False
            self.track.arm = True
        else:
            self.track.arm = True if self.track.arm == False else False

    def _looper_instance(self, i):
        return self.looper_mode.global_looper_list[i]

class LooperInstance(object):
    def __init__(self, looper, num, track_instance, looper_mode):
        self.looper_mode = looper_mode
        self.track_instance = track_instance
        self.num = num
        self.looper = looper
        self.state_param = looper.parameters[1]
        self.state_change = {0: 1, 1: 2, 2: 3, 3: 2}
        self.state_param.add_value_listener(self.on_looper_state_changed)

    def show_looper(self):
        self.track_instance.on_track_color_changed()
        self.track_instance.on_monitoring_changed()
        self.track_instance.on_track_mute_changed()
        self.on_looper_state_changed()

    def on_looper_state_changed(self):
        self.looper_mode.update_looper_state_button(self.state_param.value, self.num)

    def change_looper_state(self):
        if self.looper_mode._song.is_playing:
            looper_state = self.state_param.value
            self.state_param.value = self.state_change[looper_state]

    def select_looper_device(self):
        self.looper_mode._song_view.selected_track = self.track_instance.track
        self.looper_mode._song_view.selected_track.view.selected_device = self.looper
