import os
# Defining path
mainPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
# necessary helpers
dllFileName = 'TarCo.SensorDroid'
dllFolder = mainPath + "/Python/NET/"

import sys
import clr
sys.path.append(dllFolder)
clr.AddReference(dllFileName)
from TarCo.SensorDroid import Client # pylint: disable=unused-import

import SensorDroidPlot # pylint: disable=unused-import

cliPlot = SensorDroidPlot.ClientPlot()
# connection handler
def ConnectionUpdatedEventHandler(sender, e):
    if e is not None:
        if e.Connected:
            print("Connected")
        else:
            print("Disonnected") 

# activating plotting
def SensorsReceivedEventHandler(sender, e):
    global plotSensors
    plotSensors = True
# not used here but can be used
def CameraReceivedEventHandler(sender, e):
    global showImage
    showImage = True


client = Client("Any")
# settings and updates
client.ConnectionUpdated += ConnectionUpdatedEventHandler
client.SensorsReceived += SensorsReceivedEventHandler

client.SensorsSampleRate = 100
client.CameraResolution = 15

client.Connect()

plotSensors = False
showImage = False
# if connected plot datas
while True:
    if client.Connected:
        if plotSensors and client.DataCurrent is not None:
            cliPlot.plotSensors(client.DataCurrent)
            plotSensors = False
        if showImage and client.Image is not None:
            cliPlot.showImage(client.Image.Data)
            showImage = False

input("Press ENTER to exit") 

client.Close()