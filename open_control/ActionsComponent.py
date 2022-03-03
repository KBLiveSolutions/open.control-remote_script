import Live
from _Framework.SubjectSlot import subject_slot
from _Framework.SubjectSlot import subject_slot
from _Framework.CompoundComponent import CompoundComponent
from .consts import *
import sys, os
from .ClyphXTrackActions import ClyphXTrackActions
# from .ClyphXSnapActions9 import ClyphXSnapActions
from .ClyphXGlobalActions import ClyphXGlobalActions
from .ClyphXDeviceActions import ClyphXDeviceActions
from .ClyphXDRActions9 import ClyphXDRActions9
from .ClyphXClipActions import ClyphXClipActions
# from .ClyphXControlSurfaceActions9 import ClyphXControlSurfaceActions9 # specialized version for L9
# from .ClyphXTriggers import ClyphXTrackComponent, ClyphXControlComponent, ClyphXCueComponent
# from .ClyphXUserActions import ClyphXUserActions
# from .ClyphXM4LBrowserInterface import ClyphXM4LBrowserInterface

class UserAction:
    def __init__(self, action_name, *a, **k):
        if action_name.startswith("["):
            self.name = action_name
        else:
            self.name = "[] " + action_name
        super(UserAction, self).__init__(*a, **k)

    def update_custom_action(self, action_name):
        if action_name.startswith("["):
            self.name = action_name
        else:
            self.name = "[] " + action_name

