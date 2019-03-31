# reverent_kilby

## Description

This is a predictable model for menstruation based on K-Means Clustering and Vector Space Model

This program contains several opensource libraries, namely
```
pandas numpy matplotlib sklearn python-telegram-bot
```

data.py - Contains the dataset used for training and testing
constants.py - Contains the tweakable weights of the model
model.py - Contains the Vector Space Model model
presentation.ipynb - Contains graphs and K-Means Model used for inferences and presentation
run.py - The console interface for the model
telegrambot.py - The telegram interface for the model

## Instructions 

To setup
```
install.bat
```

To run via telegram bot
```
py -3 telegrambot.py
```

To run via console, please set your query in run.py, then
```
py -3 run.py
```
