import Live
# from builtins import str
from _Framework.TransportComponent import TransportComponent as TransportBase
from _Framework.SubjectSlot import subject_slot
from _Framework.ControlSurface import ControlSurface
from . import Options

import logging, traceback
logger = logging.getLogger(__name__)
# def print(text):
#     logger.warning(text)

class TransportComponent(TransportBase):
    def __init__(self, *a, **k):
        self._name_controls = None
        self._metronome_button = None
        self._start_stop_button = None
        self._loop_button = None
        self._record_button = None
        self._restart_button = None   
        self._session_record_button = None
        self._jump_to_start_button = None
        self._punch_in_button = None
        self._punch_out_button = None
        self.prev_beat = False
        self._inc_bpm_button = None
        self._dec_bpm_button = None
        self._back_to_arrangement_button = None
        self._midi_recording_quantization_button = None
        self._set_or_delete_cue_button = None
        self.prev_cue = None
        self.selected_cue = None
        self.groove_amount = None
        self.temp_midi_rec_q = Live.Song.RecordingQuantization.rec_q_sixtenth
        self.previous_quarter = 0

        super(TransportComponent, self).__init__(*a, **k)
        self._setup_transport_listeners()
        self.compare_cue(int(self.song().current_song_time))
        self.restart_position = self.song().current_song_time

    def disconnect(self):
        super(TransportComponent, self).disconnect()
        
    def set_name_controls(self, name):
        self._name_controls = name
        self.update()

    def set_start_stop(self, button):
        self._start_stop_button = button
        self._start_stop_button_value.subject = button
        self.update()

    def set_restart_button(self, button):
        self._restart_button = button
        self._restart_button_value.subject = button

    def set_punch_in_button(self, button):
        self._punch_in_button = button
        self._punch_in_button_value.subject = button

    def set_punch_out_button(self, button):
        self._punch_out_button = button
        self._punch_out_button_value.subject = button

    def set_re_enable_automation_button(self, button):
        self._re_enable_automation_button = button
        self._re_enable_automation_button_value.subject = button

    @subject_slot('value')
    def _re_enable_automation_button_value(self, value):
        if value:
            self.song().re_enable_automation()

    @subject_slot('value')
    def _punch_in_button_value(self, value):
        if value:
            self.song().punch_in = 1 if self.song().punch_in == 0 else 0

    @subject_slot('value')
    def _punch_out_button_value(self, value):
        if value:
            self.song().punch_out = 1 if self.song().punch_out == 0 else 0

    @subject_slot('value')
    def _restart_button_value(self, value):
        if value:
            self.song().start_playing()
            self.song().current_song_time = self.restart_position

    def set_groove_amount(self, button):
        self.groove_amount = button
        self.groove_amount_value.subject = button

    @subject_slot('value')
    def groove_amount_value(self, value):
        self.song().groove_amount = value/127*1.3

    def set_jump_to_start(self, button):
        self._jump_to_start_button = button
        self._jump_to_start_button_value.subject = button

    @subject_slot('value')
    def _jump_to_start_button_value(self, value):
        self.song().jump_by(-self.song().current_song_time)
        self.song().current_song_time = 0

    @subject_slot('value')
    def _start_stop_button_value(self, value):
        if self.is_enabled() and self._start_stop_button:
            if value:
                self.song().stop_playing() if self.song().is_playing else self.song().start_playing()

    def set_metronome(self, button):
        self._metronome_button = button
        self._on_metronome_button.subject = button
        # self.update()

    @subject_slot(u'value')
    def _on_metronome_button(self, value):
        if value:
            self.song().metronome = 0 if self.song().metronome else 1

    def set_loop_button(self, button):
        self._loop_button = button
        self._on_loop_button.subject = button

    @subject_slot(u'value')
    def _on_loop_button(self, value):
        if value:
            self.song().loop = 0 if self.song().loop else 1

    def set_record_button(self, button):
        self._record_button = button
        self._on_record_button.subject = button
        # self.update()

    @subject_slot(u'value')
    def _on_record_button(self, value):
        if value:
            self.song().record_mode = 0 if self.song().record_mode else 1

    def set_session_record_button(self, button):
        self._session_record_button = button
        self._on_session_record_button.subject = button
        self.update()

    @subject_slot(u'value')
    def _on_session_record_button(self, value):
        if value:
            self.song().session_record = 0 if self.song().session_record else 1

    def set_set_or_delete_cue_button(self, button):
        self._set_or_delete_cue_button = button
        self._on_set_or_delete_cue.subject = button

    @subject_slot(u'value')
    def _on_set_or_delete_cue(self, value):
        if value:
            self.song().set_or_delete_cue()

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

    def set_inc_bpm_button(self, button):
        self._inc_bpm_button = button
        self._on_inc_bpm_changed.subject = button

    @subject_slot(u'value')
    def _on_inc_bpm_changed(self, value):
        if self._inc_bpm_button != None and value:
            self.song().tempo += 1

    def set_dec_bpm_button(self, button):
        self._dec_bpm_button = button
        self._on_dec_bpm_changed.subject = button

    @subject_slot(u'value')
    def _on_dec_bpm_changed(self, value):
        if self._dec_bpm_button != None and value:
            self.song().tempo -= 1

    def set_back_to_arrangement_button(self, button):
        self._back_to_arrangement_button = button
        self._back_to_arrangement_button_value.subject = button

    @subject_slot('value')
    def _back_to_arrangement_button_value(self, value):
        if self.is_enabled():
            if value is not 0:
                self.song().back_to_arranger = 0

    def set_midi_recording_quantization_button(self, button):
        self._midi_recording_quantization_button = button
        self._midi_recording_quantization_button_value.subject = button

    @subject_slot('value')
    def _midi_recording_quantization_button_value(self, value):
        if self.is_enabled():
            if value is not 0:
                if self.midi_recording_quantization is not Live.Song.RecordingQuantization.rec_q_no_q:
                    self.temp_midi_rec_q = self.midi_recording_quantization
                self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q if self.song().midi_recording_quantization is not Live.Song.RecordingQuantization.rec_q_no_q else self.temp_midi_rec_q
                
    def update(self):
        super(TransportComponent, self).update()
        self._on_metronome_changed()
        self._on_start_stop_changed()
        self._on_name_changed()
        self._on_loop_changed()
        self._on_record_changed()
        self._on_session_record_changed()
        self._on_punch_in_changed()
        self._on_punch_out_changed()
        self._on_back_to_arrangement_changed()
        self._on_midi_recording_quantization_changed()

    def _setup_transport_listeners(self):
        self.song().add_current_song_time_listener(self.on_time_change)
        self._on_start_stop_changed.subject = self.song()
        self._on_loop_changed.subject = self.song()
        self._on_metronome_changed.subject = self.song()
        self._on_record_changed.subject = self.song()
        self._on_session_record_changed.subject = self.song()
        self._on_cue_points_changed.subject = self.song()
        self._on_punch_in_changed.subject = self.song()
        self._on_punch_out_changed.subject = self.song()
        self._on_re_enable_automation_changed.subject = self.song()
        self._on_back_to_arrangement_changed.subject = self.song()
        self._on_midi_recording_quantization_changed.subject = self.song()

        # self._on_can_jump_to_next_cue_changed.subject = self.song()
        # self._on_can_jump_to_prev_cue_changed.subject = self.song()

    @subject_slot('midi_recording_quantization')
    def _on_midi_recording_quantization_changed(self):
        if self._midi_recording_quantization_button is not None:
            self.midi_recording_quantization = self.song().midi_recording_quantization
            color = 0 if self.midi_recording_quantization == Live.Song.RecordingQuantization.rec_q_no_q else 126       
            self._midi_recording_quantization_button.send_value(color, force=True)

    @subject_slot('back_to_arranger')
    def _on_back_to_arrangement_changed(self):
        if self._back_to_arrangement_button is not None:
            color = 0 if self.song().back_to_arranger == 0 else 2
            self._back_to_arrangement_button.send_value(color, force=True)

    @subject_slot('re_enable_automation_enabled')
    def _on_re_enable_automation_changed(self):
        if self._re_enable_automation_button is not None:
            color = 0 if self.song().re_enable_automation_enabled == 0 else 15
            self._re_enable_automation_button.send_value(color, force=True)

    @subject_slot('cue_points')
    def _on_cue_points_changed(self): 
        self.on_time_change()

    @subject_slot('is_playing')
    def _on_start_stop_changed(self):
        if self.is_enabled() and self._start_stop_button and self._metronome_button:
            if self.song().is_playing:
                self.restart_position = self._song.current_song_time
                color = 65
            else:
                color = 0
            self._start_stop_button.send_value(color, force=True)

    @subject_slot('session_record')
    def _on_session_record_changed(self):
        if self.is_enabled() and self._session_record_button:
            color = 0
            if self.song().session_record:
                color = 127
            self._session_record_button.send_value(color, channel=14, force=True)

    @subject_slot('punch_in')
    def _on_punch_in_changed(self):
        if self.is_enabled() and self._punch_in_button:
            color = 0
            if self.song().punch_in:
                color = 81
            self._punch_in_button.send_value(color, force=True)

    @subject_slot('punch_out')
    def _on_punch_out_changed(self):
        if self.is_enabled() and self._punch_out_button:
            color = 0
            if self.song().punch_out:
                color = 81
            self._punch_out_button.send_value(color, force=True)

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

    @subject_slot('loop')
    def _on_loop_changed(self):
        if self.is_enabled() and self._loop_button:
            if self.song().loop:
                color = 2
            else:
                color = 0
            self._loop_button.send_value(color, force=True)

    @subject_slot('record_mode')
    def _on_record_changed(self):
        if self.is_enabled() and self._record_button:
            if self.song().record_mode:
                color = 127
            else:
                color = 0
            self._record_button.send_value(color, force=True)

    def on_time_change(self):
        self.compare_cue(int(self.song().current_song_time))
        # time = self.song().get_current_beats_song_time()
        # quarter = time.sub_division
        # if int(self.song().current_song_time) is not self.prev_beat:
        #     self.compare_cue(int(self.song().current_song_time))
        #     self.prev_beat = int(self.song().current_song_time)
        # if quarter is not self.previous_quarter and self._start_stop_button:
        #     message = [240, 122, 29, 1, 19, 21, 38, 44, quarter]
        #     self._start_stop_button._send_midi(tuple(message))
        #     self.previous_quarter = quarter

    def compare_cue(self, beat):
        for cue_point in reversed(self.song().cue_points):
            if cue_point.time <= beat:
                self.selected_cue = cue_point
                if self.check_stop(self.selected_cue.name):
                    self.song().stop_playing()
                    self.selected_cue.jump()
                break
        if self.selected_cue and self.prev_cue != self.selected_cue:
            self._send_sysex_for_name(self.selected_cue.name)
            if self.prev_cue:
                self.prev_cue.remove_name_listener(self._on_name_changed)
            self.prev_cue = self.selected_cue
            self.prev_cue.add_name_listener(self._on_name_changed)

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

    def _on_name_changed(self):
        if self.prev_cue:
            self._send_sysex_for_name(self.prev_cue.name)
        else:
            self._send_sysex_for_name("No Marker")

    def check_stop(self, name):
        num1 = name.find("(STOP)")
        res = True if num1 > -1 else False
        return (res)

    def _send_sysex_for_name(self, name):
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 21, 4, _len]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self._name_controls:
            self._name_controls._send_midi(tuple(message))