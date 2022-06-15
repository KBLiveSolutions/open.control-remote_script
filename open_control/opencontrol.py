    # Remote Script to make open.control work with Ableton Live
    # Copyright (C) 2021 Pierre-Antoine GRISON
    # more info on open.control on http://opencontrol.me

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.


""" to do
improve arrangement marker name
fix track selection
1.2.2 changelog:
- added colors to Markers for SONGS
- fixed (SONG) detection for arrangement markers
"""

# coding: utf-8
from __future__ import print_function
from __future__ import absolute_import
import Live
import time
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.SubjectSlot import subject_slot
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModesComponent import ModesComponent, AddLayerMode

from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement

from .SpecialSessionComponent import SessionComponent
from .SpecialMixerComponent import MixerComponent
from .SpecialTransportComponent import TransportComponent
from .SpecialDeviceComponent import DeviceComponent
from .LooperComponent import LooperComponent
from .Skin import make_default_skin
from . import Options



SCRIPT_NAME = 'open.control'
SCRIPT_VER = 'v1.2.2'

MIDI_CHANNEL = 15
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
    "Start/Stop": 1,
    "Metronome": 2,
    "Continue Playing": 100,
    "Undo": 4,
    "Redo": 40,
    "Capture": 5,
    "BPM +1": 28,
    "BPM -1": 29,
    "Arrangement/Session Toggle": 75,
    "MIDI Recording Quantization": 104,
    "Clip/Device Toggle": 76,
    "--- Arrangement ---": 0,
    "Jump to 1.1.1": 74,
    "Arrangement Rec": 6,
    "Arrangement Loop": 7,
    "Go to Prev Marker": 9,
    "Go to Next Marker": 8,
    "Add/Delete Marker": 10,
    "Loop to Next Marker": 102,
    "Re-enable Automation": 41,
    "Back To Arrangement": 42,
    "Punch In": 38,
    "Punch Out": 39,
    "Restart From Last Position": 103,
    "--- Session ---": 0,
    "Session Rec": 11,
    "Launch Scene": 13,
    "Sel Prev Scene": 14,
    "Sel Next Scene": 15,
    "Jump 4 Scenes Up": 105,
    "Jump 4 Scenes Down": 106,
    "Fixed Length Rec 1 Bars": 107,
    "Fixed Length Rec 2 Bars": 108,
    "Fixed Length Rec 4 Bars": 109,
    "Fixed Length Rec 8 Bars": 110,
    "Jump to Playing Scene": 16,
    "Insert Scene": 17,
    "Capture and Insert Scene": 43,
    "Stop All Clips": 3,
    "Disable Follow Actions": 12,
    "--- Tracks ---": 0,
    "Sel Prev Track": 18,
    "Sel Next Track": 19,
    "Launch Clip": 22,
    "Find Empty Slot": 23,
    "Mute": 24,
    "S Solo": 25,
    "Arm": 26,
    "Stop": 27,
    "U Fold/Unfold Track": 55,
    "Add Audio Track": 20,
    "Add MIDI Track": 21,
    "--- Setlist ---": 0,
    "Prev Setlist Song": 33,
    "Next Setlist Song": 34,
    "Launch Setlist Song": 44,
    "Refresh Setlist": 46,
    "Launch Setlist Song NoQ": 45,
    "--- Looper ---": 0,
    "MIDI Map 1 (Big Button)": 0,
    "MIDI Map 2 (Clear)": 0,
    "MIDI Map 3 (Undo)": 0,
    "Stop Looper": 35,
    "Arm Looper Track": 30,
    "Mute Looper Track": 31,
    "+ Add Looper": 47,
    "Show Looper": 32,
    "Prev Looper": 48,
    "Next Looper": 49,
    "Clear All": 36,
    "--- Variations ---": 0,
    "Prev Device": 65,
    "Next Device": 66,
    "Prev Variation": 67,
    "Next Variation": 68,
    "Launch Variation": 69,
    "Store Variation": 70,
    "Recall Last Used": 72, 
    "Randomize Macros": 71,
    "--- Pages ---": 0,
    "Page 1/2": 50,
    "Page 1/3": 51,
    "Prev Page": 56,
    "Next Page": 57,
    "Custom MIDI": 0
  }
