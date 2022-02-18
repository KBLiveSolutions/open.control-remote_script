import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
import logging, traceback
logger = logging.getLogger(__name__)
def print(text):
    logger.warning(text)

BROWSER_TAGS = ('Drums', 'Instruments', 'Audio Effects', 'MIDI Effects', 'Max for Live')

class CustomBrowserItem:
    def __init__(self, item, parent_folder, is_folded = True):
        self.item = item
        self.uri = item.uri
        self.name = item.name
        self.children = item.children
        self.is_folder = item.is_folder
        self.parent_folder = parent_folder
        self.is_container = False
        self.is_folded = is_folded
        if len(self.item.children) > 0:
            self.is_container = True
        return super(CustomBrowserItem, self).__init__()

class BrowserComponent(ControlSurfaceComponent):
    def __init__(self, parent):
        print("browser")
        ControlSurfaceComponent.__init__(self, parent)
        self.parent = parent
        self.item_index = None
        self.selected_item = None
        # self.get_browser_tags()        
        self.browser = self.application().browser
        self.application().view.add_browse_mode_listener(self.on_hotswap_changed)
        self.browser_categories = [self.browser.audio_effects] #, self.browser.instruments, self.browser.packs, self.browser.drums, self.browser.midi_effects , self.browser.max_for_live, self.browser.plugins, self.browser.user_library, self.browser.current_project, self.browser.sounds]

    # Initiate Hotswap
    def initiate_hotswap(self):
        self.browser_items = []
        for item in self.browser_categories:
            self.get_hotswap_index(item)
        print("INIT")
        self.item_index = self.get_item_index(self.browser_items, self.selected_item)

    def get_hotswap_index(self, item):
        for sub_item in item.children:
            browser_item = CustomBrowserItem(sub_item, item)
            self.browser_items.append(browser_item)
            if self.browser.relation_to_hotswap_target(sub_item) == Live.Browser.Relation.ancestor:
                browser_item.is_folded = False
                self.get_hotswap_index(sub_item)
            elif self.browser.relation_to_hotswap_target(sub_item) == Live.Browser.Relation.equal:
                self.currently_open_folder = self.get_custom_browser_item(browser_item.parent_folder)
                list_children = list(item.iter_children)
                for sel in list_children:
                    if sel.uri == browser_item.uri:
                        self.selected_item = browser_item


    def get_selected_index(self):
        for item in self.browser_categories:
            for sub_item in item.children:
                print([sub_item.name, sub_item.is_selected])
                # browser_item = CustomBrowserItem(sub_item, item)
                # self.browser_items.append(browser_item)
                # if self.sub_item.is_selected:
                #     browser_item.is_folded = False
                #     self.get_hotswap_index(sub_item)
                # else:
                #     self.currently_open_folder = self.get_custom_browser_item(browser_item.parent_folder)
                #     list_children = list(item.iter_children)
                #     for sel in list_children:
                #         if sel.uri == browser_item.uri:
                #             self.selected_item = browser_item

    def get_item_index(self, _list, item):
        index = -1
        for i, sel in zip(range(len(_list)), _list):
            if sel.uri == item.uri:
                print(["BIIIIIIM", i, sel.name, sel.uri, item.uri])
                index = i
        return index
    
    def get_custom_browser_item(self, item):
        it = None
        for i in self.browser_items:
            if i.item == item:
                it = i
        return it
    # Update Browser

    def remove_folder(self):
        self.currently_open_folder.is_folded = True
        print("REMOVE")
        self.currently_open_folder_index = self.get_item_index([i.item for i in self.browser_items], self.currently_open_folder)
        pop_start = self.currently_open_folder_index + 1
        pop_end = self.currently_open_folder_index + len(list(self.currently_open_folder.children)) + 1
        self.browser_items = self.browser_items[0:pop_start] + self.browser_items[pop_end:]
        self.currently_open_folder = None

    def add_folder(self, inserted_folder):
        print("ADD")
        insert_index = self.get_item_index(self.browser_items, self.selected_item) + 1
        self.browser_items = self.browser_items[0:insert_index] + inserted_folder + self.browser_items[insert_index:]

    # Open Folder
    def set_open_folder(self, button):
        self._open_folder_button = button
        self.open_folder.subject = button

    @subject_slot(u'value')
    def open_folder(self, value):
        if value:
            self.go_right()
            inserted_folder = [CustomBrowserItem(item, self.selected_item.item) for item in list(self.selected_item.children)]
            self.selected_item.is_folded = False
            if self.currently_open_folder and self.currently_open_folder: # is not self.get_custom_browser_item(self.selected_item.parent):
                self.remove_folder()
            self.add_folder(inserted_folder)
            self.currently_open_folder = self.selected_item
            self.collapse_folders()
            self.item_index = self.get_item_index(self.browser_items, self.selected_item)
            self.print_browser()

    def print_browser(self):
        print("==============================")
        for i in self.browser_items:
            print(["===>", i.name, i.is_folded])
        print("==============================")
        print("==============================")

    # Close Folder
    def set_close_folder(self, button):
        self._close_folder_button = button
        self.close_folder.subject = button

    @subject_slot(u'value')
    def close_folder(self, value):
        if value:
            direction = self.application().view.NavDirection.left
            self.application().view.scroll_view(direction, u'Browser', False)
            self.remove_folder()

    #Hotswap
    def set_hotswap(self, button):
        self._hotswap_button = button
        self._on_hotswap.subject = button

    @subject_slot(u'value')
    def _on_hotswap(self, value):
        if value:
            self.application().view.toggle_browse()

    def on_hotswap_changed(self):
        if self.application().view.browse_mode:
            self.initiate_hotswap()
        else:
            self.parent.display_message("Browser", "Hotswap Off")  

    #Select Next
    def set_load_next(self, button):
        self._load_next_button = button
        self._on_load_next.subject = button

    @subject_slot(u'value')
    def _on_load_next(self, value):
        if value:
            print("refresh")
            # self.browser.full_refresh = 1
            # self.get_selected_index()

    def collapse_folders(self):
        _len = len(self.selected_item.children)
        if len(self.selected_item.children[0].children) > 0:
            for i in range(_len):
                for j in range(i+1):
                    print("down")
                    self.go_down()
                print("++++++++++++++")
                for i in range(4):
                    self.go_left()
                for i in range(2):
                    self.go_right()



            # self.initiate_hotswap()
            # self.select_item('Next')
            # self.load_selected_item(1)
            # self.display_item_name()

    #Select Prev
    def set_load_prev(self, button):
        self._load_prev_button = button
        self._on_load_prev.subject = button

    @subject_slot(u'value')
    def _on_load_prev(self, value):
        if value:
            self.initiate_hotswap()
            self.select_item('Prev')
            self.load_selected_item(1)
            self.display_item_name()

    # Select Prev/Next (Encoder)
    def set_prev_next_item(self, button):
        self._prev_next_item_button = button
        self._on_prev_next_item.subject = button

    @subject_slot(u'value')
    def _on_prev_next_item(self, value):
        if value > 64:
            self.select_item('Next')
        if value < 64:
            self.select_item('Prev')
        self._prev_next_item_button.send_value(64, force=True)

    def select_item(self, direction):
        if direction == "Next":
            self.go_down()
            if self.item_index and self.item_index < len(self.browser_items)-1:
                self.item_index += 1
        elif direction == "Prev":
            self.go_up()
            if self.item_index and self.item_index > 0:
                self.item_index -= 1
        if self.item_index:
            self.selected_item = self.browser_items[self.item_index]
            print(["SELECTED", self.item_index, self.selected_item.name, self.selected_item.is_folded])
            self.display_item_name()

    def go_down(self):
        direction = self.application().view.NavDirection.down
        self.application().view.scroll_view(direction, u'Browser', False)
    def go_up(self):
        direction = self.application().view.NavDirection.up
        self.application().view.scroll_view(direction, u'Browser', False)
    def go_right(self):
        direction = self.application().view.NavDirection.right
        self.application().view.scroll_view(direction, u'Browser', False)
    def go_left(self):
        direction = self.application().view.NavDirection.left
        self.application().view.scroll_view(direction, u'Browser', False) 

    # Load Item
    def set_load_item(self, button):
        self._load_item_button = button
        self.load_selected_item.subject = button

    @subject_slot(u'value')
    def load_selected_item(self, value):
        if value:
            if self.application().view.browse_mode:
                if len(list(self.selected_item.children)) > 0:
                    print("OPEN FOLDER")
                    if self.selected_item.is_folded:
                        print("OPEN")
                        self.open_folder(1)
                    else:
                        print("CLOSE")
                        self.close_folder(1)
                else:
                    self.browser.load_item(self.selected_item.item)
            else:
                self.go_right()


    # Display Item Name
    def display_item_name(self):
        name = self.selected_item.name
        if self.selected_item.is_container:
            name = "> " + name.ljust(6)
        self.parent.display_message("Browser", name)      