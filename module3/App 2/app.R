library(dplyr)
library(ggplot2)
library(RColorBrewer)
library(shiny)


#data
data = read.csv("https://raw.githubusercontent.com/hvasquez81/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")
head(data)

ui = fluidPage(
  
  titlePanel("Crude Mortality: State vs. National Average"),
  sidebarLayout(
    sidebarPanel(
      #select one cause
      selectInput(
        inputId = "causeInput",
        label = "Cause of Death",
        choices = unique(data[, 'ICD.Chapter']),
        multiple = FALSE
      ),
      selectInput(
        inputId = "stateInput",
        label = "Select State",
        choices = unique(data[, 'State']),
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
    filteredData = data %>% filter(ICD.Chapter == input$causeInput)
    
    #create the df that pulls yearly average- calculate average by total population not just rate
    averagedf = filteredData %>% 
      select('ICD.Chapter', 'Year', 'Deaths', 'Population') %>% 
      group_by(ICD.Chapter, Year) %>%
      summarize(TotalDeaths = sum(Deaths),
                TotalPopulation = sum(as.numeric(Population))
                ) %>%
      mutate('Crude.Rate' = round((100000*TotalDeaths/TotalPopulation),2),
             'State' = as.factor('National Average')) %>%
      select('ICD.Chapter', 'State', 'Year', 'Crude.Rate')
    
    #state data
    statedf = filteredData %>%
      select('ICD.Chapter', 'State', 'Year', 'Crude.Rate') %>%
      filter(State == input$stateInput)
      
    #graph data 
    graphData = rbind(as.data.frame(averagedf), as.data.frame(statedf))
    
    #plot 
    ggplot(graphData, aes(x = Year, y = Crude.Rate, group = State)) + 
      geom_line(aes(color = State, linetype = State)) + 
      labs(title = paste0('Crude Rate by Desease ', "(", input$causeInput, ")"),
           subtitle = input$yearInput,
           x = 'State',
           y = 'Crude Rate',
           color = 'State') +
      scale_color_manual(values = c('#90AFC5', '#336B87')) +
      theme_classic() 
  })
}
shinyApp(ui, server)