led_actions = {
    "Off": 0,
    "--- Global ---": 0,
    "Start/Stop": 1,
    "Metronome": 2,
    "Arrangement Rec": 6,
    "Arrangement Loop": 7,
    "Go to Next Marker": 8,
    "Go to Prev Marker": 9,
    "Add/Delete Marker": 10,
    "Session Rec": 11,
    "Disable Follow Actions": 12,
    "MIDI Recording Quantization": 104,
    "--- Scenes ---": 0,
    "Scene Color": 13,
    "Prev Scene Color": 14,
    "Next Scene Color": 15,
    "--- Tracks ---": 0,
    "Current Track Color": 54,
    "Prev Track Color": 18,
    "Next Track Color": 19,
    "Clip Color": 22,
    "Mute": 24,
    "S Solo": 25,
    "Arm": 26,
    "Stop": 27,
    "--- Looper ---": 0,
    "Prev Looper Track Color": 48,
    "Next Looper Track Color": 49,
    "Looper State": 53,
    "State (LOOPER1)": 77,
    "State (LOOPER2)": 78,
    "State (LOOPER3)": 79,
    "State (LOOPER4)": 80,
    "State (LOOPER5)": 81,
    "State (LOOPER6)": 82,
    "--- Pages ---": 0,
    "Page Color": 58,
  }
slider_actions = {    
    "--- Global ---": 0,
    "Last Selected Parameter": 73,
    "Global Groove Amount": 37,
    "Master Volume": 89,
    "Cue Volume": 90,
    "BPM +/- 1": 87,
    "Crossfader": 111,
    "Track Select": 112,
    "--- Arrangement ---": 0,
    "Skip Fwd/Bckwd": 83,
    "Loop Position": 84,
    "Loop Length": 85,
    "Jump to Next/Prev Marker": 88,
    "Horizontal Zoom": 99,
    "--- Session ---": 0,
    "Scroll Scenes": 86,
    "--- Selected Track ---": 0,
    "Volume": 91,
    "Pan": 96,
    "Send A": 59,
    "Send B": 60,
    "--- Selected Device ---": 0,
    "Parameter 1": 61,
    "Parameter 2": 62,
    "Parameter 3": 63,
    "Parameter 4": 64,
    # "Device 1 Param 1": 92,
    # "Device 1 Param 2": 93,
    # "Device 1 Param 3": 94,
    # "Device 1 Param 4": 95,
    "--- Custom ---": 0,
    "Custom MIDI": 122
  }
display_actions =  {"Scene Name": 0,
                    "Track Name": 1,
                    "Looper Number": 2,
                    "Variation Number": 3,
                    "Left Marker Name": 4,
                    "Setlist Song": 5}

