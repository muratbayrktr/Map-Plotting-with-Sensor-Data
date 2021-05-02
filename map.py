from sensordroid import Client
import matplotlib.pyplot as plt
import numpy as np
import time
import numpy as np
import pandas as pd
import shapefile as shp
import seaborn as sns
import os
# gettin the current path
cdir=os.path.dirname(os.path.abspath(__file__))

# discovers devices and connects to the first one it finds
def devicesDiscoveredEventHandler(devices):
    print(devices)
    if len(devices) > 0:
        client = Client(devices[0])
        # trigger connection handler
        client.connectionUpdated = connectionUpdatedEventHandler
        # trigger sensor data handler
        client.sensorsReceived = sensorsReceivedEventHandler
        #client.imageReceived = cameraReceivedEventHandler

        # sample rate and resolution settings
        client.sensorsSampleRate = 100
        client.cameraResolution = 13
        
        client.connect()
        
# connection handler
def connectionUpdatedEventHandler(sender, msg):
    if sender is not None:
        if sender.connected:
            print("Connected")
        else:
            print("Disonnected") 

# variable for checking the existence of dot
# we need this because with the sample rate of 100
# if we plot even when the location don't change it will cause
# program to run slowly
# also location is set to zero naturally
dot = False
last_location = [0,0]
def sensorsReceivedEventHandler(sender, dataCurrent):
    # defining global variables
    global fig, last_location,dot
    # converting all the data to the list of floats from the string form
    loc = [float(i) for i in dataCurrent.Location.Values.AsString.split(",\t")]
    #printing location 
    print(loc, last_location)
    # initializing plotting
    # this is required due to the speed difference of plotting and getting the data
    # causes some problems such as dot being not plotted at the beggining
    if not dot:
        # comma is necessary because it returns tuple
        point, = plt.plot(loc[1],loc[0], marker = "o", markersize = 10, color = "red")
        dot = True
        # letting figure draw the dot
        fig.canvas.draw()
        fig.canvas.flush_events()
        
    # checking if location changes and if so
    # assigning dot to be false and letting the function plot the data next round
    if last_location[0] != loc[0] or last_location[1] != loc[1]:
        dot = False
        point.remove()
    # updating last location
    last_location[0] = loc[0]
    last_location[1] = loc[1] 

# defining figure
sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))
# reading shapefile
# YOU CAN CHANGE THE PATH AS THE WAY YOU ARRANGE YOUR PROJECT
shp_path = cdir+ "\\isciblok\\map\\landcover-polygon.shp"
sf = shp.Reader(shp_path)

# PLOTTING SHAPEFILE

x_lim, y_lim = None, None
# required for interactivity
plt.ion()
# figsize
fig = plt.figure(figsize = (11,9))
ax = fig.add_subplot(111)
id = 0
x,y = 0,0
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]

    plt.plot(x,y,"k")

    if (x_lim == None) & (y_lim == None):
        x0 = np.mean(x)
        y0 = np.mean(y)
        plt.text(x0,y0,id, fontsize = 10)
    id = id + 1

    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)    

# starting device discovery and initializing other functions
Client.devicesDiscovered = devicesDiscoveredEventHandler
Client.startDiscovery()

#from SensorDroidNet import *

# exit key
key = input("Press ENTER to exit\n") 

Client.closeAll()