from tkinter import Misc
from typing import Any, Literal
import src.graphs as graphs
from src.log import log
from tkinter import *
from math import ceil, floor
from src.calculations import read_term

class Application():

    def __init__(self):
        button_bg = '#5555af'
        button_fg = '#ffffff'
        root_bg = '#1f1f2f'
        zoom = 1

        self.root = Tk()
        self.root.geometry("1200x900")
        self.root.title("Graphical Calculator")
        self.root.configure(border = 0, background = root_bg)

        self.zoom_scale = Scale(
                                self.root,
                                from_ = 0.01,
                                to = 400,
                                orient = 'horizontal',
                                bg = '#4f4f5f',
                                fg = '#ffffff',
                                repeatdelay = 750,
                                command = self.change_zoom
                                )
        self.zoom_scale.set(1)
        self.zoom_scale.place(
                              relx = 0.18,
                              rely = 0.01,
                              relwidth=0.7,
                              height = 40
                              )

        func_frame = Frame(self.root, bg='#0f0f1f')
        func_frame.place(
                         relx = 0.0,
                         rely = 0.05,
                         relwidth = 0.18,
                         relheight=0.9
                         )

        self.canvas = Graphics(self.root, bg = '#868686')
        self.canvas.initialise(func_frame, button_bg, button_fg, zoom)
        self.canvas.place(
                          relx = 0.18,
                          rely = 0.05,
                          relwidth = 0.7,
                          relheight = 0.9
                          )

        entry_add_button = Button(
                                  self.root,
                                  bg=button_bg,
                                  fg=button_fg,
                                  text = 'add function',
                                  command = self.canvas.add_graph
                                  )
        entry_add_button.place(relx = 0.02, y = 20, height = 20, relwidth = 0.12)

        x_offset_label = Label(self.root, text='x offset:')
        x_offset_label.place(
                             relx = 0.895,
                             y = 20,
                             height = 20,
                             relwidth= 0.085
                             )
        
        self.x_offset_entry = Entry(self.root)
        self.x_offset_entry.place(
                                  relx = 0.895,
                                  y = 40,
                                  height = 20,
                                  relwidth= 0.1
                                  )
        x_offset_button = Button(self.root, text= 'y', command = self.set_x)
        x_offset_button.place(
                              relx = 0.98,
                              y = 20,
                              height = 20,
                              relwidth= 0.015
                              )

        y_offset_label = Label(
                               self.root,
                               text='x offset:'
                               )
        y_offset_label.place(
                             relx = 0.895,
                             y = 80,
                             height = 20,
                             relwidth= 0.085
                             )
        self.y_offset_entry = Entry(self.root)
        self.y_offset_entry.place(
                                  relx = 0.895,
                                  y = 100,
                                  height = 20,
                                  relwidth = 0.1
                                  )
        y_offset_button = Button(
                                 self.root,
                                 text= 'y',
                                 command = self.set_y
                                 )
        y_offset_button.place(
                              relx = 0.98,
                              y = 80,
                              height = 20,
                              relwidth= 0.015
                              )

    def run(self):
        self.root.mainloop()

    def change_zoom(self, zoom):
        zoom = float(zoom)
        self.zoom_scale.configure(resolution = zoom/100)
        self.zoom = zoom
        self.canvas.set_zoom(zoom)
        self.canvas.reset()
        self.canvas.render_all()

    def set_x(self):
        self.canvas.set_x(float(read_term(self.x_offset_entry.get())))
    def set_y(self):
        self.canvas.set_y(float(read_term(self.y_offset_entry.get())))

