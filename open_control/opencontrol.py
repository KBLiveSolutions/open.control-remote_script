# coding: utf-8
from __future__ import print_function
from __future__ import absolute_import
import Live  #
from functools import partial
import time
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.Dependency import depends, inject
from _Framework.SubjectSlot import subject_slot
from _Framework.Util import const, mixin, recursive_map
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModesComponent import ModesComponent, CompoundMode, LayerMode, AddLayerMode, ImmediateBehaviour, CancellableBehaviour, AlternativeBehaviour

from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement

from .SpecialSessionComponent import SessionComponent
from .SpecialMixerComponent import MixerComponent
from .SpecialTransportComponent import TransportComponent
from .SpecialDeviceComponent import DeviceComponent
from .LooperComponent import LooperComponent
from .Skin import make_default_skin
from . import Options

MIDI_CHANNEL = 15

SCRIPT_NAME = 'open.control'
SCRIPT_VER = 'v0.9'
MAX_REQUESTS = 10
prefix = (240, 122, 29, 1, 19)
REQUEST_MSG = (240, 122, 29, 1, 19, 2, 247)
REPLY_MSG = (240, 122, 29, 1, 19, 2, 247)
ACKNOWLEDGMENT_MSG = (240, 122, 29, 1, 19, 78, 247)
NUM_TRACKS = 1

import logging, traceback
logger = logging.getLogger(__name__)
def print(text):
    logger.warning(text)

""" Dictionnaries containing all the actions performed by the buttons/sliders or interpreted by the LEDs.
 It consists of a dictionnary with the name of the action and the associated CC number."""

button_actions = {
    "Off": 0,
    "--- Global ---": 0,
    "■/▶ Start/Stop": 1,
    "●○ Metronome": 2,
    "⤶ Undo": 4,
    "▢ Capture": 5,
    "⊕ BPM +1": 28,
    "⊖ BPM -1": 29,
    "⮂ Arrangement/Session Toggle": 75,
    "Clip/Device Toggle": 76,
    "--- Arrangement ---": 0,
    "↞ Jump to 1.1.1": 74,
    "● Arrangement Rec": 6,
    "⥁ Arrangement Loop": 7,
    "⇤ Go to Prev Marker": 9,
    "⇥ Go to Next Marker": 8,
    "⤓ Add/Delete Marker": 10,
    "⥀ Loop to Next Marker": 102,
    "⇉ Restart From Last Position": 103,
    "--- Session ---": 0,
    "○ Session Rec": 11,
    "▶ Launch Scene": 13,
    "⬆ Sel Prev Scene": 14,
    "⬇ Sel Next Scene": 15,
    "⥴ Jump to Playing Scene": 16,
    "⥅ Insert Scene": 17,
    "⧈ Stop All Clips": 3,
    "➟ Disable Follow Actions": 12,
    "--- Tracks ---": 0,
    "← Sel Prev Track": 18,
    "→ Sel Next Track": 19,
    "▷ Launch Clip": 22,
    "↳ Find Empty Slot": 23,
    "⌧ Mute": 24,
    "S Solo": 25,
    "⌻ Arm": 26,
    "■ Stop": 27,
    "U Fold/Unfold Track": 55,
    "☆ Add Audio Track": 20,
    "✬ Add MIDI Track": 21,
    "--- Looper ---": 0,
    "① MIDI Map 1 (Big Button)": 0,
    "② MIDI Map 2 (Clear)": 0,
    "③ MIDI Map 3 (Undo)": 0,
    "▣ Stop Looper": 35,
    "⌻ Arm Looper Track": 30,
    "⌧ Mute Looper Track": 31,
    "+ Add Looper": 47,
    "⌸ Show Looper": 32,
    "⧀ Prev Looper": 48,
    "⧁ Next Looper": 49,
    "∅ Clear All": 36,
    "--- Variations ---": 0,
    "⍇ Prev Device": 65,
    "⍈ Next Device": 66,
    "⌃ Prev Variation": 67,
    "⌵ Next Variation": 68,
    "▹ Launch Variation": 69,
    "◦ Store Variation": 70,
    "↩︎ Recall Last Used": 72, 
    "⌁ Randomize Macros": 71,
    "--- Pages ---": 0,
    "⇆ Page 1/2": 50,
    "⇆ Page 1/3": 51,
    "↩ Prev Page": 56,
    "↪ Next Page": 57,
    "Custom MIDI": 0
  }
