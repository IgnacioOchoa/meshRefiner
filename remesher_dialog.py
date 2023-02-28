from abaqusGui import getAFXApp, AFXDataDialog, FXLabel, FXGroupBox, FXHorizontalFrame, AFXComboBox,  AFXTextField, \
AFXCOMBOBOX_VERTICAL, AFXVerticalAligner, AFXList, FXSwitcher, FXText, FXFont, AFXTEXTFIELD_READONLY, \
FXCheckButton, showAFXInformationDialog, FXMatrix, FXButton, FXTabBook, FXTabItem, FXFrame, FXVerticalFrame, FRAME_RIDGE, \
FRAME_SUNKEN, LAYOUT_FILL_X, MATRIX_BY_COLUMNS, LAYOUT_LEFT, LAYOUT_RIGHT, LAYOUT_FILL_ROW, LAYOUT_FIX_WIDTH, HSCROLLING_OFF, \
JUSTIFY_CENTER_X, FRAME_LINE, FONTSLANT_ITALIC, TABBOOK_NORMAL, \
FXMAPFUNC, SEL_COMMAND, FRAME_NONE, FRAME_NORMAL, FXRGB, TEXT_WORDWRAP, JUSTIFY_LEFT, getCurrentContext, afxCreatePNGIcon
from abaqusConstants import *
from abaqusGui import mdb, sendCommand
import os

# To log things in the message area -->   getAFXApp().getAFXMainWindow().writeToMessageArea('Modelo cambiado')
# Default font: 'Segoe UI' size 9. To create such font use FXFont(getAFXApp(), 'Segoe UI', 9), be careful because .getSize() returns 90

