from abaqusGui import AFXForm, getAFXApp, AFXGuiCommand, AFXStringKeyword, AFXMode, afxCreatePNGIcon
from abaqusConstants import *
from remesher_dialog import MainDialog
import os

examplesFolder = 'examples'
# To log things in the message area -->   getAFXApp().getAFXMainWindow().writeToMessageArea('Modelo cambiado')

class FormRemesher(AFXForm):
    def __init__(self, owner):
        AFXForm.__init__(self,owner)
        self.mainCommand = AFXGuiCommand(mode=self, method='remesh', objectName='Remesher', registerQuery = False)
        self.kwOriginModelName = AFXStringKeyword(self.mainCommand, 'originModelName', True, defaultValue='')
        self.kwOriginPartName = AFXStringKeyword(self.mainCommand, 'originPartName', True, defaultValue='')
        self.kwDestPartName = AFXStringKeyword(self.mainCommand, 'destPartName', True, defaultValue='remeshedPart')     
        self.kwDestModelName = AFXStringKeyword(self.mainCommand, 'destModelName', True, defaultValue='')

        self.inpFiles = []
        self.examplePartNames = []
        self.workPartNames = []
        self.examplePartDescriptions = []
        self.exampleImgs = []
        self.exampleMdbNames = []
        self.parseInpFiles()
        self.parseImages()
        self.generateNames()        
        
        if(self.exampleMdbNames):
            defaults = [self.exampleMdbNames[0]['model'], self.exampleMdbNames[0]['model'], self.exampleMdbNames[0]['origin'], \
            self.exampleMdbNames[0]['destiny'], self.inpFiles[0]]
        else:
            defaults = ['','','','','']
        self.exampleCommand = AFXGuiCommand(mode=self, method='remesh', objectName='Remesher', registerQuery = False)
        self.kwExampleOriginModelName = AFXStringKeyword(self.exampleCommand, 'originModelName', True, defaultValue=defaults[0])
        self.kwExampleDestModelName = AFXStringKeyword(self.exampleCommand, 'destModelName', True, defaultValue=defaults[1])
        self.kwExampleOriginPartName = AFXStringKeyword(self.exampleCommand, 'originPartName', True, defaultValue=defaults[2])
        self.kwExampleDestPartName = AFXStringKeyword(self.exampleCommand, 'destPartName', True, defaultValue=defaults[3])
        self.kwExampleInpFileName = AFXStringKeyword(self.exampleCommand, 'inpFileName', True, defaultValue=defaults[4])
        
    def activate(self):
        AFXForm.activate(self)

    def getFirstDialog(self):
        mainWindow = getAFXApp().getAFXMainWindow()
        self.setModal(True)
        return MainDialog(self)
        #output = Remesher.remesh()
        #mainWindow.writeToMessageArea(output)  
        #showAFXInformationDialog(mainWindow, output)
        
    def parseInpFiles(self):
        thisPath = os.path.abspath(__file__)
        thisDir = os.path.dirname(thisPath) + '\\' + examplesFolder + '\\'
        #Find the inp files
        for f in os.listdir(thisDir):
            if f.endswith('.inp'):
                self.inpFiles.append(f)              
        #From all the inp files select those that include a name and description
        for inpFileName in self.inpFiles:
            inputFile = open(thisDir + inpFileName, 'r')
            lineCounter = 0
            while(True):
                line = inputFile.readline()
                if (line.startswith('**') and 'EXAMPLE NAME' in line): #Look for Name
                    spl_line = line.split(':')
                    partName = spl_line[1].strip()
                    lineCounter+=1
                if (line.startswith('**') and 'DESCRIPTION' in line): #Look for Description
                    spl_line = line.split(':')
                    partDescription = spl_line[1].strip()
                    lineCounter+=1
                if (line.startswith('*Part') and ('name=' in line or 'name =' in line)):
                    workPart = line[line.find("=")+1:].strip()
                    self.workPartNames.append(workPart)
                    lineCounter+=1
                elif (line.startswith('*Node')):
                    break
            if (lineCounter == 3):      #Name and descritpion found, we accept the partDescription
                self.examplePartNames.append(partName)
                self.examplePartDescriptions.append(partDescription)
            inputFile.close()
            
    def parseImages(self):
        thisPath = os.path.abspath(__file__)
        thisDir = os.path.dirname(thisPath) + '\\' + examplesFolder + '\\'
        defaultImg = os.path.join(thisDir, 'defaultImg.png')
        defaultIcon = afxCreatePNGIcon(defaultImg)
        for idx in range(len(self.examplePartNames)):
            imageFound = False
            for f in os.listdir(thisDir):
                if f.endswith('.png'):
                    if f.startswith('example' + str(idx+1)):
                        thisImg = os.path.join(thisDir, f)
                        icon = afxCreatePNGIcon(thisImg)
                        self.exampleImgs.append(icon)
                        imageFound = True
            if not imageFound:
                self.exampleImgs.append(defaultIcon)
                
    def generateNames(self):
        for i in range(len(self.workPartNames)):
            dic = {}
            dic['model'] = 'Mdl' + self.workPartNames[i]
            dic['origin'] = self.workPartNames[i]
            dic['destiny'] = self.workPartNames[i] + 'rmshd'
            self.exampleMdbNames.append(dic)
        
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(  buttonText='CERO|Remesher',
                                object=FormRemesher(toolset),
                                messageId = AFXMode.ID_ACTIVATE, # This is the default value
                                icon=None,
                                kernelInitString='import Remesher',
                                applicableModules=ALL,
                                version='N/A',
                                author='N/A',
                                description='N/A',
                                helpUrl='N/A')
