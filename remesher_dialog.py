from abaqusGui import getAFXApp, AFXDataDialog, FXLabel, FXGroupBox, FXHorizontalFrame, AFXComboBox,  AFXTextField, \
FXCheckButton, showAFXInformationDialog, FXMatrix, FXButton, FXTabBook, FXTabItem, FXFrame, FXVerticalFrame,  \
AFXCOMBOBOX_VERTICAL, FRAME_SUNKEN, LAYOUT_FILL_X, MATRIX_BY_COLUMNS, LAYOUT_LEFT, LAYOUT_FILL_ROW, LAYOUT_FIX_WIDTH, \
FXMAPFUNC, SEL_COMMAND, FRAME_NONE, FRAME_NORMAL, FXRGB, getCurrentContext
from abaqusConstants import *
from abaqusGui import mdb, sendCommand
import os

# To log things in the message area -->   getAFXApp().getAFXMainWindow().writeToMessageArea('Modelo cambiado')

class MainDialog(AFXDataDialog):

    [ID_1, ID_2, ID_3, ID_4, ID_LAST] = range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST+5)

    def __init__(self, mode):
    
        WFIELDS = 200
        self.prevModelName = ''
        self.form = mode
    
        AFXDataDialog.__init__(self, mode, 'Remesher', self.DISMISS | self.OK)
        
        mode.kwModelName.setTarget(self)
        mode.kwModelName.setSelector(self.ID_1)
        mode.kwOriginPartName.setTarget(self)
        mode.kwOriginPartName.setSelector(self.ID_2)
        
        mainTabBook = FXTabBook(self, None, 0, LAYOUT_FILL_X)
        FXTabItem(mainTabBook, 'Remesher')
        tab1Frame = FXVerticalFrame(mainTabBook)
        FXTabItem(mainTabBook, 'Examples')
        tab2Frame = FXHorizontalFrame(mainTabBook)
        
        FXLabel(tab1Frame, 'Enter the source and destiny parts')
        
        gbParts = FXGroupBox(tab1Frame, text="Part names", opts=FRAME_SUNKEN | LAYOUT_FILL_X)
        
        mat = FXMatrix(gbParts, 2, opts= LAYOUT_FILL_X | MATRIX_BY_COLUMNS, w = WFIELDS)
        label1 = FXLabel(mat, 'Origin model name', opts=LAYOUT_LEFT)
        self.modelsComboBox = AFXComboBox(mat, ncols=1, nvis=1, text="", tgt=mode.kwModelName, sel=0, opts = LAYOUT_FIX_WIDTH, w = WFIELDS)
        label2 = FXLabel(mat, 'Origin part name', opts=LAYOUT_LEFT)
        self.partsComboBox =  AFXComboBox(mat, ncols=1, nvis=1, text="", tgt=mode.kwOriginPartName, sel=0, opts = LAYOUT_FIX_WIDTH, w = WFIELDS)
        
        FXFrame(mat, opts = FRAME_NONE)  #Frame placeholder for matrix
        
        chbDestModel = FXCheckButton(mat, 'Use the same model as destination')
        chbDestModel.setCheck(True)
        
        label3 = FXLabel(mat, 'Destiny part name', opts=LAYOUT_LEFT)
        AFXTextField(mat, ncols=1, labelText="", opts = LAYOUT_FIX_WIDTH, w = WFIELDS)
            
        gbParameters = FXGroupBox(tab1Frame, text="Parameters", opts=FRAME_SUNKEN | LAYOUT_FILL_X)
        FXCheckButton(gbParameters, "Maximum quality")       
        
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_1, MainDialog.onModelChangedFromGUI)   #(4)

        
    def onModelChangedFromMDB(self):
        # This function is called in response to a query in the mdb.models repository
        # We need to react to an update in the repository
        modelKeys = mdb.models.keys()
        currentModelName = self.form.kwModelName.getValue()
        if (not currentModelName in modelKeys):             # If the first time we load the plugin or if the previous model has been eliminated                                 
            currentModelName = mdb.models.keys()[0]
        self.form.kwModelName.setValue(currentModelName)                            #(1)
        self.updateCBmodels()                                                       #(2)
        self.updateParts(currentModelName)                                          #(3)
        
    def updateParts(self, currentModelName):
        modelKeys = mdb.models.keys()
        currentPart = self.form.kwOriginPartName.getValue()
        
        # Registering and unregistering queries
        if (currentModelName != self.prevModelName):     # If they are equal, nothing has changed
            if (self.prevModelName in modelKeys):        # If this is false it means that the model has been eliminated, no need to unregister query
                mdb.models[self.prevModelName].unregisterQuery(self.onPartsChangedFromMDB)
            mdb.models[currentModelName].registerQuery(self.onPartsChangedFromMDB, True)
            self.prevModelName = currentModelName
            
        #Updating parts
            if (len(mdb.models[currentModelName].parts.keys()) != 0):
                #If the same part name is present in the new model, we can keep it, if not, we select the first part
                if (not (currentPart in mdb.models[currentModelName].parts.keys())):
                    self.form.kwOriginPartName.setValue(mdb.models[currentModelName].parts.keys()[0]) #(6)
        
    def onModelChangedFromGUI(self, sender, sel, ptr):
        self.updateParts(self.form.kwModelName.getValue())                          #(5)
               
    def onPartsChangedFromMDB(self):      
        currentModel = self.form.kwModelName.getValue()
        if(not self.form.kwOriginPartName.getValue() in mdb.models[currentModel].parts.keys()): #If the current part is no longer in the model, select the first one in the list
            if (len(mdb.models[currentModel].parts) > 0): # We have to check that the part repository is not empty
                self.form.kwOriginPartName.setValue(mdb.models[currentModel].parts.keys()[0])
            else:
                self.form.kwOriginPartName.setValue('')
        self.updateCBparts()
              
    def updateCBmodels(self):
        self.modelsComboBox.clearItems()
        nroModels = len(mdb.models)
        for i in range(nroModels):
            self.modelsComboBox.appendItem(mdb.models.keys()[i])
        self.modelsComboBox.setNumVisible(nroModels)
        
    def updateCBparts(self):
        self.partsComboBox.clearItems()
        modelName = self.form.kwModelName.getValue()
        nroParts = len(mdb.models[modelName].parts)
        if (nroParts == 0):
            self.partsComboBox.disable()
            return
        else:
            self.partsComboBox.enable()
        for i in range(nroParts):
            self.partsComboBox.appendItem(mdb.models[modelName].parts.keys()[i])
        self.partsComboBox.setNumVisible(nroParts)
        
    def show(self):
        AFXDataDialog.show(self)
        currentModelName = getCurrentContext()['modelName']
        self.form.kwModelName.setValue(currentModelName)
        mdb.models.registerQuery(self.onModelChangedFromMDB, True)
        
    def showModal(self, occludedWindow):
        AFXDataDialog.showModal(self, occludedWindow)
        currentModelName = getCurrentContext()['modelName']
        self.form.kwModelName.setValue(currentModelName)
        mdb.models.registerQuery(self.onModelChangedFromMDB, True)
               
    def hide(self):
        mdb.models.unregisterQuery(self.onModelChangedFromMDB)
        mdb.models[self.form.kwModelName.getValue()].unregisterQuery(self.onPartsChangedFromMDB)
        AFXDataDialog.hide(self)

