# coding=utf-8
import os, sys
from random import *

try:
    import tkinter as tk
except:
    import Tkinter as tk

import ast
import operator as op

from math import floor

# For Text-To-Speech support
#try:
#    import pyttsx
#except:
#    pass

class App:
    def __init__(self):
        # The problem object generates the problems and answers
        self.problem = Problem()
        # True = asking, False = answering
        self.asking = True
        # True = Full Screen, False = not Full Screen
        self.full_screen = False
        # The padding 
        padding = 20

        #Text to speech
        #try:
        #    self.engine = pyttsx.init()
        #except:
        #    pass
        
        # The colors
        self.colors = dict({'0':'#FFFFFF',
                            '1':'#FFAA00',
                            '2':'#FF8800',
                            '3':'#FF6600',
                            '4':'#FF4400',
                            '5':'#FF0000',
                            'teal':'#21BCFF',
                            'teal_light':'#7AD6FE',
                            'bg_color_dark':'#c70039',
                            'bg_color_light':'#FFBD16',
                            'bg_color_light_bright':'#FFD874'})

        self.text_colors = dict({'5':'#000000',
                                 '4':'#000000',
                                 '3':'#000000',
                                 '2':'#000000',
                                 '1':'#000000',
                                 '0':'#000000'})

        # The Root tkinter
        self.root = tk.Tk()
        self.root.update()
        self.root.iconbitmap(r'./calculator.ico')
        self.root.winfo_toplevel().title("Arithmetic Trainer")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # get screen width and height
        w = self.root.winfo_screenwidth() # width of the screen
        h = self.root.winfo_screenheight() # height of the screen
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (int(w/1.3), int(h/1.5), x, y))
        self.root.minsize(int(w/1.3), int(h/1.5))
        
        self.root.bind('<Escape>', lambda f: self.root.destroy())
        self.root.bind('<space>', lambda g: self.change())
        self.root.bind('<Return>', lambda g: self.change())
        self.root.bind('<Left>', lambda g: self.change())
        self.root.bind('<Right>', lambda g: self.change())
        self.root.bind('<Up>', lambda x: self.widget_click_press(self.right))
        self.root.bind('<KeyRelease-Up>', lambda x: self.widget_click(self.right, True))
        self.root.bind('<Down>', lambda x: self.widget_click_press(self.left))
        self.root.bind('<KeyRelease-Down>', lambda x: self.widget_click(self.left, False))
        self.root.bind("<F11>", self.toggle_fullscreen)

        # The Frame
        self.frame = tk.Frame(self.root, style=None, width=200, height=100, 
                              bg=self.colors['teal'])
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)

        # The Help Label
        self.left = tk.Label(self.frame, width=25, height=6, 
                             bg=self.colors['bg_color_light'], 
                             fg=self.text_colors['0'], relief=tk.GROOVE)
        self.left['text'] = ''.join(["EASIER"])
        self.left["font"]=("Verdana", 10, "bold")
        self.left.bind("<Button-1>", lambda x: self.widget_click_press(self.left))
        self.left.bind("<ButtonRelease-1>", 
                       lambda x: self.widget_click(self.left, False))
        self.left.bind("<Enter>", lambda x: self.highlight(self.left))
        self.left.bind("<Leave>", lambda x: self.lowlight(self.left))
        self.left.config(highlightbackground='black')
        self.left.grid(row=1, column=0, sticky='SNEW', padx=15, pady=15)
        
        # The Right Label
        self.right = tk.Label(self.frame, width=25, height=6, 
                              bg=self.colors['bg_color_light'], 
                              fg=self.text_colors['4'], relief=tk.GROOVE)
        self.right['text'] = ''.join(["HARDER"])
        self.right["font"]=("Verdana", 10, "bold")
        self.right.bind("<Button-1>", lambda x: self.widget_click_press(self.right))
        self.right.bind("<ButtonRelease-1>", 
                        lambda x: self.widget_click(self.right, True))
        self.right.bind("<Enter>", lambda x: self.highlight(self.right))
        self.right.bind("<Leave>", lambda x: self.lowlight(self.right))
        self.right.grid(row=1, column=2, sticky='SNEW', padx=padding, pady=padding)

        # The Problem Label
        self.label_problem = tk.Label(self.frame, text="Hi there!", relief=tk.GROOVE, bg=self.colors['0'])
        self.label_problem["font"]=("Verdana", 60, "bold")
        self.label_problem.bind("<Button-1>", lambda g: self.change())
        self.label_problem.grid(row=0,column=0, columnspan=3, sticky='NSEW', padx=padding, pady=padding)

        # The Answer Label
        self.label_answer = tk.Label(self.frame, text="", 
                                     bg=self.colors['teal_light'], 
                                     relief=tk.GROOVE)
        self.label_answer["font"]=("Times", 20, "bold")
        self.label_answer.grid(row=1,column=1, sticky='NSEW', padx=padding, pady=padding)

    def toggle_fullscreen(self, event=None):
        self.full_screen = not self.full_screen  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.full_screen)
        return "break"

    def run(self):
        self.root.mainloop()

    def change(self):
        if (self.asking == True):
            new_problem = self.problem.generateProblem()
            if len(new_problem) > 7:
                self.label_problem["font"]=("Verdana", 80, "bold")
            else:
                self.label_problem["font"]=("Verdana", 150, "bold")
            self.label_problem['text'] = new_problem.replace('-','−').replace('*','×')
            # Try to say the problem outloud
            #try:
            #    self.engine.say(new_problem.replace('−', 'minus').replace('×', 'times'))
            #    self.engine.runAndWait()
            #except:
            #    pass
            self.label_problem['bg'] = self.colors[str(self.problem.complexity)]
            self.label_answer['text'] = ""
            self.asking = not self.asking
        else:
            self.label_answer['text'] = \
            self.problem.answer(self.problem.last_problem)
            self.asking = not self.asking

    def highlight(self, widget):
        self.original_color = widget['bg']
        widget['bg'] = self.colors['bg_color_light_bright']
        
    def lowlight(self, widget):
        widget['bg'] = self.original_color

    def widget_click(self, widget, increase):
        if (increase):
            self.problem.increase_complexity()
            self.label_problem['bg'] = self.colors[str(self.problem.complexity)]
            self.label_problem['fg'] = self.text_colors[str(self.problem.complexity)]
        else:
            self.problem.decrease_complexity()
            self.label_problem['bg'] = self.colors[str(self.problem.complexity)]
            self.label_problem['fg'] = self.text_colors[str(self.problem.complexity)]
        widget['relief'] = tk.GROOVE

    def widget_click_press(self, widget):
        widget['relief'] = tk.SUNKEN

    def __del__(self):
        try:
            self.root.destroy()
        except:
            pass


