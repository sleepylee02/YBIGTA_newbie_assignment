library(tidyverse)
### Advertising.csv를 불러와 데이터 로드하기!
data <- read.csv("Advertising.csv")


### Multiple Linear Regression을 수행해봅시다!
model <- lm(sales ~ TV + radio + newspaper, data= data)
model %>% summary

### Correlation Matrix를 만들어 출력해주세요!
data %>% colnames
data %>% select(-"X") %>% cor