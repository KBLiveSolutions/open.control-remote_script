from __future__ import division
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import Live
from . import consts_SM

MATRIX_LENGTH = len(consts_SM.PAD_MATRIX)
HALF_MATRIX_LENGTH = old_div(MATRIX_LENGTH, 2)


class Arrangement(object):
    def __init__(self, song_mode):
        self.song_mode = song_mode
        self.control_surface = self.song_mode.control_surface
        self.is_active = False
        self.latching = False
        self.pad_held_list = []
        self.prev_cue = -1
        self.selected_cue = -1
        self.actual_marker_list = []
        self.playing_song = -1
        self.triggered_song = -1
        self.launched_marker = -1
        self.playing_marker_index = -1
        self.triggered_marker_index = -1
        self.selected_song_page = 0
        self.selected_song = 0
        self.max_pages = 0
        self.selected_marker_page = 0
        self.song_mode._song.add_cue_points_listener(self.rebuild_song_list)
        self.rebuild_song_list()

    @property
    def _selected_song(self):
        if self.selected_song in self.song_list:
            return self.song_list[self.selected_song]
        else:
            return self.song_list[-1]

    @property
    def _default_song(self):
        return self.song_list[-1]

    @property
    def _leds(self):
        return self.song_mode.leds

    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def compare_cue(self, beat):
        if not self.no_marker:
            for cue_point in reversed(self._default_song.marker_list):
                if cue_point.marker.time <= beat:
                    self.selected_cue = cue_point
                    break
            if self.prev_cue != self.selected_cue:
                self.playing_song = self.get_song_number(cue_point.name)
                if self.check_stop(cue_point) and cue_point.marker.time <= beat <= (cue_point.marker.time+1) and self.song_mode.is_playing:
                    self.song_mode._song.stop_playing()
                if self.is_active and not self.song_mode.color_mode_on:
                    self.set_song_buttons()
                self.prev_cue = self.selected_cue

    def get_song_number(self, name):
        num1 = name.find("(SONG")
        num3 = 0
        if num1 > -1:
            num3 = name[num1+5:name.find(")", num1)]
        return(int(num3)-1)

    def check_stop(self, cue_point):
        num1 = cue_point.name.find("(STOP)")
        res = True if num1 > -1 else False
        return (res)

    def set_view_on(self):
        self.song_mode.set_button('SHIFT_BUTTON', 'half')
        self.song_mode.set_button('STOP_ALL_CLIPS_BUTTON', 'half')
        self.song_mode.set_button('DELETE_BUTTON', 'off')
        self.song_mode.set_button('RESTART_BUTTON', 'half')
        self.song_mode.set_button('NEW_BUTTON', 'half')
        self.set_song_buttons()

    def rebuild_song_list(self):
        self.my_song_list = MarkerList(self.song_mode)
        self.song_list = self.my_song_list.song_list
        self.marker_amount = self.my_song_list.marker_amount
        self.song_amount = len(self.song_list)
        if self.marker_amount == 0:
            self.no_marker = True
        else:
            self.no_marker = False
        try:
            self.layout = self.last_mode
        except:
            if self.song_amount > 1:
                self.layout = 'advanced'
            else:
                self.layout = 'simple'
        self.set_layout(self.layout)

    def set_layout(self, layout):
        self.layout = layout
        if layout == "simple":
            self.selected_song = -1
            self.matrix_length = len(consts_SM.PAD_MATRIX)
        else:
            self.matrix_length = old_div(len(consts_SM.PAD_MATRIX),2)
            liste = [i for i in self.song_list]
            del liste[-1]
            if self.selected_song == -1:
                self.selected_song = min(liste) if len(liste) > 0 else 0
        if self.is_active:
            self.set_song_buttons()

    def switch_layout(self):
        self.layout = "advanced" if self.layout == "simple" else "simple"
        self.last_mode = self.layout
        self.set_layout(self.layout)

    def set_song_arrow_buttons(self):
        self._leds.set_arrow_color('up_button', self.selected_song_page > 0 )
        self._leds.set_arrow_color('down_button', self.selected_song_page < self.max_pages)

    def set_scene_arrow_buttons(self):
        self._leds.set_arrow_color('left_button', self.current_page > 0 )
        self._leds.set_arrow_color('right_button', self.current_page < self.max_marker_pages)

    def set_song_buttons(self):
        if self.no_marker:
            self._leds.set_zero('dim_white2')
            self.song_mode.set_button('SHIFT_BUTTON', 'off')
        else:
            self.song_mode.set_button('SHIFT_BUTTON', 'on')
            if self.layout == "simple":
                self.set_marker_buttons()
                self.song_mode.set_button('UP_BUTTON', 'off')
                self.song_mode.set_button('DOWN_BUTTON', 'off')
            else:
                try:
                    if max(self.song_list) > self.matrix_length:
                        self.max_pages = int(old_div(max(self.song_list), self.matrix_length))
                    else:
                        self.max_pages = 0
                        self.selected_song_page = 0
                except:
                    pass
                for i in range(self.matrix_length):
                    song_num_pad = self.selected_song_page * self.matrix_length + i
                    try:
                        song = self.song_list[song_num_pad]
                        color_index, blink_type = (song.get_color(0), 'normal')
                        if song.num == self.selected_song:
                            blink_type = 'slow_blink'
                        if self.selected_cue in song.marker_list:
                            color_index, blink_type = ('green', 'fast_blink')
                    except:
                        color_index, blink_type = ('black', 'normal')
                    self.song_mode.set_song_pad_led_color(color_index, i, blink_type)
                self.set_marker_buttons()
                self.set_song_arrow_buttons()

    def set_marker_buttons(self):
        self.current_page = self._selected_song.selected_marker_page
        self.max_marker_pages = int(old_div(len(self._selected_song.marker_list),self.matrix_length))
        current_list_length = min(len(self._selected_song.marker_list[self.current_page * self.matrix_length:]), self.matrix_length)
        self.actual_scene_list = []
        if self.layout == "simple":
            for i in range(self.matrix_length):
                index = i + self.matrix_length * self.current_page
                try :
                    marker = self._default_song.marker_list[index]
                    color_index, blink_type = (self._default_song.get_color(index), 'normal')
                    if self.is_in_loop(marker) and self.song_mode.loop:
                        color_index, blink_type = ('yellow', 'slow_blink')
                    if marker == self.selected_cue:
                        color_index, blink_type = ('green', 'fast_blink')
                    if self.check_stop(marker):
                        color_index, blink_type = ('red', 'fast_blink')

                except:
                    color_index, blink_type = ('dim_white2', 'normal')
                self.song_mode.set_pad_led_color(color_index, i, blink_type)
        else:
            for i in range(self.matrix_length):
                scene_num_pad = self.current_page * self.matrix_length + i
                try :
                    marker = self._selected_song.marker_list[scene_num_pad]
                    color_index, blink_type = (marker.color, 'normal')
                    if self.is_in_loop(marker) and self.song_mode.loop:
                        color_index, blink_type = ('yellow', 'slow_blink')
                    if marker == self.selected_cue and marker.time >= self.song_list[self.playing_song].marker_list[0].time:
                        color_index, blink_type = ('green', 'fast_blink')
                    if marker == self.selected_cue and self.is_in_loop(marker):
                        color_index, blink_type = ('green', 'fast_blink_yellow')
                    if self.check_stop(marker):
                        color_index, blink_type = ('red', 'fast_blink')
                    self.actual_marker_list.append(scene_num_pad)
                except:
                    color_index, blink_type = ('dim_white2', 'normal')
                self.song_mode.set_scene_pad_led_color(color_index, i, blink_type)

        self.set_scene_arrow_buttons()

    def is_in_loop(self, marker):
        return (self.song_mode._song.loop_start <= marker.time <= self.song_mode._song.loop_start + self.song_mode._song.loop_length)

    def on_pad_pressed(self, id, value):
        self.current_page = self._selected_song.selected_marker_page
        index = id.index + self.matrix_length * self.current_page
        if self.layout == "simple":
            try:
                self._selected_song.marker_list[index]
                self.on_marker_button_pressed(index, value)
            except:
                pass
        else:
            if id.index < self.matrix_length:
                self.on_song_button_pressed(id.index)
            else:
                try:
                    self._selected_song.marker_list[index - self.matrix_length]
                    self.on_marker_button_pressed(index - self.matrix_length, value)
                except:
                    pass

    def on_song_button_pressed(self, index):

        try:
            selected_song = self.selected_song_page * self.matrix_length + index
            self.song_list[selected_song]
            self.song_mode.set_song_pad_led_color(self._selected_song.marker_list[0].color, self.selected_song % self.matrix_length, 'normal')
            self.selected_song = selected_song
            if self.is_in_song_page(self.selected_song):
                color_index, blink_type = (self._selected_song.marker_list[0].color, 'slow_blink')
                if self.selected_song == self.playing_song:
                    color_index, blink_type = ('green','fast_blink')
                self.song_mode.set_song_pad_led_color(color_index, self.selected_song % self.matrix_length, blink_type)
                self.set_marker_buttons()
        except:
            pass

    def on_marker_button_pressed(self, index, value):

        if value > 0:
            self.pad_held_list.append(index)
            if len(self.pad_held_list) > 1:
                mini = min([self._selected_song.marker_list[i].time for i in self.pad_held_list])
                maxi = max([self._selected_song.marker_list[i].time for i in self.pad_held_list])
                length = maxi - mini
                self.song_mode._song.loop = 1
                self.song_mode._song.loop_start = mini
                self.song_mode._song.loop_length = length
                self.latching = True
                self.set_marker_buttons()

        else:
            if len(self.pad_held_list) == 1 and not self.latching:
                marker = self._selected_song.marker_list[self.pad_held_list[0]]
                self.song_mode._song.loop = 0
                marker.marker.jump()
                self.song_mode._song.loop = self.song_mode.loop
                self.song_mode.restart_position = self.song_mode._song.current_song_time
                if not self.song_mode.is_playing:
                    self.song_mode._song.start_playing()
                    self.song_mode.restart_position = marker.time
                self.pad_held_list = []
            else:
                self.pad_held_list.remove(index)
                if len(self.pad_held_list) == 0:
                    self.latching = False

    def is_in_song_page(self, song_number):
        return self.selected_song_page * self.matrix_length <= song_number < (self.selected_song_page + 1) * self.matrix_length

    def is_playing_song(self, song_number):
        return song_number == self.playing_song

    def select_song(self, id):
        self.selected_song = self.selected_song_page * self.matrix_length + id.index

    def select_launcher(self, id):
        self.current_page = self._selected_song.selected_marker_page
        i = self.current_page * self.matrix_length + id.index
        if self.layout == "simple":
            i = self.current_page * self.matrix_length + id.index
            marker = self._selected_song.marker_list[i]
        else:
            if id.index < self.matrix_length:
                selected_song = self.selected_song_page * self.matrix_length + id.index
                marker = self._selected_song.marker_list[0]
            else:
                i = self.current_page * self.matrix_length + id.index - self.matrix_length
                marker = self._selected_song.marker_list[i]
        self.changing_color_cue = marker

    def change_launcher_color(self, color_num):
        self.song_mode._song.set_data("cuepoint_color"+str(self.changing_color_cue.time), color_num)
        index = self._selected_song.marker_list.index(self.changing_color_cue)
        self._selected_song.marker_list[index].change_marker_color(color_num)
        self.set_song_buttons()

    def on_new_button_pressed(self, value):
        if not self._song.is_cue_point_selected():
            self._song.set_or_delete_cue()

    def on_shift_button_pressed(self, value):
        pass

    def on_up_button_pressed(self):
        if self.selected_song_page > 0:
            self.selected_song_page -= 1
            self.set_song_buttons()

    def on_down_button_pressed(self):
        if self.selected_song_page < self.max_pages:
            self.selected_song_page += 1
            self.set_song_buttons()

    def on_left_button_pressed(self):
        if self._selected_song.selected_marker_page > 0:
            self._selected_song.selected_marker_page -= 1
            self.set_marker_buttons()

    def on_right_button_pressed(self):
        if self._selected_song.selected_marker_page < int(old_div(len(self._selected_song.marker_list),self.matrix_length)):
            self._selected_song.selected_marker_page += 1
            self.set_marker_buttons()

