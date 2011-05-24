#!/usr/bin/env python
import logging
from logging import Handler

from gi.repository import Clutter as clutter
from gi.repository import GObject as gobject
from gi.repository import GtkClutter as cluttergtk
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

# Init Clutter
cluttergtk.init(0, "")

import settings

from pointsons.ui.osc_control import OSCControl
from pointsons.ui.configuration import UIConfiguration

from pointsons.configuration import Configurations

from pointsons.ui.bowl import Bowl

from pointsons import logger


class BowlConfigUI(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file('res/interface.glade')

        self.dialog = builder.get_object('bowl_window')

    def run(self):
        r = self.dialog.run()
        print r

        r.destroy()

        self.dialog.destroy()


class BowlAddUI(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file('res/interface.glade')

        self.dialog = builder.get_object('bowl_add_window')

    def run(self):
        r = self.dialog.run()

        if r:
            bowl = Bowl()
            print bowl

        self.dialog.destroy()


class PSLogHandler(Handler):
    def __init__(self):
        Handler.__init__(self, level=logging.DEBUG)
        
    def emit(self, aRecord):
        print aRecord

class AreaCallbacksMixin(object):
    """
    Callbacks for the Area Popup
    """
    def on_area_x_value_changed(self, aWidget):
        self.configs.current.area.x = int(aWidget.get_value())
        print self.configs.current.area

    def on_area_z_value_changed(self, aWidget):
        self.configs.current.area.z = int(aWidget.get_value())

    def on_area_radius_value_changed(self, aWidget):
        self.configs.current.area.radius = int(aWidget.get_value())

class PSUI(AreaCallbacksMixin):
    def __init__(self):
        self.configs = Configurations()
        self.configs.set_current(UIConfiguration(self))

        self.log_handler = PSLogHandler()
        logger.addHandler(self.log_handler)
        
        self.builder = gtk.Builder()
        self.builder.add_from_file('res/interface.glade')

        self.main_window = self.builder.get_object('main_window')
        self.main_window.connect('destroy', self.on_destroy)

        # Create the Clutter stage
        self.canvas = cluttergtk.Embed.new()
        self.stage = self.canvas.get_stage()
        self.stage.set_user_resizable(True)
        
        stage_viewport = self.builder.get_object('stage_viewport')
        stage_viewport.add(self.canvas)

        self.populate_stage()

        # Connect signals
        self.builder.connect_signals(self)

    def on_main_window_show(self, aWidget):
        """
        Try to establish a connection to the server
        """
        self.osc_control.connect_server()

    def on_destroy(self, aWidget):
        gtk.main_quit()

    def populate_stage(self):

        def make_bowl(x, y):
            color = clutter.Color()
            color.from_string("red")

            rect = clutter.Rectangle()
            rect.set_size(100, 100)
            rect.set_position(x, y)
            rect.set_color(color)
            rect.set_reactive(True)

            return rect

        bowl1 = make_bowl(20, 20)
        bowl2 = make_bowl(200, 200)
        
        bowls = [bowl1, bowl2]
            
        def on_rect_click(anEvent, aRectangle):
            print "click:", anEvent, aRectangle
            bowl_config_ui = BowlConfigUI()
            bowl_config_ui.run()

            return True

        bowl1.connect("button-press-event", on_rect_click)
        bowl2.connect("button-press-event", on_rect_click)

        for bowl in bowls:
            self.stage.add_actor(bowl)
            bowl.show()

        
    def main(self):
        # Run an OSC connection to the server
        self.osc_control = OSCControl(self,
                                      settings.SERVER_OSC_PORT,
                                      settings.UI_OSC_PORT)
        
        gobject.idle_add(self.osc_control.recv, 10)

        # Display everything !
        self.main_window.show_all()
        
        # Gtk main loop
        gtk.main()


    #-- Callback --#
    def on_bowl_add_activate(self, aWidget):
        dialog = BowlAddUI()
        dialog.run()

    def on_configure_area_activate(self, aWidget):
        config_win = self.builder.get_object('area_window')
        print "dialog", config_win.run()
        config_win.hide()


if __name__ == "__main__":
    psui = PSUI()
    psui.main()
    




