from mididings import config

config(
    backend='alsa',
    client_name='pointsons',
    in_ports=1,
    out_ports=1,
    start_delay=0.5 # to prevent too early bindings
)


DEBUG = True

# Servers config
UI_OSC_PORT = 56420
SERVER_OSC_PORT = 56418
KINECT_OSC_PORT = ('fresnoy.local', 56419) #('localhost', 56419) 

# Musical config
MIDI_HAMMER_CHANNEL = 1
MIDI_DAMPER_CHANNEL = 2
MIDI_REPEAT_CHANNEL = 3
BOWL_LOWER = 'c2'
BOWL_UPPER = 'c4'


