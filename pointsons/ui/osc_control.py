# -*- coding: utf-8 -*-
import logging

import liblo

logger = logging.getLogger('pointsons')

class OSCControl(liblo.Server):
    def __init__(self, aPSUI, control_port, listen_port):
        liblo.Server.__init__(self, listen_port)

        self.psui = aPSUI
        self.control_port = control_port

        self._scenes = {}

    def connect_server(self):
        spinner = self.psui.builder.get_object('connection_spinner')
        spinner.start()
        
        self.query()

    def query(self):
        self.send(self.control_port, '/mididings/query')

    def switch_scene(self, n):
        self.send(self.control_port, '/mididings/switch_scene', n)

    def switch_subscene(self, n):
        self.send(self.control_port, '/mididings/switch_subscene', n)

    def prev_scene(self):
        self.send(self.control_port, '/mididings/prev_scene')

    def next_scene(self):
        self.send(self.control_port, '/mididings/next_scene')

    def prev_subscene(self):
        self.send(self.control_port, '/mididings/prev_subscene')

    def next_subscene(self):
        self.send(self.control_port, '/mididings/next_subscene')

    def panic(self):
        self.send(self.control_port, '/mididings/panic')

    @liblo.make_method('/mididings/data_offset', 'i')
    def data_offset_cb(self, path, args):
        print "data_offset_cb", path, args
        #self.dings.set_data_offset(args[0])

    @liblo.make_method('/mididings/begin_scenes', '')
    def begin_scenes_cb(self, path, args):
        self._scenes = {}

    @liblo.make_method('/mididings/add_scene', None)
    def add_scene_cb(self, path, args):
        number, name = args[:2]
        subscenes = args[2:]
        
        logger.info(u"Ajout d'une scène : %d - %s" % (number, name))

        self._scenes[number] = (name, subscenes)

    @liblo.make_method('/mididings/end_scenes', '')
    def end_scenes_cb(self, path, args):
        print "end_scenes_cb", path, args
        spinner = self.psui.builder.get_object('connection_spinner')
        spinner.stop()

        connection_status_label = self.psui.builder.get_object('connection_status_label')
        connection_status_label.set_label('Connecté')

        logger.info(u"Connecté au serveur")
        

    @liblo.make_method('/mididings/current_scene', 'ii')
    def current_scene_cb(self, path, args):
        print "current_scene_cb", path, args
        #self.dings.set_current_scene(args[0], args[1])






