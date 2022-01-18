# from builtins import zip
# from builtins import str
# from builtins import range
import Live
from _Framework.DeviceComponent import DeviceComponent as DeviceBase
from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement import ButtonElement

MIDI_CHANNEL = 15
state_color = {0: 122, 1: 127, 2: 126, 3: 125}

import logging, traceback
logger = logging.getLogger(__name__)
# def print(text):
#     logger.warning(text)

class LooperComponent(DeviceBase):

    def __init__(self, *a, **k):
        self._name_controls = None
        self.looper_state_button = None
        self.sel_prev_looper_button = None
        self.sel_next_looper_button = None
        self.sel_current_looper_button = None
        self.arm_looper_track_button = None
        self.mute_looper_track_button = None
        self.first_device_parameters = None
        self.set_stop_looper_button = None
        self.set_clear_all_button = None
        self._color_buttons = [None, None]
        self._active_looper_number = 0
        self._6_looper_buttons = None
        super(LooperComponent, self).__init__(*a, **k)
        self.song().add_tracks_listener(self.build_loopers_list)
        self.song().view.add_selected_track_listener(self.on_selected_track_changed)
        self.build_loopers_list()

    def set_name_controls(self, name):
        self._name_controls = name
        self.update()

    def set_looper_colors(self, buttons):
        self._color_buttons = buttons

    def set_add_looper(self, button):
        self.add_looper_button = button
        self.add_looper_button_value.subject = button

    def set_looper_buttons(self, buttons):
        self._6_looper_buttons = buttons
        
    @subject_slot('value')
    def add_looper_button_value(self, value):
        if value:
            if self._device.class_display_name == "Looper" and self._get_looper_number(self._device) < 1:
                # self._song.view.select_device(self._device)
                name = self._device.name
                num = min(self.looper_list.keys()) if len(self.looper_list) else 1
                while num in list(self.looper_list.keys()): num += 1
                new_name = name + " (LOOPER%s)" % str(num)
                self._device.name = new_name.replace("  ", " ")
            else:
                self._song.view.select_device(self.looper_list[self._active_looper_number])

    def set_arm_looper_track(self, button):
        self.arm_looper_track_button = button
        self.arm_looper_track_button_value.subject = button

    @subject_slot('value')
    def arm_looper_track_button_value(self, value):
        if value:
            if self.song().exclusive_arm:
                arm = self._parent_track.arm
                for track in self.song().tracks:
                    track.arm = False
                self._parent_track.arm = True if arm == False else False
            else:
                self._parent_track.arm = True if self._parent_track.arm == False else False

    def set_mute_looper_track(self, button):
        self.mute_looper_track_button = button
        self.mute_looper_track_button_value.subject = button

    @subject_slot('value')
    def mute_looper_track_button_value(self, value):
        if value:
            self._parent_track.mute = not (self._parent_track.mute)

    def set_stop_looper(self, button):
        self.set_stop_looper_button = button
        self.set_stop_looper_button_value.subject = button

    @subject_slot('value')
    def set_stop_looper_button_value(self, value):
        if value:
            self.looper_list[self._active_looper_number].parameters[1].value = 0

    def set_clear_all(self, button):
        self.set_clear_all_button = button
        self.set_clear_all_button_value.subject = button

    @subject_slot('value')
    def set_clear_all_button_value(self, value):
        if value:
            for num in range(len(self.looper_list)):
                self.looper_buttons_list[num+1]._send_midi((240, 122, 29, 1, 19, 53, num+24, 0, 15, 247))

    def set_sel_prev_looper(self, button):
        self.sel_prev_looper_button = button
        self._color_buttons[0] = button
        self.sel_prev_looper_button_value.subject = button

    def set_sel_current_looper(self, button):
        self.sel_current_looper_button = button

    def set_looper_stop(self, button):
        self.looper_stop_button = button
        self.looper_stop_button_value.subject = button

    @subject_slot('value')
    def looper_stop_button_value(self, value):
        if value and self._active_looper_number != 0:
            self.looper_list[self._active_looper_number].parameters[1].value = 0
            # self.update()

    @subject_slot('value')
    def sel_prev_looper_button_value(self, value):
        if value and self._active_looper_number != 0:
            self._active_looper_number = self.find_previous_looper_number()
            self.update()

    def find_previous_looper_number(self):
        temp = list(self.looper_list.keys())
        index = temp.index(self._active_looper_number)
        return temp[index-1]

    def set_sel_next_looper(self, button):
        self.sel_next_looper_button = button
        self._color_buttons[1] = button
        self.sel_next_looper_button_value.subject = button

    def set_show_looper(self, button):
        self.show_looper_button = button
        self.show_looper_button_value.subject = button

    @subject_slot('value')
    def show_looper_button_value(self, value):
        if value:
            self.application().view.focus_view("Detail/DeviceChain")
            self.song().view.select_device(self.looper_list[self._active_looper_number])
            self.song().view.selected_track = self.looper_list[self._active_looper_number].canonical_parent

    @subject_slot('value')
    def sel_next_looper_button_value(self, value):
        if value and self._active_looper_number != 0:
            self._active_looper_number = self.find_next_looper_number()
            self.update()

    def find_next_looper_number(self):
        temp = list(self.looper_list.keys())
        index = temp.index(self._active_looper_number)
        try:
            return temp[index+1]
        except:
            return temp[0]
    
    @property
    def _parent_track(self):
        can_parent = self.looper_list[self._active_looper_number].canonical_parent
        while not can_parent in self.song().tracks:
            can_parent = can_parent.canonical_parent
        return can_parent

    def _looper_selected_changed(self):
        print(["looper", self._active_looper_number])
        if self._active_looper_number > 0:
            self._change_looper_buttons(self._active_looper_number)
            self.looper_state_changed()
            self.update_track_colors()
            self.on_track_arm_changed.subject = self._parent_track
            self.on_track_mute_changed.subject = self._parent_track
            self.on_track_arm_changed()
            self.on_track_mute_changed()
    
    def update_track_colors(self):
        color = 0
        for i in range(2):
            j = self.cycle_list(i)
            if self.looper_list[j]:
                color = self.looper_list[j].canonical_parent.color_index
            if self._color_buttons[i]: 
                self._color_buttons[i].send_value(color, force=True)
    
    def cycle_list(self, i):
        _list = list(self.looper_buttons_list.keys())
        index = _list.index(self._active_looper_number)
        if i is 0:
            new_index = index-1 if index-1 > -1 else len(_list)-1
        else:
            new_index = index+1 if index+1 < len(_list) else 0
        return _list[new_index]

    @subject_slot('arm')
    def on_track_arm_changed(self):
        color = 0
        if self._parent_track.arm == 1:
            color = 127
        if self.arm_looper_track_button:
            self.arm_looper_track_button.send_value(color, force=True)

    @subject_slot('mute')
    def on_track_mute_changed(self):
        color = 80
        if self._parent_track.mute == 1:
            color = 81
        if self.mute_looper_track_button:
            self.mute_looper_track_button.send_value(color, force=True)

    def on_selected_track_changed(self):
        if self.is_enabled():
            track = self.song().view.selected_track
            if not track.devices_has_listener(self.build_loopers_list):
                track.add_devices_listener(self.build_loopers_list)

    @subject_slot('name')
    def _on_device_name_changed(self):
        if self.is_enabled() and self._name_controls and self._device:
            if self._device.class_display_name == "Looper":
                num = self._get_looper_number(self._device)
                if num > -1:
                    self._add_looper(num, self._device)

    def _get_looper_number(self, device):
        name = device.name
        num1 = name.find("(LOOPER")
        num3 = -1
        if num1 > -1:
            num3 = name[num1+7:name.find(")", num1)]
        return int(num3)

    def _add_looper(self, num, looper_instance):
        self.looper_list[num] = looper_instance
        self.looper_buttons_list[num] = self._add_control(num)
        self._active_looper_number = num
        try:
            looper_instance.parameters[1].add_value_listener(self.looper_state_changed)
        except:
            pass

    def looper_state_changed(self):
        for i in range(len(self.looper_list)):
            i = i+1
            if i < 5 and self.looper_list[i] is not None and self._6_looper_buttons is not None:
                looper_state = self.looper_list[i].parameters[1].value
                self._6_looper_buttons[i-1].send_value(state_color[looper_state], force=True)
            if i is self._active_looper_number and self.looper_state_button:
                looper_state = self.looper_list[self._active_looper_number].parameters[1].value
                self.looper_state_button.send_value(state_color[looper_state], force=True)

    def _add_control(self, number):
        return ButtonElement(True, MIDI_NOTE_TYPE, MIDI_CHANNEL, number)

    def _change_looper_buttons(self, num):
        if self.is_enabled() and num in list(self.looper_buttons_list.keys()):
            # Receiving {240, 01, 19, 70, Layout Number, Button number, Note/CC Number, Type, Channel, 247} changes the corresponding button        
            # Assign note num channel 11 
            self.looper_buttons_list[num]._send_midi((240, 122, 29, 1, 19, 52, num+23, 0, 11, 247))            
            # Assign note num channel 12 
            self.looper_buttons_list[num]._send_midi((240, 122, 29, 1, 19, 52, num+23, 0, 12, 247))            
            # Assign note num channel 13 
            self.looper_buttons_list[num]._send_midi((240, 122, 29, 1, 19, 52, num+23, 0, 13, 247))            
            # Assign note num channel 14 
            self.looper_buttons_list[num]._send_midi((240, 122, 29, 1, 19, 52, num+23, 0, 14, 247))
            # Assign note num channel 15 
            self.looper_buttons_list[num]._send_midi((240, 122, 29, 1, 19, 52, num+23, 0, 15, 247))
            # Assign note num channel 16 
            self.looper_buttons_list[num]._send_midi((240, 122, 29, 1, 19, 52, num+23, 0, 16, 247))
            self._looper_main_button_value.subject = self.looper_buttons_list[num]

    @subject_slot('value')
    def _looper_main_button_value(self, value):
        if self.is_enabled() and value:
            state_change = {0: 1, 1: 2, 2: 3, 3: 2}
            looper_state = self.looper_list[self._active_looper_number].parameters[1].value
            self.looper_list[self._active_looper_number].parameters[1].value = state_change[looper_state]

    def set_looper_state(self, button):
        self.looper_state_button = button

    def build_loopers_list(self):
        self.looper_list = {}
        self.looper_buttons_list = {}
        for track in self._song.tracks:
            for dev in track.devices:
                if dev.can_have_chains:
                    self.check_chain(dev.chains)
                else:
                    self.check_looper(dev)
        if len(self.looper_list) > 0:
            self._active_looper_number = max(self.looper_list)
            self._looper_selected_changed()

    def check_chain(self, _chains):
        for chain in _chains:
            for dev in chain.devices:
                if dev.can_have_chains:
                    self.check_chain(dev.chains)
                else:
                    self.check_looper(dev)

    def check_looper(self, device):
        if device and device.class_display_name == "Looper":
            num = self._get_looper_number(device)
            if num > -1:
                self._add_looper(num, device)

    def remove_looper_from_name(self, number):
        new_name = self.looper_list[number].name if number != 0 else ''
        num1 = new_name.find("(LOOPER")
        if num1 > -1:
            num2 = new_name.find(")", num1) + 1
            new_name = new_name[:num1] + new_name[num2:]
        return new_name

    def _send_sysex_for_name(self, name):       
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 51, 2]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self.is_enabled() and self._name_controls:     
            self._name_controls._send_midi(tuple(message))

    def set_device(self, device):
        self._on_device_name_changed.subject = device
        super(LooperComponent, self).set_device(device)

    def disconnect(self):
        super(LooperComponent, self).disconnect()

    def update(self):
        print("update")
        super(LooperComponent, self).update()
        self._looper_selected_changed()
        self._send_sysex_for_name("L%s " % str(self._active_looper_number) + self.remove_looper_from_name(self._active_looper_number))
