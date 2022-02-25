from __future__ import absolute_import
from itertools import count
from this import d
import Live
from _Framework.SessionComponent import SessionComponent as SessionBase
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from . import Colors, Options

class SessionComponent(SessionBase):
    """ SessionComponent extends the standard to use a custom SceneComponent, use custom
    ring handling and observe the status of scenes. """
    def __init__(self, parent, *a, **k):
        self.parent = parent
        self._launch_scene_button = None
        self._launch_setlist_song_button = None
        self.selected_setlist_song = None
        self.playing_song = None
        self._track_leds = [None, None, None]
        self._custom_action = None
        super(SessionComponent, self).__init__(*a, **k)

    def set_custom_action(self, custom_action):
        self._custom_action = custom_action

    def update(self):
        super(SessionComponent, self).update()
        self._update_scene_position()
        self.on_selected_scene_changed()
        self.update_track_selection()

    # def _change_offsets(self, track_increment, scene_increment):
    #     self._update_stop_clips_led(0)
    #     super(SessionComponent, self)._change_offsets(track_increment, scene_increment)
    #     # self._update_scene_position()

    # Detail View
    def set_detail_view_toggle(self, button):
        self._detail_view_toggle_button = button
        self._detail_view_toggle_button_value.subject = button

    def on_view_changed(self):
        self.view = "Detail/Clip"

    @subject_slot('value')
    def _detail_view_toggle_button_value(self, value):
        if value:
            if self.view == "Detail/Clip":
                self.application().view.focus_view("Detail/DeviceChain")
                self.view = "Detail/DeviceChain"
            else:
                self.application().view.focus_view("Detail/Clip")
                self.view = "Detail/Clip"

    # Main View
    def set_main_view_toggle(self, button):
        self._main_view_toggle_button = button
        self._main_view_toggle_button_value.subject = button
        # self.application().view.add_focused_document_view_listener(self.on_view_changed)

    @subject_slot('value')
    def _main_view_toggle_button_value(self, value):
        if value:
            if self.application().view.focused_document_view == "Session":
                self.application().view.focus_view("Arranger")
            else:
                self.application().view.focus_view("Session")

    # Undo
    def set_undo(self, button):
        self._undo_button = button
        self._undo_value.subject = button

    @subject_slot('value')
    def _undo_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.undo()

    # Redo
    def set_redo(self, button):
        self._undo_button = button
        self._redo_value.subject = button

    @subject_slot('value')
    def _redo_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.redo()

    # Master Volume
    def set_master_volume(self, button):
        self.master_volume_button=button
        self._master_volume_button_value.subject = button

    @subject_slot('value')
    def _master_volume_button_value(self, value):
        self.song().master_track.mixer_device.volume = value/127

    # Last Selected Parameter
    def set_last_selected_parameter(self, button):
        self._last_selected_parameter_button = button
        self._last_selected_parameter_value.subject = button

    @subject_slot('value')
    def _last_selected_parameter_value(self, value):
        if self.is_enabled() and self.song().view.selected_parameter:
            # self.last_parameter_button_changing = True
            parameter = self.song().view.selected_parameter
            parameter.value = self.get_parameter_MIDI_value(parameter, value)
            string = parameter.str_for_value(parameter.value)
            self.parent.set_temp_message(string[:3]+string[3:])
            # self.last_parameter_button_changing = False

    def on_selected_parameter_changed(self):
        parameter = self.song().view.selected_parameter
        if parameter:
            self._last_selected_parameter_button.send_value(self.get_parameter_value(parameter, parameter.value), force=True)

    def get_parameter_MIDI_value(self, parameter, value):
        _min = parameter.min
        _max = parameter.max
        _value = value / 127 * (_max - _min) + _min
        return _value

    def get_parameter_value(self, parameter, value):
        _min = parameter.min
        _max = parameter.max
        _value =  (value - _min )/ (_max - _min)
        return _value * 127

    """ SCENES """

    # Insert Scene
    def set_insert_scene(self, button):
        self._insert_scene_button = button
        self._insert_scene_value.subject = button

    @subject_slot('value')
    def _insert_scene_value(self, value):
        if self.is_enabled():
            if self.selected_scene in self._song.scenes and Options.session_box_linked_to_selection:
                self._scene_offset = int(list(self._song.scenes).index(self.selected_scene))
            if value is not 0:
                self._scene_offset += 1
                self.song().create_scene(self._scene_offset)
                self._reassign_scenes()
                self._update_scene_position()

    # Capture and Insert Scene
    def set_capture_and_insert_scene(self, button):
        self._capture_and_insert_scene_button = button
        self._capture_and_insert_scene_value.subject = button

    @subject_slot('value')
    def _capture_and_insert_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.song().capture_and_insert_scene()

    # Stop All Clips
    def set_stop_all_clips_button(self, button):
        self._stop_all_clips_button = button
        self._stop_all_clips_button_value.subject = button

    @subject_slot('value')
    def _stop_all_clips_button_value(self, value):
        if value:
            self.song().stop_all_clips()

    # Select Prev Scene
    def set_scene_bank_up_button(self, button):
        self._scene_bank_up_button = button
        self._scene_bank_up_value.subject = button

    @subject_slot('value')
    def _scene_bank_up_value(self, value):
        if value == 127: 
            value = 1 
        if value:
            self.set_offsets(self.track_offset(), max(0, self.scene_offset() - value))
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]
            self._update_scene_position()

    def set_scene_bank_up_x4_button(self, button):
        self._scene_bank_up_x4_button = button
        self._scene_bank_up_x4_value.subject = button

    @subject_slot('value')
    def _scene_bank_up_x4_value(self, value):
        if value:
            self._scene_bank_up_value(4)

    # Select Next Scene 
    def set_scene_bank_down_button(self, button):
        self._scene_bank_down_button = button
        self._scene_bank_down_value.subject = button

    @subject_slot('value')
    def _scene_bank_down_value(self, value):
        if value == 127: value = 1 
        if value:
            self.set_offsets(self.track_offset(), max(0, self.scene_offset() + value))
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[self.scene_offset()]
            self._update_scene_position()

    def set_scene_bank_down_x4_button(self, button):
        self._scene_bank_down_x4_button = button
        self._scene_bank_down_x4_value.subject = button

    @subject_slot('value')
    def _scene_bank_down_x4_value(self, value):
        if value:
            self._scene_bank_down_value(4)

    # Scroll Scenes
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

    # Jump to Playing Scene
    def set_jump_to_playing_scene(self, button):
        self._jump_to_playing_scene_button = button
        self._jump_to_playing_scene_value.subject = button

    @subject_slot('value')
    def _jump_to_playing_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.set_offsets(self._track_offset, self._last_triggered_scene_index)
                if Options.session_box_linked_to_selection:
                    self.song().view.selected_scene = self.song().scenes[self._last_triggered_scene_index]
                self._update_scene_position()

    # Scene Launch
    def set_launch_scene_button(self, button):
        self._launch_scene_button = button
        self._launch_scene_value.subject = button
        self._on_scene_triggered.replace_subjects(self._song.scenes, count())
        self._last_triggered_scene_index = None

    @subject_slot('value')
    def _launch_scene_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.scenes[self._scene_offset].fire_as_selected()

    @subject_slot_group('is_triggered')
    def _on_scene_triggered(self, index):
        self._last_triggered_scene_index = index    
        is_triggered = self._song.scenes[index].is_triggered
        self._on_scene_color_changed()
        # self._update_scene_position(is_triggered=is_triggered)
        # self._on_scene_triggered.replace_subjects(self._song.scenes, count())
        if self.check_stop(self._song.scenes[index]) and is_triggered == 0:
            self._song.stop_playing()

    def _update_scene_position(self, is_triggered=False):
        if self.is_enabled() and self._track_offset > -1 and self._scene_offset > -1:
            self._on_scene_color_changed()
            self.display_scene_name()

    # Selected Scene Listener
    def on_scene_list_changed(self):
        self._on_scene_triggered.replace_subjects(self._song.scenes, count())
        super(SessionComponent, self).on_scene_list_changed()

    def on_selected_scene_changed(self):
        self.selected_scene = self._song.view.selected_scene
        self._on_scene_color_changed.subject = self.selected_scene
        self._on_scene_name_changed.subject = self.selected_scene
        if self._custom_action is not None:
            self._custom_action.on_selected_clip_changed()
        if self.selected_scene in self._song.scenes and Options.session_box_linked_to_selection:
            self._scene_offset = int(list(self._song.scenes).index(self.selected_scene))
            if self._track_offset is not -1 and self._scene_offset is not -1:
                self.set_offsets(self._track_offset, self._scene_offset)
                self._reassign_scenes()
                self._update_scene_position()

    # Scene Color
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

    # Scene Name
    @subject_slot('name')
    def _on_scene_name_changed(self):
        if self._song.scenes[self._scene_offset] == self.song().view.selected_scene:
            self.display_scene_name()
        self.scan_setlist()

    def check_stop(self, scene):
        num1 = scene.name.find("(STOP)")
        res = True if num1 > -1 else False
        return (res)

    def display_scene_name(self):
        scene = self._song.scenes[self._scene_offset]
        name = scene.name.strip()
        if len(name) == 0:
            name = str(list(self._song.scenes).index(scene)+1)
        self.parent.display_message("Scene Name", name)

    """ TRACK """

    @property
    def active_track(self):
        if Options.session_box_linked_to_selection:
            return self.selected_track 
        else:
            return self.song().visible_tracks[self.track_offset()]

    # Add Audio Track
    def set_add_audio_track(self, button):
        self._add_audio_track_button = button
        self._add_audio_track_value.subject = button

    @subject_slot('value')
    def _add_audio_track_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.create_audio_track()

    # Add MIDI Track
    def set_add_MIDI_track(self, button):
        self._add_MIDI_track_button = button
        self._add_MIDI_track_value.subject = button

    @subject_slot('value')
    def _add_MIDI_track_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.create_midi_track()

    # Fold/Unfold Track
    def set_unfold_track(self, button):
        self._unfold_track_button = button
        self._unfold_track_button_value.subject = button

    @subject_slot('value')
    def _unfold_track_button_value(self, value):
        track = self.active_track
        if value:
            if track.is_foldable:
                track.fold_state = not track.fold_state
            elif track.can_show_chains:
                track.is_showing_chains = not track.is_showing_chains

    # Select Prev Track
    def set_track_bank_left_button(self, button):
        self._track_bank_left_button = button
        self._track_leds[0] = button
        self._track_bank_left_value.subject = button

    @subject_slot('value')
    def _track_bank_left_value(self, value):
        if value:
            self.set_offsets(max(0, self._track_offset - 1), self.scene_offset())
            if Options.session_box_linked_to_selection:
                self._song.view.selected_track = self._song.tracks[self.track_offset()]
            self.update_track_selection()

    # Select Next Track
    def set_track_bank_right_button(self, button):
        self._track_bank_right_button = button
        self._track_leds[2] = button
        self._track_bank_right_value.subject = button

    @subject_slot('value')
    def _track_bank_right_value(self, value):
        if value:
            self.set_offsets(min(self._track_offset + 1, len(self._song.visible_tracks)-1), self.scene_offset())
            if Options.session_box_linked_to_selection:
                self._song.view.selected_track = self._song.tracks[self.track_offset()]
            self.update_track_selection()

    # Selected Track Listener
    def on_selected_track_changed(self):
        self.selected_track = self._song.view.selected_track
        self._on_track_color_changed.subject = self.song().view.selected_track
        self._on_track_name_changed.subject = self.song().view.selected_track
        self._on_mute_changed.subject = self.song().view.selected_track
        self._on_arm_changed.subject = self.song().view.selected_track
        if self._custom_action is not None:
            self._custom_action.on_selected_clip_changed()
        if self.selected_track in self._song.visible_tracks and Options.session_box_linked_to_selection:
            self._track_offset = list(self._song.visible_tracks).index(self.selected_track)
            if self._track_offset > -1: # and self._scene_offset > -1:
                self.update_track_selection()

    def update_track_selection(self):
        try:
            self._mixer.set_track_offset(self.track_offset())
            self._mixer._selected_strip.set_track(self._song.tracks[self.track_offset()])
            print(self._song.view.selected_track)
            # if Options.session_box_linked_to_selection:
            #     self._song.view.selected_track = self._song.tracks[self.track_offset()]
            self.display_track_name()
            self._on_track_color_changed()
            self._on_mute_changed()
            self._on_arm_changed()
        except:
            pass

    # def _update_track_position(self):
    #         self._on_track_color_changed()
    #         self.display_track_name()

    # Track Color
    def set_current_track_color(self, button):
        self._current_track_color = button
        self._track_leds[1] = button
        self.on_selected_track_changed()
        # self._on_track_color_changed()

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

    # Track Name
    @subject_slot('name')
    def _on_track_name_changed(self):
        if self.selected_track == self.song().tracks[self._track_offset]:
            self.display_track_name()

    def display_track_name(self):
        if self.is_enabled():
            self.parent.display_message("Track Name", self.song().tracks[self._track_offset].name)
           
    # Clip Launch/Stop
    def set_clip_launch_buttons(self, button):
        super(SessionComponent, self).set_clip_launch_buttons(button)
        self._clip_launch_buttons = button
        clip_color_table = Colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
        clip_color_table[16777215] = 119
        self.set_rgb_mode(clip_color_table, Colors.RGB_COLOR_TABLE)

    def set_stopped_clip_value(self, value):
        self._stopped_clip_value = value

    def _enable_skinning(self):
        super(SessionComponent, self)._enable_skinning()
        self.set_stopped_clip_value(u'Session.StoppedClip')

    # Find Next Empty Slot
    def set_find_next_empty_slot(self, button):
        self._find_next_empty_slot_button = button
        self._find_next_empty_slot_value.subject = button

    @subject_slot('value')
    def _find_next_empty_slot_value(self, value):
        if self.is_enabled():
            if value is not 0:
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
                else:
                    self.song().view.selected_scene = self._song.scenes[scene_index] 

    # Fixed Length Recording
    def set_fixed_length_rec_1bars(self, button):
        self._fixed_length_rec_1bars_button = button
        self._fixed_length_rec_1bars_value.subject = button

    @subject_slot('value')
    def _fixed_length_rec_1bars_value(self, value):
        if value:
            self.song().trigger_session_record(4)

    def set_fixed_length_rec_2bars(self, button):
        self._fixed_length_rec_2bars_button = button
        self._fixed_length_rec_2bars_value.subject = button

    @subject_slot('value')
    def _fixed_length_rec_2bars_value(self, value):
        if value:
            self.song().trigger_session_record(8)

    def set_fixed_length_rec_4bars(self, button):
        self._fixed_length_rec_4bars_button = button
        self._fixed_length_rec_4bars_value.subject = button

    @subject_slot('value')
    def _fixed_length_rec_4bars_value(self, value):
        if value:
            self.song().trigger_session_record(16)

    def set_fixed_length_rec_8bars(self, button):
        self._fixed_length_rec_8bars_button = button
        self._fixed_length_rec_8bars_value.subject = button

    @subject_slot('value')
    def _fixed_length_rec_8bars_value(self, value):
        if value:
            self.song().trigger_session_record(32)

    # Mute Track
    def set_mute_button(self, button):
        self._mute_button = button
        self._mute_button_value.subject = button
        
    @subject_slot('value')
    def _mute_button_value(self, value):
        if value:
            track = self.active_track
            track.mute = 0 if track.mute == 1 else 1 
            self._on_mute_changed()

    @subject_slot('mute')
    def _on_mute_changed(self):
        track = self.active_track
        if self.is_enabled() and self._mute_button != None:
            color = 80
            if track.mute == 1:
                color = 81
            self._mute_button.send_value(color, force=True)

    # Arm Track
    def set_arm_button(self, button):
        self._arm_button = button
        self._arm_button_value.subject = button
        
    @subject_slot('value')
    def _arm_button_value(self, value):
        if value:
            track = self.active_track
            track.arm = 0 if track.arm == 1 else 1 
            self._on_arm_changed()

    @subject_slot('arm')
    def _on_arm_changed(self):
        track = self.active_track
        if self.is_enabled() and self._arm_button != None:
            color = 0
            if track.arm == 1 and track.can_be_armed:
                color = 127
            self._arm_button.send_value(color, force=True)

    # Solo Track
    def set_solo_button(self, button):
        self._solo_button = button
        self._solo_button_value.subject = button
        
    @subject_slot('value')
    def _solo_button_value(self, value):
        if value:
            track = self.active_track
            track.solo = 0 if track.solo == 1 else 1 
            self._on_solo_changed()

    @subject_slot('solo')
    def _on_solo_changed(self):
        track = self.active_track
        if self.is_enabled() and self._solo_button != None:
            color = 0
            if track.solo == 1:
                color = 23
            self._solo_button.send_value(color, force=True)

    # Stop Track
    def set_stop_button(self, button):
        self._stop_button = button
        self._stop_button_value.subject = button
        
    @subject_slot('value')
    def _stop_button_value(self, value):
        if value:
            self.active_track.stop_all_clips()

    """ Setlist"""
    
    # Build Setlist
    def scan_setlist(self):
        self.setlist = {}
        for s in self.song().scenes:
            number = self.find_song_in_name(s.name)
            if number > -1 and number not in self.setlist:
                self.setlist[number] = s
        for cue in self.song().cue_points:
            number = self.find_song_in_name(cue.name)
            if number > -1 and number not in self.setlist:
                self.setlist[number] = cue
        if len(self.sorted_setlist_keys) > 0:
            if self.selected_setlist_song is None:
                self.selected_setlist_song = self.sorted_setlist_keys[0]
            self.show_song_name()
            self._on_setlist_song_color_changed()
        else:
            self.parent.display_message("Setlist Song", "Add Songs")

    def select_scene_cuepoint(self):
        song = self.setlist[self.selected_setlist_song]
        if song in self.song().scenes:
            scene_offset = int(list(self._song.scenes).index(song))
            if Options.session_box_linked_to_selection:
                self._song.view.selected_scene = self._song.scenes[scene_offset]
            self.set_offsets(self.track_offset(), scene_offset)
            self.application().view.focus_view("Session")
        else:
            self.parent._transport.selected_cue = song
            self.application().view.focus_view("Arranger")

    def _setlist_song_index(self):
        return self.sorted_setlist_keys.index(self.selected_setlist_song)

    @property
    def sorted_setlist_keys(self):
        return sorted(list(self.setlist.keys()))

    # Select Prev Setlist Song
    def set_prev_setlist_song(self, button):
        self._prev_setlist_song_button = button
        self._prev_setlist_song_button_value.subject = button

    @subject_slot('value')
    def _prev_setlist_song_button_value(self, value):
        if value:
            index = max(self._setlist_song_index() - 1, 0)
            self.selected_setlist_song = self.sorted_setlist_keys[index]
            self.select_scene_cuepoint()
            self.show_song_name()
            self._on_setlist_song_color_changed()
   

    # Select Next Setlist Song
    def set_next_setlist_song(self, button):
        self._next_setlist_song_button = button
        self._next_setlist_song_button_value.subject = button

    @subject_slot('value')
    def _next_setlist_song_button_value(self, value):
        if value:
            index = min(self._setlist_song_index() + 1, len(self.sorted_setlist_keys))
            self.selected_setlist_song = self.sorted_setlist_keys[index]
            self.select_scene_cuepoint()
            self.show_song_name()
            self._on_setlist_song_color_changed()


    # Launch Setlist Song
    def set_launch_setlist_song(self, button):
        self._launch_setlist_song_button = button
        self._launch_setlist_song_button_value.subject = button
        self.scan_setlist()

    def set_launch_setlist_song_noq(self, button):
        self._launch_setlist_song_noq_button = button
        self._launch_setlist_song_noq_button_value.subject = button

    @subject_slot('value')
    def _launch_setlist_song_button_value(self, value):
        if value:
            self.launch_song()

    @subject_slot('value')
    def _launch_setlist_song_noq_button_value(self, value):
        if value:
            # self.song().stop_playing()
            self.launch_song(no_q = True)

    def launch_song(self, no_q = False):
        self.timer = Live.Base.Timer(callback=self.on_timer_reached, interval=20, repeat=False)
        self.playing_song = self.setlist[self.selected_setlist_song]
        if self.playing_song in self.song().scenes:
            if no_q:
                self.song().stop_playing()
                self.timer.start()
            else:
                self.playing_song.fire()
        elif self.playing_song in self.song().cue_points:
            if no_q:
                quantization = self.song().clip_trigger_quantization
                self.song().clip_trigger_quantization = Live.Song.Quantization.q_no_q
                self.song().current_song_time = self.playing_song.time
                self.song().clip_trigger_quantization = quantization
            self.playing_song.jump()
            self.song().back_to_arranger = 0
            self.song().re_enable_automation()
            if not self.song().is_playing:
                self.song().start_playing()
        self._on_setlist_song_color_changed()

    def on_timer_reached(self):
        self.timer.stop()
        self.playing_song.fire()

    # Setlist Song Color
    @subject_slot('color')
    def _on_setlist_song_color_changed(self, is_triggered=False):
            index_list = [-1, 0, 1]
            if self._launch_setlist_song_button and self._prev_setlist_song_button and self._next_setlist_song_button:
                buttons = [self._prev_setlist_song_button, self._launch_setlist_song_button, self._next_setlist_song_button]
                for index, button in zip(index_list, buttons):
                    ind = self._setlist_song_index() + index
                    if -1 < ind < len(self.sorted_setlist_keys):
                        song = self.setlist[self.sorted_setlist_keys[ind]]
                        channel = 15
                        if song in self.song().scenes:
                            if song.color_index:
                                color = song.color_index
                            else:
                                color = 124
                        else:
                            color = self.find_color_in_name(song)
                        # if self.playing_song is not None and song == self.playing_song:
                            # channel = 14
                    else:
                        color = 0
                        channel = 15
                    button.send_value(color, force=True, channel=channel)

    def find_color_in_name(self, item):
        color = 118
        num1 = item.name.find("(COLOR")
        if num1 > -1:
            num2 = item.name.find(")", num1)
            color = int(item.name[num1+6:num2])
        return color

    # Setlist Song Name
    def find_song_in_name(self, name):
        number = -1
        num1 = name.find("(SONG")
        if num1 > -1:
            num2 = name.find(")", num1)
            number = int(name[num1+5:num2])
        return number

    def remove_string_from_name(self, string_to_temove, name):
        num1 = name.find("(" + string_to_temove)
        if num1 > -1:
            num2 = name.find(")", num1)
            name = name[:num1] + name[num2+1:]
        return name

    def show_song_name(self):
        name = self.setlist[self.selected_setlist_song].name
        self.parent.display_message("Setlist Song", "[" + str(self.find_song_in_name(name)) + "] " + self.remove_string_from_name("SONG", (self.remove_string_from_name("COLOR", name))))