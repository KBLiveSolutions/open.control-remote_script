from __future__ import division
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent
from . import consts_SM

MATRIX_LENGTH = len(consts_SM.PAD_MATRIX)
HALF_MATRIX_LENGTH = old_div(MATRIX_LENGTH, 2)

class Session(object):
    def __init__(self, song_mode, *a, **k):
        self.song_mode = song_mode
        self.is_active = False
        self.actual_scene_list = []
        self.playing_song = -1
        self.triggered_song = -1
        self.launched_scene = -1
        self.playing_scene_index = -1
        self.playing_scene = -1
        self.triggered_scene = -1
        self.triggered_scene_index = -1
        self.selected_song_page = 0
        self.selected_song = -1
        self.max_pages = 0
        self.selected_scene_page = 0
        self.new_button = False
        self.song_mode._song.add_scenes_listener(self.rebuild_song_list)
        self.rebuild_song_list()

    @property
    def _selected_song(self):
        return self.song_list[self.selected_song]
    @property
    def _default_song(self):
        return self.song_list[-1]
    @property
    def _leds(self):
        return self.song_mode.leds
    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def _print(self, *args):
        self.song_mode.control_surface.log_message(args)

    def on_selected_scene_changed(self):
        self.selected_scene = self._song.view.selected_scene
        if self.song_mode.color_mode_on == 0 and self.is_active:
            self.set_scene_buttons()

    def set_view_on(self):
        state = 'half'
        if self.song_amount == 1:
            state = 'off'
        self.song_mode.set_button('DELETE_BUTTON', state)
        self.song_mode.set_button('SHIFT_BUTTON', 'half')
        self.song_mode.set_button('RESTART_BUTTON', 'off')
        self.song_mode.set_button('STOP_ALL_CLIPS_BUTTON', 'half')
        self.song_mode.set_button('NEW_BUTTON', 'half')
        self.set_song_buttons()

    def rebuild_song_list(self):

        self.my_song_list = SongList(self.song_mode)
        self.song_amount = len(self.my_song_list.song_list)
        self.song_list = self.my_song_list.song_list
        if not self.new_button:
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
        self.set_song_buttons()

    def set_song_buttons(self):
        if self.layout == "advanced":
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
                        color_index, blink_type = (color_index, 'slow_blink')
                    if song.num == self.playing_song:
                        color_index, blink_type = ('green', 'fast_blink')
                except:
                    color_index, blink_type = ('black', 'normal')
                self.song_mode.set_song_pad_led_color(color_index, i, blink_type)
        self.set_scene_buttons()
        self.set_song_arrow_buttons()

    def set_scene_buttons(self):
        try:
            self.current_page = self._selected_song.selected_scene_page
            self.max_scene_pages = int(old_div(len(self._selected_song.scene_list),self.matrix_length))
            current_list_length = min(len(self._selected_song.scene_list[self.current_page * self.matrix_length:]), self.matrix_length)
        except:
            self.current_page = 0
            self.max_scene_pages = 0
            current_list_length = 0
        self.actual_scene_list = []
        if self.layout == "simple":
            for i in range(self.matrix_length):
                index = i + self.matrix_length * self.current_page
                try :
                    color_index, blink_type = (self._default_song.get_color(index), 'normal')
                    if self.my_song_list.scenes_list[index].scene == self.selected_scene:
                        color_index, blink_type = (self._default_song.get_color(index), 'slow_blink')
                    if index == self.playing_scene:
                        color_index, blink_type = ('green', 'slow_blink')
                    if index == self.triggered_scene:
                        color_index, blink_type = ('green', 'fast_blink')
                    if self.check_stop(self.song_mode._song.scenes[index]):
                        color_index, blink_type = ('red', 'fast_blink')
                except:
                    color_index, blink_type = ('dim_white', 'normal')
                self.song_mode.set_pad_led_color(color_index, i, blink_type)
        else:
            for i in range(self.matrix_length):
                scene_num_pad = self.current_page * self.matrix_length + i
                try :
                    color_index, blink_type = (self._selected_song.get_color(scene_num_pad), 'normal')
                    if self.check_stop(self._selected_song.scene_list[scene_num_pad]):
                        color_index, blink_type = ('red', 'fast_blink')
                    self.actual_scene_list.append(scene_num_pad)
                except:
                    color_index, blink_type = ('dim_white', 'normal')
                self.song_mode.set_scene_pad_led_color(color_index, i, blink_type)
            if self.selected_song == self.triggered_song and self.triggered_scene_index in self.actual_scene_list:
                self.song_mode.set_scene_pad_led_color('green', self.playing_scene_index % self.matrix_length, 'fast_blink')
            if self.selected_song == self.playing_song and self.playing_scene_index in self.actual_scene_list:
                self.song_mode.set_scene_pad_led_color('green', self.playing_scene_index % self.matrix_length, 'slow_blink')
        self.set_scene_arrow_buttons()

    def set_song_arrow_buttons(self):
        if self.layout == 'simple':
            self.select_scene_mode_on()
        else:
            self._leds.set_arrow_color('up_button', self.selected_song_page > 0 )
            self._leds.set_arrow_color('down_button', self.selected_song_page < self.max_pages)

    def set_scene_arrow_buttons(self):
        self._leds.set_arrow_color('left_button', self.current_page > 0 )
        self._leds.set_arrow_color('right_button', self.current_page < self.max_scene_pages)

    def switch_layout(self):
        layout = "advanced" if self.layout == "simple" else "simple"
        self.last_mode = layout
        self.set_layout(layout)

    def on_color_changed(self, scene):
        if self.is_active:
            if self.layout == 'simple':
                self.song_mode.set_pad_led_color(scene.color_index, scene.num % self.matrix_length, 'normal')
            else:
    # 1. if in selected_song and not playing scene : change scene color
                if scene.song_number == self.selected_song:
                    if scene.index in self.actual_scene_list and scene.index is not self.playing_scene_index:
                        self.song_mode.set_scene_pad_led_color(scene.color_index, scene.index % self.matrix_length, 'normal')
    # 2. if in selected_song and index = 0 : change scene color, change song color
                    if scene.index == 0 and self.is_in_song_page(scene.song_number)  and scene.song_number is not self.playing_song:
                        self.song_mode.set_song_pad_led_color(scene.color_index, scene.song_number % self.matrix_length, 'slow_blink')
    # 3. if index = 0: and in actual_song_list and song not playing : change song color
                else:
                    if scene.index == 0 and self.is_in_song_page(scene.song_number) and scene.song_number is not self.playing_song:
                        self.song_mode.set_song_pad_led_color(scene.color_index, scene.song_number % self.matrix_length, 'normal')

    def update_scene_triggered(self, triggered_song, triggered_scene_index, value, num):

        if self.layout == "simple":
            if value:
                self.triggered_scene = num
            else:
                self.triggered_scene = -1
                self.playing_scene = num
            if self.is_active:
                self.set_scene_buttons()

        else:
            if value and self.is_active:
                if triggered_song == self.selected_song:
    # update triggered scene
                    self.triggered_scene_index = triggered_scene_index
                    if self.triggered_scene_index in self.actual_scene_list:
                        self.song_mode.set_scene_pad_led_color('green', self.triggered_scene_index % self.matrix_length, 'fast_blink')
            else:
        # 1. switch off previously playing Scene if displayed
                if self.selected_song == self.playing_song and self.playing_scene_index in self.actual_scene_list:
                    self.song_mode.set_scene_pad_led_color(self._selected_song.get_color(self.playing_scene_index), self.playing_scene_index % self.matrix_length, 'normal')
        #2. switch off previous Song
                if self.is_in_song_page(self.playing_song):
                    self.song_mode.set_song_pad_led_color(self.song_list[self.playing_song].get_color(0), self.playing_song % self.matrix_length, 'normal')
        #3. change playing_song, playing_scene_index
                self.playing_song = triggered_song
                self.playing_scene_index = triggered_scene_index
                if self.selected_song == self.playing_song:
    #4. switch off triggered Scene
                    if self.triggered_scene_index in self.actual_scene_list:
                        self.song_mode.set_scene_pad_led_color(self._selected_song.get_color(self.triggered_scene_index), self.triggered_scene_index % self.matrix_length, 'normal')
    #5. turn on playing Scene
                    if self.playing_scene_index in self.actual_scene_list:
                        self.song_mode.set_scene_pad_led_color('green', self.playing_scene_index % self.matrix_length, 'slow_blink')
        #6. turn on playing Song
                if self.is_in_song_page(self.playing_song):
                    self.song_mode.set_song_pad_led_color('green', self.playing_song % self.matrix_length, 'fast_blink')

    def is_in_song_page(self, song_number):
        return self.selected_song_page * self.matrix_length <= song_number < (self.selected_song_page + 1) * self.matrix_length

    def is_playing_song(self, song_number):
        return song_number == self.playing_song

    def add_scene_to_song(self, id):
        selected_song = self.selected_song_page * self.matrix_length + id.index
        song_num = selected_song + 1
        new_name = self.delete_song_name(self.selected_scene.name)
        new_name = new_name + " (SONG" + str(song_num) + ")"
        self.replace_scene_name(self.selected_scene, new_name)
        self.selected_song = selected_song

    def select_launcher(self, id):

        if self.layout == "simple":
            self.current_page = self._selected_song.selected_scene_page
            i = id.index + self.matrix_length * self.current_page
            self.song_mode._song.view.selected_scene = self.my_song_list.scenes_list[i].scene
        else:
            if id.index < self.matrix_length:
                self.select_song(id)
            else:
                scene = self._selected_song.scene_list[self._selected_song.selected_scene_page * self.matrix_length + id.index - self.matrix_length]
                self.song_mode._song.view.selected_scene = scene.scene

    def select_song(self, id):
        if self.layout == "simple":
            pass
        else:
            selected_song = self.selected_song_page * self.matrix_length + id.index
            scene = self.song_list[selected_song].scene_list[0]
            self.song_mode._song.view.selected_scene = scene.scene

    def change_launcher_color(self, color):
        self.song_mode._song.view.selected_scene.color_index = color
        self.set_song_buttons()

    def delete_song_name(self, name):
        new_name = name
        num1 = name.find("(SONG")
        if num1 > -1:
            num2 = name.find(")", num1) + 1
            new_name = name[:num1] + name[num2:]
        return new_name

    def delete_scene(self, id):
        scene = self._selected_song.scene_list[self._selected_song.selected_scene_page * self.matrix_length + id.index - self.matrix_length]
        name = str(scene.name)
        new_name = name
        num1 = name.find("(SONG")
        if num1 > -1:
            num2 = name.find(")", num1) + 1
            new_name = name[:num1] + name[num2:]
        new_name = new_name.replace("  ", " ")
        scene.scene.name = new_name

    def replace_scene_name(self, scene, name):
        new_name = name.replace("  ", " ")
        scene.name = new_name

    def on_shift_button_pressed(self, value):
        if value:
            self.select_scene_mode_on()
        else:
            self.set_song_arrow_buttons()

    def on_new_button_pressed(self, value):

        layout = 'advanced'
        self.new_button = True if value else False
        if value == 0 and self.song_amount == 1:
            layout = 'simple'
        self.set_layout(layout)

    def select_scene_mode_on(self):
        self.song_mode.set_button('UP_BUTTON', 'white')
        self.song_mode.set_button('DOWN_BUTTON', 'white')

    def on_pad_pressed(self, id, value):
        if value:
            if self.new_button:
                self.add_scene_to_song(id)
            if self.song_mode.delete_button:
                self.delete_scene(id)
            else:
                if self.layout == "simple":
                    self.current_page = self._selected_song.selected_scene_page
                    i = id.index + self.matrix_length*self.current_page
                    if self.check_stop(self.song_mode._song.scenes[i]):
                        self.song_mode._song.stop_playing()
                    else:
                        self.song_mode._song.scenes[i].fire()
                else:
                    if id.index < self.matrix_length:
                        self.on_song_button_pressed(id)
                    else:
                        self.on_scene_button_pressed(id)

    def on_song_button_pressed(self, id):
        selected_song = self.selected_song_page * self.matrix_length + id.index
        try:
            # previous selected_song
            if self.is_in_song_page(self.selected_song):
                color_index, blink_type = (self._selected_song.get_color(0), 'normal')
                if self.selected_song == self.playing_song:
                    color_index, blink_type = ('green','fast_blink')
            self.song_mode.set_song_pad_led_color(color_index, self.selected_song % self.matrix_length, blink_type)
        except:
            pass
        self.selected_song = selected_song
        try:
            if self.is_in_song_page(self.selected_song):
                color_index, blink_type = (self._selected_song.get_color(0), 'slow_blink')
                if self.selected_song == self.playing_song:
                    color_index, blink_type = ('green','fast_blink')
            self.song_mode.set_song_pad_led_color(color_index, self.selected_song % self.matrix_length, blink_type)
            self.set_scene_buttons()
        except:
            pass

    def on_scene_button_pressed(self, id):
        scene = self._selected_song.scene_list[self._selected_song.selected_scene_page * self.matrix_length + id.index - self.matrix_length]
        if  self.song_mode.shift_button:
            self.song_mode._song.view.selected_scene = scene.scene
        else:
            try:
                if self.check_stop(scene):
                    self.song_mode._song.stop_playing()
                else:
                    self.song_mode._song.scenes[scene.num].fire()
            except:
                pass

    def on_left_button_pressed(self):
        if self._selected_song.selected_scene_page > 0:
            self._selected_song.selected_scene_page -= 1
            self.set_scene_buttons()

    def on_right_button_pressed(self):
        if self._selected_song.selected_scene_page < int(old_div(len(self._selected_song.scene_list),self.matrix_length)):
            self._selected_song.selected_scene_page += 1
            self.set_scene_buttons()

    def on_up_button_pressed(self):
        if self.layout == 'simple' or (self.layout == 'advanced' and self.song_mode.shift_button):
            self.on_prev_scene_button_pressed(127)
        else:
            if self.selected_song_page  > 0:
                self.selected_song_page -= 1
                self.set_song_buttons()

    def on_down_button_pressed(self):
        if self.layout == 'simple' or (self.layout == 'advanced' and self.song_mode.shift_button):
            self.on_next_scene_button_pressed(127)
        else:
            if self.selected_song_page < self.max_pages:
                self.selected_song_page += 1
                self.set_song_buttons()

    def on_next_scene_button_pressed(self, value):
        if value:
            selected_scene_index = list(self._song.scenes).index(self._song.view.selected_scene)
            # next_index = max(selected_scene_index + 1, len(self._song.scenes))
            next_index = selected_scene_index + 1
            self._song.view.selected_scene = self._song.scenes[next_index]

    def on_prev_scene_button_pressed(self, value):
        if value:
            selected_scene_index = list(self._song.scenes).index(self._song.view.selected_scene)
            # prev_index = min(selected_scene_index - 1, 0)
            prev_index = selected_scene_index - 1
            self._song.view.selected_scene = self._song.scenes[prev_index]

    def check_stop(self, scene):
        num1 = scene.name.find("(STOP)")
        res = True if num1 > -1 else False
        return (res)

