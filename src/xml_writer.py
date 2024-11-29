import xml.sax
from math import ceil, floor

# this class is no longer in use

class XML_Writer():

    def __init__(self, height: int, width: int, x_offset: int, y_offset: int, radius: int):
        self.height = height
        self.width = width
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.radius = radius
        self.outfile = open('graph.svg','w')
        self.Head()
        self.Add_Scene()


    def Head(self):
        self.outfile.write('<?xml version="1.0"?>\n')
        self.outfile.write('<!DOCTYPE svg>\n')
        self.outfile.write(f'<svg viewBox="-{self.width/4} -{self.height/4} {self.width/2} {self.height/2}" style="background: white" xmlns="http://www.w3.org/2000/svg">\n')


        return
    
    def Add_Scene(self):
        x_1 = self.width/2 + self.x_offset
        x_2 = -self.width/2 + self.x_offset
        y_1 = self.y_offset
        y_2 = self.y_offset
        self.outfile.write(f'       <line x1="{x_1}" y1="{y_1}" x2="{x_2}" y2="{y_2}" style="stroke:black;stroke-width:{ceil(self.width/300)}"/>\n')

        x_1 = self.x_offset
        x_2 = self.x_offset
        y_1 = self.height/2 + self.y_offset
        y_2 = -self.height/2 + self.y_offset
        self.outfile.write(f'       <line x1="{x_1}" y1="{y_1}" x2="{x_2}" y2="{y_2}" style="stroke:black;stroke-width:{ceil(self.height/300)}"/>\n')
        for x in range(floor(self.width/100)):
            self.outfile.write(f'       <line x1="{x*self.width/10}" y1="{-self.height/2+self.y_offset}" x2="{x*self.width/10}" y2="{self.height/2+self.y_offset}" style="stroke:grey;stroke-width:{ceil(self.height/600)}"/>\n')
            self.outfile.write(f'       <line x1="{-x*self.width/10}" y1="{-self.height/2+self.y_offset}" x2="{-x*self.width/10}" y2="{self.height/2+self.y_offset}" style="stroke:grey;stroke-width:{ceil(self.height/600)}"/>\n')

        for y in range(floor(self.height/100)):
            self.outfile.write(f'       <line x1="{-self.width/2+self.x_offset}" y1="{y*self.height/10}" x2="{self.width/2+self.x_offset}" y2="{y*self.height/10}" style="stroke:grey;stroke-width:{ceil(self.height/600)}"/>\n')
            self.outfile.write(f'       <line x1="{-self.width/2+self.x_offset}" y1="{-y*self.height/10}" x2="{self.width/2+self.x_offset}" y2="{-y*self.height/10}" style="stroke:grey;stroke-width:{ceil(self.height/600)}"/>\n')

        self.outfile.write(f'       <line x1="{ceil(self.width/1000)}" y1="{10+self.y_offset}" x2="{-ceil(self.width/1000)}" y2="{10+self.y_offset}" style="stroke:black;stroke-width:{ceil(self.height/200)}"/>\n')


        return

    def Add_Point(self, point: tuple[int, int],radius: int):
        self.outfile.write(f'       <circle r="{radius}" cx="{point[0]+self.x_offset}" cy="{point[1]+self.y_offset}" fill="black"/>\n')
        return
    

    def Final(self):
        self.outfile.write(f'</svg>')
        return


    def Add_All_Points(self, points, radius: int):
        x_intervall= (-self.width/2+self.x_offset,self.width/2+self.x_offset)
        y_intervall= (-self.height/2+self.y_offset,self.height/2+self.y_offset)
        print(points)
        for p in points:
            if x_intervall[0] <= p[0] and p[0] <= x_intervall[1]and y_intervall[0] <= p[0] and p[0] <= y_intervall[1]:
                self.Add_Point(p, radius)
        return