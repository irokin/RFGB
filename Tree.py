from Utils import Utils
from Logic import Logic
class node(object):
    '''this is a node in a tree'''
    expandQueue = [] #Breadth first search node expansion strategy
    depth = 0 #initial depth is 0 because no node present
    maxDepth = 1 #max depth set to 1 because we want to at least learn a tree of depth 1
    learnedDecisionTree = [] #this will hold all the clauses learned
    data = None #stores all the facts, positive and negative examples

    @staticmethod
    def setMaxDepth(depth):
        '''method to set max depth'''
        node.maxDepth = depth

    def __init__(self,test=None,examples=None,information=None,level=None,parent=None,pos=None):
        '''constructor for node class
           contains test condition or clause
           contains examples
           contains information notion (some score)
           contains level in the tree of node
           contains parent node pointer
           and contains position in the tree
        '''
        self.test = test #set test condition, which will be a horn clause
        if level > 0: #check if root
            self.parent = parent #if not root set parent as the nodes parent
        else:
            self.parent = "root" #if root, set parent to "root" to signify root
        self.pos = pos #position of the node, i.e. "left" or "right"
        self.examples = examples #all examples that are available for testing at this node
        self.information = information #information contained at this node
        self.level = level #level of the node, 0 for root
        self.left = None #left subtree
        self.right = None #right subtree
        node.expandQueue.insert(0,self) #add to the queue of nodes to expand

    @staticmethod
    def initTree(trainingData):
        '''method to create the root node'''
        node.data = trainingData
        node.expandQueue = [] #reset node queue for every tree to be learned
        node.learnedDecisionTree = [] #reset clauses for every tree to be learned
        examples = trainingData.pos.keys()+trainingData.neg.keys() #collect all examples
        node(None,examples,Utils.variance(examples),0,"root") #create root node

    @staticmethod
    def learnTree(data):
        '''method to learn the decision tree'''
        node.initTree(data) #create the root
        while len(node.expandQueue) > 0:
            curr = node.expandQueue.pop()
            curr.expandOnBestTest(data)

    def expandOnBestTest(self,data=None):
        '''expands the node based on the best test'''
        target = data.getTarget() #get the target
        clause = target+":-" #initialize clause learned at this node with empty body
        curr = self #while loop to obtain clause learned at this node
        while curr.parent!="root":
            if curr.pos == "left":
                clause += curr.parent.test
            elif curr.pos == "right":
                clause += "!"+curr.parent.test
            curr = curr.parent
        if self.level == node.maxDepth:
            node.learnedDecisionTree.append(clause)
            return
        minWeightedVariance = 0 #initialize minimum weighted variance to be 0
        bestTest = "" #initalize best test to empty string
        bestTExamples = [] #list for best test examples that satisfy clause
        bestFExamples = [] #list for best test examples that don't satisfy clause
        literals = data.getLiterals() #get all the literals that the data (facts) contains
        for literal in literals: #for every literal generate test conditions
            literalName = literal
            literalTypeSpecification = literals[literal]
            tests = Logic.generateTests(literalName,literalTypeSpecification,target)