class Problem:
    def __init__(self):
        self.complexity = 0
        self.maximum_complexity = 5
        self.minimum_complexity = 0
        self.last_problem = ""
        self.digits = ['1','2','3','4','5','6','7','8','9','0']
        self.operations = ['+', '*', '-', '/']#['+', '×', '−', '/']
        # supported operators
        self.operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                          ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                          ast.USub: op.neg}

    def increase_complexity(self):
        if (self.complexity < self.maximum_complexity):
            self.complexity += 1

    def decrease_complexity(self):
        if (self.complexity > self.minimum_complexity):
            self.complexity -= 1

    def generateProblem(self):
        if (self.complexity == 0): # Only sums of numbers of certain number of digits.
            problem = ''.join([self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)], 
                               self.digits[randrange(0,9)], 
                               self.digits[randrange(0,9)], ' ', self.operations[0], ' ',
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)], 
                               self.digits[randrange(0,9)], 
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)],
                               self.digits[randrange(0,9)]])
        elif (self.complexity == 1): # Multiplications of two digits
            problem = ''.join([self.digits[randrange(0,5)], ' ', self.operations[1], ' ', 
                               self.digits[randrange(0,9)]])
        elif (self.complexity == 2): # Sums, multiplications, and subtractions of two digits.
            problem = ''.join([self.digits[randrange(0,9)], ' ', 
                               self.operations[randrange(0,3)], ' ', 
                               self.digits[randrange(0,9)]])
        elif (self.complexity == 3): # Sums, multiplications, and subtractions of a two-digits number and a digit.
            problem = ''.join([self.digits[randrange(0,9)], self.digits[randrange(0,10)], 
                               ' ', self.operations[randrange(0,3)], ' ', 
                               self.digits[randrange(0,9)]])
        elif (self.complexity == 4): # Sums, multiplications, and subtractions of two two-digits numbers.
            problem = ''.join([self.digits[randrange(0,9)], self.digits[randrange(0,10)], 
                               ' ', self.operations[randrange(0,3)], ' ', 
                               self.digits[randrange(0,9)], self.digits[randrange(0,10)]])
        elif (self.complexity == 5): # Sums, multiplications, subtractions, and divisions of two two-digits numbers.
            problem = ''.join([self.digits[randrange(0,9)], self.digits[randrange(0,10)], 
                               ' ', self.operations[randrange(0,4)], 
                               ' ', self.digits[randrange(0,9)], self.digits[randrange(0,10)]])
        else:
            problem = ''.join([self.digits[randrange(0,9)], ' ', self.operations[0], ' ', 
                               self.digits[randrange(0,9)]])
        self.last_problem = problem
        return problem

    def eval_(self, node):
        try:
            if isinstance(node, ast.Num): # <number>
                return node.n
            elif isinstance(node, ast.BinOp): # <left> <operator> <right>
                return self.operators[type(node.op)](self.eval_(node.left), 
                                                     self.eval_(node.right))
            elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
                return self.operators[type(node.op)](self.eval_(node.operand))
            else:
                return "Error"
        except:
            return "Error"

    def answer(self, problem):
        try:
            return str(self.eval_(ast.parse(problem.replace('−', '-').replace('×', '*').replace(' ', ''), mode='eval').body))
        except:
            return  "Error"


if __name__ == '__main__':
    app = App()
    app.run()
