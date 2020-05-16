library(shiny)

library('qrmdata')
library('ggplot2')
library('forecast')
library('tseries')
library('xts')
library('graphics')

xts.to.ts <- function(X, freq = 12L) {
    ts(as.numeric(X), 
          start = c(.indexyear(X)[1] + 1900, .indexmon(X)[1] + 1),
          freq = freq)
}

ui <- fluidPage(
  titlePanel("Forecast"),
  sidebarLayout(
    sidebarPanel(
      radioButtons("dataset", "Dataset:",
               c("Gold" = "gold",
                 "British Pound" = "cur_gbp",
                 "Euro" = "cur_eur",
                 "Canadian Dollar" = "cur_can",
                 "Crypto [BTC]" = "crypto_btc",
                 "Crypto [ETH]" = "crypto_eth",
                 "Crypto [XRP]" = "crypto_xrp")),
      radioButtons("method", "Method:",
               c("ETS" = "ets",
                 "ARIMA" = "arima",
                 "ARFIMA" = "arfima",
                 "STL" = "stl",
                 "TBATS" = "tbats"))
    ),
    mainPanel(
      tabsetPanel(type = "tabs",
                  tabPanel("Hist", plotOutput("hist")),
                  tabPanel("Plot", plotOutput("plot"))
      )
    )
  )
)

data("GOLD")
data("crypto")
data("CAD_USD")
data("GBP_USD")
data("EUR_USD")

serverEts <- function(dataset) {
  dataset %>%
    ets() %>%
    forecast()
}

serverArima <- function(dataset) {
  dataset %>%
    auto.arima() %>%
    forecast(h=20)
}

serverArfima <- function(dataset) {
  arfima(dataset) %>%
    forecast(h=30)
}

serverStl <- function(dataset) {
  dataset %>%
    stlm(modelfunction=ar) %>%
    forecast(h=36)
}

serverTbats <- function(dataset) {
  dataset %>%
    tbats() %>%
    forecast()
}

server <- function(input, output) {
  dataset <- reactive({
    data <- switch(input$dataset,
                     cur_gbp = GBP_USD['2010/'],
                     cur_eur = EUR_USD['2010/'],
                     cur_can = CAD_USD['2010/'],
                     crypto_btc = crypto$BTC,
                     crypto_eth = crypto$ETH,
                     crypto_xrp = crypto$XRP,
                     GOLD['2010/'])
    data <- xts.to.ts(data)
    data
  })

  method <- reactive({
    switch(input$method,
                     ets = serverEts,
                     arima = serverArima,
                     arfima = serverArfima,
                     stl = serverStl,
                     serverTbats)
  })

  output$plot <- renderPlot({
    d <- dataset()
    method()(d) %>%
      autoplot()
  })

  output$hist <- renderPlot({
    d <- dataset()
    hist(d)
  })
}

server <- function(input, output) {
  dataset <- reactive({
    dnorm(100)
  })

  output$plot <- renderPlot({
    dataset() %>%
      plot()
  })

  output$hist <- renderPlot({
    dataset() %>%
      hist()
  })
}

shinyApp(ui = ui, server = server)