import Live
from _Framework.TransportComponent import TransportComponent as TransportBase
from _Framework.SubjectSlot import subject_slot
from . import Options

class TransportComponent(TransportBase):
    def __init__(self, parent, *a, **k):
        self.parent = parent
        self.prev_cue = None
        self.selected_cue = None
        super(TransportComponent, self).__init__(*a, **k)

    def set_session(self, session):
        self._session = session

    def disconnect(self):
        super(TransportComponent, self).disconnect()
         
    # Start/Stop
    def set_start_stop(self, button):
        self._start_stop_button = button
        self._start_stop_button_value.subject = button
        self._on_start_stop_changed()

    @subject_slot('value')
    def _start_stop_button_value(self, value):
        if self.is_enabled() and self._start_stop_button:
            if value:
                self.song().stop_playing() if self.song().is_playing else self.song().start_playing()

    def _on_start_stop_changed(self):
        if self.is_enabled() and self._start_stop_button and self._continue_playing_button:
            if self.song().is_playing:
                self.restart_position = self._song.current_song_time
                color1 = 65
                color2 = 126
            else:
                color1 = 0
                color2 = 65
            self._start_stop_button.send_value(color1, force=True)
            self._continue_playing_button.send_value(color2, force=True)

    # Restart
    def set_restart_button(self, button):
        self._restart_button = button
        self._restart_button_value.subject = button
        self.restart_position = self.song().current_song_time

    @subject_slot('value')
    def _restart_button_value(self, value):
        if value:
            self.song().start_playing()
            self.song().current_song_time = self.restart_position

    # Capture
    def set_capture(self, button):
        self._capture_button = button
        self._capture_value.subject = button
        self._on_capture_changed.subject = self.song()
        self._on_capture_changed()

    @subject_slot('value')
    def _capture_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self._song.capture_midi()

    @subject_slot('can_capture_midi')
    def _on_capture_changed(self):
        if self._capture_button is not None:
            color = 100 if self.song().can_capture_midi else 0
            self._capture_button.send_value(color, force=True)

    # Re-Enable Automation
    def set_re_enable_automation_button(self, button):
        self._re_enable_automation_button = button
        self._re_enable_automation_button_value.subject = button
        self._on_re_enable_automation_changed.subject = self.song()
        self._on_re_enable_automation_changed()

    @subject_slot('value')
    def _re_enable_automation_button_value(self, value):
        if value:
            self.song().re_enable_automation()

    @subject_slot('re_enable_automation_enabled')
    def _on_re_enable_automation_changed(self):
        if self._re_enable_automation_button is not None:
            color = 0 if self.song().re_enable_automation_enabled == 0 else 15
            self._re_enable_automation_button.send_value(color, force=True)

    # Punch In
    def set_punch_in_button(self, button):
        self._punch_in_button = button
        self._punch_in_button_value.subject = button
        self._on_punch_in_changed.subject = self.song()
        self._on_punch_in_changed()

    @subject_slot('value')
    def _punch_in_button_value(self, value):
        if value:
            self.song().punch_in = 1 if self.song().punch_in == 0 else 0

    @subject_slot('punch_in')
    def _on_punch_in_changed(self):
        if self.is_enabled() and self._punch_in_button:
            color = 0
            if self.song().punch_in:
                color = 81
            self._punch_in_button.send_value(color, force=True)

    # Punch Out
    def set_punch_out_button(self, button):
        self._punch_out_button = button
        self._punch_out_button_value.subject = button
        self._on_punch_out_changed.subject = self.song()
        self._on_punch_out_changed()

    @subject_slot('value')
    def _punch_out_button_value(self, value):
        if value:
            self.song().punch_out = 1 if self.song().punch_out == 0 else 0

    @subject_slot('punch_out')
    def _on_punch_out_changed(self):
        if self.is_enabled() and self._punch_out_button:
            color = 0
            if self.song().punch_out:
                color = 81
            self._punch_out_button.send_value(color, force=True)

    # Groove Amount
    def set_groove_amount(self, button):
        self.groove_amount = button
        self.groove_amount_value.subject = button

    @subject_slot('value')
    def groove_amount_value(self, value):
        self.song().groove_amount = value/127*1.3
        self.parent.set_temp_message(str(int(self.song().groove_amount*100+1))+ "%")

    # Jump to start
    def set_jump_to_start(self, button):
        self._jump_to_start_button = button
        self._jump_to_start_button_value.subject = button

    @subject_slot('value')
    def _jump_to_start_button_value(self, value):
        self.song().jump_by(-self.song().current_song_time)
        self.song().current_song_time = 0

    # Metronome
    def set_metronome(self, button):
        self._metronome_button = button
        self._on_metronome_button.subject = button
        self._on_metronome_changed.subject = self.song()
        self._on_metronome_changed()

    @subject_slot(u'value')
    def _on_metronome_button(self, value):
        if value:
            self.song().metronome = 0 if self.song().metronome else 1

    @subject_slot('metronome')
    def _on_metronome_changed(self):
        if self.is_enabled() and self._metronome_button:
            channel = 15
            if self.song().metronome:
                self.metro_color = 80
            else:
                self.metro_color = 81
            if Options.metronome_blinking:
                channel = 14
            self._metronome_button.send_value(self.metro_color, channel=channel, force=True)

    # Arrangement Loop
    def set_loop_button(self, button):
        self._loop_button = button
        self._on_loop_button.subject = button
        self._on_loop_changed.subject = self.song()
        self._on_loop_changed()

    @subject_slot(u'value')
    def _on_loop_button(self, value):
        if value:
            self.song().loop = 0 if self.song().loop else 1

    @subject_slot('loop')
    def _on_loop_changed(self):
        if self.is_enabled() and self._loop_button:
            if self.song().loop:
                color = 2
            else:
                color = 0
            self._loop_button.send_value(color, force=True)

    # Loop Position
    def set_loop_position(self, button):
        self._loop_position_button = button
        self._on_loop_position_button.subject = button

    @subject_slot(u'value')
    def _on_loop_position_button(self, value):
        if value > 64:
            self.song().loop_start += 4
        if value < 64:
            try:
                self.song().loop_start -= 4
            except:
                pass
        self._loop_position_button.send_value(64, force=True)

    # Loop Length
    def set_loop_length(self, button):
        self._loop_length_button = button
        self._on_loop_length_button.subject = button

    @subject_slot(u'value')
    def _on_loop_length_button(self, value):
        if value > 64:
            self.song().loop_length += 4
        if value < 64:
            try:
                self.song().loop_length -= 4
            except:
                pass
        self._loop_length_button.send_value(64, force=True)

    # Continue Playing
    def set_continue_playing(self, button):
        self._continue_playing_button = button
        self._on_continue_playing_button.subject = button

    @subject_slot(u'value')
    def _on_continue_playing_button(self, value):
        if value:
            if self.song().is_playing:
                self.song().stop_playing()
            else:
                self.song().continue_playing()

    # Arrangement Record
    def set_record_button(self, button):
        self._record_button = button
        self._on_record_button.subject = button
        self._on_record_changed.subject = self.song()
        self._on_record_changed()

    @subject_slot(u'value')
    def _on_record_button(self, value):
        if value:
            self.song().record_mode = 0 if self.song().record_mode else 1

    @subject_slot('record_mode')
    def _on_record_changed(self):
        if self.is_enabled() and self._record_button:
            if self.song().record_mode:
                color = 127
            else:
                color = 0
            self._record_button.send_value(color, force=True)

    # Session Record
    def set_session_record_button(self, button):
        self._session_record_button = button
        self._on_session_record_button.subject = button
        self._on_session_record_changed.subject = self.song()
        self._on_session_record_changed()

    @subject_slot(u'value')
    def _on_session_record_button(self, value):
        if value:
            self.song().session_record = 0 if self.song().session_record else 1

    @subject_slot('session_record')
    def _on_session_record_changed(self):
        if self.is_enabled() and self._session_record_button:
            color = 0
            if self.song().session_record:
                color = 127
            self._session_record_button.send_value(color, channel=14, force=True)

    # Skip Forward/Backward
    def set_skip(self, button):
        self._skip_button = button
        self._on_skip_button.subject = button

    @subject_slot(u'value')
    def _on_skip_button(self, value):
        if value > 64:
            self._song.current_song_time += 4
        if value < 64:
            try:
                self._song.current_song_time -= 4
            except:
                pass
        self._skip_button.send_value(64, force=True)

    # Horizontal Zoom
    def set_h_zoom(self, button):
        self._h_zoom_button = button
        self._on_h_zoom_changed.subject = button

    @subject_slot(u'value')
    def _on_h_zoom_changed(self, value):
        if value < 64:
            self.application().view.zoom_view(2, "", True)
        if value > 64:
            self.application().view.zoom_view(3, "", True)
        self._h_zoom_button.send_value(64, force=True)

    # Set BPM
    def set_inc_dec_bpm_button(self, button):
        self._inc_dec_bpm_button = button
        self._on_inc_dec_bpm_changed.subject = button

    @subject_slot(u'value')
    def _on_inc_dec_bpm_changed(self, value):
        if value < 64:
            self._on_dec_bpm_changed(1)
        if value > 64:
            self._on_inc_bpm_changed(1)
        self._inc_dec_bpm_button.send_value(64, force=True)

    def set_inc_bpm_button(self, button):
        self._inc_bpm_button = button
        self._on_inc_bpm_changed.subject = button

    @subject_slot(u'value')
    def _on_inc_bpm_changed(self, value):
        if self._inc_bpm_button != None and value:
            self.song().tempo += 1
            self.parent.set_temp_message(str(self.song().tempo)+ " BPM")

    def set_dec_bpm_button(self, button):
        self._dec_bpm_button = button
        self._on_dec_bpm_changed.subject = button

    @subject_slot(u'value')
    def _on_dec_bpm_changed(self, value):
        if self._dec_bpm_button != None and value:
            self.song().tempo -= 1
            self.parent.set_temp_message(str(self.song().tempo)+ " BPM")

    # Back To Arrangement
    def set_back_to_arrangement_button(self, button):
        self._back_to_arrangement_button = button
        self._back_to_arrangement_button_value.subject = button
        self._on_back_to_arrangement_changed.subject = self.song()
        self._on_back_to_arrangement_changed()

    @subject_slot('value')
    def _back_to_arrangement_button_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.song().back_to_arranger = 0

    @subject_slot('back_to_arranger')
    def _on_back_to_arrangement_changed(self):
        if self._back_to_arrangement_button is not None:
            color = 0 if self.song().back_to_arranger == 0 else 2
            self._back_to_arrangement_button.send_value(color, force=True)

    # MIDI Record Quantization
    def set_midi_recording_quantization_button(self, button):
        self._midi_recording_quantization_button = button
        self._midi_recording_quantization_button_value.subject = button
        self.temp_midi_rec_q = Live.Song.RecordingQuantization.rec_q_sixtenth
        self._on_midi_recording_quantization_changed.subject = self.song()
        self._on_midi_recording_quantization_changed()

    @subject_slot('value')
    def _midi_recording_quantization_button_value(self, value):
        if self.is_enabled():
            if value is not 0:
                if self.midi_recording_quantization is not Live.Song.RecordingQuantization.rec_q_no_q:
                    self.temp_midi_rec_q = self.midi_recording_quantization
                self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q if self.song().midi_recording_quantization is not Live.Song.RecordingQuantization.rec_q_no_q else self.temp_midi_rec_q

    @subject_slot('midi_recording_quantization')
    def _on_midi_recording_quantization_changed(self):
        if self._midi_recording_quantization_button is not None:
            self.midi_recording_quantization = self.song().midi_recording_quantization
            color = 0 if self.midi_recording_quantization == Live.Song.RecordingQuantization.rec_q_no_q else 126       
            self._midi_recording_quantization_button.send_value(color, force=True)

   # Set/Delete Marker
    def set_set_or_delete_cue_button(self, button):
        self._set_or_delete_cue_button = button
        self._on_set_or_delete_cue.subject = button
        self._on_cue_points_changed.subject = self.song()
        self._on_cue_points_changed()
        self.compare_cue()

    @subject_slot(u'value')
    def _on_set_or_delete_cue(self, value):
        if value:
            self.song().set_or_delete_cue()

    @subject_slot('cue_points')
    def _on_cue_points_changed(self): 
        self.compare_cue()

    def compare_cue(self):
        beat = int(self.song().current_song_time)
        highest_cue = 0
        for cue_point in self.song().cue_points:
            if cue_point.time <= beat and not self.check_hide(cue_point.name):
                if cue_point.time > highest_cue:
                    highest_cue = cue_point.time
                    self.selected_cue = cue_point
        if self.selected_cue is not None and self.prev_cue is not self.selected_cue:
            self.parent.display_message("Left Marker Name", self.selected_cue.name)
            if self.prev_cue:
                self.prev_cue.remove_name_listener(self._on_name_changed)
            self.prev_cue = self.selected_cue
            self.prev_cue.add_name_listener(self._on_name_changed)

    # Next/Prev Marker
    def set_prev_next_cue_button(self, button):
        self._prev_next_cue_button = button
        self._on_jump_to_prev_next_cue.subject = button

    def set_prev_cue_button(self, button):
        self._prev_cue_button = button
        self._on_jump_to_prev_cue.subject = button

    @subject_slot(u'value')
    def _on_jump_to_prev_cue(self, value):
        if value:
            if self.song().can_jump_to_prev_cue:
                self.song().jump_to_prev_cue()

    def set_next_cue_button(self, button):
        self._next_cue_button = button
        self._on_jump_to_next_cue.subject = button

    @subject_slot(u'value')
    def _on_jump_to_next_cue(self, value):
        if value:
            if self.song().can_jump_to_next_cue:
                self.song().jump_to_next_cue()

    @subject_slot(u'value')
    def _on_jump_to_prev_next_cue(self, value):
        if value < 64:
            self._on_jump_to_prev_cue(1)
        if value > 64:
            self._on_jump_to_next_cue(1)
        self._prev_next_cue_button.send_value(64, force=True)

    # Marker Loop
    def set_marker_loop_button(self, button):
        self._marker_loop_button = button
        self._on_marker_loop_changed.subject = button

    @subject_slot(u'value')
    def _on_marker_loop_changed(self, value):
        index = list(self.song().cue_points).index(self.prev_cue)
        if value:
            next_cue_time = self.song().cue_points[index+1].time
            self.song().loop = 1
            self.song().loop_start = self.prev_cue.time
            self.song().loop_length = next_cue_time - self.prev_cue.time
    
    # Marker name
    def _on_name_changed(self):
        if self.prev_cue:
            name = self.prev_cue.name
            if len(name) == 0:
                name = 'No Name'
            self.parent.display_message("Left Marker Name", name)
        else:
            self.parent.display_message("Left Marker Name", "No Marker")
        self._session.scan_setlist()

    def check_stop(self, name):
        num1 = name.find("(STOP)")
        res = True if num1 > -1 else False
        return (res)

    def check_hide(self, name):
        num1 = name.find("(HIDE)")
        res = True if num1 > -1 else False
        return (res)

    def update(self):
        self._on_start_stop_changed()
        self._on_metronome_changed()
        self._on_name_changed()
        self._on_loop_changed()
        self._on_record_changed()
        self._on_session_record_changed()
        self._on_punch_in_changed()
        self._on_punch_out_changed()
        self._on_back_to_arrangement_changed()
        self._on_midi_recording_quantization_changed()
        super(TransportComponent, self).update()
