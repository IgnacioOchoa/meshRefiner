from abaqusGui import AFXForm, getAFXApp, showAFXInformationDialog
import Remesher

class MyForm(AFXForm):
    def __init__(self, owner):
        AFXForm.__init__(self,owner)
        
    def activate(self):
        AFXForm.activate(self)
        getAFXApp().getAFXMainWindow().writeToMessageArea('GUI plugin activado')  

    def getFirstDialog(self):
        mainWindow = getAFXApp().getAFXMainWindow()
        output = Remesher.remesh()
        mainWindow.writeToMessageArea(output)  
        showAFXInformationDialog(mainWindow, output)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(buttonText='CERO|Remesher',object=MyForm(toolset))
