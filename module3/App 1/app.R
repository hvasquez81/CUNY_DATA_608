#packages)
library(dplyr)
library(ggplot2)
library(shiny)





#data
data = read.csv("https://raw.githubusercontent.com/hvasquez81/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")
head(data)

ui = fluidPage(
  
  titlePanel("Crude Mortality in US by Cause"),
  sidebarLayout(
    sidebarPanel(
      #select one cause
      selectInput(
        inputId = "causeInput",
        label = "Cause of Death",
        choices = unique(data[, 'ICD.Chapter']),
        multiple = FALSE
        )
    ),
    mainPanel(
      plotOutput("plot")
    )
  )
  
)



server = function(input, output) { 
  output$plot = renderPlot({
    #filter by inputs
    filteredData = data %>% filter(Year == 2010 & ICD.Chapter == input$causeInput)
    ggplot(filteredData, aes(x = reorder(State, -Crude.Rate), y = Crude.Rate, fill = Crude.Rate)) + 
      geom_histogram(stat = 'identity') + 
      labs(title = paste0('Crude Rate by Desease ', "(", input$causeInput, ")"),
           subtitle = '2010',
           x = 'States',
           y = 'Crude Rate',
           color = 'States') +
      theme_classic()
  })
}
shinyApp(ui, server)