class opencontrol(ControlSurface):

    def __init__(self, *a, **k):
        super(opencontrol, self).__init__(*a, **k)
        self._has_been_identified = False
        self._request_count = 0
        self._last_sent_layout_byte = None
        self.prev_beat = False
        self.previous_quarter = 0
        self.quarter_lock = False
        self._skin = make_default_skin()
        self.linked_page = {0: "None", 1: "None", 2: "None"}
        self.timer = Live.Base.Timer(callback=self.on_timer_reached, interval=150, repeat=False)
        self.timer_running = False
        self.last_message_time = time.time()
        """ calls all the functions to create the buttons and Components"""
        with self.component_guard():
            self._create_buttons()
            self._session = SessionComponent(self, num_tracks=NUM_TRACKS, num_scenes=1, enable_skinning = True)
            self._mixer = MixerComponent(num_tracks=NUM_TRACKS)
            self._mixer.set_parent(self)
            self._session.set_mixer(self._mixer)
            self._transport = TransportComponent(self)
            self._transport.set_session(self._session)
            self._device = DeviceComponent(self, device_selection_follows_track_selection=True)
            self._looper = LooperComponent(self, device_selection_follows_track_selection=False)
            self._create_pages()
            self.set_device_component(self._device)
            self._device.set_mixer(self._mixer)
            self.song().add_current_song_time_listener(self.on_time_change)
            self.song().add_is_playing_listener(self.on_is_playing_change)
            self.application().view.add_focused_document_view_listener(self.on_view_changed)
            # self.set_device_component(self._looper)
            self.check_session_box()
            if Live.Application.get_application().get_major_version() == 9:
                self._create_m4l_interface()

        self.log_message('Loaded %s %s' % (SCRIPT_NAME, SCRIPT_VER))
        self.show_message('Loaded %s %s' % (SCRIPT_NAME, SCRIPT_VER))

    def on_view_changed(self):
        for page in self.linked_page:
            if self.linked_page[page] == self.application().view.focused_document_view and  self.current_page != page:
                self.current_page = page
                self.enable_page()


    def _create_buttons(self):
        """ Create all the buttons one by one then buils the button matrixes if needed"""
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

        clip_launch_row = []

        for i in range(NUM_TRACKS):
            clip_launch_row.append(self.buttons["Launch Clip"])
                    
        self.looper_buttons = ButtonMatrixElement(rows=[[self.buttons["State (LOOPER1)"], self.buttons["State (LOOPER2)"], self.buttons["State (LOOPER3)"],
                                                self.buttons["State (LOOPER4)"], self.buttons["State (LOOPER5)"], self.buttons["State (LOOPER6)"]]])
        self.clip_launch_buttons = ButtonMatrixElement(rows=[clip_launch_row])

    def make_button(self, identifier, channel, name, msg_type = MIDI_CC_TYPE, skin = None, is_modifier = False):
        return ButtonElement(True, msg_type, channel, identifier, skin=self._skin, name=name, resource_type=PrioritizedResource if is_modifier else None)

    def _create_pages(self):
        """ Create pages and Layers"""
        self._pages = ModesComponent(name='pages_0_1', is_enabled=False)

        """Session Actions"""
        self._session_layer_mode = AddLayerMode(self._session, Layer(launch_scene_button=self.buttons["Launch Scene"],
                                                                    scene_bank_up_button=self.buttons["Sel Prev Scene"],
                                                                    scene_bank_down_button=self.buttons["Sel Next Scene"],
                                                                    scene_bank_up_x4_button=self.buttons["Jump 4 Scenes Up"],
                                                                    scene_bank_down_x4_button=self.buttons["Jump 4 Scenes Down"],
                                                                    track_bank_left_button=self.buttons["Sel Prev Track"],
                                                                    track_bank_right_button=self.buttons["Sel Next Track"],
                                                                    find_next_empty_slot=self.buttons["Find Empty Slot"],
                                                                    jump_to_playing_scene=self.buttons["Jump to Playing Scene"],
                                                                    add_audio_track=self.buttons["Add Audio Track"],
                                                                    add_MIDI_track=self.buttons["Add MIDI Track"],
                                                                    insert_scene=self.buttons[ "Insert Scene"],
                                                                    capture_and_insert_scene=self.buttons[ "Capture and Insert Scene"],
                                                                    undo=self.buttons["Undo"],
                                                                    redo=self.buttons["Redo"],
                                                                    mute_button=self.buttons["Mute"],
                                                                    solo_button=self.buttons["S Solo"],
                                                                    arm_button=self.buttons["Arm"],
                                                                    stop_button=self.buttons["Stop"],
                                                                    current_track_color=self.buttons["Current Track Color"],
                                                                    unfold_track=self.buttons["U Fold/Unfold Track"],
                                                                    stop_all_clips_button=self.buttons["Stop All Clips"],
                                                                    clip_launch_buttons=self.clip_launch_buttons,
                                                                    last_selected_parameter=self.buttons["Last Selected Parameter"],
                                                                    main_view_toggle=self.buttons["Arrangement/Session Toggle"],
                                                                    scroll_scenes=self.buttons["Scroll Scenes"],
                                                                    detail_view_toggle=self.buttons["Clip/Device Toggle"],
                                                                    fixed_length_rec_1bars=self.buttons["Fixed Length Rec 1 Bars"],
                                                                    fixed_length_rec_2bars=self.buttons["Fixed Length Rec 2 Bars"],
                                                                    fixed_length_rec_4bars=self.buttons["Fixed Length Rec 4 Bars"],
                                                                    fixed_length_rec_8bars=self.buttons["Fixed Length Rec 8 Bars"],
                                                                    prev_setlist_song=self.buttons[ "Prev Setlist Song"],
                                                                    next_setlist_song=self.buttons["Next Setlist Song"],
                                                                    launch_setlist_song=self.buttons["Launch Setlist Song"],
                                                                    launch_setlist_song_noq=self.buttons["Launch Setlist Song NoQ"],
                                                                    crossfader=self.buttons["Crossfader"]
                                                                    ))

        """Transport Actions"""
        self._transport_mode = AddLayerMode(self._transport, Layer(start_stop=self.buttons["Start/Stop"],
                                                                    continue_playing=self.buttons["Continue Playing"],
                                                                    loop_button=self.buttons["Arrangement Loop"],
                                                                    capture=self.buttons["Capture"],
                                                                    loop_position=self.buttons["Loop Position"],
                                                                    loop_length=self.buttons["Loop Length"],
                                                                    jump_to_start=self.buttons["Jump to 1.1.1"],
                                                                    restart_button=self.buttons["Restart From Last Position"],
                                                                    set_or_delete_cue_button=self.buttons["Add/Delete Marker"],
                                                                    inc_bpm_button=self.buttons["BPM +1"],
                                                                    dec_bpm_button=self.buttons["BPM -1"],
                                                                    inc_dec_bpm_button=self.buttons["BPM +/- 1"],
                                                                    punch_in_button=self.buttons["Punch In"],
                                                                    punch_out_button=self.buttons["Punch Out"],
                                                                    h_zoom=self.buttons["Horizontal Zoom"],
                                                                    back_to_arrangement_button=self.buttons["Back To Arrangement"],
                                                                    midi_recording_quantization_button=self.buttons["MIDI Recording Quantization"],
                                                                    re_enable_automation_button=self.buttons["Re-enable Automation"],
                                                                    prev_cue_button=self.buttons["Go to Prev Marker"],
                                                                    next_cue_button=self.buttons["Go to Next Marker"],
                                                                    prev_next_cue_button=self.buttons["Jump to Next/Prev Marker"],
                                                                    marker_loop_button=self.buttons["Loop to Next Marker"],
                                                                    metronome=self.buttons["Metronome"],
                                                                    record_button=self.buttons["Arrangement Rec"],
                                                                    session_record_button=self.buttons["Session Rec"],
                                                                    skip=self.buttons["Skip Fwd/Bckwd"],
                                                                    groove_amount=self.buttons["Global Groove Amount"]
                                                                    ))
        """Mixer Actions"""
        self._mixer_mode = AddLayerMode(self._mixer, Layer(prehear_volume=self.buttons["Cue Volume"],
                                                            master_volume=self.buttons["Master Volume"],
                                                            volume=self.buttons["Volume"],
                                                            pan=self.buttons["Pan"],
                                                            send_controls=ButtonMatrixElement(rows=[[self.buttons["Send A"], self.buttons["Send B"]]])
                                                            ))
        """Devices Actions"""
        self._device_layer_mode = AddLayerMode(self._device, Layer(launch_variation_button=self.buttons["Launch Variation"],
                                                                    prev_variation_button=self.buttons["Prev Variation"],
                                                                    next_variation_button=self.buttons["Next Variation"],
                                                                    next_device_button=self.buttons["Next Device"],
                                                                    prev_device_button=self.buttons["Prev Device"],
                                                                    store_variation_button=self.buttons["Store Variation"],
                                                                    recall_variation_button=self.buttons["Recall Last Used"],
                                                                    randomize_macros_button=self.buttons["Randomize Macros"],
                                                                    selected_device_parameters=ButtonMatrixElement(rows=[[self.buttons["Parameter 1"], self.buttons["Parameter 2"], self.buttons["Parameter 3"], self.buttons["Parameter 4"]]]),
                                                                    priority=1))

        """Looper Actions"""
        self._looper_layer_mode = AddLayerMode(self._looper, Layer(add_looper = self.buttons["+ Add Looper"],
                                                                    sel_prev_looper=self.buttons["Prev Looper"],
                                                                    sel_next_looper=self.buttons["Next Looper"],
                                                                    arm_looper_track=self.buttons[ "Arm Looper Track"],
                                                                    mute_looper_track=self.buttons["Mute Looper Track"],
                                                                    show_looper=self.buttons["Show Looper"],
                                                                    looper_state=self.buttons["Looper State"],
                                                                    stop_looper=self.buttons["Stop Looper"],
                                                                    clear_all=self.buttons["Clear All"],
                                                                    looper_buttons=self.looper_buttons
                                                                    ))


        """ Pages switching """
        self.pages = 'page_0'
        self.current_page = 0

        active_layers = [self._session_layer_mode, self._mixer_mode, self._transport_mode, self._device_layer_mode, self._looper_layer_mode]
        self._pages.add_mode(self.pages, active_layers)
        self.set_page_0_1_button(self.buttons["Page 1/2"])
        self.set_page_0_2_button(self.buttons["Page 1/3"])
        self.set_prev_page_button(self.buttons["Prev Page"])
        self.set_next_page_button(self.buttons["Next Page"])
        self._pages.selected_mode = self.pages
        self._pages.set_enabled(True)

    def set_page_0_1_button(self, button):
        self.page_0_1_button = button
        self._on_page_0_1_button_value.subject = button

    def set_page_0_2_button(self, button):
        self.page_0_2_button = button
        self._on_page_0_2_button_value.subject = button

    def set_prev_page_button(self, button):
        self.prev_page_button = button
        self._on_prev_page_button_value.subject = button

    def set_next_page_button(self, button):
        self.next_page_button = button
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
        self.show_message('Page %s' % str(self.current_page+1))
        self._send_midi((240, 122, 29, 247))
        self._send_midi((240, 122, 29, 1, 19, 40, self.current_page, 247))
        self.update_pages()

    def update_pages(self):
        self._session.update()
        self._mixer.update()
        self._transport.update()
        self._device.update()
        self._looper.update()

    def handle_sysex(self, midi_bytes):
        """Handle Sysex messages"""
        """ Handles handshake message with the Controller"""
        if not self._has_been_identified and midi_bytes == REPLY_MSG:
            self._has_been_identified = True
            self.set_enabled(True)
            self.set_highlighting_session_component(self._session)
            self.schedule_message(1, self.refresh_state)
        """ If Handshake successful, call the update function for each Layout"""
        if midi_bytes == ACKNOWLEDGMENT_MSG:
            # self._session.scene(0)._on_scene_name_changed()
            # self._mixer.channel_strip(0)._on_track_name_changed()
            # self._device._on_device_name_changed()
            # self._transport._on_prev_cue_name_changed()
            self._session.update()
            self._mixer.update()
            self._transport.update()
            self._device.update()
            self._looper.update()
        """ Handle Option received"""
        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 30):
            """ Option 0 = Metronome blinking"""
            if midi_bytes[6] == 0:
                Options.metronome_blinking = 0 if midi_bytes[7] == 1 else 1
                self._transport._on_metronome_changed()
            """ Option 1 = Session Box enabled"""
            if midi_bytes[6] == 1:
                Options.session_box_linked_to_selection = midi_bytes[7]
                self.check_session_box()
        if midi_bytes[0:6] == (240, 122, 29, 1, 19, 24):
            pages = {0: "None", 1: "Session", 2: "Arranger", 3: "Browser"}
            rcvd = midi_bytes[6]
            self.linked_page[rcvd] = pages[midi_bytes[7]]

    def check_session_box(self):
        self._session._show_highlight = False
        if Options.session_box_linked_to_selection ==0:
            self._session._show_highlight = True
        self._session._do_show_highlight()

    def on_time_change(self):
        self._transport.compare_cue()
  
        if int(self.song().current_song_time) is not self.prev_beat:
            self.prev_beat = int(self.song().current_song_time)
            self._do_send_midi(tuple([251]))

        """ BLINK """
        quarter = self.song().get_current_beats_song_time().sub_division
        if quarter is not self.previous_quarter:
            self.previous_quarter = quarter
            self.send_clock()

    """ DISPLAY """

    def set_temp_message(self, name):
        if not self.timer_running:
            self.timer.start()
            self.timer_running = True
        else:
            self.timer.restart()
        self.temp_message = name
        self.display_temp_message(name)

    def on_timer_reached(self):
        self.timer.stop()
        self.timer_running = False
        self.display_temp_message(self.temp_message)

    def display_temp_message(self, name):
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 54, 3]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self.buttons["Left Marker Name"] is not None and time.time() - self.last_message_time > Options.display_time:
            self.buttons["Left Marker Name"]._send_midi(tuple(message))
            self.last_message_time = time.time()

    def display_message(self, display_type, name):
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 51, display_actions[display_type]]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self.buttons["Left Marker Name"]:     
            self.buttons["Left Marker Name"]._send_midi(tuple(message))

        # """ FADE """  
        # quarter = self.song().get_current_beats_song_time().ticks%20
        # if quarter is not self.previous_quarter:
        #     # print(quarter)
        #     if quarter < 10 and not self.quarter_lock:
        #         self.quarter_lock = True
        #         # print("on")
        #         self.previous_quarter = quarter
        #         self.send_clock()
        #         self._transport.compare_cue()
        #     if quarter > 5 and self.quarter_lock:
        #         self.quarter_lock = False

    def on_is_playing_change(self):
        self._transport._on_start_stop_changed()
        if self.song().is_playing:
            self._do_send_midi(tuple([250]))
        else:
            self._do_send_midi(tuple([252]))
            self.quarter_lock = False
            self.previous_quarter = 100


    def send_clock(self):
        self._do_send_midi(tuple([248]))

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

    # def _create_m4l_interface(self):
    #     """ Creates and sets up the M4L interface for easy interaction from
    #     M4L devices in Live 9. """
    #     from _Framework.M4LInterfaceComponent import M4LInterfaceComponent
    #     self._m4l_interface = M4LInterfaceComponent(controls=self.controls,
    #                                                 component_guard=self.component_guard,
    #                                                 priority=1)
    #     self._m4l_interface.name = 'M4L_Interface'
    #     self._m4l_interface.is_private = True
    #     self.get_control_names = self._m4l_interface.get_control_names
    #     self.get_control = self._m4l_interface.get_control
    #     self.grab_control = self._m4l_interface.grab_control
    #     self.release_control = self._m4l_interface.release_control
        
    def _add_control(self, number):
        return ButtonElement(True, MIDI_CC_TYPE, MIDI_CHANNEL, number)

    # def _add_slider(self, number):
    #     return EncoderElement(MIDI_CC_TYPE, MIDI_CHANNEL, number, Live.MidiMap.MapMode.absolute)

    def disconnect(self):
        super(opencontrol, self).disconnect()
        self._send_midi(prefix + (3, 247))
        self._session = None