led_actions = {
    "Off": 0,
    "--- Global ---": 0,
    "■/▶ Start/Stop": 1,
    "●○ Metronome": 2,
    "● Arrangement Rec": 6,
    "⥁ Arrangement Loop": 7,
    "⇥ Go to Next Marker": 8,
    "⇤ Go to Prev Marker": 9,
    "⤓ Add/Delete Marker": 10,
    "○ Session Rec": 11,
    "➟ Disable Follow Actions": 12,
    "--- Scenes ---": 0,
    "▶ Scene Color": 13,
    "⬆ Prev Scene Color": 14,
    "⬇ Next Scene Color": 15,
    "--- Tracks ---": 0,
    "✽ Current Track Color": 54,
    "← Prev Track Color": 18,
    "→ Next Track Color": 19,
    "▷ Clip Color": 22,
    "⌧ Mute": 24,
    "S Solo": 25,
    "⌻ Arm": 26,
    "■ Stop": 27,
    "--- Looper ---": 0,
    "⧀ Prev Looper Track Color": 48,
    "⧁ Next Looper Track Color": 49,
    "◈ Looper State": 53,
    "◈ State (LOOPER1)": 77,
    "◈ State (LOOPER2)": 78,
    "◈ State (LOOPER3)": 79,
    "◈ State (LOOPER4)": 80,
    "◈ State (LOOPER5)": 81,
    "◈ State (LOOPER6)": 82,
    "--- Pages ---": 0,
    "⇆ Page Color": 58,
  }
slider_actions = {
    "--- Global ---": 0,
    "Last Selected Parameter": 73,
    "Global Groove Amount": 37,
    "Arrangement Loop Start": 0,
    "Arrangement Loop Length": 0,
    "Scroll Scenes": 0,
    "--- Selected Track ---": 0,
    "Send A": 59,
    "Send B": 60,
    "Selected Device Param 1": 61,
    "Selected Device Param 2": 62,
    "Device 1 Param 1": 63,
    "Device 1 Param 2": 64,
    "Looper Device 1 Param 1": 33,
    "Looper Device 1 Param 2": 34,
  }
display_actions =  {"Scene Name": 80,
                    "Track Name": 81,
                    "Looper Number": 82,
                    "Variation Number": 83,
                    "Left Marker Name": 84}

