import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
import logging, traceback
logger = logging.getLogger(__name__)
def print(text):
    logger.warning(text)

BROWSER_TAGS = ('Drums', 'Instruments', 'Audio Effects', 'MIDI Effects', 'Max for Live')
    
class BrowserComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = """ ClyphXM4LBrowserInterface provides access to browser data and methods for use in M4L devices. 
    NOTE: Lazy initialization is used, get_browser_tags method needs to be called first in order to use other methods. """
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
        self._selected_tag = None
        self._selected_device = None
        self._selected_folder = None
        self._selected_item = None
        self._browser = {}
        self.browser = self.application().browser
        # self.get_browser_tags()
            

    def disconnect(self):
        self._parent = None
        self._selected_tag = None
        self._selected_device = None
        self._selected_folder = None
        self._selected_item = None
        self._browser = None
        ControlSurfaceComponent.disconnect(self)                
            
    
    def on_enabled_changed(self):
        pass
        

    def update(self):    
        pass    
    
    
    def load_device(self):
        """ Loads the selected device if there is one. """
        if self._selected_device:
            self.application().browser.load_item(self._selected_device['device'])
                   
    def load_item(self):
        """ Loads the selected item if there is one. """
        if self._selected_item:
            self._selected_item = self.current_list[self.current_index]
            self.application().browser.load_item(self._selected_item)
            
    def set_hotswap_button(self, button):
        self.hotswap_button = button
        self.activate_hotswap.subject = button

    @subject_slot('value')        
    def activate_hotswap(self, value):
        if value:
            """ Activates hotswap for the device selected in Live, finds the appropriate tag and device to use and returns the items for the device. """
            device = self.song().view.selected_track.view.selected_device
            items = []
            print("brose")
            if device:
                if self.application().view.browse_mode:
                    self.application().view.toggle_browse()
                if device.class_name == 'PluginDevice' or self._track_contains_browser():
                    pass
                else:
                    tag_to_use = None
                    device_to_use = device.class_display_name
                    if device.can_have_drum_pads:
                        tag_to_use = 'Drums'
                    elif device.class_display_name.startswith('Max'):
                        tag_to_use = 'Max for Live'
                    elif device.type == Live.Device.DeviceType.audio_effect:
                        tag_to_use = self.application().browser.audio_effects
                    elif device.type == Live.Device.DeviceType.midi_effect:
                        tag_to_use = self.application().browser.midi_effects
                    elif device.type == Live.Device.DeviceType.instrument:
                        tag_to_use = self.application().browser.instruments
            if tag_to_use and device_to_use:
                self.application().view.toggle_browse()
                for child in tag_to_use.children:
                    if device.class_name == child.name:
                        self.current_list = child.children
                        self.current_index = 0
                        for sub_child in child.children:
                            print(sub_child.name)
            #     self._selected_tag = self._browser[tag_to_use]
            #     self._selected_device = self._selected_tag['devices'][device_to_use]
            #     items = sorted(self._selected_device['folders'].keys()) + sorted(self._selected_device['items'])
            # return items
    
            
    def deactivate_hotswap(self):
        """ Deactivates hotswap and closes the browser. """
        if self.application().view.browse_mode:
            self.application().view.toggle_browse()
            self.application().view.hide_view('Browser')
            
    def set_select_next_item(self, button):
        self.select_next_item_button = button
        self.select_next_item_button_value.subject = button

    def set_select_prev_item(self, button):
        self.select_prev_item_button = button
        self.select_prev_item_button_value.subject = button

    @subject_slot('value')
    def select_next_item_button_value(self, value):
        if value:
            direction = self.application().view.NavDirection.down
            self.application().view.scroll_view(direction, u'Browser', False)
            # self.browser.view.scroll_view(self.application().view.NavDirection.down, u'', False)
            
            # self.current_index += 1
            self.show_target_name()



    @subject_slot('value')
    def select_prev_item_button_value(self, value):
        if value:
            direction = self.application().view.NavDirection.up
            self.application().view.scroll_view(direction, u'Browser', False)
            # self.current_index -= 1
            self.show_target_name()

    def show_target_name(self):
        print(self.browser.filter_type)
        for item in self.browser.audio_effects.children:
            self.check_is_selected(item)
    
    def check_is_selected(self, item):
        # self.browser.full_refresh = 1

        self.application().view.focus_view('Browser')
        print([item.name, item.is_selected])
        # if self.browser.relation_to_hotswap_target(item) == Live.Browser.Relation.equal:
        #     print(["HOTSWAP", item.name])
        #     self._send_sysex_for_name(item.name)
        if item.is_selected:
            for child in item.children:
                self.check_is_selected(child)
                print(["HOTSWAP", item.name])
                self._send_sysex_for_name(item.name)
                


    def set_load_item(self, button):
        self.load_item_button = button
        self.load_item_button_value.subject = button

    @subject_slot('value')
    def load_item_button_value(self, value):
        if value:
            print(self.current_list[self.current_index].name)
            print(["loadable", self.current_list[self.current_index].is_folder])
            if self.current_list[self.current_index].is_folder:
                direction = self.application().view.NavDirection.right
                self.application().view.scroll_view(direction, u'Browser', False)
                # self.browser.hotswap_target = self.current_list[self.current_index]._expanded = 1
                print(["children", self.current_list[self.current_index].iter_children])
                self.current_list = self.current_list[self.current_index].children
                self.current_index = 0
                self.show_target_name()
            if self.current_list[self.current_index].is_loadable:
                self.application().browser.load_item(self.current_list[self.current_index])

    def select_non_folder_item(self, item_name):
        """ Stores an item that is not contained within a folder. """
        self._selected_item = self._selected_device['items'][item_name]

    def select_folder_item(self, item_name):
        """ Stores an item that is contained within a folder. """
        self._selected_item = self._selected_folder[item_name]
        
        
    def get_browser_tags(self):
        """ Returns the list of browser tags. 
        Also, initializes browser if it hasn't already been initialized. """
        print(self.application().browser.audio_effects.name)
        # if not self._browser:
        #     for tag in self.application().browser.audio_effects:
        #         print(tag)
                # if tag.name in BROWSER_TAGS:
                #     self._browser[tag.name] = {'tag' : tag, 'devices' : self._create_devices_for_tag(tag)}
        # return BROWSER_TAGS
    
    
    def get_devices_for_tag(self, tag_name):
        """ Returns the list of devices for the given tag and stores the tag. """
        self._selected_tag = self._browser[tag_name]
        return sorted(self._selected_tag['devices'])
    
    
    def get_items_for_device(self, device_name):
        """ Returns the list of folders and items for the given device and stores the device. """
        self._selected_device = self._selected_tag['devices'][device_name]
        return sorted(self._selected_device['folders'].keys()) + sorted(self._selected_device['items'])
    
    
    def get_items_for_folder(self, folder_name):
        """ Returns the list of items in the given folder and stores the folder. """
        self._selected_folder = self._selected_device['folders'][folder_name]
        return sorted(self._selected_folder)
    
    
    def _track_contains_browser(self):
        """ Returns whether or not the selected track contains the Device Browser, in which case hotswapping isn't possble. """
        for device in self.song().view.selected_track.devices:
            if device and device.name == 'Device Browser':
                return True
        return False
    
    
    def _create_devices_for_tag(self, tag):
        """ Creates dict of devices for the given tag. Special handling is needed for M4L tag, which only contains folders, and Drums tag, which contains devices and folders. """
        device_dict = {}
        if tag.name == 'Max for Live':
            for child in tag.children:
                if child.is_folder:
                    for device in child.children:
                        if device.is_device:
                            device_dict[child.name] = {'device' : device, 'items' : self._create_items_for_device(child), 'folders' : {}}
                            break
        else:
            for child in tag.children:
                if child.is_device:
                    if tag.name == 'Drums':
                        device_dict[child.name] = {'device' : child, 'items' : self._create_items_for_device(tag), 'folders' : {}}
                    else:
                        device_dict[child.name] = {'device' : child, 'items' : self._create_items_for_device(child), 'folders' : self._create_folders_for_device(child)}
            if len(device_dict) == 1:
                device_dict[' '] = {} 
        return device_dict
    
    
    def _create_items_for_device(self, device):
        """ Creates dict of loadable items for the given device or folder. """

        items_dict = {}
        for child in device.children:
            if child.is_loadable and not child.name == 'Drum Rack':
                items_dict[child.name] = child
        if len(items_dict) == 1:
            items_dict[' '] = {} 
        return items_dict
    
    
    def _create_folders_for_device(self, device):
        """ Creates dict of folders for the given device. """
        folders_dict = {}
        for child in device.children:
            if child.is_folder:
                folders_dict[child.name + ' >'] = self._create_items_for_device(child)
        return folders_dict


    def _send_sysex_for_name(self, name):       
        _len = min(len(name), 32)
        message = [240, 122, 29, 1, 19, 51, 6]
        for i in range(_len):
            if 0 <= ord(name[i])-32 <= 94:
                message.append(ord(name[i])-32)
            else:
                message.append(95)
        message.append(247)    
        if self.is_enabled() and self.select_next_item_button:     
            self.select_next_item_button._send_midi(tuple(message))        
    
     
# local variables:
# tab-width: 4