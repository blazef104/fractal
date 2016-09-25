import svgwrite, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image

width = 900
height = 900
class Win(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Fractal Generator")
        vbox = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(spacing = 5)
        hbox1 = Gtk.Box(spacing = 5)
        self.add(vbox)

        label = Gtk.Label("Generate your fractal, more features to come...")
        vbox.pack_start(label, True, True, 0)



        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        vbox.pack_start(self.pbar, True, True, 0)

        labelW = Gtk.Label("Width: ")
        self.entryWidth = Gtk.Entry()
        self.entryWidth.set_text(str(width))

        labelH = Gtk.Label("Height: ")
        self.entryHeight = Gtk.Entry()
        self.entryHeight.set_text(str(height))

        hbox1.pack_start(labelW, True, True, 0)
        hbox1.pack_start(self.entryWidth, True, True, 0)
        hbox1.pack_start(labelH, True, True, 0)
        hbox1.pack_start(self.entryHeight, True, True, 0)
        vbox.pack_start(hbox1, True, True, 0)

        vbox.pack_start(hbox, True, True, 0)

        radioBox = Gtk.Box(spacing=5)
        self.svgButton = Gtk.CheckButton.new_with_label("Generate as .SVG file")
        self.pngButton = Gtk.CheckButton.new_with_label("Generate as .PNG file")
        self.pngButton.set_active(True)
        self.svgButton.set_active(False)
        radioBox.pack_start(self.svgButton, True, True, 0)
        radioBox.pack_start(self.pngButton, True, True, 0)
        vbox.pack_start(radioBox, True, True, 0)


        button = Gtk.Button.new_with_label("Generate!")
        button.connect("clicked", self.fract)

        hbox.pack_start(button, True, True, 0)

    def fract(self, button):
        self.pbar.set_text("Generating SVG file")
        global width, height
        width = int(self.entryWidth.get_text())
        height = int(self.entryHeight.get_text())
        if (self.svgButton.get_active()):
            print("Generating svg. Dimension: ", width, height)
            generateMandelbrot()
            return
        print("Generating png. Dimension: ", width, height)
        generateMandelbrot_new()
        return

def generateMandelbrot_new():
    img = Image.new("RGB", (width, height))
    arr = []
    a = 0
    while(a<width):
        b = 0
        while (b<height):
            checkMembership(a, b, arr)
            b+=1
        a+=1
    img.putdata(arr)
    img.save("fract.png")
    print("Done")
    return

def generateMandelbrot():
    draw = svgwrite.Drawing(filename = "test-fract.svg", size = (str(width)+"px", str(width)+"px"))
    a = 0
    while (a<=width):
        b = 0
        while (b<=height):
            checkMembership(a,b, draw)
            b+=1
        a+=1
    print(draw.tostring())
    draw.save()
    print("Done!")
    return


def checkMembership(x, y, draw):
    x1 = (x-(width*0.7))/(width*0.28)
    y1 = (y-(height-(height/2)))/(height/2)


    #print("checking", x1, y1)
    z0 = 0
    z = complex(x1, y1)
    n = 0
    while(n<256):
        z0 = z0**2 + z
        if(abs(z0)>200):
            if(type(draw) is list):
                draw.append((0,0,255))
                return
            #print("diverges with z=", abs(z0))
            return
        n+=1
    if(type(draw) is list):
        draw.append((0,255,0))
        return
    drawPoint(x,y, draw, color="black")
    #print("converges")
    return

def drawPoint(x, y, draw, color):
    draw.add(draw.circle((x, y), 1, fill=color))
    return

window = Win()
window.connect("delete_event", Gtk.main_quit)
window.show_all()
Gtk.main()
