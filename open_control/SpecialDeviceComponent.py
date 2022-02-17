from _Framework.DeviceComponent import DeviceComponent as DeviceComponentBase
from _Framework.SubjectSlot import subject_slot
from _Generic.Devices import device_parameters_to_map, number_of_parameter_banks, parameter_banks, parameter_bank_names, best_of_parameter_bank
from . import Colors, Options
# from .BrowserManager import BrowserManager
import Live

class DeviceComponent(DeviceComponentBase):

    def __init__(self, parent, *a, **k):
        self.parent = parent
        super(DeviceComponent, self).__init__(*a, **k)
        self.selected_device_listener()
        # self.browser = self.application().browser
        # self.application().view.add_browse_mode_listener(self.on_hotswap_changed)
        # self.browser_categories = [self.browser.audio_effects] #, self.browser.instruments, self.browser.packs, self.browser.drums, self.browser.midi_effects , self.browser.max_for_live, self.browser.plugins, self.browser.user_library, self.browser.current_project, self.browser.sounds]

    def set_mixer(self, mixer):
        self._mixer = mixer

    @property
    def selected_track(self):
        if Options.session_box_linked_to_selection:
            track = self.song().view.selected_track
        else:
            track = self._mixer.channel_strip(0)._track
        return track

    # """ BROWSER"""

    # #Hotswap
    # def set_hotswap(self, button):
    #     self._hotswap_button = button
    #     self._on_hotswap.subject = button

    # @subject_slot(u'value')
    # def _on_hotswap(self, value):
    #     if value:
    #         self.application().view.toggle_browse()

    # def on_hotswap_changed(self):
    #     if self.application().view.browse_mode:
    #         self.get_selected_browser_item()
    #     else:
    #         self.parent.display_message("Browser", "Hotswap Off")  

    # #Select Next
    # def set_load_next(self, button):
    #     self._load_next_button = button
    #     self._on_load_next.subject = button

    # @subject_slot(u'value')
    # def _on_load_next(self, value):
    #     if value:
    #         self.get_selected_browser_item()
    #         self.select_item('Next')
    #         self.load_selected_item(1)
    #         self.display_item_name()

    # #Select Prev
    # def set_load_prev(self, button):
    #     self._load_prev_button = button
    #     self._on_load_prev.subject = button

    # @subject_slot(u'value')
    # def _on_load_prev(self, value):
    #     if value:
    #         self.get_selected_browser_item()
    #         self.select_item('Prev')
    #         self.load_selected_item(1)
    #         self.display_item_name()

    # # Select Prev/Next (Encoder)
    # def set_prev_next_item(self, button):
    #     self._prev_next_item_button = button
    #     self._on_prev_next_item.subject = button

    # @subject_slot(u'value')
    # def _on_prev_next_item(self, value):
    #     if value > 64:
    #         self.select_item('Next')
    #         direction = self.application().view.NavDirection.down
    #         self.application().view.scroll_view(direction, u'Browser', False)
    #     if value < 64:
    #         self.select_item('Prev')
    #         direction = self.application().view.NavDirection.up
    #         self.application().view.scroll_view(direction, u'Browser', False)
    #     self._prev_next_item_button.send_value(64, force=True)

    # def select_item(self, direction):
    #     if direction == "Next":
    #         self.item_index += 1
    #     else:
    #         self.item_index -= 1
    #     self.selected_item = self.browser_items[self.item_index]
    #     self.display_item_name()

    #     # if self.item_index < 0 or self.item_index > len(self.list_children):
    #     #     self.get_parent_folder(self.selected_item)

    # def get_parent_folder(self, item):
    #     hierarchy_up = self.browser_hierarchy[len(self.browser_hierarchy)-1]
    #     self.selected_item = hierarchy_up[1]
    #     self.list_children = hierarchy_up[0].children
    #     print(self.browser_hierarchy)
    #     for i, sel in zip(range(len(self.list_children)), self.list_children):
    #         if sel.uri == self.selected_item.uri:
    #             print([sel.name, i])
    #             self.item_index = i
    #         # self.selected_item = self.browser_hierarchy[len(self.browser_hierarchy)-1]
    #         # for item in self.browser_categories:
    #         #     self.get_item_position(item, self.selected_item)

    # # def get_item_position(self, item):

    # #         for i, sel in zip(range(len(self.list_children)), self.list_children):
    # #             if sel.uri == self.browser_hierarchy[len(self.browser_hierarchy)]:
    # #                 self.item_index = i
    # #                 print(self.browser_hierarchy[len(self.browser_hierarchy)])
    # #                 print(self.item_index)

    # # Load Item
    # def set_load_item(self, button):
    #     self._load_item_button = button
    #     self.load_selected_item.subject = button

    # @subject_slot(u'value')
    # def load_selected_item(self, value):
    #     if value:
    #         if len(list(self.selected_item.children)) > 0:
    #             self.open_folder(1)
    #         else:
    #             self.browser.load_item(self.selected_item)

    # # Open Folder
    # def set_open_folder(self, button):
    #     self._open_folder_button = button
    #     self.open_folder.subject = button

    # @subject_slot(u'value')
    # def open_folder(self, value):
    #     if value:
    #         direction = self.application().view.NavDirection.right
    #         self.application().view.scroll_view(direction, u'Browser', False)
    #         self.refesh_browser()

    # # Close Folder
    # def set_close_folder(self, button):
    #     self._close_folder_button = button
    #     self.close_folder.subject = button

    # @subject_slot(u'value')
    # def close_folder(self, value):
    #     if value:
    #         direction = self.application().view.NavDirection.left
    #         self.application().view.scroll_view(direction, u'Browser', False)
    #         self.refesh_browser()

    # # Get selected item
    # def refesh_browser(self):
    #     inserted_folder = list(self.browser_items[self.item_index].children)
    #     self.previous_folder_index = self.get_item_index(self.browser_items, self.previous_folder)
    #     pop_start = self.previous_folder_index + 1
    #     pop_end = self.previous_folder_index + len(list(self.previous_folder.children)) + 1
    #     self.browser_items = self.browser_items[0:pop_start] + self.browser_items[pop_end:]
    #     insert_index = self.item_index + 1
    #     self.browser_items = self.browser_items[0:insert_index] + inserted_folder + self.browser_items[insert_index:]
    #     print(self.browser_items)

    # def get_item_index(self, _list, item):
    #     for i, sel in zip(range(len(_list)), _list):
    #         if sel.uri == item.uri:
    #             index = i
    #     return index

    # # Get selected item
    # def get_selected_browser_item(self):
    #     self.browser_items = []
    #     for item in self.browser_categories:
    #         self.get_hotswap_index(item)
    #     for i, sel in zip(range(len(self.browser_items)), self.browser_items):
    #         if sel.uri == self.selected_item.uri:
    #             self.item_index = i

    # def get_hotswap_index(self, item):
    #     for sub_item in item.children:
    #         self.browser_items.append(sub_item)
    #         if self.browser.relation_to_hotswap_target(sub_item) == Live.Browser.Relation.ancestor:
    #             self.get_hotswap_index(sub_item)
    #         elif self.browser.relation_to_hotswap_target(sub_item) == Live.Browser.Relation.equal:
    #             self.previous_folder = item
    #             list_children = list(item.iter_children)
    #             for sel in list_children:
    #                 if sel.uri == sub_item.uri:
    #                     self.selected_item = sel

    # Display Item Name
    def display_item_name(self):
        self.parent.display_message("Browser", self.selected_item.name)      

    """ VARIATIONS """

    def set_launch_variation_button(self, button):
        self._launch_variation_button = button
        self._on_launch_variation.subject = button

    @subject_slot(u'value')
    def _on_launch_variation(self, value):
        if value or not self._launch_variation_button.is_momentary():
            self._device.recall_selected_variation()

    def set_store_variation_button(self, button):
        self._store_variation_button = button
        self._on_store_variation.subject = button

    @subject_slot(u'value')
    def _on_store_variation(self, value):
        if value or not self._store_variation_button.is_momentary():
            self._device.store_variation()

    def set_recall_variation_button(self, button):
        self._recall_variation_button = button
        self._on_recall_variation.subject = button

    @subject_slot(u'value')
    def _on_recall_variation(self, value):
        if value or not self._recall_variation_button.is_momentary():
            self._device.recall_last_used_variation()

    def set_randomize_macros_button(self, button):
        self._randomize_macros_button = button
        self._on_randomize_macros.subject = button

    @subject_slot(u'value')
    def _on_randomize_macros(self, value):
        if value or not self._randomize_macros_button.is_momentary():
            self._device.randomize_macros()

    def set_prev_device_button(self, button):
        self._prev_device_button = button
        self._on_jump_to_prev_device.subject = button

    @subject_slot(u'value')
    def _on_jump_to_prev_device(self, value):
        if value or not self._prev_device_button.is_momentary():
            self._scroll_device_view(Live.Application.Application.View.NavDirection.left)
            self.update()
            
    def set_next_device_button(self, button):
        self._next_device_button = button
        self._on_jump_to_next_device.subject = button

    @subject_slot(u'value')
    def _on_jump_to_next_device(self, value):
        if value or not self._next_device_button.is_momentary():
            self._scroll_device_view(Live.Application.Application.View.NavDirection.right)
            self.update()

    def set_prev_variation_button(self, button):
        self._prev_variation_button = button
        self._on_jump_to_prev_variation.subject = button

    @subject_slot(u'value')
    def _on_jump_to_prev_variation(self, value):
        if value or not self._prev_variation_button.is_momentary():
            if self._device.selected_variation_index > 0:
                self._device.selected_variation_index -= 1
                self._update_name()

    def set_next_variation_button(self, button):
        self._next_variation_button = button
        self._on_jump_to_next_variation.subject = button

    @subject_slot(u'value')
    def _on_jump_to_next_variation(self, value):
        if value or not self._next_variation_button.is_momentary():
            if self._device.selected_variation_index < self._device.variation_count-1:
                self._device.selected_variation_index += 1
                self._update_name()

    def _update_name(self):
        appointed_device = self.song().appointed_device
        if appointed_device is not None:
            name = appointed_device.name
            if self._device and self._device.can_have_chains:
                name = "V" + str(self._device.selected_variation_index+1) +":"+ name
            else:
                name = "XX " + name
            self.parent.display_message("Variation Number", name)      

    def selected_device_listener(self):
        self.song().view.selected_track.view.add_selected_device_listener(self._update_name)

    def set_first_device_parameter(self, buttons):
        self.first_device_parameters = buttons
        if buttons:
            self._on_first_device_parameter_value.subject = buttons

    @subject_slot('value')
    def _on_first_device_parameter_value(self, *args):
        self._device = self.song().view.selected_track.devices[0]
        self.set_parameter_controls(self.first_device_parameters)

    def set_selected_device_parameters(self, buttons):
        self.selected_device_parameters = buttons
        self.set_parameter_controls(self.selected_device_parameters)
        if buttons:
            self._on_selected_device_parameter_value.subject = buttons

    @subject_slot('value')
    def _on_selected_device_parameter_value(self, *args):
        self._device = self.song().view.selected_track.view.selected_device
        banks = parameter_banks(self._device) 
        parameter = banks[0][args[1]]
        self.parent.set_temp_message(parameter.str_for_value(parameter.value))

    def _scroll_device_view(self, direction):
        self.application().view.show_view(u'Detail')
        self.application().view.show_view(u'Detail/DeviceChain')
        self.application().view.scroll_view(direction, u'Detail/DeviceChain', False)
        self._update_name()

    def update(self):
        self._update_name()
        super(DeviceComponent, self).update()

    def disconnect(self):
        super(DeviceComponent, self).disconnect()
        
    @subject_slot('name')
    def _on_device_name_changed(self):
        appointed_device = self.song().appointed_device
        if self.is_enabled() and appointed_device is not None:
            name = appointed_device.name
            if self.song().appointed_device.can_have_chains:
                name = "v " + name