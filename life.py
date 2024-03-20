import pygame
import random
import sys
import time

pygame.font.init()

class Life():
    def __init__(self):
        self.cellcolors=[(255, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.sickcolor=(128, 128, 128)
        self.spawncolor=self.cellcolors[0]
        self.screencolor=(0, 0, 0)

        self.cells=self.birth_cells(100, 100, 1000)
        self.resolution=[700, 700]

        self.screen=pygame.display.set_mode(self.resolution)
        self.alive=True

        self.cell_w=self.resolution[0]/len(self.cells[0])
        self.cell_h=self.resolution[1]/len(self.cells)

        self.paused=True
        self.delay=0.3

        self.font=pygame.font.SysFont("times new roman", 25)

    def birth_cells(self, cellnumx, cellnumy, alivecells):
        board=[]

        for y in range(cellnumy):
            row=[]
            
            for x in range(cellnumx):
                row.append(0)

            board.append(row)
        
        takenpos=[]
        everycellscolor={}
        for c in self.cellcolors:
            everycellscolor[c]=0
        everycellsnumber=int(alivecells/len(self.cellcolors))

        for a in range(alivecells):
            nowcolor=None
            for c in everycellscolor:
                if everycellscolor[c]<everycellsnumber:
                    everycellscolor[c]+=1
                    nowcolor=c
                    break    
            if nowcolor==None:
                break 

            celly=random.randint(0, len(board)-1)
            cellx=random.randint(0, len(board[0])-1)

            while [cellx, celly] in takenpos:
                celly=random.randint(0, len(board)-1)
                cellx=random.randint(0, len(board[0])-1)
            board[celly][cellx]=nowcolor
            takenpos.append([cellx, celly])
        
        return board

    def check_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.alive=False
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                self.paused=not self.paused
            elif self.paused and (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT):
                self.develop()
            elif not self.paused and event.type==pygame.MOUSEWHEEL:
                self.delay+=event.y/25
                if self.delay<0:
                    self.delay=0
                elif self.delay>2:
                    self.delay=2
        
        if self.paused:
            msbuttons=pygame.mouse.get_pressed()
            if msbuttons[0]:
                mspos=pygame.mouse.get_pos()

                if (mspos[0]>0 and mspos[0]<self.resolution[0]) and (mspos[1]>0 and mspos[1]<self.resolution[1]):
                    cellpos=[int(mspos[0]/self.cell_w), int(mspos[1]/self.cell_h)]
                    self.cells[cellpos[1]][cellpos[0]]=self.spawncolor
            elif msbuttons[2]:
                mspos=pygame.mouse.get_pos()

                if (mspos[0]>0 and mspos[0]<self.resolution[0]) and (mspos[1]>0 and mspos[1]<self.resolution[1]):
                    cellpos=[int(mspos[0]/self.cell_w), int(mspos[1]/self.cell_h)]
                    self.spawncolor=self.cells[cellpos[1]][cellpos[0]]

    def develop(self):
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                neighbors=self.get_neighbors(x, y)
                if cell!=0:
                    if cell!=self.sickcolor:
                        colneighbor, result=self.get_dominant_color(neighbors)
                        if len(neighbors)>3 or len(neighbors)<2:
                            self.cells[y][x]=0
                        elif result[self.sickcolor]>=1:
                            contamine=random.randint(0, 99)
                            if contamine:
                                self.cells[y][x]=self.sickcolor
                        elif (result!=0 and cell!=colneighbor and result[cell]+1<result[colneighbor]):
                            self.cells[y][x]=colneighbor
                    else:
                        colneighbor, result=self.get_dominant_color(neighbors)
                        badchance=random.randint(0, 99)

                        if badchance>25:
                            self.cells[y][x]=0
                        if badchance<=10:
                            newcivilisation=random.randint(0, 199)
                            newcolor=self.cellcolors[random.randint(0, len(self.cellcolors)-1)]
                            if newcivilisation==0:
                                self.cells[y][x]=newcolor
                                if y+1<len(self.cells)-1:
                                    self.cells[y+1][x]=newcolor
                                if x+1<len(self.cells[0])-1:
                                    self.cells[y][x+1]=newcolor
                                if y+1<len(self.cells)-1 and x+1<len(self.cells[0])-1:
                                    self.cells[y+1][x+1]=newcolor
                else:
                    if len(neighbors)==3:
                        sick=random.randint(0, 50000)
                        if sick==0:
                            self.cells[y][x]=self.sickcolor
                        else:
                            colneighbor, result=self.get_dominant_color(neighbors)
                            self.cells[y][x]=colneighbor
                            
    def get_neighbors(self, x, y):
        celllenx = len(self.cells[0])
        cellleny = len(self.cells)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    continue
                if 0 <= x + i < celllenx and 0 <= y + j < cellleny and self.cells[y + j][x + i] != 0:
                    neighbors.append(self.cells[y + j][x + i])
        
        return neighbors

    def get_dominant_color(self, neighbors):
        colneighbors = {}
        for col in self.cellcolors:
            colneighbors[col] = 0
        colneighbors[self.sickcolor]=0
        for neighbor in neighbors:
            colneighbors[neighbor] += 1
        
        dominant_color = self.get_key_with_max_value(colneighbors)
        #print(colneighbors, dominant_color) debugging

        return dominant_color, colneighbors

    def get_key_with_max_value(self, input_dict):
        if not input_dict:
            return None

        max_value = max(input_dict.values())
        max_keys = [key for key, value in input_dict.items() if value == max_value]
        return max_keys[random.randint(0, len(max_keys)-1)]

    def draw(self):
        self.screen.fill(self.screencolor)

        for y, row in enumerate(self.cells):
            for x, column in enumerate(row):
                if column!=0:
                    pygame.draw.rect(self.screen, column, (x*self.cell_w, y*self.cell_h, self.cell_w, self.cell_h))
        
        delaynum=self.font.render(f"DELAY BETWEEN GENERATIONS: {str(self.delay)} seconds", True, (255, 255, 255))
        self.screen.blit(delaynum, (0, 0))

    def count_colors(self):
        color_count = {}
        for color in self.cellcolors:
            color_count[color] = 0
        for row in self.cells:
            for cell in row:
                if cell in self.cellcolors:
                    color_count[cell] += 1
        print("Color counts:", color_count)

    def live(self):
        while self.alive:
            self.check_events()
            if not self.paused:
                self.develop()
            #self.count_colors() debugging
            self.draw()
            pygame.display.flip()

            if not self.paused and self.delay>0:
                time.sleep(self.delay)

        pygame.quit()
        sys.exit()


class RealLife():
    def __init__(self):
        self.cellcolors=[(255, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.sickcolor=(128, 128, 128)
        self.spawncolor=self.cellcolors[0]
        self.screencolor=(0, 0, 0)

        self.cells=self.birth_cells(100, 100, 1500)
        self.resolution=[700, 700]

        self.screen=pygame.display.set_mode(self.resolution)
        self.alive=True

        self.cell_w=self.resolution[0]/len(self.cells[0])
        self.cell_h=self.resolution[1]/len(self.cells)

        self.paused=True
        self.delay=0.3

        self.font=pygame.font.SysFont("times new roman", 25)

    def birth_cells(self, cellnumx, cellnumy, alivecells):
        board=[]

        for y in range(cellnumy):
            row=[]
            
            for x in range(cellnumx):
                row.append([0, 0])

            board.append(row)
        
        takenpos=[]
        everycellscolor={}
        for c in self.cellcolors:
            everycellscolor[c]=0
        everycellsnumber=int(alivecells/len(self.cellcolors))

        for a in range(alivecells):
            nowcolor=None
            for c in everycellscolor:
                if everycellscolor[c]<everycellsnumber:
                    everycellscolor[c]+=1
                    nowcolor=c
                    break    
            if nowcolor==None:
                break 

            celly=random.randint(0, len(board)-1)
            cellx=random.randint(0, len(board[0])-1)

            while [cellx, celly] in takenpos:
                celly=random.randint(0, len(board)-1)
                cellx=random.randint(0, len(board[0])-1)
            board[celly][cellx]=[nowcolor, 1]
            takenpos.append([cellx, celly])
        
        return board

    def check_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.alive=False
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                self.paused=not self.paused
            elif self.paused and (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT):
                self.develop()
            elif not self.paused and event.type==pygame.MOUSEWHEEL:
                self.delay+=event.y/25
                if self.delay<0:
                    self.delay=0
                elif self.delay>2:
                    self.delay=2
        
        if self.paused:
            msbuttons=pygame.mouse.get_pressed()
            if msbuttons[0]:
                mspos=pygame.mouse.get_pos()

                if (mspos[0]>0 and mspos[0]<self.resolution[0]) and (mspos[1]>0 and mspos[1]<self.resolution[1]):
                    cellpos=[int(mspos[0]/self.cell_w), int(mspos[1]/self.cell_h)]
                    self.cells[cellpos[1]][cellpos[0]][0]=self.spawncolor
                    self.cells[cellpos[1]][cellpos[0]][1]=self.spawncolor
            elif msbuttons[2]:
                mspos=pygame.mouse.get_pos()

                if (mspos[0]>0 and mspos[0]<self.resolution[0]) and (mspos[1]>0 and mspos[1]<self.resolution[1]):
                    cellpos=[int(mspos[0]/self.cell_w), int(mspos[1]/self.cell_h)]
                    self.spawncolor=self.cells[cellpos[1]][cellpos[0]][0]

    def develop(self):
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                neighbors=self.get_neighbors(x, y)
                if cell[0]!=0:
                    if cell[0]!=self.sickcolor:
                        colneighbor, result=self.get_dominant_color(neighbors)
                        if len(neighbors)>3 or len(neighbors)<2:
                            self.cells[y][x][1]=0
                        elif result[self.sickcolor]>=1:
                            contamine=random.randint(0, 99)
                            if contamine:
                                self.cells[y][x][1]=self.sickcolor
                        elif (result!=0 and cell[0]!=colneighbor and result[cell[0]]+1<result[colneighbor]):
                            self.cells[y][x][1]=colneighbor
                    else:
                        colneighbor, result=self.get_dominant_color(neighbors)
                        badchance=random.randint(0, 99)

                        if badchance>25:
                            self.cells[y][x][1]=0
                        if badchance<=10:
                            newcivilisation=random.randint(0, 199)
                            newcolor=self.cellcolors[random.randint(0, len(self.cellcolors)-1)]
                            if newcivilisation==0:
                                self.cells[y][x][1]=newcolor
                                if y+1<len(self.cells)-1:
                                    self.cells[y+1][x][1]=newcolor
                                if x+1<len(self.cells[0])-1:
                                    self.cells[y][x+1][1]=newcolor
                                if y+1<len(self.cells)-1 and x+1<len(self.cells[0])-1:
                                    self.cells[y+1][x+1][1]=newcolor
                else:
                    if len(neighbors)==3:
                        sick=random.randint(0, 500)
                        if sick==0:
                            self.cells[y][x][1]=self.sickcolor
                        else:
                            colneighbor, result=self.get_dominant_color(neighbors)
                            self.cells[y][x][1]=colneighbor
        
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell[0]==0 and cell[1]!=0:
                    cell[0]=cell[1]
                elif cell[0]!=0 and cell[1]==0:
                    cell[0]=0
                            
    def get_neighbors(self, x, y):
        celllenx = len(self.cells[0])
        cellleny = len(self.cells)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    continue
                if 0 <= x + i < celllenx and 0 <= y + j < cellleny and self.cells[y + j][x + i][0] != 0:
                    neighbors.append(self.cells[y + j][x + i][0])
        
        return neighbors

    def get_dominant_color(self, neighbors):
        colneighbors = {}
        for col in self.cellcolors:
            colneighbors[col] = 0
        colneighbors[self.sickcolor]=0
        for neighbor in neighbors:
            colneighbors[neighbor] += 1
        
        dominant_color = self.get_key_with_max_value(colneighbors)
        #print(colneighbors, dominant_color) debugging

        return dominant_color, colneighbors

    def get_key_with_max_value(self, input_dict):
        if not input_dict:
            return None

        max_value = max(input_dict.values())
        max_keys = [key for key, value in input_dict.items() if value == max_value]
        return max_keys[random.randint(0, len(max_keys)-1)]

    def draw(self):
        self.screen.fill(self.screencolor)

        for y, row in enumerate(self.cells):
            for x, column in enumerate(row):
                if column[0]!=0:
                    pygame.draw.rect(self.screen, column[0], (x*self.cell_w, y*self.cell_h, self.cell_w, self.cell_h))
        
        delaynum=self.font.render(f"DELAY BETWEEN GENERATIONS: {str(self.delay)} seconds", True, (255, 255, 255))
        self.screen.blit(delaynum, (0, 0))

    def count_colors(self):
        color_count = {}
        for color in self.cellcolors:
            color_count[color] = 0
        for row in self.cells:
            for cell in row:
                if cell[0] in self.cellcolors:
                    color_count[cell[0]] += 1
        print("Color counts:", color_count)

    def live(self):
        while self.alive:
            self.check_events()
            if not self.paused:
                self.develop()
            #self.count_colors() debugging
            self.draw()
            pygame.display.flip()

            if not self.paused and self.delay>0:
                time.sleep(self.delay)

        pygame.quit()
        sys.exit()

if __name__=='__main__':
    choice=input("Do you want the classic Conway's game of life's rules or my custom rules (more interesting)? [c/m]")
    
    while choice!="c" and choice!="m":
        print("Please input a valid option.")
        input("Do you want the classic Conway's game of life's rules or my custom rules (more interesting)? [c/m]")

    if choice=="c":
        life=RealLife()
    elif choice=="m":
        life=Life()
    life.live()