#!/usr/bin/Rscript

df = read.table('normals15', sep=" ")

lengths = sqrt(df[[1]] ** 2 + df[[2]] ** 2 + df[[3]] ** 2)

hist(lengths)
