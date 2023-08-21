############################################################################################
#### preliminary ###########################################################################
############################################################################################

## This skript takes a txt file containing some meta information and sequential positional information about
## where in the tree (meaning at which literal assignment) the program was after a given amount of steps of 
## running the program.
## From this sequential information we wirst create a dictionary where each key leads to a list with up to two values,
## keys represent variables at which we branch and the vales in the list represent the possible variable assignments 
## we might choose.
## This dictionary is then used to create an extended newick formula, which is a commonly used format for trees.
## This can then in turn be used to plot the trees with ggtree.

passedArgs <- commandArgs(trailingOnly=TRUE)

# extract path and weather or not to plot numbers on trees from the argument passed
path <- passedArgs

## Loading the libraries:
library(ggtree)
library(treeio)
library(ggplot2)
library(stringr)
library(readr)
library(Dict)

# construct the path for the directory to save pictures to based on the path to the .txt file
pathPict <- sub(".txt([^.txt]*)$", "_pictures/\\1", path)

#alternative: manully set path and pathPict:
#path <- ...
#pathPict <- ...

dir.create(pathPict)


############################################################################################
#### reading the information from the the .txt file ########################################
############################################################################################

# reading the file
tree_dat <- read.delim(path, header = FALSE, sep = "\n", dec = ".")

# extracting the total number of variables
num_var_total <- strtoi(sub(".*= ", "", tree_dat[1,]))

# print a warning and turn off the labeling of branches if trees are big
if (num_var_total > 7){
  print("Warning: for more than 7 variables the trees can become too big to still have distinguishable branches")
  printNumbers <- FALSE
}else{
  printNumbers <- TRUE
  }

# number of lines that contain information about trees represents the 
steps <- (nrow(tree_dat)-4)

# create list of sequential, (partial) variable assignments
assignmentSequence <- c()
for (i in (1:steps+1)){
  currentlyConsideredLits <- gsub(", ","/",sub(".*= ", "", tree_dat[i+3,]))
  assignmentSequence <- append(assignmentSequence,currentlyConsideredLits)
}

# fill up assignment sequence:
# this will become necessary for unit resolution and pure literal elimination because in these cases
# we basically choose mutibple variables at each step so we do not have each single step in the
# assignment sequence but that is inofmarion we need in order to correctly construct the dictionary.
# Therefore we first add all the intermediate steps in the sequence if they are not already present
# and then we porceed.

# for this we first define a function. It will also be used when plotting the actual tree in order to
# get and color the current path!

# we use the positional information in the variables to reconstruct every variable assignement representing a step of the path
generatePath <- function(fullPathVar){
  literalList <- as.list(strsplit(fullPathVar, "/")[[1]])
  partialPath <- ""
  pathList <- c()
  for(literal in literalList){
    if(nchar(partialPath)==0){
      partialPath <- paste(literal)
    }else{
      partialPath <- paste(partialPath,"/",literal,sep="")
    }
    pathList <- append(pathList,partialPath)
  }
  return(pathList)
}

# now we "fill up" the assignment sequence with our intermediate assignments
fullAssignmentSequence <- c()
for(partialAssignemnt in assignmentSequence){
  candidateAssignments <- generatePath(partialAssignemnt)
  for(candidate in candidateAssignments){
    if(!(candidate %in% fullAssignmentSequence)){
      fullAssignmentSequence <- append(fullAssignmentSequence,candidate)
    }
  }
}


############################################################################################
#### creating a dictionary with the information for the tree ###############################
############################################################################################

## We want to create a dictionary that uses the sequences of considered literals to build a complete tree
## in order to do so, we create entries of the format L_1,L_2, ... , L_n-1 = c(L_n, -L_n) where L are literals.
## this is iterativeley done so we have one entry for every branching (in the case of the example above for 
## the branching at position L_n-1).

# Set the branch length to desired value
# Since this seems to be relative and we just want all branches to be of the same length,
# this does not really seem to matter either way.
branch_length <- 0.4