class opencontrol(ControlSurface):

    def __init__(self, *a, **k):
        super(opencontrol, self).__init__(*a, **k)
        self._has_been_identified = False
        self._request_count = 0
        self._last_sent_layout_byte = None

        with self.component_guard():
            self._skin = make_default_skin()
            with inject(skin=const(self._skin)).everywhere():
                self._create_buttons()
            self._session = SessionComponent( num_tracks=NUM_TRACKS, num_scenes=1, enable_skinning = True)
            self._mixer = MixerComponent(num_tracks=NUM_TRACKS)
            self._session.set_mixer(self._mixer)
            self._transport = TransportComponent()
            self._device = DeviceComponent(device_selection_follows_track_selection=True)
            self._looper = LooperComponent(device_selection_follows_track_selection=False)
            self._create_pages()
            self.set_device_component(self._device)
            self._device.set_mixer(self._mixer)
            # self.set_device_component(self._looper)
            self.check_session_box()
            if Live.Application.get_application().get_major_version() == 9:
                self._create_m4l_interface()

        self.log_message('Loaded %s %s' % (SCRIPT_NAME, SCRIPT_VER))
        self.show_message('Loaded %s %s' % (SCRIPT_NAME, SCRIPT_VER))

    def _create_buttons(self):
        self.buttons = {}
        for control in button_actions:
            self.buttons[control] = self.make_button(button_actions[control], MIDI_CHANNEL, msg_type=MIDI_CC_TYPE, name=control)
        for control in led_actions:
            if led_actions[control] not in list(button_actions.values()):
                self.buttons[control] = self.make_button(led_actions[control], MIDI_CHANNEL, msg_type=MIDI_CC_TYPE, name=control)
        for control in slider_actions:
            self.buttons[control] = self.make_button(slider_actions[control], MIDI_CHANNEL, msg_type=MIDI_CC_TYPE, name=control)
        for control in display_actions:
            self.buttons[control] = ButtonMatrixElement(rows=[[self._add_control(display_actions[control]), self._add_control(display_actions[control]+1), self._add_control(display_actions[control]+2), self._add_control(display_actions[control]+3)]])
        
        mute_row = []
        arm_row = []
        stop_row = []
        solo_row = []
        clip_launch_row = []

        for i in range(NUM_TRACKS):
            mute_row.append(self.buttons["⌧ Mute"])
            arm_row.append(self.buttons["⌻ Arm"])
            stop_row.append(self.buttons["■ Stop"])
            solo_row.append(self.buttons["S Solo"])
            clip_launch_row.append(self.buttons["▷ Launch Clip"])
                    
        self.looper_buttons = ButtonMatrixElement(rows=[[self.buttons["◈ State (LOOPER1)"], self.buttons["◈ State (LOOPER2)"], self.buttons["◈ State (LOOPER3)"],
                                                self.buttons["◈ State (LOOPER4)"], self.buttons["◈ State (LOOPER5)"], self.buttons["◈ State (LOOPER6)"]]])
        self.mute_buttons = ButtonMatrixElement(rows=[mute_row])
        self.arm_buttons = ButtonMatrixElement(rows=[arm_row])
        self.stop_buttons = ButtonMatrixElement(rows=[stop_row])
        self.solo_buttons = ButtonMatrixElement(rows=[solo_row])
        self.clip_launch_buttons = ButtonMatrixElement(rows=[clip_launch_row])

    @depends(skin=None)
    def make_button(self, identifier, channel, name, msg_type = MIDI_CC_TYPE, skin = None, is_modifier = False):
        return ButtonElement(True, msg_type, channel, identifier, skin=skin, name=name, resource_type=PrioritizedResource if is_modifier else None)

    def _create_pages(self):
        self._pages_0_1 = ModesComponent(name='pages_0_1', is_enabled=False)
        self._pages_0_2 = ModesComponent(name='pages_0_2', is_enabled=False)
        """Session Actions"""
        self._session_layer_mode = AddLayerMode(self._session, Layer(scene_bank_up_button=self.buttons["⬆ Sel Prev Scene"],
                                                                    scene_bank_down_button=self.buttons["⬇ Sel Next Scene"],
                                                                    # scene_launch_buttons=self.scene_launch_buttons,
                                                                    launch_scene_button=self.buttons["▶ Launch Scene"],
                                                                    track_bank_left_button=self.buttons["← Sel Prev Track"],
                                                                    track_bank_right_button=self.buttons["→ Sel Next Track"],
                                                                    find_next_empty_slot=self.buttons["↳ Find Empty Slot"],
                                                                    add_audio_track=self.buttons["☆ Add Audio Track"],
                                                                    add_MIDI_track=self.buttons["✬ Add MIDI Track"],
                                                                    undo=self.buttons["⤶ Undo"],
                                                                    current_track_color=self.buttons["✽ Current Track Color"],
                                                                    unfold_track=self.buttons["U Fold/Unfold Track"],
                                                                    capture=self.buttons["▢ Capture"],
                                                                    stop_track_clip_buttons=self.stop_buttons,
                                                                    clip_launch_buttons=self.clip_launch_buttons,
                                                                    last_selected_parameter=self.buttons["Last Selected Parameter"],
                                                                    main_view_toggle=self.buttons["⮂ Arrangement/Session Toggle"],
                                                                    detail_view_toggle=self.buttons["Clip/Device Toggle"]))



        self._scene_layer_mode = AddLayerMode(self._session.scene(0), Layer(name_controls = self.buttons["Scene Name"]))

        """Transport Actions"""
        self._transport_mode = AddLayerMode(self._transport, Layer(start_stop=self.buttons["■/▶ Start/Stop"],
                                                                    loop_button=self.buttons["⥁ Arrangement Loop"],
                                                                    name_controls=self.buttons["Left Marker Name"],
                                                                    jump_to_start=self.buttons["↞ Jump to 1.1.1"],
                                                                    restart_button=self.buttons["⇉ Restart From Last Position"],
                                                                    set_or_delete_cue_button=self.buttons["⤓ Add/Delete Marker"],
                                                                    inc_bpm_button=self.buttons["⊕ BPM +1"],
                                                                    dec_bpm_button=self.buttons["⊖ BPM -1"],
                                                                    prev_cue_button=self.buttons["⇤ Go to Prev Marker"],
                                                                    next_cue_button=self.buttons["⇥ Go to Next Marker"],
                                                                    marker_loop_button=self.buttons["⥀ Loop to Next Marker"],
                                                                    metronome=self.buttons["●○ Metronome"],
                                                                    record_button=self.buttons["● Arrangement Rec"],
                                                                    session_record_button=self.buttons["○ Session Rec"],
                                                                    groove_amount=self.buttons["Global Groove Amount"]
                                                                    ))
        """Mixer Actions"""
        self._mixer_mode = AddLayerMode(self._mixer, Layer(mute_buttons=self.mute_buttons,
                                                            arm_buttons=self.arm_buttons,
                                                            solo_buttons=self.solo_buttons
                                                            ))
        """Devices Actions"""
        self._device_layer_mode = AddLayerMode(self._device, Layer(name_controls = self.buttons["Variation Number"],
                                                                    launch_variation_button=self.buttons["▹ Launch Variation"],
                                                                    prev_variation_button=self.buttons["⌃ Prev Variation"],
                                                                    next_variation_button=self.buttons["⌵ Next Variation"],
                                                                    next_device_button=self.buttons["⍈ Next Device"],
                                                                    prev_device_button=self.buttons["⍇ Prev Device"],
                                                                    store_variation_button=self.buttons["◦ Store Variation"],
                                                                    recall_variation_button=self.buttons["↩︎ Recall Last Used"],
                                                                    randomize_macros_button=self.buttons["⌁ Randomize Macros"],
                                                                    selected_device_parameters=ButtonMatrixElement(rows=[[self.buttons["Selected Device Param 1"], self.buttons["Selected Device Param 2"]]]),
                                                                    first_device_parameter=ButtonMatrixElement(rows=[[self.buttons["Device 1 Param 1"], self.buttons["Device 1 Param 2"]]]), priority=1))



        self._looper_layer_mode = AddLayerMode(self._looper, Layer(name_controls = self.buttons["Looper Number"],
                                                                    add_looper = self.buttons["+ Add Looper"],
                                                                    sel_prev_looper=self.buttons["⧀ Prev Looper"],
                                                                    sel_next_looper=self.buttons["⧁ Next Looper"],
                                                                    arm_looper_track=self.buttons[ "⌻ Arm Looper Track"],
                                                                    mute_looper_track=self.buttons["⌧ Mute Looper Track"],
                                                                    select_looper=self.buttons["⌸ Show Looper"],
                                                                    looper_state=self.buttons["◈ Looper State"],
                                                                    stop_looper=self.buttons["▣ Stop Looper"],
                                                                    clear_all=self.buttons["∅ Clear All"],
                                                                    looper_buttons=self.looper_buttons
                                                                    ))

        """Channel Strip Actions"""
        self._channel_strip_layer_mode = AddLayerMode(self._mixer.channel_strip(0), Layer(
                                                                                        name_controls=self.buttons["Track Name"],
                                                                                        send_controls=ButtonMatrixElement(rows=[[self.buttons["Send A"], self.buttons["Send B"]]]),
                                                                                        ))



        """Modes switching"""
        self.pages = ['page_0', 'page_1', 'page_2']
        active_layers = [self._session_layer_mode, self._mixer_mode, self._scene_layer_mode, self._transport_mode, self._channel_strip_layer_mode, self._device_layer_mode, self._looper_layer_mode]
        self._pages_0_1.add_mode(self.pages[0], active_layers)
        self._pages_0_1.add_mode(self.pages[1], active_layers, behaviour=CancellableBehaviour())
        self._page_2 = AddLayerMode(self._pages_0_1, self._pages_0_1.layer)
        self._pages_0_2.add_mode(self.pages[0], active_layers)
        self._pages_0_2.add_mode(self.pages[2], active_layers, behaviour=CancellableBehaviour())
        self.current_page = 0
        self.previous_page_0_1 = 0
        self.set_page_0_1_button(self.buttons["⇆ Page 1/2"])
        self.set_page_0_2_button(self.buttons["⇆ Page 1/3"])
        self.set_prev_page_button(self.buttons["↩ Prev Page"])
        self.set_next_page_button(self.buttons["↪ Next Page"])
        self.page_color_button = ButtonElement(True, MIDI_CC_TYPE, MIDI_CHANNEL, self.buttons["⇆ Page Color"])
        self._pages_0_1.selected_mode = self.pages[0]
        # self._pages_0_2.selected_page = self.pages[2]
        self._pages_0_2.set_enabled(False)
        self._pages_0_1.set_enabled(True)

    def set_page_0_1_button(self, button):
        self.page_0_1_button = button
        self._on_page_0_1_button_value.subject = button

    def set_page_0_2_button(self, button):
        self.page_0_2_button = button
        self._on_page_0_2_button_value.subject = button

    def set_prev_page_button(self, button):
        self.next_page_button = button
        self._on_prev_page_button_value.subject = button

    def set_next_page_button(self, button):
        self.page_0_2_button = button
        self._on_next_page_button_value.subject = button

    @subject_slot('value')
    def _on_prev_page_button_value(self, value):
        if value:
            self.current_page -= 1 
            if self.current_page == -1:
                self.current_page = 2
            self.enable_page()      

    @subject_slot('value')
    def _on_next_page_button_value(self, value):
        if value:
            self.current_page += 1 
            if self.current_page == 3:
                self.current_page = 0
            self.enable_page()      


    @subject_slot('value')
    def _on_page_0_1_button_value(self, value):
        if value:
            if self.current_page < 1:
                self.current_page = 1
            else :
                self.current_page = 0
            self.enable_page()

    @subject_slot('value')
    def _on_page_0_2_button_value(self, value):
        if value:
            if self.current_page < 2:
                self.current_page = 2
            else :
                self.current_page = 0
            self.enable_page()
    
    def enable_page(self):
        pages_color = [Options.page_1_color, Options.page_2_color, Options.page_3_color]
        self.show_message('Page %s' % str(self.current_page+1))
        self._send_midi(prefix + (20, self.current_page, 247))
        if self.current_page == 2:
            self._pages_0_2.selected_mode = self.pages[2]
            self._pages_0_1.set_enabled(False)
            self._pages_0_2.set_enabled(True)
        else :
            self._pages_0_1.selected_mode = self.pages[self.current_page]
            self._pages_0_2.set_enabled(False)
            self._pages_0_1.set_enabled(True)
        self._send_midi((176 + MIDI_CHANNEL, 58, pages_color[self.current_page]))
        self.update_pages()

    def update_pages(self):
        self._session.update()
        self._mixer.update()
        self._transport.update()
        self._device.update()
        self._looper.update()

    def handle_sysex(self, midi_bytes):
        if not self._has_been_identified and midi_bytes == REPLY_MSG:
            self._has_been_identified = True
            self.set_enabled(True)
            self.set_highlighting_session_component(self._session)
            self.schedule_message(1, self.refresh_state)
        if midi_bytes == ACKNOWLEDGMENT_MSG:
            self._session.scene(0)._on_scene_name_changed()
            self._mixer.channel_strip(0)._on_track_name_changed()
            # self._device._on_device_name_changed()
            self._transport._on_name_changed()
            self._session.update()
            self._mixer.update()
            self._transport.update()
            self._device.update()
            self._looper.update()

        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 30):
            Options.metronome_blinking = midi_bytes[6]
            self._transport._on_metronome_changed()
        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 31):
            Options.session_box_linked_to_selection = midi_bytes[6]
            self.check_session_box()
        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 32):
            Options.page_1_color = midi_bytes[6]
        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 33):
            Options.page_3_color = midi_bytes[6]
        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 34):
            Options.page_3_color = midi_bytes[6]

    def check_session_box(self):
        self._session._show_highlight = False
        if Options.session_box_linked_to_selection ==0:
            self._session._show_highlight = True
        self._session._do_show_highlight()

    def port_settings_changed(self):
        self.set_enabled(False)
        self.set_highlighting_session_component(None)
        self._request_count = 0
        self._has_been_identified = False
        self._request_identification()

    def _request_identification(self):
        """ Sends request and schedules message to call this method again and do
        so repeatedly until handshake succeeds or MAX_REQUESTS have been sent. """
        if not self._has_been_identified and self._request_count < MAX_REQUESTS:
            self._send_midi(REQUEST_MSG)
            self.schedule_message(2, self._request_identification)
            self._request_count += 1

    def _create_m4l_interface(self):
        """ Creates and sets up the M4L interface for easy interaction from
        M4L devices in Live 9. """
        from _Framework.M4LInterfaceComponent import M4LInterfaceComponent
        self._m4l_interface = M4LInterfaceComponent(controls=self.controls,
                                                    component_guard=self.component_guard,
                                                    priority=1)
        self._m4l_interface.name = 'M4L_Interface'
        self._m4l_interface.is_private = True
        self.get_control_names = self._m4l_interface.get_control_names
        self.get_control = self._m4l_interface.get_control
        self.grab_control = self._m4l_interface.grab_control
        self.release_control = self._m4l_interface.release_control
        
    def _add_control(self, number):
        return ButtonElement(True, MIDI_CC_TYPE, MIDI_CHANNEL, number)

    def _add_slider(self, number):
        return EncoderElement(MIDI_CC_TYPE, MIDI_CHANNEL, number, Live.MidiMap.MapMode.absolute)

    def disconnect(self):
        super(opencontrol, self).disconnect()
        self._send_midi(prefix + (3, 247))
        self._session = None