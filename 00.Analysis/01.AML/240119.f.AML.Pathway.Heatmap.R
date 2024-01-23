library(ggplot2)
library(readxl)
library(pheatmap)
library(RColorBrewer)
#--------------------------------------------------------------------------------#
setwd('/labmed/11.AML/')
#--------------------------------------------------------------------------------#
Name <- read_excel('/labmed/11.AML/240123.AML.Total.Info.xlsx', sheet = 'Sample_Call')
#--------------------------------------------------------------------------------#
Pathway <- list.files('/labmed/11.AML/03.GeneSet/', 'tsv')
Pathway <- strsplit(Pathway, '.v')
Pathway <- sapply(Pathway, function(x) x[1])
#--------------------------------------------------------------------------------#
for (pathway in Pathway){
  Sample <- data.frame(sample=Name$WGBS[Name$WGBS != "NA"])
  GO <- list.files('/labmed/11.AML/', pathway)
  for (go in GO){
    Header <- strsplit(go, '\\.')
    Header <- sapply(Header, function(x) x[2])
    Data <- read.table(go, 
                       sep='\t', 
                       header = T,
                       col.names=Header)
    Sample <- cbind(Sample, Data)
  }
  rownames(Sample) <- as.character(Sample[, 1])
  Sample <- Sample[,-1]
  CR <- Sample[1:12,]
  NR <- as.data.frame(t(colMeans(Sample[13:24,])))

  Diff <- data.frame(
    CpGIShelf = CR$CpGIShelf - NR$CpGIShelf,
    CpGIShore = CR$CpGIShore - NR$CpGIShore,
    CpGIsland = CR$CpGIsland - NR$CpGIsland,
    Enhancer = CR$Enhancer - NR$Enhancer,
    Exon = CR$Exon - NR$Exon,
    Intron = CR$Intron - NR$Intron,
    Promoter = CR$Promoter - NR$Promoter)

  rownames(Diff) <- paste0(rownames(Sample)[1:12], ' vs NR')
  Heatmap <- pheatmap(Diff,
                      color =  colorRampPalette(rev(RColorBrewer::brewer.pal(n = 10, name ="RdYlGn")))(100),
                      legend_breaks = c(-2,2),
                      border_color = NA,
                      row_names_side = "left",
                      legend_labels = c("Low", "High"),
                      clustering_method = 'average',
                      show_rownames = T,
                      show_colnames = T,
                      treeheight_row = 0,
                      clustering_distance_rows = "correlation",
                      cluster_rows = T,
                      cluster_cols = T,
                      display_numbers = TRUE,
                      fontsize_number = 10,
                      scale = "row",
                      main = paste0(pathway, '\n'))
  # 
  png(paste0('/labmed/11.AML/00.Plot/', pathway, ".heatmap.png"), width = 2000, height = 2000, units = "px",res = 300)
  print(Heatmap)
  dev.off()
}
#--------------------------------------------------------------------------------#