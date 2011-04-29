from mididings import config

config(
    backend='alsa',
    client_name='pointsons',
    in_ports=1,
    out_ports=1,
    start_delay=0.5 # to prevent too early bindings
)


DEBUG = True





