from mididings import Transpose, Process, Filter, PROGRAM, Print, Scene

def debug(event):
    print "got event:", event

ps_control = Process(debug)




