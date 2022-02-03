from __future__ import absolute_import
from _Framework.SubjectSlot import subject_slot
from . import Options

from _Framework.MixerComponent import MixerComponent as MixerBase

class MixerComponent(MixerBase):
    """ MixerComponent extends the standard to use a custom SceneComponent, use custom
    ring handling and observe the status of scenes. """

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(*a, **k)
    
    def set_parent(self, parent):
        self.parent = parent

    def disconnect(self):
        super(MixerComponent, self).disconnect()

    def update(self):
        super(MixerComponent, self).update()

    def on_track_list_changed(self):
        # self._setup_track_listeners()
        super(MixerComponent, self).on_track_list_changed()
    
    # Master Volume
    def set_master_volume(self, button):
        self.master_volume_button = button
        self.master_strip().set_volume_control(button)
        self._master_volume_value.subject = button

    @subject_slot('value')
    def _master_volume_value(self, value):
        volume = self.song().master_track.mixer_device.volume
        self.parent.set_temp_message(self.slice_dB(str(volume)))

    # Cue Volume
    def set_prehear_volume(self, button):
        self.prehear_volume_button = button
        self.set_prehear_volume_control(button)
        self._prehear_volume_value.subject = button

    @subject_slot('value')
    def _prehear_volume_value(self, value):
        volume = self.song().master_track.mixer_device.cue_volume
        self.parent.set_temp_message(self.slice_dB(str(volume)))

    # Track Volume
    @subject_slot('value')
    def _volume_value(self, value):
        volume = self._selected_strip._track.mixer_device.volume
        self.parent.set_temp_message(self.slice_dB(str(volume)))

    def set_volume(self, button):
        self.selected_strip().set_volume_control(button)
        self._volume_value.subject = button

    # Track Panning
    def set_pan(self, button):
        self.selected_strip().set_pan_control(button)
        self._pan_value.subject = button

    @subject_slot('value')
    def _pan_value(self, value):
        panning = self._selected_strip._track.mixer_device.panning
        self.parent.set_temp_message(str(panning))

    # Track Sends
    def set_send_controls(self, buttons):
        self.selected_strip().set_send_controls(buttons)
        self._send_controls_value.subject = buttons

    @subject_slot('value')
    def _send_controls_value(self, *args):
        sends = self._selected_strip._track.mixer_device.sends[args[1]]
        self.parent.set_temp_message(self.slice_dB(str(sends)))

    def slice_dB(self, value):
        remove_db = str(round(float(value[:len(value)-2]), 1)) + "dB"
        return remove_db