class graph_entry():

    def __init__(self, frame, canvas: Canvas, button_bg, button_fg, zoom):
        self.graph = graphs.Graph()
        self.data_points = []
        self.canvas = canvas
        self.zoom = zoom

        self.graph_entry = Entry(
                                frame
                                )
        self.graph_entry.insert(
                                0, 'y = '
                                )
        self.button_visibility = Button(
                                        frame,
                                        text = 'refresh',
                                        bg = button_bg,
                                        fg = button_fg,
                                        command = self.set_func
                                        )
        self.button_remove = Button(
                                    frame,
                                     text = 'x',
                                     bg = button_bg,
                                     fg = button_fg
                                    )


    def set_func(self):

        if self.graph.function == self.graph_entry.get():
            return
        self.graph.set_function(self.graph_entry.get())
        self.graph.points.clear()
        self.canvas.reset()
        if not self.graph.function.find('x'):
            self.graph.calculate_point(0)
            self.canvas.render_all()
            return
        self.canvas.max_width = 0
        self.calculate_interval(0)
        return

    
    def calculate_interval(self, max_width):


        height = self.canvas.winfo_height()/self.zoom
        width = self.canvas.winfo_width()/self.zoom
        if max_width == 0:
            self.graph.calculate_interval(-width/2, width/2, self.zoom, True)
        else:
            if max_width < width:
                self.canvas.max_width = width
                self.graph.calculate_interval(-width/2, -max_width/2, self.zoom, True)
                self.graph.calculate_interval(max_width/2, width/2, self.zoom, False)

        self.canvas.render_all()
        return

    def render(self):
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        x = self.canvas.x_offset
        y = self.canvas.y_offset
        zoom = self.zoom

        log.info(f'render graph called')            

        data_points = self.graph.get_points()

        # if not entry.has_x :
        #    data_points[0]
        log.info(f'render called, h {height}, w {width}')

        for i, data in enumerate(data_points):

            if data[1] == None:
                continue

            #if -width/1.8 / zoom + x > data[0] or data[0] > width/1.8 / zoom + x or -height/1.8 / zoom + y > data[1] or data[1] > height/1.8 / zoom + y:
            #    continue
            if -width/2 / zoom + x > data[0] or data[0] > width/2 / zoom + x or -height/1.6 / zoom + y > data[1] or data[1] > height/1.6 / zoom + y:
                continue
            if len(data_points) <= i+1 or i == 0:
                self.place_point(data, height, width, zoom)
                continue
            if data_points[i+1][1] == None:
                self.place_point(data, height, width, zoom)
                continue
            self.canvas.create_line(data[0] * zoom + width/2,
                                    -data[1] * zoom + height/2,
                                    data_points[i+1][0] * zoom + width/2,
                                    -data_points[i+1][1] * zoom + height/2,
                                    width= 3, fill = "black")
        return
    
    
    def place_point(self, data, height, width, zoom):
        self.canvas.create_oval(float(data[0]) * zoom + width/2,
                                (-float(data[1])) * zoom + height/2,
                                float(data[0]) * zoom + width/2,
                                (-float(data[1])) * zoom + height/2,
                                width = 3, fill = "black")

class Graphics(Canvas):

    def initialise(self, func_frame, button_bg, button_fg, zoom):
        self.entries = []
        self.func_frame = func_frame
        self.button_bg = button_bg
        self.button_fg = button_fg
        self.zoom = zoom
        self.max_width = 0
        self.x_offset = 0
        self.y_offset = 0

    def set_interval(self):
        width = self.winfo_width()/self.zoom
        if width > self.max_width:
            self.max_width = width
        return

    def set_x(self, x):
        self.x_offset = x
        self.reset()
        self.render_all()

    def set_y(self, y):
        self.y_offset = y
        self.reset()
        self.render_all()


    def set_zoom(self, zoom):
        for entry in self.entries:
            entry.zoom = zoom
            entry.calculate_interval(self.max_width)
        self.zoom = zoom
        self.set_interval()
        return


    def reset(self):
        height = self.winfo_height()
        width = self.winfo_width()
        zoom = self.zoom
        log.info(f'reset called, h {height}, w {width}')

        self.delete('all')


        for i in range(9): 
            self.create_line(
                (i+1) * width/10,
                0,
                (i+1) * width/10,
                height,
                fill = '#A6A6A6')
            
            self.create_text(
                             (i+1) * width/10,
                             height/2 + height*0.01,
                             text = round(((i+1) * width/10 - width/2)/zoom,2)
                             )
            self.create_line(
                             0,
                             (i+1) * height/10,
                             width,
                             (i+1) * height/10,
                             fill = '#A6A6A6'
                             )
            self.create_text(
                             width/2 - width*0.015,
                             (i+1) * height/10,
                             text = round(-((i+1) * height/10 - height/2)/zoom, 2)
                             )
        ### for-loop end ###
        self.create_line(
                         0,
                         height/2,width,
                         height/2,
                         width = 2
                         )
        self.create_line(
                         width/2,
                         0,
                         width/2,
                         height,
                         width = 2
                         )

        return


    def add_graph(self):
        log.info('add_graph called.')
        entry = graph_entry(
                            self.func_frame,
                            self,
                            self.button_bg,
                            self.button_fg,
                            self.zoom
                            )

        i = len(self.entries)
        func_entry = Entry(self.func_frame, width=200)

        entry.graph_entry.place(
                                relx = 0.02, y = 50*i,
                                height = 20,
                                relwidth = 0.96
                                )
        entry.button_visibility.place(
                                      relx = 0.02,
                                      y = 20+50*i,
                                      height = 20,
                                      relwidth = 0.85
                                      )
        entry.button_remove.place(
                                  relx = 0.9,
                                  y = 20+50*i,
                                  height = 20,
                                  width = 20
                                  )
        self.entries.append(entry)


    def render_all(self):
        log.info('render all called')
        for entry in self.entries:
            if entry.graph.function == None:
                continue
            entry.render()

