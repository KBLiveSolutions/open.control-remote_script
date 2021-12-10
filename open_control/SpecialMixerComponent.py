from __future__ import absolute_import
from itertools import count
from _Framework.SubjectSlot import subject_slot
import time

from _Framework.MixerComponent import MixerComponent as MixerBase
from _Framework.SubjectSlot import subject_slot_group

from .SpecialChannelStripComponent import ChannelStripComponent

import logging, traceback
logger = logging.getLogger(__name__)
# def print(text):
#     logger.warning(text)

class MixerComponent(MixerBase):
    """ MixerComponent extends the standard to use a custom SceneComponent, use custom
    ring handling and observe the status of scenes. """

    channel_strip_component_type = ChannelStripComponent

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(*a, **k)
        self._rgb_controls = None
        self._name_controls = None
        self.last_message_time = 0

    def disconnect(self):
        super(MixerComponent, self).disconnect()

    def _create_strip(self):
        return ChannelStripComponent()

    def update(self):
        super(MixerComponent, self).update()

    def on_track_list_changed(self):
        # self._setup_track_listeners()
        super(MixerComponent, self).on_track_list_changed()
    
    def set_master_volume(self, button):
        self.master_volume_button = button
        self.master_strip().set_volume_control(button)
        self._master_volume_value.subject = button

    def set_volume(self, button):
        self.selected_strip().set_volume_control(button)
        self._volume_value.subject = button

    def set_pan(self, button):
        self.selected_strip().set_pan_control(button)
        self._pan_value.subject = button

    @subject_slot('value')
    def _master_volume_value(self, value):
        volume = self.song().master_track.mixer_device.volume
        self._send_direct_sysex_for_name(str(volume))

    def set_send_controls(self, buttons):
        self.selected_strip().set_send_controls(buttons)
        self._send_controls_value.subject = buttons

    @subject_slot('value')
    def _send_controls_value(self, *args):
        sends = self.song().view.selected_track.mixer_device.sends[args[1]]
        self._send_direct_sysex_for_name(str(sends))

    @subject_slot('value')
    def _volume_value(self, value):
        volume = self.song().view.selected_track.mixer_device.volume
        self._send_direct_sysex_for_name(str(volume))

    @subject_slot('value')
    def _pan_value(self, value):
        panning = self.song().view.selected_track.mixer_device.panning
        self._send_direct_sysex_for_name(str(panning))

    def _send_direct_sysex_for_name(self, name):
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 54, 3, _len]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self.master_volume_button and time.time() - self.last_message_time > 0.05  :
            self.master_volume_button._send_midi(tuple(message))
            self.last_message_time = time.time()

