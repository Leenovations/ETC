library(ggplot2)
library(ggplot2)
library(cowplot)
library(ggbiplot)
library(gridExtra)
library(patchwork)

Gene <- c('TAL1', 'BCL11A', 'GATA1', 'GATA2', 'NFE2')

for (gene in Gene){
  data <- read.table(paste0('/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.', gene, '.Methyl.txt'),
                    sep='\t',
                    header=TRUE)

  data$color <- ifelse(data$CR.NR > 0, 'tan1', 'lightskyblue')

  CR <- ggplot(data, aes(x = Start, y = CR)) +
    geom_bar(fill = 'tan1',
            color=NA,
            stat = "identity", 
            position = "identity", 
            width = 150) +
    theme_classic() +
    xlab('') + 
    ylab('') + 
    ylim(0, 101) + 
    ggtitle('TAL1\n', subtitle='CR') + 
    coord_fixed(ratio = 40) + 
    scale_y_continuous(breaks = c(0, 100), labels=c(0, 100), expand = c(0, 1)) + 
    theme(axis.line.x = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.y = element_text(size=10),
          plot.subtitle = element_text(size=10, hjust=0.5, face = c('bold')),
          plot.title = element_text(size=15, hjust=0.5, face = c('bold.italic')),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank())

  NR <- ggplot(data, aes(x = Start, y = NR)) +
    geom_bar(fill = 'lightskyblue',
            color=NA,
            stat = "identity", 
            position = "identity", 
            width = 150) +
    theme_classic() +
    xlab('') + 
    ylab('') + 
    coord_fixed(ratio = 40) + 
    ggtitle('NR') + 
    scale_y_continuous(breaks = c(0, 100), labels=c(0, 100), expand = c(0, 1)) + 
    theme(axis.line.x = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.y = element_text(size=10),
          plot.title = element_text(size=10, hjust=0.5, face = c('bold')),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank())

  CR_NR <- ggplot(data, aes(x = Start, y = CR-NR)) +
    geom_bar(fill = data$color,
            color=NA,
            stat = "identity", 
            position = "identity", 
            width = 150) + 
    theme_classic() +
    xlab('') + 
    ylab('') + 
    ggtitle('CR vs NR') + 
    coord_fixed(ratio = 100) + 
    geom_hline(yintercept = 0,
              linetype='solid',
              color='black',
              alpha=0.3,
              size=0.1) + 
    theme(panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.y = element_text(size=10),
          plot.title = element_text(size=10, hjust=0.5, face = c('bold')),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank())

  Plot <- CR + NR + CR_NR + plot_layout(ncol = 1)
  Plot
  ggsave(paste0('/media/node01-HDD01/00.AML/01.Results/240119.', gene, '.png'),
        width = 5,
        height=5,
        plot=Plot)
}