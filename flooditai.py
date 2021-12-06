from fltk import *
import random
import time

class Game(Fl_Double_Window):
    def __init__(self, w, h, l):
        Fl_Double_Window.__init__(self, w,h,l)
        self.begin()
        self.color = [248,88,63,95,216]
        self.colorname = ['Magenta','Red','Green','Yellow','Blue']
        self.colorbuttons=[]
        for color in range(len(self.color)):
            self.colorbuttons.append(Fl_Button(60,90*color,60,60,self.colorname[color]))
            self.colorbuttons[-1].color(self.color[color])
            self.colorbuttons[-1].callback(self.colorcb)
        self.startai = Fl_Button(150,90,60,60,"AI")
        self.startai.callback(self.AIcb)
        self.pointbox = Fl_Box(145,30,120,40)
        self.pointbox.box(FL_FLAT_BOX)
        self.resetbutton=Fl_Button(150,180,60,60,"Reset")
        self.resetbutton.callback(self.reset)
        self.reset()
        
    def reset(self,wid='first'):
        self.clickthis = 0
        self.gameover=False
        self.clicks = 0
        self.pointbox.label(f"Clicks: {self.clicks}/25")
        self.pointbox.redraw()
        if wid == 'first':
            self.box=[]
            for y in range(14):
                l = []
                for x in range(14):
                    l.append(Fl_Box((x*30)+300,y*30,30,30))
                    l[-1].color(random.choice(self.color))
                    l[-1].box(FL_FLAT_BOX)
                    l[-1].redraw()
                self.box.append(l)
        else:
            for i in self.box:
                for j in i:
                    j.color(random.choice(self.color))
                    j.redraw()

    def checkwin(self):
        endcolor=self.box[0][0].color()
        #(endcolor)
        for i in self.box:
            for j in i:
                if j.color()!=endcolor:   
                    self.gameover = False            
                    return False
        self.gameover = True
        return True


    def AIcb(self,wid='hi'):
        self.checked=[]
        self.howmany = [0,0,0,0,0]
        self.fakecheckcol(0,0)
        # print(self.howmany)

        #print(self.colorname[self.howmany.index(max(self.howmany))]) #move to play
        self.clickthis = self.color[self.howmany.index(max(self.howmany))] 
        self.colorcb(self.color[self.howmany.index(max(self.howmany))])
        self.clickthis = 0
        for i in self.box:
            for j in i:
                j.redraw()
        time.sleep(0.1)#speed of AI
        Fl.check()
        if not self.gameover:
            self.AIcb()

    def colorcb(self,wid):
        if self.clickthis == 0:
            self.clicked = wid.color()
        else:
            self.clicked = self.clickthis
        self.origin = self.findcol(0,0)
        self.redrawthese = []
        self.checked = []
        self.checkcol(0,0)
        for i in self.redrawthese:
            self.box[i[1]][i[0]].color(self.clicked)
            self.box[i[1]][i[0]].redraw()
        self.box[0][0].color(self.clicked)
        self.box[0][0].redraw()
        self.clicks+=1
        if self.checkwin() and self.clicks<=25:
            self.pointbox.label(f"You Win!")
            self.pointbox.redraw()
        elif self.clicks>=25:
            self.pointbox.label(f"You Lose!")
            self.pointbox.redraw()
        else:
            self.pointbox.label(f"Clicks: {self.clicks}/25")
            self.pointbox.redraw()

    def findcol(self,x,y):
        return self.box[y][x].color()
    def checkcol(self,x,y):
        check = ((1,0),(0,1),(-1,0),(0,-1))
        for i in check:
            fx,fy=x+i[0],y+i[1]
            if fx>=0 and fx<=13 and fy>=0 and fy<=13:
                if [fx,fy] not in self.checked:
                    self.checked.append([fx,fy])
                    #print(self.checked)
                    if self.findcol(fx,fy)==self.origin:
                        self.checkcol(fx,fy)
                        self.redrawthese.append([fx,fy])
    def fakecheckcol(self,x,y):
        self.origin = self.box[0][0].color()
        # check = ((1,0),(0,1),(-1,0),(0,-1))
        check = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
        # check = ((1,0),(1,1),(0,1),(-1,0),(0,-1))
        for i in check:
            fx,fy=x+i[0],y+i[1]
            if fx>=0 and fx<=13 and fy>=0 and fy<=13:
                if [fx,fy] not in self.checked:
                    self.checked.append([fx,fy])
                    # print(self.checked)
                    if self.findcol(fx,fy)!=self.origin:
                        self.howmany[self.color.index(self.findcol(fx,fy))]+=1
                        # print(fx,fy)
                    if self.findcol(fx,fy)==self.origin:
                        self.fakecheckcol(fx,fy)

app = Game(720,420,r"Flood it but with an AI that beats the game 90% of the time")
app.show()
Fl.run()

 