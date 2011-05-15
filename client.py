#!/usr/bin/python
import logging
from logging import Handler

from gi.repository import Clutter as clutter
from gi.repository import GObject as gobject
from gi.repository import GtkClutter as cluttergtk
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

# Init Clutter
cluttergtk.init(0, "")

from pointsons.ui.osc_control import OSCControl

logger = logging.getLogger('pointsons')

class PSUIConfig(object):
    pass

class BowlConfigUI(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file('res/interface.glade')

        self.window = builder.get_object('bowl_window')

    def run(self):
        self.window.show_all()

class PSLogHandler(Handler):
    def __init__(self):
        Handler.__init__(self, level=logging.DEBUG)
        
    def emit(self, aRecord):
        print aRecord


class PSUI(object):
    def __init__(self):
        self.config = PSUIConfig()
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
        self.osc_control = OSCControl(self, 56418, 56419)
        gobject.idle_add(self.osc_control.recv, 10)

        # Display everything !
        self.main_window.show_all()
        
        # Gtk main loop
        gtk.main()
        

if __name__ == "__main__":
    psui = PSUI()
    psui.main()
    




