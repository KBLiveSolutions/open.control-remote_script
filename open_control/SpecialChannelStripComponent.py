# from builtins import zip
# from builtins import str
# from builtins import range
from _Framework.ChannelStripComponent import ChannelStripComponent as ChannelStripBase
from _Framework.SubjectSlot import subject_slot
from itertools import chain
import math

import logging, traceback
logger = logging.getLogger(__name__)
# def print(text):
#     logger.warning(text)

class ChannelStripComponent(ChannelStripBase):
    def __init__(self, *a, **k):
        self.empty_color = 43
        super(ChannelStripComponent, self).__init__(*a, **k)
        self.is_private = True
        self._name_controls = None
        self._mute_button_led = None
        self._arm_button_led = None
        self._input_level_control = None
        self._output_level_control = None

    def disconnect(self):
        super(ChannelStripComponent, self).disconnect()
        self._rgb_controls = None
        self._name_controls = None

    def set_name_controls(self, name):
        self._name_controls = name
        self.update()

    def set_mute_button(self, button):
        self._mute_button_led = button
        super(ChannelStripComponent, self).set_mute_button(button)
        # self.update()

    def set_input_level(self, button):
        self._input_level_control = button
        # self.update()

    def set_output_level(self, button):
        self._output_level_control = button
        # self.update()

    def _on_mute_changed(self):
        if self.is_enabled() and self._mute_button_led != None:
            if self._track != None or self.empty_color == None:
                if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute != self._invert_mute_feedback:
                    self._mute_button_led.send_value(81, force=True)
                else:
                    self._mute_button_led.send_value(80, force=True)
            else:
                self._mute_button_led.send_value(80, force=True)
        return

    def _on_solo_changed(self):
        if self.is_enabled() and self._solo_button != None:
            if self._track != None or self.empty_color == None:
                if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
                    self._solo_button.send_value(23, force=True)
                else:
                    self._solo_button.turn_off()
            else:
                self._solo_button.set_light(43)


    def set_arm_button(self, button):
        self._arm_button_led = button
        super(ChannelStripComponent, self).set_arm_button(button)
        # self.update()

    def _on_arm_changed(self):
        if self.is_enabled() and self._arm_button_led != None:
            if self._track != None or self.empty_color == None:
                if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
                    self._arm_button_led.send_value(127, force=True)
                else:
                    self._arm_button_led.send_value(0, force=True)
            else:
                self._arm_button_led.send_value(0, force=True)
        return

    def set_trigger_session_record(self, button):
        self._trigger_session_record_button = button
        self._on_trigger_session_record_value.subject = button
        self._song.trigger_session_record()

    @subject_slot('value')
    def _on_trigger_session_record_value(self, value):
        if self.is_enabled():
            if value is not 0 or not self._trigger_session_record_button.is_momentary():
                self.song().trigger_session_record()

    def update(self):
        super(ChannelStripComponent, self).update()
        self._on_track_name_changed()
        self._on_arm_changed()
        # self.set_output_level_listener()

    def set_input_level_listener(self):
        try:
            self._track.add_input_meter_level_listener(self._on_input_level_changed)
        except:
            pass

    def _on_input_level_changed(self):
        if self.is_enabled() and self._input_level_control:
            leveldb = (self._track.input_meter_level)**3
            level = int(leveldb*127)
            
    def set_output_level_listener(self):
        try:
            self._track.add_output_meter_level_listener(self._on_output_level_changed)
        except:
            pass

    def _on_output_level_changed(self):
        if self.is_enabled() and self._output_level_control:
            leveldb = (self._track.output_meter_level)**3
            level = int(leveldb*127)
 
    @subject_slot('name')
    def _on_track_name_changed(self):
        if self.is_enabled() and self._name_controls:
            self._send_sysex_for_name(self._track.name if self._track else '')
           
    def _send_sysex_for_name(self, name):
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 51, 1, _len]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        self._name_controls._send_midi(tuple(message))
        self._arm_button_led.send_value(12, force=True)