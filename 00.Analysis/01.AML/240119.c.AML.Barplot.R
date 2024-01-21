library(ggplot2)
library(cowplot)
library(ggbiplot)
library(gridExtra)
library(patchwork)
library(GenomicRanges)
library(ggpubr)
library(openxlsx)

# Gene <- c('TAL1')
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
    ggtitle(paste0('', '\n'), subtitle='CR') +
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
  
  Methyl <- CR + NR + CR_NR + plot_layout(ncol = 1)

  Tx <- read.table('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Exon.Intron.None.bed', sep='\t')
  colnames(Tx) <- c('Chromosome', 'Start' ,'End', 'GeneSymbol', 'Region', 'Strand')
  Table <- subset(Tx, Tx$GeneSymbol == gene)
  Table['Color'] = ifelse(Table$Region=='exon', "gray30", "gray30")
  Table['Size'] = ifelse(Table$Region=='exon', 1, 0.5)
  
  Exon_Intron <- ggplot(Table) +
    geom_segment(aes(x = Start, xend = End,
                     y = 4, yend = 4,
                     colour = Color, size= Size)) +
    scale_color_manual(values = c("gray30", 'gray30'), 
                       labels = c("exon", "intron")) + 
    scale_fill_manual(values = c("gray30", 'gray30'), 
                       labels = c("exon", "intron")) + 
    ylim(0,5) +
    xlab('') + ylab('Percent') +
    theme_bw() +
    theme(panel.background = element_blank(),
          panel.border = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.text.x = element_blank(),
          axis.title.x = element_blank(),
          axis.text.y = element_blank(),
          axis.title.y = element_blank(),
          axis.ticks.x = element_blank(),
          axis.ticks.y = element_blank(),
          legend.background = element_blank(),
          legend.position = "none",
          legend.key = element_blank(),
          legend.text = element_blank(),
          legend.title = element_blank())
  
  Plot <- Methyl + Exon_Intron +
    plot_layout(ncol = 1)
  
  Data <- read.xlsx('/labmed/11.AML/230625.AML.Total.Data.xlsx', sheet='Norm.Over.50')

  Sub_Data <- subset(Data, Data$Gene == gene)
  Sub_Data <- Sub_Data[-1]
  Trans_Data <- t(Sub_Data)
  Trans_Data <- as.data.frame(Trans_Data)
  colnames(Trans_Data) <- c('NormConunt')
  Trans_Data$Group <- rep(c('CR', 'NR'), c(8, 5))

  Barplot <- ggboxplot(Trans_Data, 
                       x = "Group", 
                       y = "NormConunt", 
                       fill = "Group", 
                       palette = c("tan1", "lightskyblue"), 
                       width = 0.3) + 
    ylab(paste0('\n', 'Normalized count')) + 
    scale_x_discrete(limits = c("NR", "CR")) +
    coord_flip() +
    theme(plot.margin = margin(2.5, 1, 2.5, 1, "cm"),
          axis.text.x = element_text(size=8),
          axis.text.y = element_text(size=8),
          axis.title.x = element_text(size=10, face='bold'),
          axis.title.y = element_blank(),
          legend.position = "none",
          legend.key = element_blank(),
          legend.text = element_blank(),
          legend.title = element_blank())

  BAR <- plot_grid(Plot, Barplot)
  
  grid_with_title <- ggdraw() +
    draw_plot(BAR) +
    draw_label(gene, size = 15, x = 0.5, y = 0.93, fontface = "bold.italic")
  
  ggsave(paste0('/labmed/11.AML/', gene, '.Exon.Bar.png'),
         height=5,
         plot=grid_with_title)
}