import Live
from _Framework.SubjectSlot import subject_slot
from _Framework.ClipSlotComponent import ClipSlotComponent as ClipSlotBase

from . import colors

import logging, traceback
logger = logging.getLogger(__name__)
def print(text):
    logger.warning(text)
groups_list = [  "A", "B", "C", "Z"]

PATT_LENGTH = 8

class LooperTrack(ClipSlotBase):
    def __init__(self, lp, track, *a, **k):
        super(LooperTrack, self).__init__(*a, **k)
        self.looper_component = lp
        self.track = track
        self.playing_clip = self.track.clip_slots[self.track.playing_slot_index].clip
        self.sequence = [1, 1, 1, 1, 1, 1, 1, 1]
        self.chut_is_on = False
        self.chut_edit_is_on = False
        self.current_chut_step = 0
        self.chut_pattern = [0, 0, 0, 0, 0, 0, 0, 0]
        self.initial_pattern = [1, 1, 1, 1, 1, 1, 1, 1]
        self.launch_button = None
        self.clip_length = None
        self.silencer_sequence_buttons = [None, None, None, None, None, None, None, None]
        self.INSTRU_macro_buttons = None
        self.INSTRU_chain_selector_buttons = None
        self.group_buttons =  [None, None, None, None]
        self.current_step = 0
        self.previous_beat = 0
        self.time = 0
        self.timer = Live.Base.Timer(callback=self.on_timer_reached, interval=1, repeat=False)
        self.previous_preset = None
        self.is_selected = False
        self.is_recording = False
        self.is_playing = False
        self.remise_a_zero = False
        self.show_sequence()
        self.GROUP_FX_device = None
        self.TRACK_FX_device = None
        self.INSTRU_device = None
        self.INSERT_FX_device = None
        self.selected_chain = 0
        self.group = "Z"
        self.previous_chain_number = 0
        self.on_playing_clip_changed.subject = self.track
        self.previous_color = colors.pad_on
        self.start_time = 0
        self.loop_notify = False
        self.on_playing_clip_changed()
        self.set_clip_listeners(self.playing_clip)
        self.find_devices()


    """ LOOPER """

    def recording_started(self, shift_rec):
        self.playing_clip = None
        self.set_clip_listeners(None)
        if not shift_rec:
            for i in range(PATT_LENGTH):
                self.sequence[i] = self.looper_component.initial_pattern[i]
            self.change_group("Z")
            if self.TRACK_FX_device:
                self.TRACK_FX_device.selected_variation_index = 0
                self.TRACK_FX_device.recall_selected_variation()          
            if self.INSERT_FX_device:
                self.INSERT_FX_device.selected_variation_index = 0
                self.INSERT_FX_device.recall_selected_variation()
        self.show_sequence()
        self.update_launch_button()

    def recording_stopped(self, clip):
        self.playing_clip = clip
        self.current_step = -1
        self.playing_clip.color_index = (self.track.playing_slot_index % 8) * 4
        self.set_clip_listeners(self.playing_clip)

    def update_launch_button(self):
        if not self.looper_component.changing_Xbars:
            color = colors.looper_off
            if self.playing_clip:
                if self.sequence[self.current_step] == 0 :
                    color = colors.pad_play_mute
                else:
                    color = colors.pad_play
            if self.is_selected:
                color = colors.pad_sel
            if self.is_recording:
                color = colors.pad_rec
            if self.launch_button: 
                self.launch_button.send_value(color, force=True)


    """ SILENCER """
    def rotate_pattern(self, direction):
        if direction == "right":
            self.sequence =  self.rotate(self.sequence, 1)
        else:
            self.sequence =  self.rotate(self.sequence, -1)
        self.show_sequence()

    def rotate(self, l, n):
        return l[-n:] + l[:-n]

    def on_seq_button_pressed(self, step):
        self.sequence[step] = 1 if self.sequence[step] == 0 else 0
        self.show_step(step)
   
    @subject_slot('playing_slot_index')
    def on_playing_clip_changed(self):
        slot = self.track.playing_slot_index 
        self.is_recording = self.track.clip_slots[slot].is_recording
        self.is_playing = self.track.clip_slots[slot].is_playing
        self.update_launch_button()
        self.show_sequence()

    def set_clip_listeners(self, clip):
        self.on_clip_jump.subject = clip
        self.on_clip_pos.subject = clip

    @subject_slot('playing_position')
    def on_clip_pos(self):
        if 0.1 > self.playing_clip.start_marker - self.playing_clip.playing_position and not self.loop_notify:
            self.bang()
            self.loop_notify = True

    @subject_slot('loop_jump')
    def on_clip_jump(self):
        self.loop_notify = False

    def select_looper_track(self, is_selected):
        self.is_selected = is_selected
        self.show_sequence()
        self.update_launch_button()

    def show_sequence(self):
        for i in range(PATT_LENGTH):
            self.show_step(i)
 
    def bang(self):
        self.current_step += 1
        if self.current_step == PATT_LENGTH: 
            self.current_step = 0 
        if self.chut_is_on and not self.looper_component.chut:
            self.current_chut_step += 1
            step = self.current_chut_step
            if self.chut_pattern[step] == 0: 
                self.end_of_chut()
        else:
            step = self.current_step
        self.timer.start()
        self.show_step(step-1 if step>0 else 7)
        self.show_step(step)

    def on_timer_reached(self):
        self.timer.stop()
        self.check_mute()
        self.update_launch_button()

    def check_mute(self):
        if self.chut_is_on:
            step_value = not self.chut_pattern[self.current_chut_step]
        else:
            step_value = self.sequence[self.current_step]
        if  step_value == 0:
            self.track.mute = 1
        else:
            self.track.mute = 0

    def set_chut_pattern(self, row, col):
        for i in range(col+1):
            self.chut_pattern[i] = 1
            self.silencer_sequence_buttons[i].send_value(colors.chut_on_2, force=True)
        self.chut_is_on = True
        self.current_chut_step = -1

    def end_of_chut(self):
        self.chut_is_on = False
        self.current_chut_step = -1
        self.chut_pattern = [0, 0, 0, 0, 0, 0, 0, 0]
        self.show_sequence()

    def show_step(self, step):
        if self.chut_is_on:
            color = colors.chut_off
            if step is self.current_chut_step:
                color = colors.pad_play
            elif self.chut_pattern[step]:
                color = colors.chut_on_2 if self.chut_pattern[step] == 1 else colors.chut_off
            if self.silencer_sequence_buttons[step]: 
                self.silencer_sequence_buttons[step].send_value(color, force=True)
        else:
            if not self.looper_component.chut:
                color = colors.pad_off
                if self.is_recording:
                    color = colors.pad_rec
                else:
                    if self.playing_clip:
                        if step is self.current_step and self.is_playing:
                            if self.sequence[step]:
                                color = colors.pad_play
                            else:
                                color = colors.pad_play_mute
                        elif self.sequence[step]:
                            color = colors.pad_sel if self.is_selected else colors.pad_on
                if self.silencer_sequence_buttons[step]: # and self.previous_color is not color: 
                    self.silencer_sequence_buttons[step].send_value(color, force=True)
                    self.previous_color = color

    """ GROUPS """

    def change_group(self, group):
        self.group_buttons[groups_list.index(self.group)].send_value(0, force=True)
        self.group = group
        for i in range(12):
            self.track.mixer_device.sends[i].value = self.looper_component.sends_values[group][i]
        if self.GROUP_FX_device:
            try:
                self.GROUP_FX_device.parameters[17].value = groups_list.index(group)
            except:
                pass
        self.update_group()
    
    def update_group(self):
        index = groups_list.index(self.group)
        if self.group_buttons[index]:
            self.group_buttons[index].send_value(colors.groups_color[index], force=True)

    """ INSTRUS """

    def find_devices(self):
        for d in self.track.devices:
            if d.name == "GROUP FX":
                self.GROUP_FX_device = d
            if d.name == "TRACK FX":
                self.TRACK_FX_device = d
            if d.name == "INSTRU":
                self.INSTRU_device = d

    def on_chain_selector_changed(self, chain_number):
        self.INSTRU_chain_selector_buttons[self.previous_chain_number].send_value(0, force=True)
        self.INSTRU_device.parameters[17].value = chain_number
        self.selected_chain = chain_number
        for i in range(8):
            self.INSTRU_device.parameters[i+1].value = self.INSTRU_device.chains[self.selected_chain].devices[0].parameters[i+1].value
            self.INSTRU_macro_buttons[i].send_value(self.INSTRU_device.parameters[i+1].value, force=True)
        self.INSTRU_chain_selector_buttons[chain_number].send_value(colors.instru1, force=True)
        self.previous_chain_number = chain_number

    def on_macro_changed(self, macro, value):
        self.INSTRU_device.parameters[macro].value = value
        self.INSTRU_device.chains[self.selected_chain].devices[0].parameters[macro].value = value

