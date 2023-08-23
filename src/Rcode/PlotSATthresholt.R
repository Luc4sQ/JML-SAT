############################################################################################
#### preliminary ###########################################################################
############################################################################################

# This script prints Visualizations of the results of the run time comparisons of multiple 
# different heuristics considering different variable combinations
# This is only for deterministic

library(ggplot2)
library(cowplot)


# extract path and arguments
passedArgs <- commandArgs(trailingOnly=TRUE)

# extract path and weather to plot a graph for Heuristics or DPLL variants
K <- passedArgs[1]
VarNum <- passedArgs[2]
path <- passedArgs[3]

# construct the path for the directory to save pictures to based on the path to the .txt file
pathPict <- sub(".csv([^.txt]*)$", "_picture.png\\1", path)

#alternative: manully set path and pathPict:
#path <- ...
#pathPict <- ...

# read data
csv <- read.csv(path)


############################################################################################
#### plotting the actual graphs ############################################################
############################################################################################

SATgraph <- ggplot(csv, aes(x = Clause_Number, y = Satisfiable_Fraction)) + geom_line() +
  labs( y = "Erfüllbarkeit \n ") +
  theme(axis.title.x=element_blank(),axis.text.x=element_blank(),axis.ticks.x=element_blank())+
  ggtitle(paste(toString(VarNum)," Variablen, Klausellänge ",toString(K),sep="")) + 
  theme(text = element_text(size = 15), plot.title = element_text(hjust = 0.5,size=20))

TIMEgraph <- ggplot(csv, aes(x = Clause_Number, y = Average_Time)) + geom_line() +
  labs(x = "Anzahl der Klauseln", y = "Durchschnittliche \n Berechnungszeit in s") +
  #ggtitle("Berechnungszeit") + 
  theme(text = element_text(size = 15), plot.title = element_text(hjust = 0.5,size=20))

plot_grid(SATgraph, TIMEgraph, 
          #labels = c("A", "B"),
          ncol = 1, nrow = 2)

ggsave(filename = pathPict, width=6, height=6)
