rm(list=ls())

library(dplyr)
library(tidyverse)
library(readr)
library(readxl)

data <- read_xlsx("C:/Users/aleks/Documents/player_data.xlsx") #reading file
data <- na.omit(data)

data$INJURY <- ifelse(data$INJURY == 1, 0, 1)
data$DAYS_REST <- data$DAYS_REST*-1

Logistic_Model <- glm(INJURY ~ Accumulated_Minutes, family = binomial(link = logit), data = data)

##predict computes the probabilities for given sample values
Pred <- predict(Logistic_Model, type = "response")

##'round' allows us to derive the binary predicted values
Binary <- round(Pred)

##both y and the object 'Binary'
##contain values 0 or 1
##here we use 'mean' to compute the proportion of 
##correctly classified cases (*100 for percentage)
100*mean(data$INJURY == Binary)
summary(Logistic_Model)

newdata <- data.frame(Accumulated_Minutes=seq(min(data$Accumulated_Minutes), max(data$Accumulated_Minutes),len=500))
newdata$INJURY = predict(Logistic_Model, newdata, type="response")

plot(INJURY ~ Accumulated_Minutes, data = data, col="steelblue")
lines(INJURY ~ Accumulated_Minutes, newdata, lwd=2)
