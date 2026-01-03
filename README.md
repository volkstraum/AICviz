
# Visualization of Data in the Art Institute of Chicago

### Project Overview
AICviz is an interactive visualization dashboard built to explore trends in the Art Institute of Chicago’s public collection data. The project investigates how artworks distribute across time, geography, and medium, and how these patterns shift when viewed decade by decade rather than as a static whole.

This repository contains both the Streamlit-based visualization app and the data processing scripts used to transform the raw AIC dataset into analysis-ready formats.

---

## What this project does

- **Data source**: Art Institute of Chicago Open Access API (artwork metadata)
- **Key transformations**: cleaning and normalizing metadata, decade-based aggregation, categorical grouping
- **Primary views**:
  - temporal distributions of artworks by decade  
  - geographic breakdowns of artwork origins  
  - categorical and medium-based comparisons  
  - interactive filtering to reveal shifts in collection emphasis over time  

The goal of this project is not only exploratory analysis, but also to prototype a public-facing interface that makes institutional collections legible through interactive visual means.

## Project Files:
**AICdashboard.py** = the main file. Contains a dashboard of interactive visualizations on the Art Institute of Chicago Collection, along with annotations on the visualizations, limitations, and future directions.

**rawDataProcessor.py** = a data processing script. The original data came with individual .json files representing artworks and their respective metadata. This script combines all the artworks into one .csv file for easier file manipulation. Furthermore, many of the original columns, such as "boost rank", "fiscal year", and "copyright notice", in the metadata was removed to save space and processing power.

**artworkTypeToCategories.py** = another data processing script. This script combines several "artwork types" into a larger "artwork category" column. This was done for the pie chart for a more comprehensive visualization and to minimize many artwork types that had very little counts, like "protoype", "icon", and "materials" with only 1 of each ever categorized.

[datasource](https://github.com/art-institute-of-chicago/api-data) = datasource for the entire project. If you would like to run any of the data processing scripts for yourself, download their full dataset in their README.md and extract that into an "artworks" folder in the main directory.

## Installation Steps:
in your environment, type 
```sh
pip install -r requirements.txt 
```
into the terminal and you should be all good to go!


To run the dashboard, make sure you are in the right directory and type 
```sh
streamlit run AICdashboard.py 
```
into the terminal and it should work!




## Development Notes:
The project took many iterations. the data from AIC is a lot, and so the first prototypes of the models and visuals were extracted from a sample rather than the whole dataset.
The API extracted each artwork as their own json file. This may be helpful in reducing memory consumption, but I wrote a script that combines all artworks into a csv file for more options in data manipulation. (See json reader stuff.py) The script also helped clear out the columns. The AIC includes an impressive amount of metadata, but most of it is not helpful for visualization purposes.

The first attempt of Word processing has come in and it's made it quite difficult to sort out. It also means that the description is very little of the actual sample size of artworks. If I were to be actually interested in what I originally wanted to do I would develop an AI that could recognize meaning in art. (that is very very difficult it seems). 

After realizing this, I decided to pivot the project into a multi-dimensional visual analysis on streamlit instead to fit into the time frame of this project. From there on, the creation process was quite smooth. I wrote out the framework of the project and checked in with my professor for feedback. Initially, the pie chart contained every single artwork type, which made it really hard to get any value out of the visualization. Additionally, the year slide bar was ineffective in showing much as each individual year had not a lot of artworks for the plot that I chose. To combat this, I made another script to put multiple artwork types into bigger artwork categories for the pie chart. For the year slider, I combined the individual years into decades, and eventually made time period buttons, which helped the visualization a lot more.

Finally, I went through and added some color and layout choices that reflect the color scheme of the Art Institute of Chicago. I annotated the graphs and added conclusions below the rows of visualizations to talk about my thoughts and evaluations.
