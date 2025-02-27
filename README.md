# AICviz
Visualization of Data in the Art Institute of Chicago

Hi there :) Welcome to my project. This project is a demonstration of my techincal capabilities in fetching data with API, data cleanup, and visualization utilizing various Python libraries.

Installation Steps:



Log:
The project took many iterations. the data from AIC is a lot, and so the first prototypes of the models and visuals were extracted from a sample rather than the whole dataset.
The API extracted each artwork as their own json file. This may be helpful in reducing memory consumption, but I wrote a script that combines all artworks into a csv file for more options in data manipulation. (See json reader stuff.py) The script also helped clear out the columns. The AIC includes an impressive amount of metadata, but most of it is not helpful for visualization purposes.

The first attempt of Word processing has come in and it's made it quite difficult to sort out. It also means that the description is very little of the actual sample size of artworks. If I were to be actually interested in what I originally wanted to do I would develop an AI that could recognize meaning in art. (that is very very difficult it seems). 