class ActionsComponent(CompoundComponent):

    def __init__(self, parent, *a, **k):
        super(ActionsComponent, self).__init__(*a, **k)
        self.transport = parent._transport
        self.session = parent._session
        self._global = ClyphXGlobalActions(self)
        self._track_actions = ClyphXTrackActions(self)
        self._clip_actions = ClyphXClipActions(self)
        self._device_actions = ClyphXDeviceActions(self)
        self._dr_actions = ClyphXDRActions9(self)
        self._is_debugging = False
        self._play_seq_clips = {}
        self.global_actions = {'ASN' : self._global.do_variable_assignment,
                            'ADDAUDIO' : self._global.create_audio_track,
                            'ADDMIDI' : self._global.create_midi_track,
                            'INSAUDIO' : self._global.insert_and_configure_audio_track,
                            'INSMIDI' : self._global.insert_and_configure_midi_track,
                            'ADDRETURN' : self._global.create_return_track,
                            'ADDSCENE' : self._global.create_scene,
                            'DELSCENE' : self._global.delete_scene,
                            'DUPESCENE' : self._global.duplicate_scene,
                            'LOADDEV' : self._global.load_device,
                            'LOADM4L' : self._global.load_m4l,
                            'SWAP' : self._global.swap_device_preset,
                            'SREC' : self._global.set_session_record,
                            'SRECFIX' : self._global.trigger_session_record,
                            'SATM' : self._global.set_session_automation_record,
                            'B2A' : self._global.set_back_to_arrange,
                            'RPT' : self._global.set_note_repeat,
                            'SWING' : self._global.adjust_swing,
                            'BPM' : self._global.adjust_tempo,  
                            'DEVFIRST' : self._global.move_to_first_device, 
                            'DEVLAST' : self._global.move_to_last_device, 
                            'DEVLEFT' : self._global.move_to_prev_device, 
                            'DEVRIGHT' : self._global.move_to_next_device, 
                            'FOCBRWSR' : self._global.focus_browser,
                            'FOCDETAIL' : self._global.focus_detail,
                            'FOCMAIN' : self._global.focus_main,
                            'GQ' : self._global.adjust_global_quantize,
                            'GRV' : self._global.adjust_groove,
                            'HZOOM' : self._global.adjust_horizontal_zoom,
                            'VZOOM' : self._global.adjust_vertical_zoom,
                            'UP' : self._global.move_up,
                            'DOWN' : self._global.move_down,
                            'LEFT' : self._global.move_left,
                            'RIGHT' : self._global.move_right,
                            'LOOP' : self._global.do_loop_action,
                            'LOC' : self._global.do_locator_action,
                            'LOCLOOP' : self._global.do_locator_loop_action,
                            'METRO' : self._global.set_metronome, 
                            'MIDI': self._global.send_midi_message,
                            'OVER' : self._global.set_overdub,    
                            'PIN' : self._global.set_punch_in,
                            'POUT' : self._global.set_punch_out,
                            'REC' : self._global.set_record,
                            'REDO' : self._global.set_redo,
                            'UNDO' : self._global.set_undo,
                            'RESTART' : self._global.restart_transport,
                            'RQ' : self._global.adjust_record_quantize,
                            'RTRIG': self._global.retrigger_recording_clips,
                            'SIG' : self._global.adjust_time_signature,
                            'SCENE' : self._global.set_scene,
                            'SHOWCLIP' : self._global.show_clip_view,
                            'SHOWDEV' : self._global.show_track_view,
                            'SHOWDETAIL' : self._global.show_detail_view,
                            'TGLBRWSR': self._global.toggle_browser,
                            'TGLDETAIL': self._global.toggle_detail_view,
                            'TGLMAIN': self._global.toggle_main_view,
                            'STOPALL' : self._global.set_stop_all,
                            'SETCONT' : self._global.set_continue_playback,
                            'SETLOC' : self._global.set_locator,
                            'SETSTOP' : self._global.set_stop_transport,
                            'SETFOLD' : self._global.set_fold_all,
                            'SETJUMP' : self._global.set_jump_all,
                            'TAPBPM' : self._global.set_tap_tempo,
                            'UNARM' : self._global.set_unarm_all,
                            'UNMUTE' : self._global.set_unmute_all,
                            'UNSOLO' : self._global.set_unsolo_all,
                            'MAKE_DEV_DOC': self._global.make_instant_mapping_docs}

        self.track_actions = {'ARM' : self._track_actions.set_arm, 
                                'MUTE' : self._track_actions.set_mute, 
                                'SOLO' : self._track_actions.set_solo,
                                'MON' : self._track_actions.set_monitor,
                                'XFADE' : self._track_actions.set_xfade,
                                'SEL' : self._track_actions.set_selection,
                                'ADDCLIP' : self._track_actions.create_clip,
                                'DEL' : self._track_actions.delete_track,
                                'DELDEV' : self._track_actions.delete_device,
                                'DUPE' : self._track_actions.duplicate_track,
                                'FOLD' : self._track_actions.set_fold,
                                'PLAY' : self._track_actions.set_play,
                                'PLAYL' : self._track_actions.set_play_w_legato,
                                'PLAYQ' : self._track_actions.set_play_w_force_qntz,
                                'PLAYLQ' : self._track_actions.set_play_w_force_qntz_and_legato,
                                'STOP' : self._track_actions.set_stop,
                                'JUMP' : self._track_actions.set_jump,
                                'VOL' : self._track_actions.adjust_volume,
                                'PAN' : self._track_actions.adjust_pan,
                                'SEND' : self._track_actions.adjust_sends,
                                'CUE' : self._track_actions.adjust_preview_volume,
                                'XFADER' : self._track_actions.adjust_crossfader,
                                'IN' : self._track_actions.adjust_input_routing,
                                'INSUB' : self._track_actions.adjust_input_sub_routing,
                                'OUT' : self._track_actions.adjust_output_routing,
                                'OUTSUB' : self._track_actions.adjust_output_sub_routing,
                                'NAME' : self._track_actions.set_name,
                                'RENAMEALL' : self._track_actions.rename_all_clips}  

        self.device_actions = {'CSEL' : self._device_actions.adjust_selected_chain,
                                'CS' : self._device_actions.adjust_chain_selector, 
                                'RESET' : self._device_actions.reset_params, 
                                'RND' : self._device_actions.randomize_params, 
                                'SEL' : self._device_actions.select_device,
                                'SET' : self._device_actions.set_all_params,
                                'P1' : self._device_actions.adjust_best_of_bank_param, 
                                'P2' : self._device_actions.adjust_best_of_bank_param, 
                                'P3' : self._device_actions.adjust_best_of_bank_param, 
                                'P4' : self._device_actions.adjust_best_of_bank_param,
                                'P5' : self._device_actions.adjust_best_of_bank_param, 
                                'P6' : self._device_actions.adjust_best_of_bank_param, 
                                'P7' : self._device_actions.adjust_best_of_bank_param, 
                                'P8' : self._device_actions.adjust_best_of_bank_param, 
                                'B1' : self._device_actions.adjust_banked_param, 
                                'B2' : self._device_actions.adjust_banked_param, 
                                'B3' : self._device_actions.adjust_banked_param, 
                                'B4' : self._device_actions.adjust_banked_param, 
                                'B5' : self._device_actions.adjust_banked_param, 
                                'B6' : self._device_actions.adjust_banked_param, 
                                'B7' : self._device_actions.adjust_banked_param, 
                                'B8' : self._device_actions.adjust_banked_param}

        self.looper_actions = {'LOOPER' : self._device_actions.set_looper_on_off, 
                                'REV' : self._device_actions.set_looper_rev, 
                                'OVER' : self._device_actions.set_looper_state,
                                'PLAY' : self._device_actions.set_looper_state, 
                                'REC' : self._device_actions.set_looper_state, 
                                'STOP': self._device_actions.set_looper_state}   

        self.clip_actions = {'CENT' : self._clip_actions.adjust_detune,
                                'SEMI' : self._clip_actions.adjust_transpose,
                                'GAIN' : self._clip_actions.adjust_gain,
                                'CUE' : self._clip_actions.adjust_cue_point,
                                'END' : self._clip_actions.adjust_end,
                                'START' : self._clip_actions.adjust_start,
                                'GRID' : self._clip_actions.adjust_grid_quantization,
                                'TGRID' : self._clip_actions.set_triplet_grid,
                                'ENVINS' : self._clip_actions.insert_envelope,
                                'ENVCLR' : self._clip_actions.clear_envelope,
                                'ENVCAP' : self._clip_actions.capture_to_envelope,
                                'ENVSHOW' : self._clip_actions.show_envelope,
                                'ENVHIDE' : self._clip_actions.hide_envelopes,
                                'QNTZ' : self._clip_actions.quantize,
                                'EXTEND' : self._clip_actions.duplicate_clip_content,
                                'DEL' : self._clip_actions.delete_clip,
                                'DUPE' : self._clip_actions.duplicate_clip,
                                'CHOP' : self._clip_actions.chop_clip,
                                'SPLIT' : self._clip_actions.split_clip,
                                'WARPMODE' : self._clip_actions.adjust_warp_mode,
                                'LOOP' : self._clip_actions.do_clip_loop_action,
                                'SIG' : self._clip_actions.adjust_time_signature,
                                'WARP' : self._clip_actions.set_warp,
                                'NAME' : self._clip_actions.set_clip_name} 

        self.dr_actions = {'SCROLL' : self._dr_actions.scroll_selector,
                            'UNMUTE' : self._dr_actions.unmute_all,
                            'UNSOLO' : self._dr_actions.unsolo_all
                        }

        self.get_user_settings()
        self.scan_clips()

    def scan_clips(self):
        self.ca_clips = []
        for t in self.song().tracks:
            for s in range(len(self.song().scenes)):
                clip_slot = t.clip_slots[s]
                if clip_slot.has_clip:
                    self.find_action(clip_slot.clip)
                    
    @property
    def selected_scene(self):
        return self.session._scene_offset

    @property
    def selected_track(self):
        return self.session._track_offset

