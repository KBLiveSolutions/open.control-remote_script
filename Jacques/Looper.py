import Live
from _Framework.SubjectSlot import subject_slot
from _Framework.Control import ButtonControl
from _Framework.SessionComponent import SessionComponent as SessionBase
from .LooperTrack import LooperTrack
from . import colors
from . import reglages

import logging, traceback
logger = logging.getLogger(__name__)
def print(text):
    logger.warning(text)

ABSOLUTE_TIMING = False
LOOPER_TRACK_NUM = 24
PATT_LENGTH = 8
SENDS_AMOUNT = 12

groups_list = ["A", "B", "C",  "Z"]
chut_track = 23

input_tracks = ["PIEZO1", "PIEZO2", "SPIDERPIEZO", "GRATT", "VOIX", "RADIO", "PHONE", "STATIQUE", "HYDRO", "GUEST"]

class LooperComponent(SessionBase):
    def __init__(self, *a, **k):
        super(LooperComponent, self).__init__(*a, **k)
        self.current_armed_track = None
        self.fired_slot = None
        self.rec_length = reglages.rec_length
        self.initial_pattern = [1, 1, 1, 1, 1, 1, 1, 1]
        self.looper_track = []
        self.recording_track_number = None
        self.selected_looper_track = None
        self.is_record_on = False
        self.shift_rec = False
        self.preset_button_held = False
        self.preset_button_held_2 = False
        self.previous_row = None
        self.inverted_patt = 0
        self.held_button = 0
        self.pattern_copied = False
        self.remise_a_zero = 0
        self.preset_button_held_number = 0
        self.sends_values = {"A": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "B": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "C": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "Z": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.number_of_buttons_held = 0
        self.chut = False
        self.previous_input_track_armed = None
        self.changing_Xbars = False
        self.start_time = 0
        self.timer = Live.Base.Timer(callback=self.on_timer_reached, interval=1, repeat=False)
        self.timer2 = Live.Base.Timer(callback=self.on_timer2_reached, interval=1, repeat=False)
        self.reglages =[reglages.pattern1, reglages.pattern2, reglages.pattern3, reglages.pattern4, reglages.pattern5, reglages.pattern6, reglages.pattern7] 
        self.groups = {"A": [], "B": [], "C":[], "Z":[]}
        self.song().add_session_record_listener(self.is_recording)
        self.song().add_is_playing_listener(self.is_playing)
        self.song().add_tempo_listener(self.on_tempo_changed)
        self.song().add_groove_amount_listener(self.on_groove_amount_changed)
        self.build_tracks()
        self.build_groups()
        clip_color_table = colors.LIVE_COLORS_TO_MIDI_VALUES.copy()  
        self.set_rgb_mode(clip_color_table, colors.RGB_COLOR_TABLE)
        self._enable_skinning()

    def build_tracks(self):
        self.input_tracks = []
        self.instru_tracks =[] 
        for i in range(min(len(self.song().tracks), LOOPER_TRACK_NUM)):
            self.looper_track.append(LooperTrack(self, self.song().tracks[i]))
        for track in self.song().tracks:
            try:
                track.arm=0
            except:
                pass
            if track.name in input_tracks:
                self.input_tracks.append(track)
            if track.name == "INPUT":
                self.input_group_track = track
                for d in self.input_group_track.devices:
                    if d.name == "INPUT FX":
                        self.INPUT_FX_device = d
                    if d.name == "INPUT EQ":
                        self.INPUT_EQ_device = d
                    if d.name == "INPUT GAIN":
                        self.INPUT_GAIN_device = d
            n = None
            if track.name.find("SENDS A DEFAULT") > -1:
                n = "A"
            if track.name.find("SENDS B DEFAULT") > -1:
                n = "B"
            if track.name.find("SENDS C DEFAULT") > -1:
                n = "C"   
            if track.name.find("SENDS Z DEFAULT") > -1:
                n = "Z"
            if n:
                for i in range(12):
                    self.sends_values[n][i] = track.mixer_device.sends[i].value

        for track in self.looper_track:
            for d in track.track.devices:
                if d.name == "INSTRU":
                    self.instru_tracks.append(track)
                if d.name == "FX INSERT":
                    track.INSERT_FX_device = d
          

    def _enable_skinning(self):
        self.set_stop_clip_triggered_value(u'Session.StopClipTriggered')
        self.set_stop_clip_value(u'Session.StopClip')
        for scene_index in range(self._num_scenes):
            scene = self.scene(scene_index)
            # scene.set_scene_value(u'Session.Scene')
            # scene.set_no_scene_value(u'Session.NoScene')
            # scene.set_triggered_value(u'Session.SceneTriggered')
            for track_index in range(self._num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_triggered_to_play_value(colors.pad_play)
                clip_slot.set_triggered_to_record_value(colors.pad_rec)
                clip_slot.set_record_button_value(colors.pad_off)
                clip_slot.set_stopped_value(colors.pad_off  )
                clip_slot.set_started_value(colors.pad_play)
                clip_slot.set_recording_value(colors.pad_rec)

    def is_recording(self):
        self.is_record_on = self.song().session_record

    def is_playing(self):
        self.is_playing = self.song().is_playing
        color = colors.pad_play
        if not self.is_playing:
            for looper_track in self.looper_track:
                looper_track.current_step = 0
                looper_track.show_sequence()
            color = colors.pad_off
        self._start_stop_button.send_value(color, force=True)

    def on_selected_looper_track_changed(self, looper_track):
        try:
            if self.selected_looper_track is not looper_track:
                self.selected_looper_track.select_looper_track(False)
                self.selected_looper_track = looper_track
                self.selected_looper_track.select_looper_track(True)
        except:
            self.selected_looper_track = looper_track
            self.selected_looper_track.select_looper_track(True)

    """ SET BUTTONS """
    def set_looper_launch_buttons(self, buttons):
        self.looper_launch_buttons = buttons
        self.on_looper_launch_button_pressed.subject = buttons
        for b in buttons:
            b.send_value(colors.looper_off, force=True)     
        for i in range(LOOPER_TRACK_NUM):
            self.looper_track[i].launch_button = buttons[i]  
    def set_stop_rec_buttons(self, buttons):
        self.stop_rec_buttons = buttons
        self.on_stop_rec_button_pressed.subject = buttons
    def set_remise_a_zero_button(self, button):
        self.remise_a_zero_button = button
        self.on_remise_a_zero_button_pressed.subject = button
    def set_rotate_pattern(self, button):
        self.rotate_pattern_button = button
        self.on_rotate_pattern.subject = button
    def set_chut_button(self, button):
        self.chut_button = button
        self.on_chut_button_pressed.subject = button
        button.send_value(colors.chut_on, force=True)
    def set_silencer_sequence_buttons(self, buttons):
        self.silencer_sequence_buttons = buttons
        self.on_silencer_buttons_pressed.subject = buttons
        for i in range(LOOPER_TRACK_NUM):
            self.looper_track[i].silencer_sequence_buttons = buttons[i*PATT_LENGTH:(i+1)*PATT_LENGTH]
            self.looper_track[i].show_sequence()
    def set_silencer_preset_buttons(self, buttons):
        self.silencer_preset_buttons = buttons
        self.on_silencer_preset_buttons_pressed.subject = buttons
        for b in buttons:
            b.send_value(colors.seq_preset_off, force=True)
    def set_sends_matrix_buttons(self, buttons):
        self.sends_matrix_buttons = buttons
        self.set_sends_matrix_buttons_value.subject = buttons
        for i in range(len(buttons)):
            index = int(i/SENDS_AMOUNT)
            control = i%SENDS_AMOUNT
            value = self.sends_values[groups_list[index]][control]*127
            buttons[i].send_value(value, force=True)

    def set_change_group_buttons(self, buttons):
        self.change_group_buttons = buttons
        self.on_change_group_button_pressed.subject = buttons
        for b in range(len(buttons)):
            t = int(b / 4)+4
            g = b % 4
            self.looper_track[t].group_buttons[g] = buttons[b]
        for i in range(20):
            self.looper_track[i+4].update_group()
    def set_instru_macro_knobs(self, buttons):
        self.instru_macro_knobs = buttons
        self.on_instru_macro_changed.subject = buttons
        for i in range(4):
            self.instru_tracks[i].INSTRU_macro_buttons = buttons[i*16:(i+1)*16]
    def set_instru_chain_selectors(self, buttons):
        self.instru_chain_selectors = buttons
        self.on_instru_chain_selector_changed.subject = buttons
        for i in range(4):
            self.instru_tracks[i].INSTRU_chain_selector_buttons = buttons[i*15:(i+1)*15]
            self.instru_tracks[i].on_chain_selector_changed(0)
    def set_shift_rec_button(self, button):
        self.shift_rec_button = button
        self.on_shift_rec_button_pressed.subject = button
        button.send_value(colors.shift_rec, force=True)
    def set_volume_faders(self, buttons):
        self.volume_faders = buttons
        self.on_volume_faders_changed.subject = buttons
    def set_start_stop(self, button):
        self._start_stop_button = button
        self.on_start_stop_pressed.subject = button
        self.is_playing()
    def set_cancel_rec(self, button):
        self._cancel_rec_button = button
        self.on_cancel_rec_pressed.subject = button
    def set_scene_bank_up_button(self, button):
        self._scene_bank_up_button = button
        self._scene_bank_up_value.subject = button
        self._scene_bank_up_button.send_value(97, force=True)
    def set_scene_bank_down_button(self, button):
        self._scene_bank_down_button = button
        self._scene_bank_down_value.subject = button
        self._scene_bank_down_button.send_value(97, force=True)
    def set_arm_input_buttons(self, buttons):
        self._arm_input_buttons = buttons
        self.on_arm_input_buttons_pressed.subject = buttons
    def set_bpm_inc_dec(self, button):
        self._bpm_inc_dec_button = button
        self.on_bpm_inc_dec_changed.subject = button   
        self.on_tempo_changed()
    def set_input_eq(self, buttons):
        self._input_eq_buttons = buttons
        self.on_input_eq_buttons_pressed.subject = buttons
    def set_input_gain(self, buttons):
        self._input_gain_buttons = buttons
        self.on_input_gain_buttons_pressed.subject = buttons

    """ GLOBAL """

    def set_groove_amount(self, button):
        self._groove_amount_button = button
        self.on_groove_amount_button_changed.subject = button   
        self.on_groove_amount_changed()

    @subject_slot('value')
    def on_groove_amount_button_changed(self, value):
        self.song().groove_amount = value/127*1.3125

    @subject_slot('value')
    def on_start_stop_pressed(self, value):
        if self.is_enabled() and self._start_stop_button:
            if value:
                self.song().stop_playing() if self.song().is_playing else self.song().start_playing()

    @subject_slot('value')
    def on_bpm_inc_dec_changed(self, value):
        if self.is_enabled() and self._start_stop_button:
            if value>63 and self.song().tempo < reglages.tempo["max"]:
                self.song().tempo += 1
            if value<63 and self.song().tempo > reglages.tempo["min"]:
                self.song().tempo -= 1

    def on_tempo_changed(self):
        tempo = min((self.song().tempo - reglages.tempo["min"]) / (reglages.tempo["max"] - reglages.tempo["min"]) * 127, 127)
        self._bpm_inc_dec_button.send_value(tempo, force=True)
    
    def on_groove_amount_changed(self):
        self._groove_amount_button.send_value(self.song().groove_amount/1.3125*127, force=True)

    @subject_slot('value')
    def _scene_bank_up_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), max(0, self.scene_offset() - 1))

    @subject_slot('value')
    def _scene_bank_down_value(self, value):
        if value:
            self.set_offsets(self.track_offset(), self.scene_offset() + 1)

    @subject_slot('value')
    def on_volume_faders_changed(self, *args):
        track = self.song().tracks[args[1]]
        track.mixer_device.volume.value = args[0]/127*0.85

    def update_display(self):
        for i in range(min(len(self.song().tracks), LOOPER_TRACK_NUM)):
            self.looper_track[i].show_sequence()
            self.looper_track[i].update_group()
            self.looper_track[i].update_launch_button()

    """ LOOPER """

    @subject_slot('value')
    def on_looper_launch_button_pressed(self, *args):   # on appuie sur un bouton de launch de rec
        if not self.changing_Xbars:     # si on est pas en mode de changement de XBars
            if args[0] and not self.is_record_on:   # si on n'est pas deja en train d'enregistrer
                track = self.song().tracks[args[1]]     #on recupere la piste sur laquelle on enregistre
                self.recording_track_number = args[1]      # le numero de cette piste
                self.start_recording(track)     # on lance la fonction start_recording
                self.stop_rec_buttons[1].send_value(127, force=True)    # on met le bouton du footswitch en rouge
                self._cancel_rec_button.send_value(0, force=True)   # on met le bouton d'effacement du clip en blanc
        else:   # on est en mode de changement de XBars 
            index = reglages.Xbar_values.index(self.rec_length[self.footswitch_number])
            self.looper_launch_buttons[index].send_value(colors.pad_off, force=True)
            self.rec_length[self.footswitch_number] = reglages.Xbar_values[args[1]]
            self.looper_launch_buttons[args[1]].send_value(colors.Xbar_select_colors[self.footswitch_number], force=True)

    def start_recording(self, track):
        if self.current_armed_track:    # on desarme la piste precedemment armee
            self.current_armed_track.arm = 0
        self.current_armed_track = track    # on reassigne self.current_armed_track
        track.arm = 1 # on arme la piste
        track.mute = 0  # on demute la piste
        scene_index = self.find_next_available_slot() # on trouve le prochain slot vide
        track.stop_all_clips(Quantized=False)   # on arrete les clips en lecture sur la piste
        self.fired_slot = track.clip_slots[scene_index] # on assigne self.fired_slot
        self.fired_slot.fire(launch_quantization=0)     # on lance le rec sur self.fired_slot
        self.on_selected_looper_track_changed(self.looper_track[self.recording_track_number])   # on reassigne selected_looper_track
        self.looper_track[self.recording_track_number].recording_started(self.shift_rec)    # on signale à la LooperTrack qu'elle est en rec

    def find_next_available_slot(self):
        song = self.song()
        scene_count = len(song.scenes)
        scene_index = 0
        while self.current_armed_track.clip_slots[scene_index].has_clip:
            scene_index += 1
            if scene_index == scene_count:
                song.create_scene(scene_count)
        return scene_index

    @subject_slot('value')
    def on_stop_rec_button_pressed(self, *args):    # si le pedalier a ete appuye
        if args[0] and self.fired_slot and self.is_record_on: 
            clip = self.fired_slot.clip
            self.current_length = self.rec_length[args[1]]  # nombre de beats de la pedale pressee
            current_clip_position = clip.playing_position   # position dans le clip au moment ou on appuie sur la pedale
            if current_clip_position > self.current_length: # si la longueur du clip est superieure a celle donnee par la pedale
                """ C'EST ICI QUE TOUT SE JOUE #1 """
                self.current_armed_track.stop_all_clips(Quantized=False)    # on arrete le clip sans quantification
                clip.loop_start = current_clip_position - self.current_length  # on positionne le point de start de la boucle X beats avant le point de fin
                clip.loop_end = current_clip_position   # on positionne le marqueur de fin de boucle sur le moment d'appui sur la pedale
                clip.end_marker = current_clip_position # on positionne le marqueur de fin de clip sur le moment d'appui sur la pedale
                self.start_time = clip.start_time   # on recupere le beut d'enregistrement du clip par rapport a l'horloge de Live
                self.timer.start()  # on lance un premier Timer parce que l'action suivante doit etre differee
                self.looper_track[self.recording_track_number].recording_stopped(clip) # on signale a LooperTrack que le clip a ete enregistre
                self.stop_rec_buttons[1].send_value(0, force=True)  # on met la LED du footsiwtch en vert

    def on_timer_reached(self):
            self.timer.stop()   # on arrete le premier Timer
            clip = self.fired_slot.clip
            length = self.current_length
            """ C'EST ICI QUE TOUT SE JOUE #2 """
            offset = length - self.start_time % length + self.song().tempo/60* reglages.compensation  # on calcule l'offset pour le marqueur Start du Clip
            try:
                clip.start_marker =  offset + length * (int(clip.loop_end / length))    # on essaie de le mettre a l'interieur du clip
            except:
                clip.start_marker =  offset + length * (int(clip.loop_end / length)-1)  # si le calcul ne passe pas, on le decale d'une mesure avant
            self.fired_slot.fire(launch_quantization=0) # on relance la lecture du Clip
            self.timer2.start() # on lance le deuxième Timer

    def on_timer2_reached(self):
        self.timer2.stop()  # on arrete le deuxieme Timer
        clip = self.fired_slot.clip
        """ C'EST ICI QUE TOUT SE JOUE #3 """
        offset = clip.loop_start - clip.start_marker + self.song().tempo/60* (0.04 + reglages.compensation)    # on calcule l'offset pour repositionner la position de lecture du Clip
        clip.move_playing_pos(offset)   # on repositionne le Clip
        self._cancel_rec_button.send_value(127, force=True) # on allume le bouton d'annulation de Rec


    @subject_slot('value')
    def on_shift_rec_button_pressed(self, value):
        self.shift_rec = False
        if value:
            self.shift_rec = True

    @subject_slot('value')
    def on_cancel_rec_pressed(self, value):
        if value:
            if self.fired_slot.has_clip:
                self.fired_slot.delete_clip()
                self._cancel_rec_button.send_value(0, force=True)

    """ ARMING / INPUTS """

    @subject_slot('value')
    def on_arm_input_buttons_pressed(self, *args):
        if args[0]:
            if self.previous_input_track_armed is not None:
                self.input_tracks[self.previous_input_track_armed].arm = 0
                self._arm_input_buttons[self.previous_input_track_armed].send_value(0, force=True)
            self.input_tracks[args[1]].arm = 1
            self.previous_input_track_armed = args[1]
            self.INPUT_FX_device.parameters[17].value = args[1]
            self.INPUT_FX_device.selected_variation_index = args[1]
            self.INPUT_FX_device.recall_selected_variation()
            self._arm_input_buttons[self.previous_input_track_armed].send_value(127, force=True)
            for i in range(8):
                self._macros_input[i].send_value(self.INPUT_FX_device.parameters[i+1].value, force=True)

    def set_macros_input_buttons(self, buttons):
        self._macros_input = buttons
        self.on_macros_input_buttons_pressed.subject = buttons
        for b in buttons:
            b.send_value(127, force=True)

    @subject_slot('value')
    def on_input_eq_buttons_pressed(self, *args):
        if args[0]:
            current = self.INPUT_EQ_device.parameters[17].value
            _max = len(self.INPUT_EQ_device.chains)
            step = -1
            if args[1] == 1:
                step = 1
            self.INPUT_EQ_device.parameters[17].value = self.cycle(current, _max, step)

    @subject_slot('value')
    def on_input_gain_buttons_pressed(self, *args):
        if args[0]:
            current = self.INPUT_GAIN_device.parameters[17].value
            _max = len(self.INPUT_GAIN_device.chains)
            step = -1
            if args[1] == 1:
                step = 1
            self.INPUT_GAIN_device.parameters[17].value = self.cycle(current, _max, step)

    def cycle(self, current, _max, step):
        value = current+step
        if value == _max:
            value = 0
        elif value < 0:
            value = _max-1
        return value
  
    """ SILENCER """

    @subject_slot('value')
    def on_chut_button_pressed(self, value):
        if value:
            self.chut = True
            self.chut_button.send_value(colors.chut_on_2, force=True)
            for l in range(LOOPER_TRACK_NUM):
                if l is not chut_track:
                    for i in range(PATT_LENGTH):
                        color=colors.chut_on_2 if self.looper_track[l].chut_pattern[i] == 1 else colors.chut_off
                        self.looper_track[l].silencer_sequence_buttons[i].send_value(color, force=True)
                else:
                    for i in range(PATT_LENGTH):
                        color=colors.chut_on if self.initial_pattern[i] == 1 else colors.chut_off
                        self.looper_track[chut_track].silencer_sequence_buttons[i].send_value(color, force=True)
            for i in range(7):
                self.silencer_preset_buttons[i].send_value(colors.Xbar_select_colors[6-i], force=True)

        else:
            for i in range(PATT_LENGTH):
                self.looper_track[chut_track].silencer_sequence_buttons[i].send_value(colors.chut_off, force=True)
            self.chut_button.send_value(colors.chut_on, force=True)
            self.chut = False
            self.changing_Xbars = False
            for button in self.silencer_preset_buttons:
                button.send_value(colors.seq_preset_off, force=True)
            for track in self.looper_track:
                track.initial_pattern = self.initial_pattern
                track.update_launch_button()
                track.show_sequence()
            
    @subject_slot('value')
    def on_silencer_buttons_pressed(self, *args):
        row = int(args[1]/PATT_LENGTH)
        col = args[1]%PATT_LENGTH
        value = args[0]
        if row is self.recording_track_number and self.is_record_on:
            pass
        else:
            if self.chut: 
                self.edit_chut_mode(row, col, value)
            elif self.preset_button_held: 
                self.edit_preset_mode(row, col, value)
            else: 
                self.edit_normal_mode(row, col, value)

    def edit_normal_mode(self, row, col, value):
        if value: 
            self.on_selected_looper_track_changed(self.looper_track[row])
            if self.pattern_copied:
                # invert copied pattern
                pass
            if self.number_of_buttons_held == 1:
                if self.held_button and self.held_button is not row:
                    self.copy_pattern(self.held_button, row)
                    self.pattern_copied = True
            self.number_of_buttons_held += 1
        if value == 0: 
            if self.number_of_buttons_held >= 1 and not self.pattern_copied:
                self.held_button = row
                self.looper_track[row].on_seq_button_pressed(col)
            self.number_of_buttons_held -= 1
            if self.number_of_buttons_held == 0 and self.pattern_copied:
                self.pattern_copied = False
                self.held_button = None

    def copy_pattern(self, source, target):
        for i in range(PATT_LENGTH):
            self.looper_track[target].sequence[i] = self.looper_track[source].sequence[i]
        self.looper_track[target].show_sequence()

    def edit_chut_mode(self, row, col, value):
        if row is not chut_track:
            if value == 0:
                    self.looper_track[row].set_chut_pattern(row, col)
        else:
            if value:
                self.initial_pattern[col] = 0 if self.initial_pattern[col] == 1 else 1
                color=colors.chut_on if self.initial_pattern[col] == 1 else colors.chut_off
                self.looper_track[chut_track].silencer_sequence_buttons[col].send_value(color, force=True)

    @subject_slot('value')
    def on_silencer_preset_buttons_pressed(self, *args):
        if self.chut:
            self.changing_Xbar_values(args[0], 6-args[1])
        else:
            self.normal_preset_mode(args[0], args[1])

    def changing_Xbar_values(self, value, num):
        if value:
            self.footswitch_number = num
            self.changing_Xbars = True
            index = reglages.Xbar_values.index(self.rec_length[num])
            for i in range(LOOPER_TRACK_NUM):
                if index == i:
                    color = colors.Xbar_select_colors[num]
                else:
                    color = colors.pad_off
                self.looper_launch_buttons[i].send_value(color, force=True)

    def normal_preset_mode(self, value, num):
        if value:
            self.preset_button_held_number = num
            self.preset_button_held = True
            self.silencer_preset_buttons[num].send_value(colors.seq_preset_on, force=True)
        if value == 0:
            if not self.preset_button_held_2:
                self.change_silencer_preset(num)
            self.silencer_preset_buttons[num].send_value(colors.seq_preset_off, force=True)
            self.preset_button_held = False
            self.preset_button_held_2 = False

    def edit_preset_mode(self, row, col, value):
            if value: 
                self.on_selected_looper_track_changed(self.looper_track[row])
                if self.preset_button_held:
                    self.change_silencer_preset(self.preset_button_held_number)
            if value == 0: 
                if self.preset_button_held:
                    self.preset_button_held_2 = True

    def change_silencer_preset(self, preset_number):
            if self.selected_looper_track:
                if self.selected_looper_track.previous_preset and preset_number == self.selected_looper_track.previous_preset:
                    self.invert_pattern(self.selected_looper_track)
                else:
                    self.selected_looper_track.sequence = self.reglages[preset_number]
                    self.selected_looper_track.previous_preset = preset_number
                    self.selected_looper_track.show_sequence()

    def invert_pattern(self, looper_track):
        for i in range(PATT_LENGTH):
            looper_track.sequence[i] = 1 if looper_track.sequence[i] == 0 else 0
            looper_track.show_sequence()

    @subject_slot('value')
    def on_remise_a_zero_button_pressed(self, value):
        if value:
            self.remise_a_zero = self.get_max_clip_length()

    def get_max_clip_length(self):
        max_length = 0
        for l in self.looper_track:
            clip_length = l.clip_length
            if clip_length is not None and clip_length > max_length:
                max_length = clip_length
        return max_length

    @subject_slot('value')
    def on_rotate_pattern(self, value):
        if value>64:
            direction = "right"
        else:
            direction = "left"  
        self.selected_looper_track.rotate_pattern(direction)

    """ SENDS """

    @subject_slot('value')
    def set_sends_matrix_buttons_value(self, *args):
        index = int(args[1]/SENDS_AMOUNT)
        control = args[1]%SENDS_AMOUNT
        value = args[0]/127 
        self.sends_values[groups_list[index]][control] = value
        for looper_track in self.groups[groups_list[index]]:
            looper_track.track.mixer_device.sends[control].value = value
    
    """ GROUPS """
    def build_groups(self):
        for track in self.looper_track:
            group = track.group
            self.groups[group].append(track)

    @subject_slot('value')
    def on_change_group_button_pressed(self, *args):
        if args[0]:
            track_num = int(args[1]/4)+4
            group = args[1]%4
            self.set_track_in_group(self.looper_track[track_num], groups_list[group])

    def set_track_in_group(self, looper_track, group):
        self.groups[looper_track.group].remove(looper_track)
        self.groups[group].append(looper_track)
        looper_track.change_group(group)

      
    """ KNOBS """

    @subject_slot('value')
    def on_instru_macro_changed(self, *args):
        self.instru_tracks[args[2]].on_macro_changed(args[1]+1, args[0])

    @subject_slot('value')
    def on_instru_chain_selector_changed(self, *args):
        if args[0]:
            self.instru_tracks[args[2]].on_chain_selector_changed(args[1])
        
    @subject_slot('value')
    def on_macros_input_buttons_pressed(self, *args):
        self.input_group_track.devices[0].parameters[args[1]+1].value = args[0]
