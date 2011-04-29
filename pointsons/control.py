from mididings import Transpose, Process, Filter, PROGRAM, Print, Scene

def test(arg):
    print "ay2", arg

ps_control = Transpose(3) >> Process(test)




