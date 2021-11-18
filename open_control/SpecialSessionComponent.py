from __future__ import absolute_import
# from builtins import str
# from builtins import zip
# from builtins import range
from itertools import count

from _Framework.SessionComponent import SessionComponent as SessionBase
from _Framework.SubjectSlot import subject_slot_group, subject_slot
# from _Framework.ClipSlotComponent import ClipSlotComponent as ClipSlotBase
# from _Framework.SceneComponent import SceneComponent as SceneBase
from . import Colors, Options
from .SpecialSceneComponent import SceneComponent

import logging, traceback
logger = logging.getLogger(__name__)
# def print(text):
#     logger.warning(text)

class SessionComponent(SessionBase):
    """ SessionComponent extends the standard to use a custom SceneComponent, use custom
    ring handling and observe the status of scenes. """
    scene_component_type = SceneComponent
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
        self.view = None
        super(SessionComponent, self).__init__(*a, **k)
        self.selected_track = self.song().view.selected_track
        self._show_highlight = True
        self._setup_scene_listeners()
        self.application().view.add_focused_document_view_listener(self.on_view_changed)
        clip_color_table = Colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
        clip_color_table[16777215] = 119
        self.set_rgb_mode(clip_color_table, Colors.RGB_COLOR_TABLE)

    def disconnect(self):
        super(SessionComponent, self).disconnect()
        self._position_status_control = None

    def _enable_skinning(self):
        super(SessionComponent, self)._enable_skinning()
        self.set_stopped_clip_value(u'Session.StoppedClip')

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

    def set_scene_bank_up_button(self, button):
        self._scene_bank_up_button = button
        self._scene_bank_up_value.subject = button

    @subject_slot('value')
    def _scene_bank_up_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), max(0, self.scene_offset() - 1))
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]

    def set_scene_bank_down_button(self, button):
        self._scene_bank_down_button = button
        self._scene_bank_down_value.subject = button

    @subject_slot('value')
    def _scene_bank_down_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), self.scene_offset() + 1)
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]

    def set_track_bank_left_button(self, button):
        self._track_bank_left_button = button
        self._track_leds[0] = button
        self._track_bank_left_value.subject = button

    @subject_slot('value')
    def _track_bank_left_value(self, value):
        if value:
            self.set_offsets(max(self.track_offset() - 1, 0), self.scene_offset())
            if Options.session_box_linked_to_selection:
                self._song.view.selected_track = self._song.tracks[self.track_offset()]

    def set_track_bank_right_button(self, button):
        self._track_bank_right_button = button
        self._track_leds[2] = button
        self._track_bank_right_value.subject = button
        
    @subject_slot('value')
    def _track_bank_right_value(self, value):
        if value:
            self.set_offsets(self.track_offset() + 1, self.scene_offset())
            if Options.session_box_linked_to_selection:
                self._song.view.selected_track = self._song.tracks[self.track_offset()]

    def set_master_volume(self, button):
        self.master_volume_button=button
        self._master_volume_button_value.subject = button

    @subject_slot('value')
    def _master_volume_button_value(self, value):
        print(self.song().master_track.mixer_device.volume)
        self.song().master_track.mixer_device.volume = value/127


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

    def set_last_selected_parameter(self, button):
        self._last_selected_parameter_button = button
        self._last_selected_parameter_value.subject = button

    def on_view_changed(self):
        self.view = "Detail/Clip"

    def set_main_view_toggle(self, button):
        self._main_view_toggle_button = button
        self._main_view_toggle_button_value.subject = button

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

    def set_detail_view_toggle(self, button):
        self._detail_view_toggle_button = button
        self._detail_view_toggle_button_value.subject = button

    @subject_slot('value')
    def _detail_view_toggle_button_value(self, value):
        if value:
            if self.view == "Detail/Clip":
                self.application().view.focus_view("Detail/DeviceChain")
                self.view = "Detail/DeviceChain"
            else:
                self.application().view.focus_view("Detail/Clip")
                self.view = "Detail/Clip"

    def set_undo(self, button):
        self._undo_button = button
        self._undo_value.subject = button

    def set_redo(self, button):
        self._undo_button = button
        self._redo_value.subject = button

    def set_jump_to_playing_scene(self, button):
        self._rjump_to_playing_scene_button = button
        self._jump_to_playing_scene_value.subject = button

    @subject_slot('value')
    def _jump_to_playing_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.set_offsets(self._track_offset, self._last_triggered_scene_index)
                if Options.session_box_linked_to_selection:
                    self.song().view.selected_scene = self.song().scenes[self._last_triggered_scene_index]

    def set_insert_scene(self, button):
        self._insert_scene_button = button
        self._insert_scene_value.subject = button

    def set_capture_and_insert_scene(self, button):
        self._capture_and_insert_scene_button = button
        self._capture_and_insert_scene_value.subject = button

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

    def _change_offsets(self, track_increment, scene_increment):
        self._update_stop_clips_led(0)
        super(SessionComponent, self)._change_offsets(track_increment, scene_increment)
        self._update_position_status_control()

    def _update_position_status_control(self, is_triggered=False):
        if self.is_enabled() and self._track_offset > -1 and self._scene_offset > -1:
            self._do_show_highlight()
            self._on_scene_color_changed(is_triggered)
            self._on_track_color_changed()
            self._setup_scene_listeners()

    def on_scene_list_changed(self):
        self._setup_scene_listeners()
        super(SessionComponent, self).on_scene_list_changed()

    def on_selected_scene_changed(self):
        self.selected_scene = self._song.view.selected_scene
        if self.selected_scene in self._song.scenes and Options.session_box_linked_to_selection:
            self._scene_offset = int(list(self._song.scenes).index(self.selected_scene))
            if self._track_offset is not -1 and self._scene_offset is not -1:
                self.set_offsets(self._track_offset, self._scene_offset)
                self._reassign_scenes()
                self._update_position_status_control()

    def on_selected_track_changed(self):
        self.selected_track = self._song.view.selected_track
        if self.selected_track in self._song.visible_tracks and Options.session_box_linked_to_selection:
            self._track_offset = list(self._song.visible_tracks).index(self.selected_track)
            if self._track_offset > -1 and self._scene_offset > -1:
                self._mixer.set_track_offset(self._track_offset)
                self._update_position_status_control()

    def set_stopped_clip_value(self, value):
        self._stopped_clip_value = value

    def set_stop_all_clips_button(self, button):
        if button:
            button.reset_state()
        super(SessionComponent, self).set_stop_all_clips_button(button)

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
                self._song.scenes[self._scene_offset].fire()

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
            _min = self.song().view.selected_parameter.min
            _max = self.song().view.selected_parameter.max
            _value = (_max - _min) * value / 127 + _min
            self.song().view.selected_parameter.value = _value

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

    def update(self):
        super(SessionComponent, self).update()
        self._update_position_status_control()
        self.on_selected_scene_changed()