createDict <- function(fullAssignmentSequence){
  newickDict <- dict("start"=c("spacer"))
  for (assignment in fullAssignmentSequence){
    
    # For each of the lines get a list containing the literals with separator "/" that will be used to name nodes
    # of the tree.
    litList <- as.list(strsplit(sub(".*= ", "", assignment), "/")[[1]])
    
    ### generate a dictionary
    
    # get the last literal that represents the one that is currently being considered
    # we convert to numeric and back to string to get rid of weird listing format
    lastLit <- toString(as.numeric(litList[length(litList)]))
    
    # generate the new key to be added from the currently considered literals without the last literal
    newKey <- toString(as.numeric(litList[1:length(litList)-1]))
    
    # if we have already considered this key, representing that we have already looked at this literal combination,
    # just with a different last literal, we do not want to overwrite the entry but only add to it
    if(length(litList)>1){
      if(newKey %in% newickDict$keys){
        newickDict[newKey] <- append(newickDict[newKey],lastLit)
      }else{
        newickDict[newKey] <- c(lastLit)
      }
    }
  }
  
  # add the start variables to entry "start"
  # in order to do so, we get the first entry of an arbitrary key and its negation 
  # (this will be the same for any key since they all begin with the first variable we branched at)
  # first we need to choose a key that is not "start"
  keyNotStart <- newickDict$keys[newickDict$keys!="start"][1]
  keyAsIntList <- as.numeric(as.list(strsplit(sub(".*= ", "", keyNotStart), ",")[[1]]))
  firstVars <- c(toString(keyAsIntList[1]),toString(-keyAsIntList[1]))
  newickDict["start"] <- firstVars
  
  return(newickDict)
}

newickDict <- createDict(fullAssignmentSequence)

############################################################################################
#### creating a newick from the dictionary #################################################
############################################################################################

## Here, all the information that we encounter at any step is used to generate a newick with extra information that 
## already contains all the nodes we will ever get to during the process of trying variables.
## This is important since the whole thing gets really messy when we generate new newicks for every variable assignment
## because then some automatism of ggtree make trees flip randomly or do stuff like that.
## We assign labels to the edges that just tell us what the last considered literal is. These are not unique since the
## same literal might be considered at different positions of the code but they can be used to label the edges in the
## pictures

### necessary definitions

varList <- c()
for(key in newickDict$keys){
  if(key != "start"){
    newEntry <- gsub(", ","/",paste(key,", ",newickDict[key],sep=""))
    varList <- append(varList,newEntry)
  }
}

# we set a mark if the second branch was never used and hence we need to add fillers at the very top level
# this will otherwise not be automatically detected because we will delete the "start" entry again before 
# constructing the tree and thus not detect a branching there.

if (toString(-strtoi(newickDict$keys[1])) %in% newickDict$keys){
  addAtUpperLevel <- FALSE
}else{
  addAtUpperLevel <- toString(-strtoi(newickDict$keys[1]))
}


### creating the newick

createNewick <- function(newickDict,topKey){
  
  # We do not want to add the "start" to the dictionary entries or have it in the tree,
  # therefore we treat this key slightly differently
  if(topKey=="start"){
    nextTopKey <- newickDict[topKey]
    newPreamble <- ""
    
  }else{
    # we create a new key by combining the key we are using with the two literals assigned to it in the dictionary 
    # representing the literals we branch at
    nextTopKey <- paste(topKey,", ",newickDict[topKey],sep="")

    # get the literal the key ends with to correctly add it to newick
    keyAsIntList <- as.numeric(as.list(strsplit(sub(".*= ", "", topKey), ",")[[1]]))
    keyLastLit <- keyAsIntList[length(keyAsIntList)]
    
    # create the newick entry for the forking, this is the last literal the tow new branches have in common
    newPreamble <- paste(gsub(", ","/",topKey),"[&&NHX:lastLit=",keyLastLit,"]:",branch_length, sep = "")
  }
  
  # if it has the length 2, then we have a fork here and need to consider both branches individually
  if(length(nextTopKey)==2){
    
    # first we test, weather the new key is in the keys of the dictionary
    # if it is, that means ther is a subtree that we need to create and add at this position, this is done by calling
    # the function createNewick here and then iterativeley building the tree
    if(nextTopKey[1] %in% newickDict$keys){
      leftEntry <- createNewick(newickDict,nextTopKey[1])
      varList <- append(varList,createNewick(newickDict,nextTopKey[1]))
      # if this is not the case we have reached a point in the tree were we showed that the current assignment is either 
      # SAT or UNSAT so we do not need to iterativeley create more treee structures but can instead just add the current assignment as a branch
    }else{
      # get the last literal of the key
      keyAsIntList <- as.numeric(as.list(strsplit(sub(".*= ", "", nextTopKey[1]), ",")[[1]]))
      lastLeftLit <- keyAsIntList[length(keyAsIntList)] 
      # and create the newick entry for the branch with it
      leftEntry <- paste(gsub(", ","/",nextTopKey[1]),"[&&NHX:lastLit=",lastLeftLit,"]:",branch_length, sep = "")
    }
    
    # do the exact same thing for the other branch of the fork
    if(nextTopKey[2] %in% newickDict$keys){
      rightEntry <- createNewick(newickDict,nextTopKey[2])
      varList <- append(varList,createNewick(newickDict,nextTopKey[2]))
    }else{
      keyAsIntList <- as.numeric(as.list(strsplit(sub(".*= ", "", nextTopKey[2]), ",")[[1]]))
      lastRightLit <- keyAsIntList[length(keyAsIntList)] 
      rightEntry <- paste(gsub(", ","/",nextTopKey[2]),"[&&NHX:lastLit=",lastRightLit,"]:",branch_length, sep = "")
    }
    
    # use the two to build a new entry
    newCompleteEntry <- paste("(",leftEntry,",",rightEntry,")",newPreamble,sep="")
    
  }else{
    
    # analogously to the generation of the left and right sides
    if(nextTopKey %in% newickDict$keys){
      singleEntry <- createNewick(newickDict,nextTopKey)
      varList <- append(varList,createNewick(newickDict,nextTopKey))

    }else{
      keyAsIntList <- as.numeric(as.list(strsplit(sub(".*= ", "", nextTopKey), ",")[[1]]))
      lastSingleLit <- keyAsIntList[length(keyAsIntList)] 
      singleEntry <- paste(gsub(", ","/",nextTopKey),"[&&NHX:lastLit=",lastSingleLit,"]:",branch_length, sep = "")
    }
    
    newCompleteEntry <- paste("(",singleEntry,")",newPreamble,sep="")
    
  }
  return(newCompleteEntry)
}

