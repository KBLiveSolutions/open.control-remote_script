from _Framework.DeviceComponent import DeviceComponent as DeviceComponentBase
from _Framework.SubjectSlot import subject_slot
from _Generic.Devices import device_parameters_to_map, number_of_parameter_banks, parameter_banks, parameter_bank_names, best_of_parameter_bank
from . import Colors, Options
import Live


class DeviceComponent(DeviceComponentBase):

    def __init__(self, parent, *a, **k):
        self.parent = parent
        super(DeviceComponent, self).__init__(*a, **k)
        self.selected_device_listener()
        self.has_variations = True if Live.Application.get_application().get_major_version() > 10 else False
        # print(["variations",   self.has_variations])
        # print("=============================================")
    def set_mixer(self, mixer):
        self._mixer = mixer

    @property
    def selected_track(self):
        if Options.session_box_linked_to_selection:
            track = self.song().view.selected_track
        else:
            track = self._mixer.channel_strip(0)._track
        return track


    """ VARIATIONS """

    def set_launch_variation_button(self, button):
        self._launch_variation_button = button
        self._on_launch_variation.subject = button

    @subject_slot(u'value')
    def _on_launch_variation(self, value):
        if value or not self._launch_variation_button.is_momentary() and self.has_variations:
            self._device.recall_selected_variation()

    def set_store_variation_button(self, button):
        self._store_variation_button = button
        self._on_store_variation.subject = button

    @subject_slot(u'value')
    def _on_store_variation(self, value):
        if value or not self._store_variation_button.is_momentary() and self.has_variations:
            self._device.store_variation()

    def set_recall_variation_button(self, button):
        self._recall_variation_button = button
        self._on_recall_variation.subject = button

    @subject_slot(u'value')
    def _on_recall_variation(self, value):
        if value or not self._recall_variation_button.is_momentary() and self.has_variations:
            self._device.recall_last_used_variation()

    def set_randomize_macros_button(self, button):
        self._randomize_macros_button = button
        self._on_randomize_macros.subject = button

    @subject_slot(u'value')
    def _on_randomize_macros(self, value):
        if value or not self._randomize_macros_button.is_momentary() and self.has_variations:
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
        if value or not self._prev_variation_button.is_momentary() and self.has_variations:
            if self._device.selected_variation_index > 0:
                self._device.selected_variation_index -= 1
                self._update_name()

    def set_next_variation_button(self, button):
        self._next_variation_button = button
        self._on_jump_to_next_variation.subject = button

    @subject_slot(u'value')
    def _on_jump_to_next_variation(self, value):
        if value or not self._next_variation_button.is_momentary() and self.has_variations:
            if self._device.selected_variation_index < self._device.variation_count-1:
                self._device.selected_variation_index += 1
                self._update_name()

    def _update_name(self):
        appointed_device = self.song().appointed_device
        if appointed_device is not None and self.has_variations:
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