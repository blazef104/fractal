import svgwrite, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image

class Win(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Fractal Generator")
        vbox = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(spacing = 5)

        self.add(vbox)

        label = Gtk.Label("Generate your fractal, more features to come...")
        vbox.pack_start(label, True, True, 0)

        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        vbox.pack_start(self.pbar, True, True, 0)

        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button.new_with_label("Generate SVG")
        button.connect("clicked", self.fract_svg)

        button1 = Gtk.Button.new_with_label("Generate PNG")
        button1.connect("clicked", self.fract_png)

        hbox.pack_start(button, True, True, 0)
        hbox.pack_start(button1, True, True, 0)

    def fract_svg(self, button):
        self.pbar.set_text("Generating SVG file")
        generateMandelbrot()
        return

    def fract_png(self, button1):
        self.pbar.set_text("Generating PNG file")
        # self.pbar.set_fraction(perc)
        # self.pbar.pulse()
        generateMandelbrot_new()
        return

def generateMandelbrot_new():
    print("generating png")
    img = Image.new("RGB", (600, 600))
    arr = []
    a = 0
    while(a<600):
        b = 0
        while (b<600):
            checkMembership(a, b, arr)
            b+=1
        a+=1
    img.putdata(arr)
    img.save("fract.png")
    print("Done")
    return

def generateMandelbrot():
    draw = svgwrite.Drawing(filename = "test-fract.svg", size = ("600px", "600px"))
    a = 0
    while (a<=600):
        b = 0
        while (b<=600):
            checkMembership(a,b, draw)
            b+=1
        a+=1
    print(draw.tostring())
    draw.save()
    print("Done!")
    return


def checkMembership(x, y, draw):
    #print("checking", x, y)
    x1 = (x-450)/200
    y1 = (y-300)/200


    print("checking", x1, y1)
    z0 = 0
    z = complex(x1, y1)
    n = 0
    while(n<256):
        z0 = z0**2 + z
        if(abs(z0)>200):
            #drawPoint(x, y, draw, color="white")
            if(type(draw) is list):
                print("diverges")
                draw.append((0,0,255))
                return
            print("diverges with z=", abs(z0))
            return
        n+=1
    if(type(draw) is list):
        draw.append((0,255,0))
        return
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
