import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
import math

FILE_DIR = "./assets/component.png"

class Rectangle(elm.Element): 
    def __init__(self, **kwargs):
        resheight = 0.25
        reswidth = 1.0 / 6
        gap = (math.nan, math.nan)
        super().__init__(**kwargs)
        self.segments.append(Segment(
            [(0, 0), (0, resheight), (reswidth*6, resheight),
             (reswidth*6, -resheight), (0, -resheight), (0, 0),
             gap, (reswidth*6, 0)]))

class Schematic:
    def __init__(self):
        pass

    def save(self, drawer):
        drawer.draw(show=False)
        drawer.save(FILE_DIR)
        del drawer

    def genComponent(self, component):
        d = schemdraw.Drawing()
        d += component
        self.save(d)

    def iSaved(self, component):
        try:
            self.genComponent(component)
            return True
        except:
            return False

    def genCapacitor(self):
        return self.iSaved(elm.Capacitor())

    def genResistor(self):
        return self.iSaved(elm.Resistor())

    def genSource(self):
        return self.iSaved(elm.SourceV().right())
        
    def genInductor(self):
        return self.iSaved(elm.Inductor())

    
"""
TLOC
d += elm.DataBusLine().length(2).flip()
d += elm.Line().length(1).up()
d += Rectangle()
d.move(1, -1)
d += elm.Line().up().linewidth(4)
d.move(0, -3)
d += elm.Line().length(2).right().linewidth(4)

TLIN
d += elm.DataBusLine().length(1).scale(0.4).flip()
d += Rectangle()
d.move(1,0)
d += elm.Line().length(1)

TLSC
d += elm.DataBusLine().length(2).flip()
d += elm.ResistorIEC().length(2).up()
d += elm.Line().length(1).right()
d.move(0, 0.5)
d += elm.Line().length(2.5).down().linewidth(4)
d += elm.Line().length(2).right().linewidth(4)

GROUND
elm.Ground()

    def genComponent(self, component, name, value, orientation):
        d = schemdraw.Drawing()
        if orientation == 'H':
            d += component.label([name, value])
        else:
            d += component.label([name, value]).up()
        self.save(d)

    def iSaved(self, component, name, value, orientation):
        try:
            self.genComponent(component, name, value, orientation)
            return True
        except:
            return False

    def genCapacitor(self, id, unit, value, orientation):
        return self.iSaved(elm.Capacitor(), "C" + str(id), str(value) + unit, orientation)

    def genResistor(self, id, unit, value, orientation):
        return self.iSaved(elm.Resistor(), "R" + str(id), str(value) + unit, orientation)

    def genSource(self, id, unit, value, orientation):
        return self.iSaved(elm.SourceV(), "V" + str(id), str(value) + unit, orientation)
        
    def genInductor(self, id, unit, value, orientation):
        return self.iSaved(elm.Inductor(), "R" + str(id), str(value) + unit, orientation)


gen = Schematic()
if (gen.genCapacitor(1, "Ω", 50, "H")):
    print("La imagen se guardo con exito")

"""

gen = Schematic()
if (gen.genSource()):
    print("La imagen se guardo con exito")