from mididings import config

config(
    backend='alsa',
    client_name='pointsons',
    in_ports=1,
    out_ports=1,
    start_delay=0.5 # to prevent too early bindings
)


DEBUG = True


UI_OSC_PORT = 56420
SERVER_OSC_PORT = 56418
KINECT_OSC_PORT = 56419





