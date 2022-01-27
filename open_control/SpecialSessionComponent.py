from __future__ import absolute_import
# from builtins import str
# from builtins import zip
# from builtins import range
from itertools import count

import time

from _Framework.SessionComponent import SessionComponent as SessionBase
from _Framework.SubjectSlot import subject_slot_group, subject_slot
# from _Framework.ClipSlotComponent import ClipSlotComponent as ClipSlotBase
# from _Framework.SceneComponent import SceneComponent as SceneBase
from . import Colors, Options
# from .SpecialSceneComponent import SceneComponent

import logging, traceback
logger = logging.getLogger(__name__)
# def print(text):
#     logger.warning(text)

class SessionComponent(SessionBase):
    """ SessionComponent extends the standard to use a custom SceneComponent, use custom
    ring handling and observe the status of scenes. """
    # scene_component_type = SceneComponent
    def __init__(self, *a, **k):
        self._clip_launch_button = None
        self._launch_scene_button = None
        self._launch_as_selected_button = None
        self._last_triggered_scene_index = None
        self._last_launched_clip_index = None
        self._next_empty_slot_button = None
        self._scene_bank_up_button = None
        self._scene_bank_down_button = None
        self._track_bank_left_button = None
        self._track_bank_right_button = None
        self._stop_all_clips_button = None
        self._name_controls = None
        self._current_track_color = None
        self._last_selected_parameter = None
        self._stopped_clip_value = 0
        self._clip_launch_buttons = None
        self._unfold_track_button = None
        self._main_view_toggle_button = None
        self._detail_view_toggle_button = None
        self._track_leds = [None, None, None]
        self._launch_setlist_song_button = None
        self.last_parameter_button_changing = False
        self.selected_setlist_song = None
        self.playing_song = None
        self.last_message_time = 0
        self.view = None
        super(SessionComponent, self).__init__(*a, **k)
        self.selected_track = self.song().view.selected_track
        self._show_highlight = True
        self._setup_scene_listeners()
        self.application().view.add_focused_document_view_listener(self.on_view_changed)
        self.song().view.add_selected_parameter_listener(self.on_selected_parameter_changed)
        clip_color_table = Colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
        clip_color_table[16777215] = 119
        self.set_rgb_mode(clip_color_table, Colors.RGB_COLOR_TABLE)
        self.scan_setlist()

    def disconnect(self):
        super(SessionComponent, self).disconnect()
        self._position_status_control = None

    def _enable_skinning(self):
        super(SessionComponent, self)._enable_skinning()
        self.set_stopped_clip_value(u'Session.StoppedClip')

    """ Functions to create buttons """
    def set_name_controls(self, name):
        self._name_controls = name
        self.update()

    def set_unfold_track(self, button):
        self._unfold_track_button = button
        self._unfold_track_button_value.subject = button

    def set_stop_all_clips_button(self, button):
        self._stop_all_clips_button = button
        self._stop_all_clips_button_value.subject = button

    def set_scroll_scenes(self, button):
        self._scroll_scenes_button = button
        self._scroll_scenes_button_value.subject = button

    def set_scene_bank_up_button(self, button):
        self._scene_bank_up_button = button
        self._scene_bank_up_value.subject = button

    def set_scene_bank_down_button(self, button):
        self._scene_bank_down_button = button
        self._scene_bank_down_value.subject = button

    def set_scene_bank_up_x4_button(self, button):
        self._scene_bank_up_x4_button = button
        self._scene_bank_up_x4_value.subject = button

    def set_scene_bank_down_x4_button(self, button):
        self._scene_bank_down_x4_button = button
        self._scene_bank_down_x4_value.subject = button

    def set_track_bank_left_button(self, button):
        self._track_bank_left_button = button
        self._track_leds[0] = button
        self._track_bank_left_value.subject = button

    def set_track_bank_right_button(self, button):
        self._track_bank_right_button = button
        self._track_leds[2] = button
        self._track_bank_right_value.subject = button

    def set_master_volume(self, button):
        self.master_volume_button=button
        self._master_volume_button_value.subject = button

    def set_launch_scene_button(self, button):
        self._launch_scene_button = button
        self._launch_scene_value.subject = button

    def set_find_next_empty_slot(self, button):
        self._find_next_empty_slot_button = button
        self._find_next_empty_slot_value.subject = button

    def set_current_track_color(self, button):
        self._current_track_color = button
        self._track_leds[1] = button

    def set_clip_launch_buttons(self, button):
        super(SessionComponent, self).set_clip_launch_buttons(button)
        self._clip_launch_buttons = button

    def set_add_audio_track(self, button):
        self._add_audio_track_button = button
        self._add_audio_track_value.subject = button

    def set_add_MIDI_track(self, button):
        self._add_MIDI_track_button = button
        self._add_MIDI_track_value.subject = button

    def set_fixed_length_rec_1bars(self, button):
        self._fixed_length_rec_1bars_button = button
        self._fixed_length_rec_1bars_value.subject = button

    def set_fixed_length_rec_2bars(self, button):
        self._fixed_length_rec_2bars_button = button
        self._fixed_length_rec_2bars_value.subject = button

    def set_fixed_length_rec_4bars(self, button):
        self._fixed_length_rec_4bars_button = button
        self._fixed_length_rec_4bars_value.subject = button

    def set_fixed_length_rec_8bars(self, button):
        self._fixed_length_rec_8bars_button = button
        self._fixed_length_rec_8bars_value.subject = button

    @subject_slot('value')
    def _fixed_length_rec_1bars_value(self, value):
        if value:
            self.song().trigger_session_record(4)

    @subject_slot('value')
    def _fixed_length_rec_2bars_value(self, value):
        if value:
            self.song().trigger_session_record(8)

    @subject_slot('value')
    def _fixed_length_rec_4bars_value(self, value):
        if value:
            self.song().trigger_session_record(16)

    @subject_slot('value')
    def _fixed_length_rec_8bars_value(self, value):
        if value:
            self.song().trigger_session_record(32)

    def set_last_selected_parameter(self, button):
        self._last_selected_parameter_button = button
        self._last_selected_parameter_value.subject = button

    def set_main_view_toggle(self, button):
        self._main_view_toggle_button = button
        self._main_view_toggle_button_value.subject = button

    def set_detail_view_toggle(self, button):
        self._detail_view_toggle_button = button
        self._detail_view_toggle_button_value.subject = button

    def set_undo(self, button):
        self._undo_button = button
        self._undo_value.subject = button

    def set_redo(self, button):
        self._undo_button = button
        self._redo_value.subject = button

    def set_jump_to_playing_scene(self, button):
        self._rjump_to_playing_scene_button = button
        self._jump_to_playing_scene_value.subject = button

    def set_insert_scene(self, button):
        self._insert_scene_button = button
        self._insert_scene_value.subject = button

    def set_capture_and_insert_scene(self, button):
        self._capture_and_insert_scene_button = button
        self._capture_and_insert_scene_value.subject = button

    def set_stop_all_clips_button(self, button):
        if button:
            button.reset_state()
        super(SessionComponent, self).set_stop_all_clips_button(button)

    """ Listeners """

    def on_scene_list_changed(self):
        self._setup_scene_listeners()
        super(SessionComponent, self).on_scene_list_changed()

    def on_selected_scene_changed(self):
        self.selected_scene = self._song.view.selected_scene
        self._on_scene_color_changed.subject = self.selected_scene
        self._on_scene_name_changed.subject = self.selected_scene
        if self.selected_scene in self._song.scenes and Options.session_box_linked_to_selection:
            self._scene_offset = int(list(self._song.scenes).index(self.selected_scene))
            if self._track_offset is not -1 and self._scene_offset is not -1:
                self.set_offsets(self._track_offset, self._scene_offset)
                self._reassign_scenes()
                self._update_position_status_control()

    def on_selected_track_changed(self):
        self.selected_track = self._song.view.selected_track
        self._on_track_color_changed.subject = self.song().view.selected_track
        if self.selected_track in self._song.visible_tracks and Options.session_box_linked_to_selection:
            self._track_offset = list(self._song.visible_tracks).index(self.selected_track)
            if self._track_offset > -1 and self._scene_offset > -1:
                self._mixer.set_track_offset(self._track_offset)
                self._update_position_status_control()

    def on_selected_parameter_changed(self):
        parameter = self.song().view.selected_parameter
        self._last_selected_parameter_button.send_value(self.get_parameter_value(parameter, parameter.value), force=True)
        self._on_last_selected_parameter_changed.subject = parameter

    @subject_slot('value')
    def _on_last_selected_parameter_changed(self):
        if not self.last_parameter_button_changing:
            parameter = self.song().view.selected_parameter
            # self.get_parameter_MIDI_value(parameter, parameter.value)
            # self._last_selected_parameter_button.send_value(self.get_parameter_MIDI_value(parameter, parameter.value), force=True)

    def get_parameter_value(self, parameter, value):
        _min = parameter.min
        _max = parameter.max
        _value =  (value - _min )/ (_max - _min)
        return _value * 127

    """ Buttons callbacks """

    @subject_slot('value')
    def _scroll_scenes_button_value(self, value):
        if value > 64:
            self._scene_bank_down_value(1)
        if value < 64:
            self._scene_bank_up_value(1)
        self._scroll_scenes_button.send_value(64, force=True)

    @subject_slot('value')
    def _stop_all_clips_button_value(self, value):
        if value:
            self.scene_offset()

    @subject_slot('value')
    def _scene_bank_up_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), max(0, self.scene_offset() - 1))
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]

    @subject_slot('value')
    def _scene_bank_down_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), self.scene_offset() + 1)
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]

    @subject_slot('value')
    def _track_bank_left_value(self, value):
        if value:
            self.set_offsets(max(self.track_offset() - 1, 0), self.scene_offset())
            if Options.session_box_linked_to_selection:
                self._song.view.selected_track = self._song.tracks[self.track_offset()]

    @subject_slot('value')
    def _scene_bank_up_x4_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), max(0, self.scene_offset() - 4))
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]

    @subject_slot('value')
    def _scene_bank_down_x4_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), self.scene_offset() + 4)
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]


    @subject_slot('value')
    def _track_bank_right_value(self, value):
        if value:
            self.set_offsets(self.track_offset() + 1, self.scene_offset())
            if Options.session_box_linked_to_selection:
                self._song.view.selected_track = self._song.tracks[self.track_offset()]

    @subject_slot('value')
    def _master_volume_button_value(self, value):
        print(self.song().master_track.mixer_device.volume)
        self.song().master_track.mixer_device.volume = value/127

    def on_view_changed(self):
        self.view = "Detail/Clip"

    @subject_slot('value')
    def _main_view_toggle_button_value(self, value):
        if value:
            if self.application().view.focused_document_view == "Session":
                self.application().view.focus_view("Arranger")
            else:
                self.application().view.focus_view("Session")

    @subject_slot('value')
    def _unfold_track_button_value(self, value):
        if Options.session_box_linked_to_selection:
            track = self.selected_track
        else:
            track = self.song().visible_tracks[self.track_offset()]
        if value:
            if track.is_foldable:
                track.fold_state = not track.fold_state
            elif track.can_show_chains:
                track.is_showing_chains = not track.is_showing_chains

    @subject_slot('value')
    def _detail_view_toggle_button_value(self, value):
        if value:
            if self.view == "Detail/Clip":
                self.application().view.focus_view("Detail/DeviceChain")
                self.view = "Detail/DeviceChain"
            else:
                self.application().view.focus_view("Detail/Clip")
                self.view = "Detail/Clip"

    @subject_slot('value')
    def _jump_to_playing_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.set_offsets(self._track_offset, self._last_triggered_scene_index)
                if Options.session_box_linked_to_selection:
                    self.song().view.selected_scene = self.song().scenes[self._last_triggered_scene_index]

    @subject_slot('value')
    def _insert_scene_value(self, value):
        if self.is_enabled():
            if self.selected_scene in self._song.scenes and Options.session_box_linked_to_selection:
                self._scene_offset = int(list(self._song.scenes).index(self.selected_scene))
            if value is not 0:
                self._scene_offset += 1
                self.song().create_scene(self._scene_offset)
                self._reassign_scenes()
                self._update_position_status_control()

    @subject_slot('value')
    def _capture_and_insert_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.song().capture_and_insert_scene()

    @subject_slot('value')
    def _find_next_empty_slot_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._find_next_empty_slot()

    @subject_slot_group('is_triggered')
    def _on_scene_triggered(self, index):
        self._last_triggered_scene_index = index    
        is_triggered = self._song.scenes[index].is_triggered
        self._update_position_status_control(is_triggered=is_triggered)
        if self.check_stop(self._song.scenes[index]) and is_triggered == 0:
            self._song.stop_playing()

    def check_stop(self, scene):
        num1 = scene.name.find("(STOP)")
        res = True if num1 > -1 else False
        return (res)

    @subject_slot('value')
    def _launch_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.scenes[self._scene_offset].fire_as_selected()

    @subject_slot('value')
    def _add_audio_track_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.create_audio_track()

    @subject_slot('value')
    def _add_MIDI_track_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.create_midi_track()

    @subject_slot('value')
    def _undo_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.undo()

    @subject_slot('value')
    def _redo_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.redo()

    @subject_slot('value')
    def _last_selected_parameter_value(self, value):
        if self.is_enabled() and self.song().view.selected_parameter:
            self.last_parameter_button_changing = True
            parameter = self.song().view.selected_parameter
            parameter.value = self.get_parameter_MIDI_value(parameter, value)
            string = parameter.str_for_value(parameter.value)
            self._send_direct_sysex_for_name(string[:3]+string[3:])
            self.last_parameter_button_changing = False

    def get_parameter_MIDI_value(self, parameter, value):
        _min = parameter.min
        _max = parameter.max
        _value = value / 127 * (_max - _min) + _min
        return _value

    def _setup_scene_listeners(self):
        self._on_scene_triggered.replace_subjects(self._song.scenes, count())

    @subject_slot('color')
    def _on_track_color_changed(self):
        if self.is_enabled() and self._track_bank_left_button and self._track_bank_right_button and self._current_track_color:
            color_index = 0
            try:
                selected_track_index = list(self._song.tracks).index(self.selected_track)
            except:
                selected_track_index = 0
            index = self._track_offset if not Options.session_box_linked_to_selection else selected_track_index
            for i, elem in enumerate([index-1, index, index+1]):
                if -1 < elem < len(self._song.tracks):
                    color_index = self._song.tracks[elem].color_index
                else:
                    color_index = 0
                self._track_leds[i].send_value(color_index, force=True)

    @subject_slot('color')
    def _on_scene_color_changed(self, is_triggered=False):
            index_list = [-1, 0, 1]
            if self._launch_scene_button and self._scene_bank_up_button and self._scene_bank_down_button:
                buttons = [[self._scene_bank_up_button], [self._launch_scene_button], [self._scene_bank_down_button]]
                for index, button in zip(index_list, buttons):
                    ind = self._scene_offset + index
                    if -1 < ind < len(self._song.scenes):
                        scene = self._song.scenes[ind]
                        if scene.color_index:
                            color = scene.color_index
                            channel = 15
                        else:
                            color = 124
                            channel = 15
                        if self._last_triggered_scene_index is not None and self._last_triggered_scene_index == ind:
                            color = 126
                            channel = 14
                        if scene.is_triggered:
                            color = 126
                            channel = 13
                    else:
                        color = 0
                        channel = 15
                    for b in button:
                        b.send_value(color, force=True, channel=channel)

    @subject_slot('name')
    def _on_scene_name_changed(self):
        name = None
        scene = self._song.scenes[self._scene_offset]
        if self.is_enabled():
            if self._scene_offset == self.song().view.selected_scene:
                name = scene.name.strip()
                if len(name) == 0:
                    name = str(list(self._song.scenes).index(scene)+1)
                self.send_sysex_for_name(0, name)
        self.scan_setlist()

    """ Various functions """

    def _change_offsets(self, track_increment, scene_increment):
        self._update_stop_clips_led(0)
        super(SessionComponent, self)._change_offsets(track_increment, scene_increment)
        self._update_position_status_control()

    def _update_position_status_control(self, is_triggered=False):
        if self.is_enabled() and self._track_offset > -1 and self._scene_offset > -1:
            self._do_show_highlight()
            self._on_scene_color_changed()
            self._on_track_color_changed()
            self._setup_scene_listeners()
            self._on_scene_name_changed()

    def set_stopped_clip_value(self, value):
        self._stopped_clip_value = value

    def _update_stop_all_clips_button(self):
        button = self._stop_all_button
        if button:
            if button.is_pressed():
                button.set_light(self._stop_clip_value)
            else:
                button.set_light(self._stopped_clip_value)

    def _find_next_empty_slot(self):
        song = self.song()
        scene_count = len(song.scenes)
        scene_index = self._scene_offset
        while song.tracks[self._track_offset].clip_slots[scene_index].has_clip:
            scene_index += 1
            if scene_index == scene_count:
                song.create_scene(scene_count)
        song.tracks[self._track_offset].stop_all_clips(Quantized=False)
        if not Options.session_box_linked_to_selection:
            self._scene_offset = scene_index
            self._do_show_highlight()
        else:
            self.song().view.selected_scene = self._song.scenes[scene_index] 

    def update(self):
        super(SessionComponent, self).update()
        self._update_position_status_control()
        self.on_selected_scene_changed()

    def _send_direct_sysex_for_name(self, name):
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 54, 3]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self._last_selected_parameter_button is not None and time.time() - self.last_message_time > Options.display_time:
            self._last_selected_parameter_button._send_midi(tuple(message))
            self.last_message_time = time.time()

    @subject_slot('value')
    def scan_setlist(self, value=127):
        if value:
            self.setlist = {}
            for s in self.song().scenes:
                number = self.find_song_in_name(s)
                if number > -1 and number not in self.setlist:
                    self.setlist[number] = s
            for cue in self.song().cue_points:
                number = self.find_song_in_name(cue)
                if number > -1 and number not in self.setlist:
                    self.setlist[number] = cue
            if len(self.sorted_setlist_keys) > 0:
                if self.selected_setlist_song is None:
                    self.selected_setlist_song = self.sorted_setlist_keys[0]
                self.show_song_name()
                self._on_setlist_song_color_changed()
            else:
                self.send_sysex_for_name(5, "Add Songs")

    def find_song_in_name(self, item):
        number = -1
        num1 = item.name.find("(SONG")
        if num1 > -1:
            num2 = item.name.find(")")
            number = int(item.name[num1+5:num2])
        return number

    def set_prev_setlist_song(self, button):
        self._prev_setlist_song_button = button
        self._prev_setlist_song_button_value.subject = button

    def set_next_setlist_song(self, button):
        self._next_setlist_song_button = button
        self._next_setlist_song_button_value.subject = button

    def set_launch_setlist_song(self, button):
        self._launch_setlist_song_button = button
        self._launch_setlist_song_button_value.subject = button

    def set_launch_setlist_song_noq(self, button):
        self._launch_setlist_song_noq_button = button
        self._launch_setlist_song_noq_button_value.subject = button

    def set_refresh_setlist(self, button):
        self._refresh_setlist_button = button
        self.scan_setlist.subject = button
        self.scan_setlist()

    def show_song_name(self):
        # if self.selected_setlist_song is not None:
        new_name = self.setlist[self.selected_setlist_song].name
        num1 = new_name.find("(SONG")
        num2 = new_name.find(")", num1)
        number = new_name[num1+5:num2]
        new_name = new_name[:num1] + new_name[num2+1:]
        self.send_sysex_for_name(5, "[" + number + "] " + new_name)

    @subject_slot('value')
    def _launch_setlist_song_button_value(self, value):
        if value:
            self.launch_song()

    @subject_slot('value')
    def _launch_setlist_song_noq_button_value(self, value):
        if value:
            self.song().stop_playing()
            self.launch_song()

    def launch_song(self):
            self.playing_song = self.setlist[self.selected_setlist_song]
            if self.playing_song in self.song().scenes:
                self.playing_song.fire()
            elif self.playing_song in self.song().cue_points:
                self.song().back_to_arranger = 0
                self.playing_song.jump()
                self.song().start_playing()
            self._on_setlist_song_color_changed()

    @subject_slot('value')
    def _next_setlist_song_button_value(self, value):
        if value:
            index = min(self._setlist_song_index() + 1, len(self.sorted_setlist_keys))
            self.selected_setlist_song = self.sorted_setlist_keys[index]
            self.select_scene_cuepoint()
            self.show_song_name()
            self._on_setlist_song_color_changed()

    @subject_slot('value')
    def _prev_setlist_song_button_value(self, value):
        if value:
            index = max(self._setlist_song_index() - 1, 0)
            self.selected_setlist_song = self.sorted_setlist_keys[index]
            self.select_scene_cuepoint()
            self.show_song_name()
            self._on_setlist_song_color_changed()
    
    def select_scene_cuepoint(self):
        if self.setlist[self.selected_setlist_song] in self.song().scenes:
            self.song().view.selected_scene = self.setlist[self.selected_setlist_song]

    def _setlist_song_index(self):
        return self.sorted_setlist_keys.index(self.selected_setlist_song)

    def send_sysex_for_name(self, display_type, name):       
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 51, display_type]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self.is_enabled() and self._launch_setlist_song_button:     
            self._launch_setlist_song_button._send_midi(tuple(message))

    @property
    def sorted_setlist_keys(self):
        return sorted(list(self.setlist.keys()))

    @subject_slot('color')
    def _on_setlist_song_color_changed(self, is_triggered=False):
            index_list = [-1, 0, 1]
            if self._launch_setlist_song_button and self._prev_setlist_song_button and self._next_setlist_song_button:
                buttons = [self._prev_setlist_song_button, self._launch_setlist_song_button, self._next_setlist_song_button]
                for index, button in zip(index_list, buttons):
                    ind = self._setlist_song_index() + index
                    if -1 < ind < len(self.sorted_setlist_keys):
                        song = self.setlist[self.sorted_setlist_keys[ind]]
                        if song in self.song().scenes:
                            if song.color_index:
                                color = song.color_index
                                channel = 15
                            else:
                                color = 124
                                channel = 15
                            # if self._last_triggered_scene_index is not None and self._last_triggered_scene_index == ind:
                            #     color = 126
                            #     channel = 14
                            # if scene.is_triggered:
                            #     color = 126
                            #     channel = 13
                        else:
                            color = 120
                            channel = 15
                        if self.playing_song is not None and song == self.playing_song:
                            channel = 14

                    else:
                        color = 0
                        channel = 15
                    button.send_value(color, force=True, channel=channel)