# Pseudocode for the remeshing algorithm

# 1 - Generate some lists
#   a - A list to put the coordinate of the element centers, we will use those centers as additional nodes
#   b - A list to put the labels of the new nodes we create to occupy those centers
#   c - A list to connect an existing node in the old part with its corresponding node in the new part. They will at the same coordinate, but they will
#       potentially have different labels. This list contains nodes of the new part, indexed by the labels of the corresponding nodes on the old part
#   d - A list of visited neighbors. In a triangular mesh, each edge has two neighboring elements. We will be visiting each element and then each of its edges.
#       This means that we will visit each edge twice, once from each element. We ony need to process each edge once, so the second time we visit it we need to 
#       do nothing. For this, we have for each element, the labels of the elements that it has interacted with (through the common edge). Those labels cannot be 
#       more than 3 for a triangular element. If we stay on an element and intend to process a certain neighbor, but the neighbor is already on the list, we skip it.


# 2 - Make list with the coordinates of each element's center

# 3 - For each triangular element <e>:
#   a - Visit each of its edges. If any of the edges has been already visited, skip it.
#   b - For each of its edges, get the elements associated with it. If there is only one element, it means that edge is an exterior border. If there are two elements, then
#       element <e> is an internal element with no exterior border.
#   c - If the edge is an internal edge, generate two elements. Each of these elements has the following 3 nodes: the two centers of the neighboring elements's centers,
#       and one of the already existing 2 nodes belonging to the edge being processed.
#   d - If the edge is a border edge, applz one of the closing algorithms:
#       i) Keep the original seed: Create only one element, joining the center of the element with the two nodes of the edge at the border.
#       ii)Split the original seed: Project the center of the element onto the border edge and create two elements. Each element connects the center of the original element,
#          the projected node, and one of the original nodes belonging to the the processed edges.
            
from abaqusConstants import *
from math import sqrt

modelName = 'meshModel'
partName = 'meshPart'
destPartName = 'destPart'
maxElLabel = 0
maxNodLabel = 0
#Coordinates of the centers of the elements, where we will put the new nodes
elementCenters = []
#Labels of the nodes at the element centers, indexed by the corresponding element labels
nodesIDsAtCenters = []
#Labels of the nodes in the new part corresponding to the nodes in the old part, indexed by old nodes labels
nodesCorrelations = []
#Neighbors already interacted with
processedNeigh = []

def initialChecks():
    if (not mdb.models.has_key(modelName)):
        mdb.Model(modelName)
        
    if (not mdb.models[modelName].parts.has_key(partName)):
        #----------------Create part---------------------
        #mdb.models[modelName].Part(name=partName, dimensionality=TWO_D_PLANAR , type=DEFORMABLE_BODY)
        #----------------Import part---------------------
        mdb.models[modelName].PartFromInputFile(inputFileName='C:/Users/ochoai/Documents/Scripts/' + partName + '.inp')
        mdb.models['meshModel'].parts.changeKey(fromName=partName.upper(), toName=partName)
        #print 'Cannot find the part ', partName
        #exit()
    
    if (len(mdb.models[modelName].parts[partName].nodes) == 0):
        return 'There is no mesh'

def maxLabels():
    global maxElLabel
    global maxNodLabel
    for el in workPart.elements:
        if (el.label > maxElLabel):
            maxElLabel = el.label
            
    for nod in workPart.nodes:
        if (nod.label > maxNodLabel):
            maxNodLabel = nod.label

def initializeContainers():
    global elementCenters
    global nodesIDsAtCenters
    global nodesCorrelations
    global processedNeigh
    elementCenters = [(0.0,0.0,0.0) for i in range(maxElLabel+1)]
    nodesIDsAtCenters = [-1 for i in range(maxElLabel+1)]
    nodesCorrelations = [-1 for i in range(maxNodLabel+1)]
    processedNeigh = [[] for i in range(maxElLabel+1)]

def calculateCenters():
    #------- Calculate element centers
    for el in workPart.elements:
        sumX = 0
        sumY = 0
        sumZ = 0
        for nod in el.getNodes():
            sumX += nod.coordinates[0]
            sumY += nod.coordinates[1]
            sumZ += nod.coordinates[2]
        elementCenters[el.label] = (sumX/3,sumY/3,sumZ/3)