class MainDialog(AFXDataDialog):

    [ID_kw1, ID_kw2, ID_kw3, ID_kw4, ID_1, ID_2, ID_3, ID_4, ID_LAST] = range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST+9)

    def __init__(self, mode):
    
        WFIELDS = 120
        self.prevModelName = ''
        self.form = mode
    
        AFXDataDialog.__init__(self, mode, 'Remesher', self.DISMISS | self.OK)
        
        mode.kwOriginModelName.setTarget(self)
        mode.kwOriginModelName.setSelector(self.ID_kw1)
        
        mainTabBook = FXTabBook(self, tgt=self, sel=self.ID_3, opts = TABBOOK_NORMAL | LAYOUT_FILL_X)
        FXTabItem(mainTabBook, 'Remesher')
        tab1Frame = FXVerticalFrame(mainTabBook)
        FXTabItem(mainTabBook, 'Examples')
        tab2Frame = FXVerticalFrame(mainTabBook)    
        FXLabel(tab1Frame, 'Enter the source and destiny parts')
        
        #Tab 1   ------------------------------------------------------------------------------------------------------------------------------------\
        gbParts = FXGroupBox(tab1Frame, text="Part names", opts=FRAME_SUNKEN | LAYOUT_FILL_X)                                                       #|
        va = AFXVerticalAligner(gbParts, opts = LAYOUT_FILL_X)                                                                                      #|
        self.modelsComboBox = AFXComboBox(va, ncols=1, nvis=1, text="Origin model name", tgt=mode.kwOriginModelName, sel=0, opts = LAYOUT_FILL_X)   #|
        self.partsComboBox =  AFXComboBox(va, ncols=1, nvis=1, text="Origin part name", tgt=mode.kwOriginPartName, sel=0, opts = LAYOUT_FILL_X)     #|        
        self.chbDestModel = FXCheckButton(va, 'Use the same model as destination', self, self.ID_1)                                                 #|
        self.chbDestModel.setCheck(True)                                                                                                            #|
        self.txtFieldDestModel = AFXTextField(va, ncols=1, labelText="Destiny model name", tgt=mode.kwDestModelName, sel=0, opts = LAYOUT_FILL_X)   #|
        self.txtFieldDestPart = AFXTextField(va, ncols=1, labelText="Destiny part name", tgt=mode.kwDestPartName, sel=0, opts = LAYOUT_FILL_X)      #|     
        gbParameters = FXGroupBox(tab1Frame, text="Parameters", opts=FRAME_SUNKEN | LAYOUT_FILL_X)                                                  #|
        FXCheckButton(gbParameters, "Maximum quality")                                                                                              #|
        #--------------------------------------------------------------------------------------------------------------------------------------------/

        #Tab 2    -------------------------------------------------------------------------------------------------------\
        
        mainVFrame = FXVerticalFrame(tab2Frame)
        tab2Title = FXLabel(mainVFrame, text = 'List of examples available', opts = FRAME_LINE | LAYOUT_FILL_X | JUSTIFY_CENTER_X)                                                         #|
        horFr = FXHorizontalFrame(mainVFrame)
        vfListLabels = FXVerticalFrame(horFr, opts=LAYOUT_FILL_X)
                                                                                                                        #|
        #Create and populate example list 
        vfList = FXVerticalFrame(vfListLabels, opts = FRAME_LINE | LAYOUT_FILL_X)
        self.exampleList = AFXList(vfList, nvis = 10, tgt = self, sel = self.ID_2, opts = HSCROLLING_OFF)         #|            
        for name in self.form.examplePartNames:                                                                         #|
            self.exampleList.appendItem(text=name)                                                                      #|
        self.exampleList.selectItem(0)                                              
        verFr = FXVerticalFrame(horFr)
                                                       #|
        #Create and populate switch                                                                                     #|
        self.switcher = FXSwitcher(verFr)                                                                               #|
        for icon in self.form.exampleImgs:                                                                              #|
            FXLabel(self.switcher, text='', ic=icon)                                                                    
            
        #self.labelDescription = FXLabel(verFr, text= 'Description: ' + self.form.examplePartDescriptions[0], w=100, h=60, opts=JUSTIFY_LEFT)
        
        self.labelDescription = FXText(verFr, opts = HSCROLLING_OFF | LAYOUT_FILL_X | TEXT_WORDWRAP)
        self.labelDescription.setText('Description: ' + self.form.examplePartDescriptions[0])
        
        botFrame = FXHorizontalFrame(mainVFrame)
        #mode.kwExampleOriginModelName.setValue('Placeholder 1')
        #mode.kwExampleOriginPartName.setValue('Placeholder 2')
        #mode.kwExampleDestPartName.setValue('Placeholder 3')
        
        vfListLabels = FXVerticalFrame(vfListLabels, opts = LAYOUT_FILL_X)
        exLabel1 = FXLabel(vfListLabels, text='Model:')
        exField1 = AFXTextField(vfListLabels, ncols=1, labelText='', tgt=mode.kwExampleOriginModelName, pt=-3, pl=10, w=WFIELDS, \
                                sel=0, opts = AFXTEXTFIELD_READONLY | FRAME_NONE | LAYOUT_FIX_WIDTH)
        exLabel2 = FXLabel(vfListLabels, text='Origin part: ')
        exField2 = AFXTextField(vfListLabels, ncols=1, labelText='', tgt=mode.kwExampleOriginPartName, pt=-3, pl=10,\
                     sel=0, opts = LAYOUT_FILL_X | AFXTEXTFIELD_READONLY | FRAME_NONE)
        exLabel3 = FXLabel(vfListLabels, text='Destiny part: ')
        exField3 = AFXTextField(vfListLabels, ncols=1, labelText='', tgt=mode.kwExampleDestPartName, pt=-3, pl=10, \
                   sel=0, opts = LAYOUT_FILL_X | AFXTEXTFIELD_READONLY | FRAME_NONE)
        
        newFont = FXFont(getAFXApp(), 'Segoe UI', 10)

        tab2Title.setFont(newFont)
        #|
        #----------------------------------------------------------------------------------------------------------------/
            
        #Connections         
        FXMAPFUNC(self, SEL_COMMAND, self.ID_kw1, MainDialog.onModelChangedFromGUI)   #(4)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_1, MainDialog.onCheckButtonToggled)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_2, MainDialog.onListChanged)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_3, MainDialog.onTabChanged)
        
    def onListChanged(self, sender, sel, ptr):
        index = self.exampleList.getSingleSelection()
        self.switcher.setCurrent(index)
        self.labelDescription.setText('Description: ' + self.form.examplePartDescriptions[index])
        self.form.kwExampleOriginModelName.setValue(self.form.exampleMdbNames[index]['model'])
        self.form.kwExampleDestModelName.setValue(self.form.exampleMdbNames[index]['model'])
        self.form.kwExampleOriginPartName.setValue(self.form.exampleMdbNames[index]['origin'])
        self.form.kwExampleDestPartName.setValue(self.form.exampleMdbNames[index]['destiny'])
        self.form.kwExampleInpFileName.setValue(self.form.inpFiles[index])
        
    def onTabChanged(self, sender, sel, ptr):
        index = sender.getCurrent()
        if (index==0):
            self.form.mainCommand.activate()
            self.form.exampleCommand.deactivate()
        elif (index==1):
            self.form.mainCommand.deactivate()
            self.form.exampleCommand.activate()
           
    def onModelChangedFromMDB(self):
        # This function is called in response to a query in the mdb.models repository
        # We need to react to an update in the repository
        modelKeys = mdb.models.keys()
        currentModelName = self.form.kwOriginModelName.getValue()
        if (not currentModelName in modelKeys):             # If the first time we load the plugin or if the previous model has been eliminated                                 
            currentModelName = mdb.models.keys()[0]
        self.form.kwOriginModelName.setValue(currentModelName)                        #(1)
        self.updateCBmodels()                                                         #(2)
        self.updateParts(currentModelName)                                            #(3)
        
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
        if(self.chbDestModel.getCheck()):
            self.form.kwDestModelName.setValue(self.form.kwOriginModelName.getValue())
        self.updateParts(self.form.kwOriginModelName.getValue())                      #(5)
               
    def onPartsChangedFromMDB(self):      
        currentModel = self.form.kwOriginModelName.getValue()
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
        modelName = self.form.kwOriginModelName.getValue()
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
        self.form.kwOriginModelName.setValue(currentModelName)
        mdb.models.registerQuery(self.onModelChangedFromMDB, True)
        
    def showModal(self, occludedWindow):
        AFXDataDialog.showModal(self, occludedWindow)
        currentModelName = getCurrentContext()['modelName']
        self.form.kwOriginModelName.setValue(currentModelName)
        mdb.models.registerQuery(self.onModelChangedFromMDB, True)
        
        #Preparing the destination model keyword
        if (self.form.kwDestModelName.getValue() == ''):
            self.form.kwDestModelName.setValue(currentModelName)
        
        #The destination model selection is initially disabled
        self.txtFieldDestModel.disable()
               
    def hide(self):
        mdb.models.unregisterQuery(self.onModelChangedFromMDB)
        mdb.models[self.form.kwOriginModelName.getValue()].unregisterQuery(self.onPartsChangedFromMDB)
        AFXDataDialog.hide(self)
        
    def onCheckButtonToggled(self, sender, sel, ptr):
        if sender.getCheck():
            self.txtFieldDestModel.disable()
            self.form.kwDestModelName.setValue(self.form.kwOriginModelName.getValue())
        else:
            self.txtFieldDestModel.enable()
        

