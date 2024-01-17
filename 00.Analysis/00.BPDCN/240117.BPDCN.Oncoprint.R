library(ComplexHeatmap)
library(readxl)
library(dplyr)

Annotation <- read.table('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/230825.BPDCN.Involve.Site.txt', 
                         sep = '\t',
                         header=T,
                         row.names = 1)

ha = HeatmapAnnotation("Involvement site" = Annotation$Involvement,
                       Age = Annotation$Age,
                       Sex = Annotation$Sex,
                       Induction=Annotation$Induction,
                       Cytogenetics=Annotation$Cytogenetics,
                       "L-asparaginase"=Annotation$Contating,
                       Transplantation=Annotation$Transplantation,
                       Survival=Annotation$Survival,
                       col = list("Involvement site" = c("Multiple skin ± systemic" = "springgreen4",
                                                         "Systemic without skin" = "springgreen3",
                                                         "Single skin" = "springgreen1"),
                                  Age = c('>=60 years'='gold', '<60 years'='lightgoldenrod1'),
                                  Cytogenetics = c('Abnormal'='#993300', 'Normal'='#CC6633', 'Not available'='gray80'),
                                  Sex = c('Male'='steelblue1', 'Female'='skyblue1'),
                                  Induction = c('AML-like chemotherapy'='slateblue4', 'ALL-like chemotherapy'='slateblue3', 'Lymphoma-like chemotherapy'='mediumpurple1'),
                                  "L-asparaginase" = c('Yes'='royalblue4', 'No'='gray80'),
                                  Transplantation = c('Allo-SCT'='indianred3', 'Salvage auto-SCT'='lightpink', 'Salvage Allo-SCT'='hotpink1','None'='gray80'),
                                  Survival = c('<24 months'='violetred1', '>=24 months'='plum2')),
                       annotation_height = unit(c(5, 5, 100), "mm"),
                       annotation_name_gp= gpar(fontsize = 8))

Onco.Data <- read_excel('~/Desktop/BPDCN.Oncotable.xlsx')
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]
Onco.Data <- Onco.Data[1:50,]

#color지정
col.Onco = c("Missense" = "#008000", "Truncating" = "red", "Duplication" = "blue", "Deletion" = "orange")

alter_fun = list(
  background = alter_graphic("rect", fill = "#CCCCCC"),
  Missense = alter_graphic("rect", fill = col.Onco["Missense"]),
  Truncating = alter_graphic("rect", height = 0.33, fill = col.Onco["Truncating"]),
  Duplication = alter_graphic("rect", width = 0.23, fill = col.Onco["Duplication"]),
  Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Deletion"])
)

column_title = "Altered in 13 of 13 BPDCN samples"
heatmap_legend_param = list(title = "Alternations", at = c("Missense", "Truncating", "Duplication", "Deletion"), 
                            labels = c("Missense", "Truncating", "Duplication", "Deletion"))

pdf('~/Desktop/240117.BPDCN.Oncoprint.pdf', height=15)
a <- oncoPrint(Onco.Data,
               alter_fun = alter_fun, col = col.Onco, 
               column_title = column_title, heatmap_legend_param = heatmap_legend_param,
               pct_side = "right", row_names_side = "left",
               alter_fun_is_vectorized = FALSE,
               bottom_annotation = ha,
               column_order = colnames(Onco.Data),
               row_names_gp = gpar(fontsize=7, fontface='italic'),
               pct_gp = gpar(fontsize=7),
               row_title_gp = gpar(fontsize=4))
draw(a, heatmap_legend_side = "bottom", annotation_legend_side = "bottom", merge_legend = TRUE,
     row_gap = unit(100, "mm"))
dev.off()