############################################################################################
#### preliminary ###########################################################################
############################################################################################

# This script prints Visualizations of the results of the run time comparisons of multiple 
# different heuristics considering different variable combinations
# This is only for deterministic

library(ggplot2)

passedArgs <- commandArgs(trailingOnly=TRUE)

# extract path and weather to plot a graph for Heuristics or DPLL variants
HEURorDPLL <- passedArgs[1]
path <- passedArgs[2]

#path <- "/Users/melanietaprogge/Desktop/SAT-Solving/generatedCNFs/ProgrammierTests/Compare1/heuristicComparison.csv"
#HEURorDPLL <- "HEUR"

csv <- read.csv(path)

# construct the path for the directory to save pictures to based on the path to the .txt file
pathPict <- sub(".csv([^.txt]*)$", "_pictures/\\1", path)

#alternative: manully set path and pathPict:
#path <- ...
#pathPict <- ...

#create a directory
dir.create(pathPict)

############################################################################################
#### prepare data and plot graphs ##########################################################
############################################################################################

# change some datatypes to factor, otherwise they will be seen as continuous values which causes issues with plots
csv$Vars <- as.factor(csv$Vars)
csv$ClauseCount <- as.factor(csv$ClauseCount)
csv$ClauseLen <- as.factor(csv$ClauseLen)

# create a df containing all the possible different combos for SAT and Variable count since we want to plot graphs for each
combos <- expand.grid(unique(csv$Satisfiability),unique(csv$Vars))#[1,]

for(i in 1:nrow(combos)){
  
  # extract the variables we want
  SatisfiabilityConsidered <- combos[i,]$Var1
  VarsConsidered <- combos[i,]$Var2
  
  if(HEURorDPLL=="HEUR"){
    # print plot for heuristics if script was called for heuristics
    
    # create a sub-data-frame and plot it
    data<- subset(csv,Satisfiability==SatisfiabilityConsidered & Vars==VarsConsidered & ClauseLenDet=="DET")
    
    if(nrow(data)!=0){
      
      # test if the max and min avarage tines are further apart than 1, if so, use log scale
      if(max(data$AverageS)/min(data$AverageS)>50){
        ggplot(data, aes(x = Heuristic, y = AverageS, shape = ClauseLen)) + geom_point(aes(color = ClauseCount),size=3) +
          labs(x = "Such-Heuristik", y = "Durchschnittliche Berechnungszeit \n in log2(s)", color = "Anzahl an \n Klauseln", shape = "Länge der \n Klauseln") +
          scale_y_continuous(trans = 'log2') +
          ggtitle(paste(toString(VarsConsidered)," Variablen, ",SatisfiabilityConsidered,sep="")) + theme(text = element_text(size = 15), plot.title = element_text(hjust = 0.5,size=20))
      }else{
        ggplot(data, aes(x = Heuristic, y = AverageS, shape = ClauseLen)) + geom_point(aes(color = ClauseCount),size=3) +
          labs(x = "Such-Heuristik", y = "Durchschnittliche Berechnungszeit in s", color = "Anzahl an \n Klauseln", shape = "Länge der \n Klauseln") +
          ggtitle(paste(toString(VarsConsidered)," Variablen, ",SatisfiabilityConsidered,sep="")) + theme(text = element_text(size = 15), plot.title = element_text(hjust = 0.5,size=20))
      }
      
      # create a name for the picture
      picNmae <- paste("HeuristicComparison_",VarsConsidered,"Var",SatisfiabilityConsidered,".png",sep="")
      picPath <- paste(pathPict,picNmae)
      # safe the picture
      ggsave(filename = picPath, width=6, height=4)
    }
  }else if(HEURorDPLL=="DPLL"){
    # print plot for DPLL variants if script was called for heuristics
    
    # create a sub-data-frame and plot it
    data<- subset(csv,Satisfiability==SatisfiabilityConsidered & Vars==VarsConsidered & ClauseLenDet=="DET")
    if(nrow(data)!=0){
      
      # test if the max and min avarage tines are further apart than 1, if so, use log scale
      if(max(data$AverageS)/min(data$AverageS)>10){
        ggplot(data, aes(x = DPLLVariant, y = AverageS, shape = ClauseLen)) + geom_point(aes(color = ClauseCount),size=3) +
          labs(x = "DPLL Variante", y = "Durchschnittliche Berechnungszeit \n in log2(s)", color = "Anzahl an \n Klauseln", shape = "Länge der \n Klauseln") +
          scale_y_continuous(trans = 'log2') +
          ggtitle(paste(toString(VarsConsidered)," Variablen, ",SatisfiabilityConsidered,sep="")) + theme(text = element_text(size = 15), plot.title = element_text(hjust = 0.5,size=20))
      }else{
        ggplot(data, aes(x = DPLLVariant, y = AverageS, shape = ClauseLen)) + geom_point(aes(color = ClauseCount),size=3) +
          labs(x = "DPLL Variante", y = "Durchschnittliche Berechnungszeit in s", color = "Anzahl an \n Klauseln", shape = "Länge der \n Klauseln") +
          ggtitle(paste(toString(VarsConsidered)," Variablen, ",SatisfiabilityConsidered,sep="")) + theme(text = element_text(size = 15), plot.title = element_text(hjust = 0.5,size=20))
      }
      
      # create a name for the picture
      picNmae <- paste("dpllComparison_",VarsConsidered,"Var",SatisfiabilityConsidered,".png",sep="")
      picPath <- paste(pathPict,picNmae)
      # safe the picture
      ggsave(filename = picPath, width=6, height=4)
    }
  }
}