completeNewick <- paste(createNewick(newickDict,"start"),";",sep="")


############################################################################################
#### fill up tree ##########################################################################
############################################################################################

## Here we fill up the tree with spacers becuse we want to see the complete search space in our visualization.
## Otherwise, we would only see the parts of the tree that we actually reached during the search.


#### necessary functions

# gets the depth of a given entr of the tree compared to the desired depth of the tree
getDepth <- function(newick, goalSize ,pos){
  # number of opening brackets "(" before variable
  brackOpen <- sum(unlist(gregexpr("(", newick,fixed=TRUE))>pos)
  # number of closing brackets ")" before variable
  brackClose <- sum(unlist(gregexpr(")", newick,fixed=TRUE))>pos)
  goalSize - (brackClose - brackOpen) +1
}

# test weather a given entry is a leaf of the tree
isLeaf <- function(newick,pos){
  # variable is a leaf if there is no closing bracket before is for some reaason str_sub starts counting with 
  # index 0 while unlist starts with 1, therefore there is a shift and we do not need to look at pos-1 but pos.
  if (str_sub(newick,pos,pos)==")"){FALSE}
  else{TRUE}
}

# generate subtrees we can use as spacers for the parts of the search space we never encounter
generateEmptyTree <- function(debth){
  for (i in 1:debth)
    if (i==1){treepart <- ""}
  else{
    treepart <- paste("(",treepart,",",treepart,")",sep="")
  }
  treepart
}


#### fill up tree itself