#     ==============================
#             CUSTOM
#     ==============================  

    def on_selected_clip_changed(self):
        if self._song.view.highlighted_clip_slot.clip:
            self._on_clip_name_changed.subject = self._song.view.highlighted_clip_slot.clip

    @subject_slot('name')
    def _on_clip_name_changed(self):
        clip = self._song.view.highlighted_clip_slot.clip
        self.find_action(clip)

    def find_action(self, clip):
        index_1 = clip.name.find("(CA")
        if index_1 > -1:
            index_2 = clip.name.find(")")
            num = int(clip.name[index_1+3:index_2])
            if num not in self.custom_action.keys():
                self.custom_action[num] = UserAction(clip.name)
            if not clip.playing_status_has_listener(self.on_ca_clip_playing):
                clip.add_playing_status_listener(self.on_ca_clip_playing)
            self.ca_clips.append(clip)
            print([num, self.custom_action[num].name])

    def on_ca_clip_playing(self):
        for clip in self.ca_clips:
            if clip.is_playing:
                print(clip.name)
                index_1 = clip.name.find("(CA")
                if index_1 > -1:
                    index_2 = clip.name.find(")")
                    num = int(clip.name[index_1+3:index_2])
                self.custom_action[num].update_custom_action(clip.name)

    def set_custom_buttons(self, buttons):
        self.custom_buttons = buttons
        self.on_custom_button_pressed.subject = buttons

    @subject_slot('value')
    def on_custom_button_pressed(self, *args):
            value = args[0]
            btn_num = args[1]
            xtrigger = self.custom_action[btn_num]
            if xtrigger:
                print(btn_num, value, xtrigger.name)
                self.custom_handle_action_list_trigger(value, self.song().view.selected_track, xtrigger)

    def get_user_settings(self):
        self.custom_action = {}
        """ Get user settings (variables, prefs and control settings) from text file and perform startup actions if any """
        path = os.path.dirname(os.path.abspath(__file__))
        user_file = path + '/CUSTOM_ACTIONS.txt'
        for line in open(user_file): 
            print(line)
            if line.startswith("CUSTOM_ACTION["):
                button_number = line[14:line.find("]")]
                action = line[line.find("=")+1:]
                self.custom_action[int(button_number)] = UserAction(action)


    def action_dispatch(self, tracks, xclip, action_name, args, ident):
        """ Main dispatch for calling appropriate class of actions, passes all necessary arguments to class method """
        if tracks:
            if action_name.startswith('SNAP'):
                self._snap_actions.store_track_snapshot(tracks, xclip, ident, action_name, args) 
            elif action_name.startswith('SURFACE') or action_name.startswith('CS'):
                self._control_surface_actions.dispatch_cs_action(tracks[0], xclip, ident, action_name, args)
            elif action_name.startswith('ARSENAL'):
                self._control_surface_actions.dispatch_arsenal_action(tracks[0], xclip, ident, action_name, args)
            elif action_name.startswith('PUSH'):
                self._control_surface_actions.dispatch_push_action(tracks[0], xclip, ident, action_name, args)
            elif action_name.startswith('PXT'):
                self._control_surface_actions.dispatch_pxt_action(tracks[0], xclip, ident, action_name, args)
            elif action_name.startswith('MXT'):
                self._control_surface_actions.dispatch_mxt_action(tracks[0], xclip, ident, action_name, args)
            elif action_name in self.global_actions:
                self.global_actions[action_name](tracks[0], xclip, ident, args)
            elif action_name == 'PSEQ' and args== 'RESET':
                for key, value in self._play_seq_clips.items(): 
                    value[1] = -1
            elif action_name == 'DEBUG':
                if type(xclip) is Live.Clip.Clip:
                    xclip.name = str(xclip.name).upper().replace('DEBUG', 'Debugging Activated')
                self.start_debugging()
            else:
                for t in tracks:                
                    if action_name in self.track_actions:
                        self.track_actions[action_name](t, xclip, ident, args)
                    elif action_name == 'LOOPER': 
                        if args and args.split()[0] in self.looper_actions: 
                            self.looper_actions[args.split()[0]](t, xclip, ident, args)
                        elif action_name in self.looper_actions:
                            self.looper_actions[action_name](t, xclip, ident, args)                       
                    elif action_name.startswith('DEV'): 
                        device_action = self.get_device_to_operate_on(t, action_name, args)
                        device_args = None
                        if device_action[0]:
                            if len(device_action) > 1:
                                device_args = device_action[1]
                            if device_args and device_args.split()[0] in self.device_actions: 
                                self.device_actions[device_args.split()[0]](device_action[0], t, xclip, ident, device_args)
                            elif device_args and 'CHAIN' in device_args: 
                                self._device_actions.dispatch_chain_action(device_action[0], t, xclip, ident, device_args)
                            elif action_name.startswith('DEV'):
                                self._device_actions.set_device_on_off(device_action[0], t, xclip, ident, device_args)                                  
                    elif action_name.startswith('CLIP') and t in self.song().tracks:
                        clip_action = self.get_clip_to_operate_on(t, action_name, args)
                        clip_args = None
                        if clip_action[0]:
                            if len(clip_action) > 1:
                                clip_args = clip_action[1]
                            if clip_args and clip_args.split()[0] in self.clip_actions: 
                                self.clip_actions[clip_args.split()[0]](clip_action[0], t, xclip, ident, clip_args.replace(clip_args.split()[0], ''))
                            elif clip_args and clip_args.split()[0].startswith('NOTES'):
                                self._clip_actions.do_clip_note_action(clip_action[0], t, xclip, ident, args)
                            elif action_name.startswith('CLIP'):
                                self._clip_actions.set_clip_on_off(clip_action[0], t, xclip, ident, args)                                       
                    elif action_name.startswith('DR'):
                        dr = self.get_drum_rack_to_operate_on(t)
                        arg = args.split()[0]
                        if dr and args:
                            if arg in self.dr_actions: 
                                self.dr_actions[arg](dr, t, xclip, ident, args.strip())
                            elif 'PAD' in args:
                                self._dr_actions.dispatch_pad_action(dr, t, xclip, ident, args.strip())
                    # elif action_name in self._user_actions._action_dict:
                    #     getattr(self._user_actions, self._user_actions._action_dict[action_name])(t, args)
        if self._is_debugging:
            print('action_dispatch triggered, ident=' + str(ident) + ' and track(s)=' + str(self.track_list_to_string(tracks)) + ' and action=' + str(action_name) + ' and args=' + str(args))


    # def handle_external_trigger(self, xtrigger):
    #     """ This replaces the below method for compatibility with scripts that also work with ClyphX Pro. """
    #     xtrigger.name = '[] %s' % xtrigger.name
    #     self.handle_action_list_trigger(self.song().view.selected_track, xtrigger)


    def handle_xclip_name(self, track, xclip): 
        """ This is just here for backwards compatibility (primarily with MapEase ClyphX Strip and ClyphX XT) and shouldn't be used if possible. """
        self.handle_action_list_trigger(track, xclip)
                        
        
    # def handle_m4l_trigger(self, name):
    #     """ Convenience method for triggering actions from M4L by simply supplying an action name. """
    #     self.handle_action_list_trigger(self.song().view.selected_track, ActionList('[]' + name))

                
    def custom_handle_action_list_trigger(self, value, track, xtrigger): 
        """ Directly dispatches snapshot recall, X-Control overrides and Seq X-Clips.  Otherwise, seperates ident from action names, splits up lists of action names and calls action dispatch. """
        if self._is_debugging:
            print('---')
        name = None
        if xtrigger is not None:
            name = self.get_name(xtrigger.name).strip() 
        if name and name[0] == '[' and ']' in name:         
            # Snap action, so pass directly to snap component
            if ' || (' in name and type(xtrigger) is Live.Clip.Clip and xtrigger.is_playing:
                self._snap_actions.recall_track_snapshot(name, xtrigger)
            # Control reassignment, so pass directly to control component
            elif '[[' in name and ']]' in name:
                self._control_component.assign_new_actions(name) 
            # Standard trigger
            else:
                ident = name[name.index('['):name.index(']')+1].strip() 
                raw_action_list = name.replace(ident, '', 1).strip()
                if raw_action_list == '':
                    return
                is_play_seq = False
                is_loop_seq = False
                
                # # X-Clips can have on and off action lists, the following handles this
                # if type(xtrigger) is Live.Clip.Clip:
                #     raw_action_list = self.custom_get_xclip_action_list(value, xtrigger, raw_action_list)
                #     if not raw_action_list:
                #         return
                
                # X-Clips can have on and off action lists, the following handles this
                # if type(xtrigger) is Live.Clip.Clip:
                raw_action_list = self.custom_get_xclip_action_list(value, xtrigger, raw_action_list)
                if not raw_action_list:
                    return

                # Check if the trigger is a PSEQ (accessible to any type of X-Trigger)
                if raw_action_list[0] == '(' and '(PSEQ)' in raw_action_list: 
                    is_play_seq = True
                    raw_action_list = raw_action_list.replace('(PSEQ)', '').strip()
                    
                # Check if the trigger is a LSEQ (accessible only to X-Clips)
                elif type(xtrigger) is Live.Clip.Clip and raw_action_list[0] == '(' and '(LSEQ)' in raw_action_list: 
                    is_loop_seq = True
                    raw_action_list = raw_action_list.replace('(LSEQ)', '').strip()
                
                # Build formatted action list    
                formatted_action_list = []
                for action in raw_action_list.split(';'): 
                    action_data = self.format_action_name(track, action.strip())
                    if action_data:
                        formatted_action_list.append(action_data)
                        
                # If seq, pass to appropriate function, else call action dispatch for each action in the formatted action list
                if formatted_action_list:
                    if is_play_seq: 
                        self.handle_play_seq_action_list(formatted_action_list, xtrigger, ident)
                    elif is_loop_seq:
                        self._loop_seq_clips[xtrigger.name] = [ident, formatted_action_list]
                        self.handle_loop_seq_action_list(xtrigger, 0)
                    else:
                        for action in formatted_action_list:
                            self.action_dispatch(action['track'], xtrigger, action['action'], action['args'], ident)
                            if self._is_debugging:
                                print(['handle_action_list_trigger triggered, ident=' + str(ident) + ' and track(s)=' + str(self.track_list_to_string(action['track'])) + ' and action=' + str(action['action']) + ' and args=' + str(action['args'])])
                
             
                
    # def handle_action_list_trigger(self, track, xtrigger): 
    #     """ Directly dispatches snapshot recall, X-Control overrides and Seq X-Clips.  Otherwise, seperates ident from action names, splits up lists of action names and calls action dispatch. """
    #     if self._is_debugging:
    #         print('---')
    #     name = None
    #     if xtrigger is not None:
    #         name = self.get_name(xtrigger.name).strip() 
    #     if name and name[0] == '[' and ']' in name:         
    #         # Snap action, so pass directly to snap component
    #         if ' || (' in name and type(xtrigger) is Live.Clip.Clip and xtrigger.is_playing:
    #             self._snap_actions.recall_track_snapshot(name, xtrigger)
    #         # Control reassignment, so pass directly to control component
    #         elif '[[' in name and ']]' in name:
    #             self._control_component.assign_new_actions(name) 
    #         # Standard trigger
    #         else:
    #             ident = name[name.index('['):name.index(']')+1].strip() 
    #             raw_action_list = name.replace(ident, '', 1).strip()
    #             if raw_action_list == '':
    #                 return
    #             is_play_seq = False
    #             is_loop_seq = False
                
    #             # X-Clips can have on and off action lists, the following handles this
    #             if type(xtrigger) is Live.Clip.Clip:
    #                 raw_action_list = self.get_xclip_action_list(xtrigger, raw_action_list)
    #                 if not raw_action_list:
    #                     return
                
    #             # Check if the trigger is a PSEQ (accessible to any type of X-Trigger)
    #             if raw_action_list[0] == '(' and '(PSEQ)' in raw_action_list: 
    #                 is_play_seq = True
    #                 raw_action_list = raw_action_list.replace('(PSEQ)', '').strip()
                    
    #             # Check if the trigger is a LSEQ (accessible only to X-Clips)
    #             elif type(xtrigger) is Live.Clip.Clip and raw_action_list[0] == '(' and '(LSEQ)' in raw_action_list: 
    #                 is_loop_seq = True
    #                 raw_action_list = raw_action_list.replace('(LSEQ)', '').strip()
                
    #             # Build formatted action list    
    #             formatted_action_list = []
    #             for action in raw_action_list.split(';'): 
    #                 action_data = self.format_action_name(track, action.strip())
    #                 if action_data:
    #                     formatted_action_list.append(action_data)
                        
    #             # If seq, pass to appropriate function, else call action dispatch for each action in the formatted action list
    #             if formatted_action_list:
    #                 if is_play_seq: 
    #                     self.handle_play_seq_action_list(formatted_action_list, xtrigger, ident)
    #                 elif is_loop_seq:
    #                     self._loop_seq_clips[xtrigger.name] = [ident, formatted_action_list]
    #                     self.handle_loop_seq_action_list(xtrigger, 0)
    #                 else:
    #                     for action in formatted_action_list:
    #                         self.action_dispatch(action['track'], xtrigger, action['action'], action['args'], ident)
    #                         if self._is_debugging:
    #                             print(['handle_action_list_trigger triggered, ident=' + str(ident) + ' and track(s)=' + str(self.track_list_to_string(action['track'])) + ' and action=' + str(action['action']) + ' and args=' + str(action['args'])])
                

    def custom_get_xclip_action_list(self, value, xclip, full_action_list):
        """ Get the action list to perform. X-Clips can have an on and off action list seperated by a comma. This will return which action list to perform 
        based on whether the clip is playing. If the clip is not playing and there is no off action, this returns None. """
        result = None   
        split_list = full_action_list.split(',')
        if value == 127:
            result = split_list[0]
        else:
            if len(split_list) == 2:
                if split_list[1].strip() == '*':
                    result = split_list[0]
                else:
                    result = split_list[1]
        if self._is_debugging:
            print('get_xclip_action_list returning ' + str(result))
        return result


    # def get_xclip_action_list(self, xclip, full_action_list):
    #     """ Get the action list to perform. X-Clips can have an on and off action list seperated by a comma. This will return which action list to perform 
    #     based on whether the clip is playing. If the clip is not playing and there is no off action, this returns None. """
    #     result = None   
    #     split_list = full_action_list.split(',')
    #     value = 127 # AJOUTER SI BOUTON ENFONCE
    #     if value:
    #         result = split_list[0]
    #     else:
    #         if len(split_list) == 2:
    #             if split_list[1].strip() == '*':
    #                 result = split_list[0]
    #             else:
    #                 result = split_list[1]
    #     if self._is_debugging:
    #         print('get_xclip_action_list returning ' + str(result))
    #     return result
    
                                
    def replace_user_variables(self, string_with_vars):
        """ Replace any user variables in the given string with the value the variable represents. """
        while '%' in string_with_vars:
            var_name = string_with_vars[string_with_vars.index('%')+1:]
            if '%' in var_name:
                var_name = var_name[0:var_name.index('%')]
                string_with_vars = string_with_vars.replace('%' + var_name + '%', self.get_user_variable_value(var_name), 1)  
            else:
                string_with_vars = string_with_vars.replace('%', '', 1)
        if '$' in string_with_vars: # For compat with old-style variables
            for string in string_with_vars.split():
                if '$' in string and not '=' in string:
                    var_name = string.replace('$', '')
                    string_with_vars = string_with_vars.replace('$' + var_name, self.get_user_variable_value(var_name), 1)  
        if self._is_debugging:
            print('replace_user_variables returning ' + str(string_with_vars))
        return string_with_vars
    
    
    def get_user_variable_value(self, var_name):
        """ Get the value of the given variable name or 0 if var name not found. """
        result = '0'
        if self._user_variables.__contains__(var_name):
            result = self._user_variables[var_name]
        if self._is_debugging:
            print('get_user_variable_value returning ' + str(var_name) + '=' + str(result))
        return result
    
    
    def handle_user_variable_assignment(self, string_with_assign):
        """ Handle assigning new value to variable with either assignment or expression enclosed in parens. """
        string_with_assign = string_with_assign.replace('$', '')# For compat with old-style variables
        var_data = string_with_assign.split('=')
        if len(var_data) >= 2 and not ';' in var_data[1] and not '%' in var_data[1] and not '=' in var_data[1]:
            if '(' in var_data[1] and ')' in var_data[1]:
                try: self._user_variables[var_data[0].strip()] = str(eval(var_data[1].strip()))
                except: pass
            else:
                self._user_variables[var_data[0].strip()] = var_data[1].strip()
            if self._is_debugging:
                print('handle_user_variable_assignment, ' + str(var_data[0].strip()) + '=' + str(var_data[1].strip()))
                        
  
    def format_action_name(self, origin_track, origin_name): 
        """ Replaces vars (if any) then splits up track, action name and arguments (if any) and returns dict """
        result_name = self.replace_user_variables(origin_name)
        if '=' in result_name:
            self.handle_user_variable_assignment(result_name)
            return
        result_track = [origin_track]
        if len(result_name) >= 4 and (('/' in result_name[:4]) or ('-' in result_name[:4] and '/' in result_name[4:]) or (result_name[0] == '"' and '"' in result_name[1:])):
            track_data = self.get_track_to_operate_on(result_name)
            result_track = track_data[0]
            result_name = track_data[1]
        args = ''
        name = result_name.split()
        if len(name) > 1:
            args = result_name.replace(name[0], '', 1)
            result_name = result_name.replace(args, '')
        if self._is_debugging:
                print('format_action_name returning, track(s)=' + str(self.track_list_to_string(result_track)) + ' and action=' + str(result_name.strip()) + ' and args=' + str(args.strip()))
        return {'track' : result_track, 'action' : result_name.strip(), 'args' : args.strip()}  
    
    
    def handle_loop_seq_action_list(self, xclip, count):
        """ Handles sequenced action lists, triggered by xclip looping """
        if self._loop_seq_clips.__contains__(xclip.name):
            if count >= len(self._loop_seq_clips[xclip.name][1]):
                count = count - ((count / len(self._loop_seq_clips[xclip.name][1]))*len(self._loop_seq_clips[xclip.name][1]))
            action = self._loop_seq_clips[xclip.name][1][count]
            self.action_dispatch(action['track'], xclip, action['action'], action['args'], self._loop_seq_clips[xclip.name][0])
            if self._is_debugging:
                print('handle_loop_seq_action_list triggered, xclip.name=' + str(xclip.name) + ' and track(s)=' + str(self.track_list_to_string(action['track'])) + ' and action=' + str(action['action']) + ' and args=' + str(action['args']))
                        
                        
    def handle_play_seq_action_list(self, action_list, xclip, ident):
        """ Handles sequenced action lists, triggered by replaying/retriggering the xtrigger """
        if self._play_seq_clips.__contains__(xclip.name): 
            count = self._play_seq_clips[xclip.name][1] + 1
            if count > len(self._play_seq_clips[xclip.name][2])-1:
                count = 0
            self._play_seq_clips[xclip.name] = [ident, count, action_list]
        else:
            self._play_seq_clips[xclip.name] = [ident, 0, action_list]
        action = self._play_seq_clips[xclip.name][2][self._play_seq_clips[xclip.name][1]]
        self.action_dispatch(action['track'], xclip, action['action'], action['args'], ident)
        if self._is_debugging:
            print('handle_play_seq_action_list triggered, ident=' + str(ident) + ' and track(s)=' + str(self.track_list_to_string(action['track'])) + ' and action=' + str(action['action']) + ' and args=' + str(action['args']))


    def do_parameter_adjustment(self, param, value):
        """" Adjust (</>, reset, random, set val) continuous params, also handles quantized param adjustment (should just use +1/-1 for those) """
        if not param.is_enabled:
            return()
        step = (param.max - param.min) / 127
        new_value = param.value
        if value.startswith(('<', '>')):
            factor = self.get_adjustment_factor(value)
            if not param.is_quantized:
                new_value += step * factor
            else:
                new_value += factor
        elif value == 'RESET' and not param.is_quantized:
            new_value = param.default_value
        elif 'RND' in value and not param.is_quantized:
            rnd_min = 0
            rnd_max = 128
            if value != 'RND' and '-' in value:
                rnd_range_data = value.replace('RND', '').split('-')
                if len(rnd_range_data) == 2:
                    new_min = 0
                    new_max = 128
                    try: new_min = int(rnd_range_data[0])
                    except: new_min = 0
                    try: new_max = int(rnd_range_data[1]) + 1
                    except: new_max = 128
                    if new_min in range(0, 129) and new_max in range(0, 129) and new_min < new_max:
                        rnd_min = new_min
                        rnd_max = new_max
            rnd_value = (Live.Application.get_random_int(0, 128) * (rnd_max - rnd_min) / 127) + rnd_min
            new_value = (rnd_value * step) + param.min
            
        else:
            try:
                if int(value) in range (128):
                    try: new_value = (int(value) * step) + param.min
                    except: new_value = param.value
            except: pass
        if new_value >= param.min and new_value <= param.max:
            param.value = new_value
            if self._is_debugging:
                print('do_parameter_adjustment called on ' + str(param.name) + ', set value to ' + str(new_value))
            
            
    def get_adjustment_factor(self, string, as_float = False):
        """ Get factor for use with < > actions """
        factor = 1
        if len(string) > 1:
            if as_float:
                try: factor = float(string[1:])
                except: factor = 1
            else:
                try: factor = int(string[1:])
                except: factor = 1
        if string.startswith('<'): 
            factor = -(factor)
        if self._is_debugging:
            print('get_adjustment_factor returning factor=' + str(factor))
        return factor      
        
    
    def get_track_to_operate_on(self, origin_name):  
        """ Gets track or tracks to operate on """
        result_tracks = []
        result_name = origin_name
        if '/' in origin_name:
            tracks = list(tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,))
            sel_track_index = tracks.index(self.song().view.selected_track)
            if(origin_name.index('/') > 0):
                track_spec = origin_name.split('/')[0].strip()
                if '"' in track_spec:
                    track_spec = self.get_track_index_by_name(track_spec, tracks)
                if 'SEL' in track_spec:
                    track_spec = track_spec.replace('SEL', str(sel_track_index + 1), 1) 
                if 'MST' in track_spec:
                    track_spec = track_spec.replace('MST', str(len(tracks)), 1) 
                if track_spec == 'ALL':
                    result_tracks = tracks
                else:
                    track_range_spec = track_spec.split('-')
                    if len(track_range_spec) <= 2:
                        track_range = []
                        try:
                            for spec in track_range_spec:
                                track_index = -1
                                if spec.startswith(('<', '>')):
                                    try: track_index = self.get_adjustment_factor(spec) + sel_track_index
                                    except: pass
                                else:
                                    try: track_index = int(spec) - 1
                                    except: track_index = (ord(spec) - 65) + len(self.song().tracks)
                                if track_index in range(len(tracks)):
                                    track_range.append(track_index)
                        except: track_range = []
                        if track_range:
                            if len(track_range) == 2:
                                if (track_range[0] < track_range[1]):
                                    for index in range(track_range[0], track_range[1] + 1):
                                        result_tracks.append(tracks[index])
                            else:
                                result_tracks = [tracks[track_range[0]]]
            result_name = origin_name[origin_name.index('/')+1:].strip()
        if self._is_debugging:
            print('get_track_to_operate_on returning result_tracks=' + str(self.track_list_to_string(result_tracks)) + ' and result_name=' + str(result_name))
        return (result_tracks, result_name)
        
    
    def get_track_index_by_name(self, name, tracks):
        """ Gets the index(es) associated with the track name(s) specified in name. """
        while '"' in name:
            track_name = name[name.index('"')+1:]
            if '"' in track_name:
                track_name = track_name[0:track_name.index('"')]
                track_index = ''
                def_name = ''
                if ' AUDIO' or ' MIDI' in track_name:
                    def_name = track_name.replace(' ', '-')# In Live GUI, default names are 'n Audio' or 'n MIDI', in API it's 'n-Audio' or 'n-MIDI' 
                for track in tracks:
                    current_track_name = self.get_name(track.name)
                    if current_track_name == track_name or current_track_name == def_name:
                        track_index = str(tracks.index(track) + 1)
                        break
                name = name.replace('"' + track_name + '"', track_index, 1)  
                name = name.replace('"' + def_name + '"', track_index, 1) 
            else:
                name = name.replace('"', '', 1) 
        return name    
    
    
    def get_device_to_operate_on(self, track, action_name, args):
        """ Get device to operate on and action to perform with args """
        device = None
        device_args = args
        if 'DEV"' in action_name:
            dev_name = action_name[action_name.index('"')+1:]
            if '"' in args:
                dev_name = action_name[action_name.index('"')+1:] + ' ' + args
                device_args = args[args.index('"')+1:].strip()
            if '"' in dev_name:
                dev_name = dev_name[0:dev_name.index('"')]
            for dev in track.devices:
                if dev.name.upper() == dev_name:
                    device = dev
                    break
        else:
            if action_name == 'DEV':
                device = track.view.selected_device
                if device == None:
                    if track.devices:
                        device = track.devices[0]
            else:
                try:
                    dev_num = action_name.replace('DEV', '')
                    if '.' in dev_num and self._can_have_nested_devices:
                        dev_split = dev_num.split('.')
                        top_level = track.devices[int(dev_split[0]) - 1]
                        if top_level and top_level.can_have_chains:
                            device = top_level.chains[int(dev_split[1]) - 1].devices[0]
                            if len(dev_split) > 2:
                                device = top_level.chains[int(dev_split[1]) - 1].devices[int(dev_split[2]) - 1]
                    else:
                        device = track.devices[int(dev_num) - 1]
                except: pass
        if self._is_debugging:
            debug_string = 'None'
            if device:
                debug_string = device.name
            print('get_device_to_operate_on returning device=' + str(debug_string) + ' and device args=' + str(device_args))
        return (device, device_args)
    
    
    def get_clip_to_operate_on(self, track, action_name, args):
        """ Get clip to operate on and action to perform with args """
        clip = None
        clip_args = args
        if 'CLIP"' in action_name:
            clip_name = action_name[action_name.index('"')+1:]
            if '"' in args:
                clip_name = action_name[action_name.index('"')+1:] + ' ' + args
                clip_args = args[args.index('"')+1:].strip()
            if '"' in clip_name:
                clip_name = clip_name[0:clip_name.index('"')]
            for slot in track.clip_slots:
                if slot.has_clip and slot.clip.name.upper() == clip_name:
                    clip = slot.clip
                    break
        else:
            sel_slot_idx = list(self.song().scenes).index(self.song().view.selected_scene)
            slot_idx = sel_slot_idx
            if action_name == 'CLIP':
                if track.playing_slot_index >= 0:
                    slot_idx = track.playing_slot_index
            elif action_name == 'CLIPSEL':
                if self.application().view.is_view_visible('Arranger'):
                    clip = self.song().view.detail_clip
            else:
                try: slot_idx = int(action_name.replace('CLIP', ''))-1
                except: slot_idx = sel_slot_idx
            if clip == None and track.clip_slots[slot_idx].has_clip:
                clip = track.clip_slots[slot_idx].clip
        if self._is_debugging:
            debug_string = 'None'
            if clip:
                debug_string = clip.name
            print('get_clip_to_operate_on returning clip=' + str(debug_string) + ' and clip args=' + str(clip_args))
        return (clip, clip_args)
    
    
    def get_drum_rack_to_operate_on(self, track):
        """ Get drum rack to operate on """
        dr = None
        for device in track.devices:
            if device.can_have_drum_pads:
                dr = device
                break
        if self._is_debugging:
            debug_string = 'None'
            if dr:
                debug_string = dr.name
            print('get_drum_rack_to_operate_on returning dr=' + str(debug_string))
        return dr
      

        
    def enable_push_emulation(self, scripts):
        """ Try to disable Push's handshake to allow for emulation. 
        If emulating for APC, set scripts on combiner component """
        for script in scripts:
            script_name = script.__class__.__name__  
            if script_name == 'Push':
                if IS_LIVE_9_5:
                    with script._component_guard():
                        script._start_handshake_task = MockHandshakeTask()
                        script._handshake = MockHandshake()
                    if self._push_apc_combiner:
                        self._push_apc_combiner.set_up_scripts(self._control_surfaces())
                else:
                    script._handshake._identification_timeout_task.kill()
                    script._handshake._identification_timeout_task = Task.Task()
                break
            

    def start_debugging(self):
        """ Turn on debugging and write all user vars/controls/actions to Live's log file to assist in troubleshooting. """
        if not self._is_debugging:
            self._is_debugging = True
            print('------- ClyphX Log: Logging User Variables -------')
            for key, value in self._user_variables.items():
                print(str(key) + '=' + str(value))
            print('------- ClyphX Log: Logging User Controls -------')
            for key, value in self._control_component._control_list.items():
                print(str(key) + ' on_action=' + str(value['on_action']) + ' and off_action=' + str(value['off_action']))
            print('------- ClyphX Log: Logging User Actions -------')
            for key, value in self._user_actions._action_dict.items():
                print(str(key) + '=' + str(value))    
            print('------- ClyphX Log: Debugging Started -------')
            
            
    def track_list_to_string(self, track_list):
        """ Convert list of tracks to a string of track names or None if no tracks. This is used for debugging. """
        result = 'None'
        if track_list:
            result = '['
            for track in track_list:
                result += track.name + ', '
            result = result[:len(result)-2]
        return result + ']'
        
            
    # def perform_startup_actions(self, action_list):
    #     """ Delay startup action so it can perform actions on values that are changed upon set load (like overdub) """
    #     self.handle_action_list_trigger(self.song().view.selected_track, ActionList(action_list))
            
            
    def setup_tracks(self):  
        """ Setup component tracks on ini and track list changes.  Also call Macrobat's get rack """
        for t in self.song().tracks:
            self._macrobat.setup_tracks(t)
            if (self._current_tracks and t in self._current_tracks):
                pass
            else:
                self._current_tracks.append(t)
                ClyphXTrackComponent(self, t)
        for r in tuple(self.song().return_tracks) + (self.song().master_track,):
            self._macrobat.setup_tracks(r)
        self._snap_actions.setup_tracks()
            
    
    def get_name(self, name):
        """ Convert name to upper-case string or return blank string if couldn't be converted """
        try: name = str(name).upper()
        except: name = ''
        return name
    
    
    def _on_track_list_changed(self):
        ControlSurface._on_track_list_changed(self)
        self.setup_tracks()
        
        
    def connect_script_instances(self, instanciated_scripts):
        """ Pass connect scripts call to control component """
        self._control_component.connect_script_instances(instanciated_scripts) 
        self._control_surface_actions.connect_script_instances(instanciated_scripts) 
        if self._push_emulation:
            self.enable_push_emulation(instanciated_scripts)
        
            
    def build_midi_map(self, midi_map_handle):
        """ Build user-defined list of midi messages for controlling ClyphX track """
        ControlSurface.build_midi_map(self, midi_map_handle)
        if self._user_settings_logged:
            self._control_component.rebuild_control_map(midi_map_handle)
        else:
            self.get_user_settings(midi_map_handle)
            self._user_settings_logged = True
        if self._push_emulation:
            self.enable_push_emulation(self._control_surfaces())
        
    
    def receive_midi(self, midi_bytes):
        """ Receive user-specified messages and send to control script """
        ControlSurface.receive_midi(self, midi_bytes)
        self._control_component.receive_midi(midi_bytes)
        
        
    def handle_sysex(self, midi_bytes):
        """ Handle sysex received from controller """
        pass    
    
    
    def handle_nonsysex(self, midi_bytes):
        """ Override so that ControlSurface doesn't report this to Log.txt """
        pass
        
   