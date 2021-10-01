from __future__ import division
from builtins import range
from builtins import object
from past.utils import old_div
import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent
from . import consts_SM

MATRIX_LENGTH = len(consts_SM.PAD_MATRIX)
HALF_MATRIX_LENGTH = old_div(MATRIX_LENGTH, 2)

class SongList(object):

    def __init__(self, song_mode):
        self.song_mode = song_mode
        self.control_surface = self.song_mode.control_surface
        self.scenes_list = []
        self.scene_amount = len(self.song_mode.control_surface.song().scenes)
        self.song_list = {}
        self.song_amount = 0
        self.build_scenes_list()

    def build_scenes_list(self):
        for sc_num in range(self.scene_amount):
            scene = MyScene(self.song_mode, sc_num)
            self.scenes_list.append(scene)
            self.build_song(-1 , scene)
            try:
                current_song = self.get_song_number(scene.name)
                self.build_song(current_song, scene)
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
        self.scene_amount = len(self.song_mode.control_surface.song().scenes)
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
        self.scene = self.song_mode.control_surface.song().scenes[num]
        self.name = self.scene.name
        self.color_index = self.get_color_index()
        self.num = num
        self.song_number = -1
        self.index = -1
        self.is_displayed = 0
        self.scene_page = int(old_div(self.index, HALF_MATRIX_LENGTH))
        self.index_modulo = self.index % HALF_MATRIX_LENGTH
        self.scene.add_is_triggered_listener(self.on_is_triggered)
        self.scene.add_name_listener(self.on_name_changed)
        self.scene.add_color_listener(self.on_color_changed)

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