def refineMesh():
#------- Main processing loop
    for el in workPart.elements:
        #------ get edges -------
        edges = el.getElemEdges()
        for ed in edges:
            adjEl = ed.getElements()   
            if len(adjEl) == 2:
            #Inner element
                #Which of the elements is the current one?
                if(adjEl[0]==el):
                    otherEl = adjEl[1]
                elif(adjEl[1]==el):
                    otherEl = adjEl[0]
                else:
                    return 'Original element not found within the ElementEdge adjacent element'
            
                #Has been the edge already processed?
                if(otherEl.label in processedNeigh[el.label]):
                    continue
                else:
                    processedNeigh[el.label].append(otherEl.label)
                    processedNeigh[otherEl.label].append(el.label)
                                                  
                #Select three nodes, one from the neighbor center, the second from the current element center, and the third an exiting node
                #First node
                #Has been already processed?
                if (nodesIDsAtCenters[otherEl.label] != -1):
                    n1 = destPart.nodes.getFromLabel(nodesIDsAtCenters[otherEl.label])
                else:
                    n1 = destPart.Node(coordinates=elementCenters[otherEl.label])
                    nodesIDsAtCenters[otherEl.label] = n1.label
                
                #Second Node
                #Has been already processed?
                if (nodesIDsAtCenters[el.label] != -1):
                    n2 = destPart.nodes.getFromLabel(nodesIDsAtCenters[el.label])
                else:
                    n2 = destPart.Node(coordinates=elementCenters[el.label])
                    nodesIDsAtCenters[el.label] = n2.label
                    
                #Third Node
                n3orig = ed.getNodes()[0]
                n4orig = ed.getNodes()[1]
                #Has been already processed?
                if (nodesCorrelations[n3orig.label] != -1):
                    n3 = destPart.nodes.getFromLabel(nodesCorrelations[n3orig.label])
                else:
                    n3 = destPart.Node(coordinates = n3orig.coordinates)
                    nodesCorrelations[n3orig.label] = n3.label
                    
                #Fourth Node
                #Has been already processed?    
                if (nodesCorrelations[n4orig.label] != -1):
                    n4 = destPart.nodes.getFromLabel(nodesCorrelations[n4orig.label])
                else:
                    n4 = destPart.Node(coordinates = n4orig.coordinates)
                    nodesCorrelations[n4orig.label] = n4.label
                
                destPart.Element(nodes=(n1,n2,n3), elemShape=TRI3)
                destPart.Element(nodes=(n1,n2,n4), elemShape=TRI3)
                
            elif (len(adjEl) == 1):
                #Border element
                #First node
                #Has been already processed?
                uniqueEl = adjEl[0]
                if (nodesIDsAtCenters[uniqueEl.label] != -1):
                    n1 = destPart.nodes.getFromLabel(nodesIDsAtCenters[uniqueEl.label])
                else:
                    n1 = destPart.Node(coordinates=elementCenters[uniqueEl.label])
                    nodesIDsAtCenters[uniqueEl.label] = n1.label
                    
                #Second node -> projection onto the edges
                n3orig = ed.getNodes()[0]
                n4orig = ed.getNodes()[1]
                
                n1c = n1.coordinates
                n3c = n3orig.coordinates
                n4c = n4orig.coordinates
                v1 = (n1c[0]-n3c[0], n1c[1]-n3c[1], n1c[2]-n3c[2])
                v2 = (n4c[0]-n3c[0], n4c[1]-n3c[1], n4c[2]-n3c[2])
                
                v2mag = sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
                
                dotProd = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
                v2unit = [vi/v2mag for vi in v2]
                
                n2coords = [dotProd/v2mag * v2unit[i] + n3c[i] for i in range(3)]
                n2 = destPart.Node(coordinates=n2coords)
                
                #Third Node
                #Has been already processed?
                if (nodesCorrelations[n3orig.label] != -1):
                    n3 = destPart.nodes.getFromLabel(nodesCorrelations[n3orig.label])
                else:
                    n3 = destPart.Node(coordinates = n3orig.coordinates)
                    nodesCorrelations[n3orig.label] = n3.label
                
                #Fourth Node
                #Has been already processed?    
                if (nodesCorrelations[n4orig.label] != -1):
                    n4 = destPart.nodes.getFromLabel(nodesCorrelations[n4orig.label])
                else:
                    n4 = destPart.Node(coordinates = n4orig.coordinates)
                    nodesCorrelations[n4orig.label] = n4.label
                
                destPart.Element(nodes=(n1,n2,n3), elemShape=TRI3)
                destPart.Element(nodes=(n1,n2,n4), elemShape=TRI3)
            else:
                return 'Edge element connects more than two elements, cannot process'
    return 'Malla cargada correctamente'

initialChecks()
workPart = mdb.models[modelName].parts[partName]
destPart = mdb.models[modelName].Part(name = destPartName, dimensionality=TWO_D_PLANAR , type=DEFORMABLE_BODY)
maxLabels()
initializeContainers()
calculateCenters()
output = refineMesh()
print output