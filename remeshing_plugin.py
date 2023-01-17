from abaqusGui import AFXForm, getAFXApp, AFXDialog, AFXDataDialog, FXLabel, FXGroupBox, FXHorizontalFrame, AFXComboBox,  AFXTextField, \
FXCheckButton, showAFXInformationDialog, FXMatrix, \
AFXCOMBOBOX_VERTICAL, FRAME_SUNKEN, LAYOUT_FILL_X, MATRIX_BY_COLUMNS, LAYOUT_LEFT, LAYOUT_FILL_ROW, LAYOUT_FIX_WIDTH, \
FXMAPFUNC, SEL_COMMAND
from abaqusConstants import *
from abaqusGui import mdb
import Remesher

class MainDialog(AFXDataDialog):

    [ID_1, ID_2, ID_LAST] = range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST+3)

    def __init__(self, mode):
    
        WFIELDS = 200
    
        AFXDataDialog.__init__(self, mode, 'Remesher', self.DISMISS | self.YES)
        FXLabel(self, 'Enter the source and destiny parts')
        gbParts = FXGroupBox(self, text="Part names", opts=FRAME_SUNKEN | LAYOUT_FILL_X)
        
        mat = FXMatrix(gbParts, 2, opts= LAYOUT_FILL_X | MATRIX_BY_COLUMNS, w = WFIELDS)
        label1 = FXLabel(mat, 'Origin model name', opts=LAYOUT_LEFT)
        self.modelsComboBox = AFXComboBox(mat, ncols=1, nvis=1, text="", tgt=self, sel=self.ID_1, opts = LAYOUT_FIX_WIDTH, w = WFIELDS)
        label2 = FXLabel(mat, 'Origin part name', opts=LAYOUT_LEFT)
        self.partsComboBox = AFXComboBox(mat, ncols=1, nvis=1, text="", opts = LAYOUT_FIX_WIDTH, w = WFIELDS)
        label3 = FXLabel(mat, 'Destiny part name', opts=LAYOUT_LEFT)
        AFXTextField(mat, ncols=1, labelText="", opts = LAYOUT_FIX_WIDTH, w = WFIELDS)
        
        self.updateCBmodels()
        self.updateCBparts()
        
        gbParameters = FXGroupBox(self, text="Parameters", opts=FRAME_SUNKEN | LAYOUT_FILL_X)
        FXCheckButton(gbParameters, "Maximum quality")
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_1, MainDialog.modelCBchange)
        
    def modelCBchange(self, sender, sel, ptr):
        #getAFXApp().getAFXMainWindow().writeToMessageArea('Modelo cambiado')
        self.updateCBparts()
        
    def updateCBmodels(self):
        #getAFXApp().getAFXMainWindow().writeToMessageArea('updateCBmodels se ejecuta')
        self.modelsComboBox.clearItems()
        nroModels = len(mdb.models)
        for i in range(nroModels):
            self.modelsComboBox.appendItem(mdb.models.keys()[i])
        self.modelsComboBox.setNumVisible(nroModels)
        
    def updateCBparts(self):
        #getAFXApp().getAFXMainWindow().writeToMessageArea('updateCBparts se ejecuta')
        self.partsComboBox.clearItems()  
        modelName = mdb.models.keys()[self.modelsComboBox.getCurrentItem()]
        nroParts = len(mdb.models[modelName].parts)
        if (nroParts == 0):
            self.partsComboBox.disable()
            return
        else:
            self.partsComboBox.enable()
        for i in range(nroParts):
            self.partsComboBox.appendItem(mdb.models[modelName].parts.keys()[i])
        self.partsComboBox.setNumVisible(nroParts)
           

class MyForm(AFXForm):
    def __init__(self, owner):
        AFXForm.__init__(self,owner)
        
    def activate(self):
        AFXForm.activate(self)
        getAFXApp().getAFXMainWindow().writeToMessageArea('GUI plugin activado')  

    def getFirstDialog(self):
        getAFXApp().getAFXMainWindow().writeToMessageArea('getFirstDialogActivado')
        mainWindow = getAFXApp().getAFXMainWindow()
        return MainDialog(self)
        #output = Remesher.remesh()
        #mainWindow.writeToMessageArea(output)  
        #showAFXInformationDialog(mainWindow, output)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(buttonText='CERO|Remesher',object=MyForm(toolset))