fillUpTree <- function(newick, newickVars, totalDepth, dict,addAtUpperLevel){
  
  # first we find out which variables do not have a fork and for these we add empty subtrees of appropriate depth.
  for(key in dict$keys){
    if(length(dict[key])==1){
      # create the new variable with "/" notation
      newVar <- paste(gsub(", ","/",key),"/",toString(-as.numeric(dict[key])),sep="")
      # the variable previous in the path, here the fork is located
      newFork <- gsub(", ","/",key)
      # we crete a regular expression we can use to locate the fork in the tree
      regExprCurrent <- paste("\\(",newFork,"\\[|\\)",newFork,"\\[|,",newFork,"\\[",sep="")
      positionCurrent <- unlist(gregexpr(regExprCurrent, newick))[1]
      # then we use that to insert the other variable in the tree
      str_sub(newick,positionCurrent,positionCurrent-1) <- paste(",",newVar,"[&&NHX]:",branch_length,sep="")
      # and add the newly added variable to the list of variables
      newickVars <- append(newickVars,newVar)
    }
  }
  
  # now we consider the case where we have to add filler at the very top layer
  if(addAtUpperLevel != FALSE){
    regExpr0 <- paste("\\(",addAtUpperLevel,"\\[|\\)",addAtUpperLevel,"\\[|,",addAtUpperLevel,"\\[",sep="")
    position0 <- unlist(gregexpr(regExpr0, newick))[1]
    if (position0<0){print("Error: Regular Expression could not be matched")}
    depthToFill <- getDepth(newick,totalDepth,position0)
    treeFiller <- generateEmptyTree(depthToFill)
    if(depthToFill > 1){
      # paste the tree-filler at the appropriate position
      str_sub(newick,position0+1,position0) <- treeFiller
    }
  }
  
  # for each of the variables in the list we first find out the depth in the tree and then use that information
  # in order to fill up the tree with generated subtrees
  
  for(var in newickVars){
    # once again, we locate the variable in the tree using regular expressions
    regExpr <- paste("\\(",var,"\\[|\\)",var,"\\[|,",var,"\\[",sep="")
    position <- unlist(gregexpr(regExpr, newick))[1]
    if (position<0){print("Error: Regular Expression could not be matched")}
    depthToFill <- getDepth(newick,totalDepth,position)
    
    # if our variable is a leaf in the current tree but the depth of its path from the origin is not as deep as the
    # max depth, we have to fill it up!
    if ((isLeaf(newick,position)) && (depthToFill>0)){
      treeFiller <- generateEmptyTree(depthToFill)
      
      if(depthToFill > 1){
        # paste the tree-filler at the appropriate position
        str_sub(newick,position+1,position) <- treeFiller
      }
    }
  }
  newick
}

filledUpNewick <- fillUpTree(completeNewick,varList,num_var_total, newickDict,addAtUpperLevel)

############################################################################################
#### iteratively print trees ###############################################################
############################################################################################

### necessary functions 

# function to get the numers of the nodes given their names
# it is only possible to map colors to edges using these inner nodes
getInnerNodeNumbers <- function(fullTree,targetNodes){
  node_num <- c(fullTree@phylo$tip.label, fullTree@phylo$node.label)
  color_nodes_numbers <- c()
  for (assignment in targetNodes){
    color_nodes_numbers <- append(color_nodes_numbers,which(node_num==assignment))
  }
  color_nodes_numbers
}


### plotting the trees

plotTrees <- function(sequence,newick){
  
  # a counter we introduce to name the pictures we generate
  picCount <- 1
  
  # we first read in the full tree that already has all the information about where all the nodes well ever visit need to go
  fullTree <- read.nhx(textConnection(newick))
  
  # we create a list to which we will append all the previously considered paths to color the part of the tree that
  # we already have searched black
  searchedPath <- c()
  
  # then we use that tree and only use the positional information of the currently considered variables we got from python
  # in order to color the branches and label the edges
  for(assignment in sequence){
    # default color is gray
    colors <- data.frame(node=1:Nnode2(fullTree), colour = 'gray')
    
    # then we want to color all the paths we already considered but found to be unsat with black
    nodesToColorBlack <- getInnerNodeNumbers(fullTree,searchedPath)
    colors[nodesToColorBlack, 2] <- "black"
    
    # we want to color all the branches orange that lead to the currently considered assignment so we look at the name 
    # that basically contains the path and take it apart and create a list with all the partial 
    # assignments (that represent the path) from it
    pathList <- generatePath(assignment)
    nodesToColorOrange <- getInnerNodeNumbers(fullTree,pathList)
    colors[nodesToColorOrange, 2] <- "orange"
    
    # we need to create a vector containing all colored nodes to lable them
    nodesToLabel <- append(nodesToColorOrange,nodesToColorBlack)
    
    # let the plotting begin!
    if (printNumbers == TRUE){
      ggtree(fullTree) %<+% colors + aes(colour=I(colour)) + geom_label2(aes(subset=(node %in% nodesToLabel),x=branch, label=lastLit))
    }else{
      ggtree(fullTree) %<+% colors + aes(colour=I(colour))
    }
    
    # save the picture
    pathPict_i <- paste(pathPict,str(1),"plot",picCount,".png",sep="")
    picCount <- picCount +1
    ggsave(filename = pathPict_i, width=4, height=4)
    
    # we add the path to our searchedPath list to color black next time
    searchedPath <- append(searchedPath,pathList)
  }
}

plotTrees(assignmentSequence,filledUpNewick)