class SongList(object):

    def __init__(self, song_mode):
        self.song_mode = song_mode
        self.control_surface = self.song_mode.control_surface
        self.scenes_list = []
        self.scene_amount = len(self._song.scenes)
        self.song_list = {}
        self.song_amount = 0
        self.build_scenes_list()

    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def build_scenes_list(self):
        for sc_num in range(self.scene_amount):
            scene = MyScene(self.song_mode, sc_num)
            self.scenes_list.append(scene)
            self.build_song(-1 , scene)
            try:
                current_song = self.get_song_number(scene.name)
                self.build_song(current_song, scene)
                self.is_stop = self.check_stop(scene)
            except:
                pass

    def get_song_number(self, name):
        num1 = name.find("(SONG")
        if num1 > -1:
            num3 = name[num1+5:name.find(")", num1)]
        return(int(num3)-1)

    def build_song(self, song_number, scene):
        try:
            self.song_list[song_number].add_scene(scene, song_number)
        except:
            self.song_list[song_number] = MySong(song_number)
            self.song_list[song_number].add_scene(scene, song_number)

    def rebuild_song_list(self):
        self.scene_amount = len(self._song.scenes)
        self.song_list = []
        self.song_amount = max(self.song_list)
        self.build_scenes_list()


class MySong(object):
    def __init__(self, num):
        self.num = num
        self.selected_scene_page = 0
        self.scene_list = []
        self.is_displayed = 0

    def add_scene(self, scene, song_number):
        self.scene_list.append(scene)
        scene.index = self.scene_list.index(scene)
        scene.song_number = song_number

    def get_color(self, index):
        return self.scene_list[index].color_index

class MyScene(object):

    def __init__(self, song_mode, num):
        self.song_mode = song_mode
        self.scene = self._song.scenes[num]
        self.name = self.scene.name
        self.color_index = self.get_color_index()
        self.num = num
        self.song_number = -1
        self.index = -1
        self.is_displayed = 0
        self.scene_page = int(old_div(self.index, HALF_MATRIX_LENGTH))
        # self.index_modulo = self.index % HALF_MATRIX_LENGTH
        self.scene.add_is_triggered_listener(self.on_is_triggered)
        self.scene.add_name_listener(self.on_name_changed)
        self.scene.add_color_listener(self.on_color_changed)

    @property
    def _song(self):
        return self.song_mode.control_surface.song()

    def on_is_triggered(self):
        self.song_mode.main_view['session'].update_scene_triggered(self.song_number, self.index, self.scene.is_triggered, self.num)

    def on_name_changed(self):
        self.song_mode.main_view['session'].rebuild_song_list()

    def on_color_changed(self):
        self.color_index = self.get_color_index()
        self.song_mode.main_view['session'].on_color_changed(self)

    def get_color_index(self):
        if self.scene.color_index is not None:
            return(self.scene.color_index)
        else:
            return('white')
