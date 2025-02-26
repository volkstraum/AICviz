# AICviz
Visualization of Data in the Art Institute of Chicago

Hi there :) Welcome to my project. This project is a demonstration of my techincal capabilities in fetching data with API, data cleanup, and visualization utilizing various Python libraries.

Installation Steps:



Log:
The project took many iterations. the data from AIC is a lot, and so the first prototypes of the models and visuals were extracted from a sample rather than the whole dataset.
The API extracted each artwork as their own json file. This may be helpful in reducing memory consumption, but I wrote a script that combines all artworks into a csv file for more options in data manipulation. (See json reader stuff.py) The script also helped clear out the columns. The AIC includes an impressive amount of metadata, but most of it is not helpful for visualization purposes.

