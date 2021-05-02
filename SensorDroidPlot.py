from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import time

class ClientPlot:

    plotCount = 0
    plotColors = ["blue", "red", "green", "black"]

    plotLast = [[0 for x in range(5)] for y in range(10)] 

    imageContent = None
    # plots
    #camera is disabled
    #figIm = plt.figure("Camera")
    figSens1 = plt.figure("Sensors1")
    figSens2 = plt.figure("Sensors2")
    #axImage = figIm.add_subplot(1, 1, 1)
    axSensorsAcc = figSens1.add_subplot(2, 2, 1)
    axSensorsOri = figSens1.add_subplot(2, 2, 2)
    axSensorsProx = figSens1.add_subplot(2, 2, 3)
    axSensorsMag = figSens1.add_subplot(2, 2, 4)
    axSensorsLight = figSens2.add_subplot(3, 2, 1)
    axSensorsPress = figSens2.add_subplot(3, 2, 2)
    axSensorsStep = figSens2.add_subplot(3, 2, 3)
    axSensorsTemp = figSens2.add_subplot(3, 2, 4)
    axSensorsHum = figSens2.add_subplot(3, 2, 5)
    axSensorsLoc = figSens2.add_subplot(3, 2, 6)

    chartsMins = [-30, -360, -20, -50, 0, 0, 0, 0, 0, -100, -200, 0, 0] 
    chartsMaxs = [30, 360, 20, 50, 100, 2000, 3000, 100, 100, 100, 200, 0, 0]
    # sensor list
    axSensors = [axSensorsAcc, axSensorsOri, axSensorsProx, axSensorsMag, axSensorsLight, axSensorsPress, axSensorsStep, axSensorsTemp, axSensorsHum, axSensorsLoc]

    def __init__(self):
        # interactivity
        plt.ion()
        plt.show(block=False)

    # function for plotting sensors
    def plotSensors(self, data):
            # error handlling
            try:
                # giving datas to the plots
                for i in range(0, 10):
                    self.axSensors[i].axis([self.plotCount-50, self.plotCount, self.chartsMins[i], self.chartsMaxs[i]])
                    # pulling values from the data argument
                    values = data.DataByIndex[i].Values.AsDouble;
                    if values is not None:
                        for j in range(len(values)):
                            # for every value of plottable plot them to their corresponding subplots
                            value = values[j]
                            line = plt.Line2D([self.plotCount-1, self.plotCount], [self.plotLast[i][j], value])
                            line.set_color(self.plotColors[j])
                            self.axSensors[i].add_line(line) 
                            self.plotLast[i][j] = value 

                            if self.plotCount > 50:
                                del self.axSensors[i].lines[0]              

                self.plotCount += 1
                # having the plot pause for 10 ms
                plt.pause(0.01) 
            except Exception as e:
                print(e)
                pass     

            
    # this is for camera but it is not used.
    def showImage(self, image):
        if image is not None:
            try:
                data = (bytearray)(image)
                dataBytes = BytesIO(data)
                img = Image.open(dataBytes)

                if self.imageContent is None:
                    #plt.subplot(1, 1, 1)
                    self.imageContent = self.axImage.imshow(img)             
                    plt.pause(0.01)
                else:
                    plt.pause(0.01)
                    self.imageContent.set_data(img)

            except Exception as e:
                print(e)
                pass