class MarkerList(object):

    def __init__(self, song_mode):
        self.song_mode = song_mode
        self.control_surface = self.song_mode.control_surface
        self.markers_list = []
        self.marker_amount = len(self._song.cue_points)
        self.song_list = {}
        self.song_amount = 0
        self.build_markers_list()

    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def build_markers_list(self):
        # self.markers_list = []
        self.marker_amount = len(self._song.cue_points)
        for i in range(self.marker_amount):
            try:
                # verifier si marker deja dans la liste
                self._song.cue_points[i] in self.markers_list.marker
            except:
                marker = MyMarker(self.song_mode, i)
                self.markers_list.append(marker)
            self.build_song(-1 , marker)
            try:
                current_song = self.get_song_number(marker.name)
                self.build_song(current_song, marker)
            except:
                pass

        for i in self.song_list:
            self.song_list[i].marker_list = sorted(self.song_list[i].marker_list, key=lambda marker: marker.time)

    def build_song(self, song_number, marker):
        try:
            self.song_list[song_number].add_marker(marker, song_number)
        except:
            self.song_list[song_number] = MySong(song_number)
            self.song_list[song_number].add_marker(marker, song_number)

    def get_song_number(self, name):
        num1 = name.find("(SONG")
        if num1 > -1:
            num3 = name[num1+5:name.find(")", num1)]
        return(int(num3)-1)

    def rebuild_song_list(self):
        self.markers_amount = len(self._song.cue_points)
        self.song_list = []
        self.song_amount = max(self.song_list)
        self.build_markers_list()

