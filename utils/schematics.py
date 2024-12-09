import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
import matplotlib
matplotlib.use('Agg') 

FILE_DIR = "./assets/component.png"

INDUCTOR = 'L'
CAPACITOR = 'C'
RESISTOR = 'R'
SOURCE = 'V'
TLIN = 'N'
TLSC = 'G'
TLOC = 'O'
        

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
    
    def removed(self, typ):
        self.id[typ] -= 1
    
    def save(self, drawer):
        drawer.draw(show=False)
        drawer.save(FILE_DIR)
        del drawer
        matplotlib.pyplot.close()

    def genComponent(self, component, id, horizontal):
        d = schemdraw.Drawing()
        if horizontal:
            d += component.label(id).right()
        else:
            d += component.label(id).up()
        self.save(d)

    def iSaved(self, component, id, horizontal):
        try:
            self.genComponent(component, id, horizontal)
            return True
        except:
            print("Algo salio mal")
            return False

    def genCapacitor(self, horizontal=True): # TESTED
        id = self.getId(CAPACITOR)
        return id if self.iSaved(elm.Capacitor(), id, horizontal) else None

    def genResistor(self, horizontal=True): # TESTED
        id = self.getId(RESISTOR)
        return id if self.iSaved(elm.Resistor(), id, horizontal) else None

    def genSource(self, horizontal=True): #TESTED
        id = self.getId(SOURCE)
        return id if self.iSaved(elm.SourceV(), id, horizontal) else None
        
    def genInductor(self, horizontal=True): 
        id = self.getId(INDUCTOR)
        return id if self.iSaved(elm.Inductor(), id, horizontal) else None
    
    def genTLIN(self, horizontal=True): #TESTED
        id = self.getId(TLIN)
        return id if self.iSaved(elm.Line().color("gray"), id, horizontal) else None
    
    def genTLOC(self, horizontal=True): #TESTED
        id = self.getId(TLOC)
        return id if self.iSaved(elm.Line().color("purple"), id, horizontal) else None
    
    def genTLSC(self, horizontal=True): #TESTED
        id = self.getId(TLSC)
        return id if self.iSaved(elm.Line().color("orange"), id, horizontal) else None
    
    def genGround(self, horizontal=True):
        id = " "
        return id if self.iSaved(elm.Line().color("brown"), id, horizontal) else None
    
    def genConector(self, horizontal=True):
        id = "     "
        return id if self.iSaved(elm.Line(), id, horizontal) else None

    def genImg(self, component, horizontal):
        id = None
        if component == 'O':
            id = self.genTLOC(horizontal)
        elif component == 'N':
            id = self.genTLIN(horizontal)
        elif component == 'G':
            id = self.genTLSC(horizontal)
        elif component == 'R':
            id = self.genResistor(horizontal)
        elif component == 'V':
            id = self.genSource(horizontal)
        elif component == 'L':
            id = self.genInductor(horizontal)
        elif component == 'C':
            id = self.genCapacitor(horizontal)
        elif component == 'U':
            self.genConector(horizontal)
            id = " "
        elif component == 'T':
            self.genGround(horizontal)
            id = " "
        return id


"""gen = Schematic()
result = gen.genInductor()
if result != None:
    print(result)"""

# ANTIGUA FORMA DE GENERAR STUBS (NO VIABLE)
    
"""
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
