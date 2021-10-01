# coding: utf-8
from __future__ import print_function
from __future__ import absolute_import
import Live  #
from functools import partial
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.Dependency import depends, inject
from _Framework.SubjectSlot import subject_slot
from _Framework.Util import const, mixin, recursive_map
from _Framework.ButtonMatrixElement import ButtonMatrixElement

from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ModesComponent import ModesComponent, CompoundMode, LayerMode, AddLayerMode, ImmediateBehaviour, CancellableBehaviour, AlternativeBehaviour

from .Looper import  LooperComponent
from . import reglages

import logging, traceback
logger = logging.getLogger(__name__)
def print(text):
    logger.warning(text)

MIDI_CHANNEL = 0


class Jacques(ControlSurface):

    def __init__(self, *a, **k):
        super(Jacques, self).__init__(*a, **k)

        with self.component_guard():
            self._create_buttons()
            self._looper = LooperComponent(24, 4)
            self._create_modes()
        self.set_highlighting_session_component(self._looper)

        self.log_message('Jacques is loaded')
        self.show_message('Jacques is loaded')

    def _create_buttons(self):

        """ REC LAUNCH BUTTONS"""
        
        self.temp_buttons_list = []
        for num in range(24):
            self.temp_buttons_list.append(self.make_control(num, 0, msg_type=MIDI_NOTE_TYPE))
        self.looper_launch_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list])

        """ REC STOP BUTTONS"""

        self.temp_buttons_list = []
        for i in range(4):
            num = i+1
            self.temp_buttons_list.append(self.make_control(num, 11, msg_type=MIDI_CC_TYPE))
        self.stop_rec_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list])

        """ SESSION MATRIX """

        self.temp_buttons_list_2 = []
        for j in range(4):
            self.temp_buttons_list = []
            for i in range(24):
                num = i+(4-j)*24
                self.temp_buttons_list.append(self.make_control(num, 0, msg_type=MIDI_NOTE_TYPE))
            self.temp_buttons_list_2.append(self.temp_buttons_list)    
        self._session_matrix = ButtonMatrixElement(rows=self.temp_buttons_list_2)

        """ ARM INPUT BUTTONS """

        self.temp_buttons_list = []
        self.temp_buttons_list_2 = []
        for i in range(8):
            num_arm = reglages.inputs_arm[i+1][0]
            channel_arm = reglages.inputs_arm[i+1][1]-1
            num_macro = reglages.macros_inputs[i+1][0]
            channel_macro = reglages.macros_inputs[i+1][1]-1
            self.temp_buttons_list.append(self.make_control(num_arm, channel_arm, msg_type=MIDI_CC_TYPE))
            self.temp_buttons_list_2.append(self.make_control(num_macro, channel_macro, msg_type=MIDI_CC_TYPE))
        self.arm_input_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list])
        self.macros_input_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list_2])

        """ SILENCER PRESET BUTTONS"""
        
        self.temp_buttons_list = []
        for i in range(7):
            num = i+96
            self.temp_buttons_list.append(self.make_control(num, 4, msg_type=MIDI_NOTE_TYPE))
        self.silencer_preset_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list])

        """ SILENCER LITTLE BUTTONS"""
        
        self.temp_buttons_list = []
        self.temp_buttons_list_2 = []
        for j in range(2):
            channel = j+3
            for num in range(96):
                self.temp_buttons_list.append(self.make_control(num, channel, msg_type=MIDI_NOTE_TYPE))
            self.temp_buttons_list_2.append(self.temp_buttons_list)
        self.silencer_sequence_matrix = ButtonMatrixElement(rows=self.temp_buttons_list_2)

        """ INDIVIDUAL BUTTON"""
        
        self.chut_button = self.make_control(103, 4, msg_type=MIDI_NOTE_TYPE)
        self.shift_rec_button = self.make_control(62, 0, msg_type=MIDI_CC_TYPE)
        self.remise_a_zero_button = self.make_control(2, 3, msg_type=MIDI_CC_TYPE)
        self.bank_up_button = self.make_control(108, 0, msg_type=MIDI_CC_TYPE)
        self.bank_down_button = self.make_control(109, 0, msg_type=MIDI_CC_TYPE)
        self.start_stop = self.make_control(110, 0, msg_type=MIDI_CC_TYPE)
        self.cancel_rec = self.make_control(111, 0, msg_type=MIDI_CC_TYPE)
        self.rotate_pattern = self.make_control(1, 3, msg_type=MIDI_CC_TYPE)
        self.bpm_inc_dec = self.make_control(61, 0, msg_type=MIDI_CC_TYPE)
        self.groove_amount = self.make_control(63, 0, msg_type=MIDI_CC_TYPE)
        self.input_gain = ButtonMatrixElement(rows=[[self.make_control(9, 11, msg_type=MIDI_CC_TYPE), self.make_control(10, 11, msg_type=MIDI_CC_TYPE)]])
        self.input_eq = ButtonMatrixElement(rows=[[self.make_control(11, 11, msg_type=MIDI_CC_TYPE), self.make_control(12, 11, msg_type=MIDI_CC_TYPE)]])


        """ GROUPS BUTTONS"""
        
        self.temp_buttons_list = []
        for num in range(4*20):
            self.temp_buttons_list.append(self.make_control(num, 1, msg_type=MIDI_NOTE_TYPE))
        self.change_groups_buttons_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list])

        """ SENDS KNOBS"""
        
        groups_list = ["GroupA", "GroupB", "GroupC"]
        sends_list = ["sendA", "sendB", "sendC", "sendD", "sendE", "sendF", "sendG", "sendH", "sendI", "sendJ", "sendK", "sendL"]
        self.temp_buttons_list_2 = []
        for j in range(3):
            self.temp_buttons_list = []
            group = reglages.sends_groups[groups_list[j]]
            for i in range(12):
                send = group[sends_list[i]]
                num = send[0]
                channel = send[1]-1
                self.temp_buttons_list.append(self.make_control(num, channel, msg_type=MIDI_CC_TYPE))
            self.temp_buttons_list_2.append(self.temp_buttons_list)   
        self.sends_matrix = ButtonMatrixElement(rows=self.temp_buttons_list_2)

        """ VOLUME FADERS """

        self.temp_buttons_list = []
        for j in range(2):
            channel = j
            for i in range(12):
                num = i+49
                self.temp_buttons_list.append(self.make_control(num, channel, msg_type=MIDI_CC_TYPE))
            self.volume_faders_matrix = ButtonMatrixElement(rows=[self.temp_buttons_list])

        """ INSTRUS MACROS KNOBS"""
        self.macro_knobs = {}
        self.chain_selectors = {}

        """ PIERRADE INSTRU 1 """
        instru_list = ["1", "2", "3", "4"]
        self.temp_buttons_list_2 = []
        for i in instru_list:
            self.temp_buttons_list = []
            inst = reglages.instrus[i]
            for i in range(16):
                num = inst[i+1][0]
                channel = inst[i+1][1]-1
                self.temp_buttons_list.append(self.make_control(num, channel, msg_type=MIDI_CC_TYPE))
            self.temp_buttons_list_2.append(self.temp_buttons_list)
        self.macro_knobs = ButtonMatrixElement(rows=self.temp_buttons_list_2)
 
        self.temp_buttons_list_2 = []
        for i in instru_list:
            inst = reglages.instrus[i]       
            self.temp_buttons_list = []
            chain_selector_notes = inst["chain_selector_notes"]
            channel = inst["chain_selector_channel"]-1
            for i in range(15):
                num = chain_selector_notes[i]
                self.temp_buttons_list.append(self.make_control(num, channel, msg_type=MIDI_NOTE_TYPE))
            self.temp_buttons_list_2.append(self.temp_buttons_list)
        self.chain_selectors = ButtonMatrixElement(rows=self.temp_buttons_list_2)

    def _create_modes(self):
        self._looper.layer = Layer(scene_bank_up_button=self.bank_up_button,
        scene_bank_down_button=self.bank_down_button,
        clip_launch_buttons=self._session_matrix,
        looper_launch_buttons=self.looper_launch_matrix, 
        stop_rec_buttons=self.stop_rec_matrix, 
        silencer_sequence_buttons=self.silencer_sequence_matrix, 
        silencer_preset_buttons=self.silencer_preset_matrix, 
        shift_rec_button=self.shift_rec_button, 
        sends_matrix_buttons=self.sends_matrix, 
        change_group_buttons=self.change_groups_buttons_matrix, 
        remise_a_zero_button=self.remise_a_zero_button, 
        chut_button=self.chut_button,  
        volume_faders = self.volume_faders_matrix,
        start_stop=self.start_stop,
        arm_input_buttons=self.arm_input_matrix,
        macros_input_buttons=self.macros_input_matrix,
        rotate_pattern=self.rotate_pattern,
        instru_macro_knobs=self.macro_knobs,
        instru_chain_selectors=self.chain_selectors,
        cancel_rec=self.cancel_rec,
        bpm_inc_dec=self.bpm_inc_dec,
        groove_amount=self.groove_amount,
        input_gain=self.input_gain,
        input_eq=self.input_eq
        )
        
    def make_control(self, identifier, channel, msg_type = MIDI_CC_TYPE, is_modifier = False):
        return ButtonElement(True, msg_type, channel, identifier, resource_type=PrioritizedResource if is_modifier else None)

    def disconnect(self):
        super(Jacques, self).disconnect()

    def port_settings_changed(self):
        # self.set_enabled(True)
        self._looper.update_display ()
        self._has_been_identified = False