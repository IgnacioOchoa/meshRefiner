from abaqusGui import AFXForm, getAFXApp, AFXGuiCommand, AFXStringKeyword, AFXMode
from abaqusConstants import *
from remesher_dialog import MainDialog

# To log things in the message area -->   getAFXApp().getAFXMainWindow().writeToMessageArea('Modelo cambiado')

class FormRemesher(AFXForm):
    def __init__(self, owner):
        AFXForm.__init__(self,owner)
        self.mainCommand = AFXGuiCommand(mode=self, method='remesh', objectName='Remesher', registerQuery = False)
        self.kwOriginModelName = AFXStringKeyword(self.mainCommand, 'originModelName', True, defaultValue='')
        self.kwOriginPartName = AFXStringKeyword(self.mainCommand, 'originPartName', True, defaultValue='')
        self.kwDestPartName = AFXStringKeyword(self.mainCommand, 'destPartName', True, defaultValue='remeshedPart')     
        self.kwDestModelName = AFXStringKeyword(self.mainCommand, 'destModelName', True, defaultValue='')
        
    def activate(self):
        AFXForm.activate(self)

    def getFirstDialog(self):
        mainWindow = getAFXApp().getAFXMainWindow()
        self.setModal(True)
        return MainDialog(self)
        #output = Remesher.remesh()
        #mainWindow.writeToMessageArea(output)  
        #showAFXInformationDialog(mainWindow, output)

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