class MySong(object):
    def __init__(self, num):
        self.num = num
        self.selected_marker_page = 0
        self.marker_list = []
        self.is_displayed = 0

    def add_marker(self, marker, song_number):
        self.marker_list.append(marker)
        marker.index = self.marker_list.index(marker)
        marker.song_number = song_number

    def get_color(self, index):
        return self.marker_list[index].color

class MyMarker(object):

    def __init__(self, song_mode, num):
        self.song_mode = song_mode
        self.marker = self._song.cue_points[num]
        self.name = self.marker.name
        self.num = num
        self.time = self.marker.time
        self.song_number = -1
        self.index = -1
        self.is_displayed = 0
        self.color = self._song.get_data("cuepoint_color"+str(self.time), 'white')
        self.marker_page = int(old_div(self.index, HALF_MATRIX_LENGTH))
        self.index_modulo = self.index % HALF_MATRIX_LENGTH
        self.marker.add_name_listener(self.on_name_changed)
        self.marker.add_time_listener(self.on_time_changed)

    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def on_name_changed(self):
        self.song_mode.main_view['arrangement'].rebuild_song_list()

    def on_time_changed(self):
        self.song_mode.main_view['arrangement'].rebuild_song_list()

    def change_marker_color(self, color_num):
        self.color = color_num
        self._song.set_data("cuepoint_color"+str(self.time), color_num)
