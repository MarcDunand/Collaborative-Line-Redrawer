import vsketch
import numpy as np
import shapely as shp
import random as rand
import json
import copy
from scipy.signal import savgol_filter



def checkDiff(t, leng, yArr):
        res = True
        for i in range(leng):
            if((abs(yArr[t-i] - yArr[t-i-1]) < 0.01)):
                res = False
        return res

def checkFlat(t, leng, yArr):
        res = True
        for i in range(leng):
            if t+i+1 >= len(yArr):
                return False
            if((abs(yArr[t+i] - yArr[t+i+1]) > 0.003)):
                res = False
        return res 




class Hw4Sketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def drawtest(self, vsk: vsketch.Vsketch, t, d, x, y):
        vsk.circle(150, 150, 100)


    def drawTower(self, vsk: vsketch.Vsketch, lineArr, t, d, x, y):
        l = t - rand.randrange(3, 10)
        r = t + rand.randrange(3, 10)

        lx = lineArr[l][0]
        rx = lineArr[r][0]
        h = lineArr[r][1] - rand.uniform(0.1, 0.75)
        w = rx-lx

        vsk.line(lx, lineArr[l][1], lx, h)
        vsk.line(rx, lineArr[r][1], rx, h)

        wt = w * rand.uniform(1.2, 2.2)
        d = t + wt + 5
        if rand.random() < 0.3:
            ht = wt*rand.uniform(0.3, 0.5)
            vsk.rect((lx+rx)/2 - wt/2, h-ht, wt, ht)
        else:
            ht = min((lineArr[r][1] - h)/1.5, w*rand.uniform(0.7, 2))
            vsk.triangle((lx+rx)/2 - wt/2, h, (lx+rx)/2 + wt/2, h, (lx+rx)/2, h - ht)
        return d
    


    def drawVillage(self, vsk: vsketch.Vsketch, lineArr, yArr, t, d, x, y):
        i = 0
        while abs(yArr[t+i] - yArr[t+i+1]) < 0.004:
            w = rand.randint(10, 30)
            if t + i + w >= len(lineArr):
                break
            wp = lineArr[i+w][0] - lineArr[i][0]
            h = lineArr[t+i][1] - rand.uniform(0.04, 0.2)

            lx = lineArr[t+i][0]
            rx = lineArr[t+i+w][0]

            vsk.line(lx, lineArr[t+i][1], lx, h)
            vsk.line(rx, lineArr[t+i+w][1], rx, h)

            i+=rand.randint(5, 20)

            wt = wp * rand.uniform(1, 1.4)
        
            ht = wt*rand.uniform(0.4, 0.7)
            vsk.triangle((lx+rx)/2 - wt/2, h, (lx+rx)/2 + wt/2, h, (lx+rx)/2, h - ht)
        
        d = t+i+1
        return d
    

    def drawStriation(self, vsk: vsketch.Vsketch, lineArr, yArr, t, d, x, y, minStria, maxStria):
        isStria = True
        for i in range(minStria):
            if t+i >= len(yArr):
                isStria = False
                break

            if y < yArr[t+i]:
                isStria = False
        
        rX = 0
        if(isStria):
            for i in range(minStria, maxStria):
                if t+i >= len(yArr):
                    break

                if y < yArr[t+i]:
                    rX = t + i
                    break
        
        if(rX != 0):
            vsk.line(x, y, lineArr[rX][0], lineArr[rX][1])


    
    def drawLake(self, vsk: vsketch.Vsketch, lineArr, yArr, t, d, x, y, minLake, maxLake, waveL):
    
        isLake = True
        for i in range(minLake):
            if t+i >= len(yArr):
                isLake = False
                break

            if y > yArr[t+i]:
                isLake = False
        
        rX = 0
        if(isLake):
            for i in range(minLake, maxLake):
                if t+i >= len(yArr):
                    break

                if y > yArr[t+i]:
                    rX = t + i
                    break

        d = rX

        if(rX != 0):
            self.drawBoats(vsk, lineArr, x, y, waveL, rX)

        return d
    



    def drawBoats(self, vsk: vsketch.Vsketch, lineArr, x, y, waveL, rX):
            lakeW = lineArr[rX][0] - x
            waveNum = int(lakeW/waveL)
            leftOver = lakeW%waveL
            waveD = waveL + leftOver/waveNum
            vsk.line(x, y, x+waveD, y)
            vsk.line(lineArr[rX][0], lineArr[rX][1], lineArr[rX][0] - waveD, lineArr[rX][1])
            boatloc = int(rand.randrange(0, int((waveNum-2)*2)))
            for i in range(waveNum-2):
                vsk.arc(x+waveD*i+waveD*1.5, lineArr[rX][1]*(i/waveNum) + y*((waveNum-i)/waveNum), waveD, waveD, np.pi, np.pi*2)
                if i == boatloc:  #generate boats
                    boatScale = 0.04 + waveNum/500
                    boatX = x+waveD*i+waveD*1.5
                    boatY = lineArr[rX][1]*(i/waveNum) + y*((waveNum-i)/waveNum) - boatScale/4
                    sailDir = rand.random() < 0.5
                    
                    vsk.arc(boatX, boatY, boatScale*2, boatScale, np.pi, 0, mode="center") 
                    vsk.line(boatX-boatScale, boatY, boatX+boatScale, boatY)
                    if sailDir:
                        vsk.triangle(boatX-boatScale/3, boatY, boatX-boatScale/3, boatY-(2*boatScale), boatX+(2/3)*boatScale, boatY)
                    else:
                        vsk.triangle(boatX+boatScale/3, boatY, boatX+boatScale/3, boatY-(2*boatScale), boatX-(2/3)*boatScale, boatY)

    


    def drawTree(self, vsk: vsketch.Vsketch, x, y, maxh):
        h = rand.uniform(0.05, maxh)  #height of trunk
        vsk.line(x, y, x, y - h)  #draw trunk
        r = rand.uniform(h/7, h/1.5)  #radius of crown
        vsk.circle(x, y - h, r)  #draw crown
        if r > maxh/2.5 and rand.random() < 0.5:  #if crown is big add branches
            vsk.line(x, (y-h)+rand.uniform(r/2.2, r/8), x-r/6,  y-h+rand.uniform(-r/8, r/8))
            vsk.line(x, (y-h)+rand.uniform(r/2.2, r/8), x+r/6,  y-h+rand.uniform(-r/8, r/8))
            vsk.line(x, y-h, x, y-h-r/8)
        elif r > maxh/2.5:
            vsk.arc(x, y-h, r/2, r/2, np.pi, 0, mode="center")
            vsk.line(x, y-h, x, y-h-r/8)


    
    def drawBird(self, vsk: vsketch.Vsketch, birdx, birdy, birdScale): #TODO convert bird then bird flocks
        vsk.arc(birdx, birdy, birdScale, 0.7*birdScale, 0.5, np.pi-0.5, mode="center")
        vsk.arc(birdx + np.cos(0.5)*birdScale, birdy, birdScale, 0.7*birdScale, 0.5, np.pi-0.5, mode="center")



    def draw(self, vsk: vsketch.Vsketch) -> None:
        print("________________________________\n")
        vsk.size("letter", landscape=True)
        vsk.scale("in")
        vsk.noFill()

        lineArr = []
        yArr = []
        

        #generate a dummy line
        # amp = 3
        # for i in np.arange(0, 10.99, 0.01):
        #     vsk.line(i, vsk.noise(i/amp)*8.5, i+0.01, vsk.noise((i+0.01)/amp)*8.5)
        #     lineArr.append((i, vsk.noise(i/amp)*8.5))
        #     yArr.append(vsk.noise(i/amp)*8.5)


        #gets line data from a json file
        file_path = './lineFinder/data.json'

        with open(file_path, 'r') as file:
            my_array = json.load(file)

        yArr = savgol_filter(np.array(my_array), window_length=30, polyorder=2)
        yArr= yArr.tolist()
        lineArr = copy.copy(yArr)

        for i in range(len(lineArr)):
            lineArr[i] = (i/200, lineArr[i])

        for i in range(len(lineArr)-1):
            vsk.line(lineArr[i][0], lineArr[i][1], lineArr[i+1][0], lineArr[i+1][1])


        #begin doodles
        t = 0
        d = 0
        madestairs = 10
        for (x, y) in lineArr:
            

            #generates towers 
            localW = 40
            if t > d and rand.random() > 0.5 and all(y <= coord[1] for coord in lineArr[t-localW:t+localW]) and t > localW and t < len(lineArr)-localW:
                d = self.drawTower(vsk, lineArr, t, d, x, y)
            
            
            #generate village
            minW = 50
            if rand.random() < 0.01 and t > d and checkFlat(t, minW, yArr):
                d = self.drawVillage(vsk, lineArr, yArr, t, d, x, y)


            #generate altitude striations
            if rand.random() < 0.05:
                self.drawStriation(vsk, lineArr, yArr, t, d, x, y, 15, 200)
            

            #generate lakes
            if t > d and rand.random() < 0.01:
                d = self.drawLake(vsk, lineArr, yArr, t, d, x, y, 50, 300, 0.05)


            #generates trees
            if t > d and (rand.random() < 0.01):
                self.drawTree(vsk, x, y, 0.6)

                
            #generate forests
            if t > d and (rand.random() < 0.1) and vsk.noise(t) < 0.3:
                self.drawTree(vsk, x, y, 0.6)



            #generate birds
            birdScale = 0.05
            if rand.random() < 0.003 and y > 2+birdScale:
                self.drawBird(vsk, x, rand.uniform(birdScale, y-2), 0.05)



            #generate flocks    
            if rand.random() < 0.0003 and y > 2+3*birdScale:
                stepSize = 0.2
                birdx = x
                birdy = rand.uniform(birdScale, y-2)
                for i in range(rand.randrange(5, 30)):
                    birdx += rand.uniform(-1*stepSize, stepSize)
                    birdy += rand.uniform(-1*stepSize, stepSize)
                    self.drawBird(vsk, birdx, birdy, birdScale)


            t+=1
                        
                
        


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Hw4Sketch.display()
