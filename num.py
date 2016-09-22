import svgwrite, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Win(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Fractal Generator")
        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button.new_with_label("Generate!")
        button.connect("clicked", self.fract)
        hbox.pack_start(button, True, True, 0)

    def fract(self, button):
        generateMandelbrot()
        return

def generateMandelbrot():
    draw = svgwrite.Drawing(filename = "test-fract.svg", size = ("900px", "600px"))
    a = 0
    while (a<=600):
        b = 0
        while (b<=600):
            checkMembership(a,b, draw)
            b+=1
        a+=1
    print(draw.tostring())
    draw.save()
    return


def checkMembership(x, y, draw):
    #print("checking", x, y)
    x1 = (x-300)/200
    y1 = (y-300)/200
    print("checking", x1, y1)
    z0 = 0
    z = complex(x1, y1)
    n = 0
    while(n<256):
        z0 = z0**2 + z
        if(abs(z0)>200):
            #drawPoint(x, y, draw, color="white")
            print("diverges with z=", abs(z0))
            return
        n+=1
    drawPoint(x,y, draw, color="black")
    print("converges")
    return

def drawPoint(x, y, draw, color):
    draw.add(draw.circle((x, y), 1, fill=color))
    return

window = Win()
window.connect("delete_event", Gtk.main_quit)
window.show_all()
Gtk.main()
