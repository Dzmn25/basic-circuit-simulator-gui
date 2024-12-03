import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
import math

FILE_DIR = "./assets/component.png"

INDUCTOR = 'L'
CAPACITOR = 'C'
RESISTOR = 'R'
SOURCE = 'V'
TLIN = 'N'
TLSC = 'G'
TLOC = 'O'


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
        self.id = {
            RESISTOR : 1,
            SOURCE : 1,
            CAPACITOR : 1,
            INDUCTOR : 1,
            TLIN : 1,
            TLSC : 1,
            TLOC : 1
            }

    def getId(self, character):
        aux = self.id[character]
        self.id[character] += 1
        return character + str(aux)
    
    def save(self, drawer):
        drawer.draw(show=False)
        drawer.save(FILE_DIR)
        del drawer

    def genComponent(self, component, values, horizontal):
        d = schemdraw.Drawing()
        if horizontal:
            d += component.label(values).right()
        else:
            d += component.label(values).up()
        self.save(d)

    def iSaved(self, component, values, horizontal):
        try:
            self.genComponent(component, values, horizontal)
            return True
        except:
            print("Algo salio mal")
            return False

    def genCapacitor(self, values, horizontal=True): # TESTED
        id = self.getId(CAPACITOR)
        values.insert(0, id)
        return id if self.iSaved(elm.Capacitor(), values, horizontal) else None

    def genResistor(self, values, horizontal=True): # TESTED
        id = self.getId(RESISTOR)
        values.insert(0, id)
        return id if self.iSaved(elm.Resistor(), values, horizontal) else None

    def genSource(self, values, horizontal=True): #TESTED
        id = self.getId(SOURCE)
        values.insert(0, id)
        return id if self.iSaved(elm.SourceV(), values, horizontal) else None
        
    def genInductor(self, values, horizontal=True): 
        id = self.getId(INDUCTOR)
        values.insert(0, id)
        return id if self.iSaved(elm.Inductor(), values, horizontal) else None
    
    def genTLIN(self, values, horizontal=True):
        id = self.getId(TLIN)
        values.insert(0, id)
        return id if self.iSaved(elm.Line().color("yellow"), values, horizontal) else None
    
    def genTLOC(self, values, horizontal=True):
        id = self.getId(TLOC)
        values.insert(0, id)
        return self.iSaved(elm.Line().color("purple"), values, horizontal)
    
    def genTLSC(self, values, horizontal=True):
        id = self.getId(TLSC)
        values.insert(0, id)
        return self.iSaved(elm.Line().color("cian"), values, horizontal)



"""gen = Schematic()
values = ["50000 Ω"]
result = gen.genInductor(values, False)
if result != None:
    print(result)"""

# ANTIGUA FORMA DE GENERAR STUBS (NO VIABLE)
    
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

"""


# GENERAR IMAGENES UNA SOLA VEZ

"""
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
    

gen = Schematic()
if (gen.genSource()):
    print("La imagen se guardo con exito")
    
"""
