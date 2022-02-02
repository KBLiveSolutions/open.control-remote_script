from _Framework.ChannelStripComponent import ChannelStripComponent as ChannelStripBase
from _Framework.SubjectSlot import subject_slot
from itertools import chain


class ChannelStripComponent(ChannelStripBase):
    def __init__(self, *a, **k):
        self.empty_color = 43
        super(ChannelStripComponent, self).__init__(*a, **k)
        self.is_private = True
        # self._name_controls = None
        self._mute_button_led = None
        self._arm_button_led = None

    def disconnect(self):
        super(ChannelStripComponent, self).disconnect()
        self._rgb_controls = None
        self._name_controls = None

    # def set_name_controls(self, name):
    #     self._name_controls = name
    #     self.update()

    def set_mute_button(self, button):
        self._mute_button_led = button
        super(ChannelStripComponent, self).set_mute_button(button)

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

    def update(self):
        super(ChannelStripComponent, self).update()
        self._on_track_name_changed()
        self._on_arm_changed()
 
    # @subject_slot('name')
    # def _on_track_name_changed(self):
    #     if self.is_enabled() and self._name_controls:
    #         self._send_sysex_for_name(self._track.name if self._track else '')
           
    # def _send_sysex_for_name(self, name):
    #     _len = min(len(name), 32)
    #     message = [240, 122, 29, 1, 19, 51, 1]
    #     for i in range(_len):
    #         if 0 <= ord(name[i])-32 <= 94:
    #             message.append(ord(name[i])-32)
    #         else:
    #             message.append(95)
    #     message.append(247)    
    #     self._name_controls._send_midi(tuple(message))