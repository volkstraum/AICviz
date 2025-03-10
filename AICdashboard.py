#%%
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

#%%
df = pd.read_csv("datasets/artworks.csv")  # Update with actual file path
dfe = pd.read_csv("datasets/artwork_category_counts.csv")

# Convert year columns to numeric for filtering
df["date_start"] = pd.to_numeric(df["date_start"], errors="coerce")
df = df.dropna(subset=["date_start"])
df["avg_year"] = ((df["date_start"] + df["date_end"]) / 2).round()
df["decade"] = (df["avg_year"] // 10) * 10  # Group by decade

df = df[df["title"] != "Indian on Horse Attacked by Bears"] #this particular point had an unusual work start date in the millions, causing issues
df = df[df["date_end"] <= 2025] #some data points had a date end of over a few thousand. This is used to limit it to 2025.


#%% Function: Line Chart - Trends in Artwork Production Over Time--------------------------------------------------------------------------------
def plot_artwork_trends():
    trend_df = df.groupby("decade")["id"].count().reset_index()
    trend_df.columns = ["decade", "count"]

    fig = px.line(
        trend_df,
        x="decade",
        y="count",
        title="Number of Artworks in the Collection per Decade",
        labels={"decade": "Decade", "count": "Number of Artworks"},
        markers=True
    )
    fig.update_traces(line_color='#B60235')
    fig.update_layout(
        plot_bgcolor="lightgray",
        paper_bgcolor="#F8F7F7")
    return fig

#%% Function: Pie Chart - Artwork Type Distribution
def plot_artwork_type_distribution():
    if "Category" in dfe.columns and "Count" in dfe.columns:
        fig = px.pie(
            dfe,
            names="Category",
            values="Count",
            title="Distribution of Artwork Categories",
            hole=0.3  # Donut-style chart
        )
        
        # Set custom background colors
        fig.update_layout(
            plot_bgcolor="lightgray",  # Plot area background
            paper_bgcolor="#F8F7F7"  # Full figure background
        )
        
        return fig
    return None

#%% Function: Tree Diagram - Classification Title Distribution
def plot_classification_distribution():
    if "artwork_type_title" in df.columns:
        classification_counts = df["artwork_type_title"].value_counts().reset_index()
        classification_counts.columns = ["artwork_type", "count"]

        fig = px.treemap(
            classification_counts,
            path=["artwork_type"],
            values="count",
            title="Distribution of Artwork Types",
            color="count",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(
        plot_bgcolor="lightgray",
        paper_bgcolor="#F8F7F7")
        return fig
    return None

#%% Function: Choropleth Map - Artwork Origins by Decade
# Adjusted function: Keep actual counts but limit the color range to 0-100+
def plot_origin_distribution(decade):
    filtered_df = df[df["decade"] == decade]

    origin_counts = filtered_df["place_of_origin"].value_counts().reset_index()
    origin_counts.columns = ["place_of_origin", "count"]

    # Create the choropleth map with color range explicitly set from 0 to 100+
    fig = px.choropleth(
        origin_counts,
        locations="place_of_origin",
        locationmode="country names",
        color="count",
        title=f"Artwork Origins in {decade}s",
        color_continuous_scale="Viridis",
        range_color=[0, 100],  # Set color scale but keep actual values unchanged
        hover_data={"place_of_origin": True, "count": True}  # Display actual count
    )
    fig.update_layout(
        plot_bgcolor="lightgray",
        paper_bgcolor="#F8F7F7")
    
    return fig

#%% Function: Bar Chart - Artwork Category Distribution by Decade
def plot_category_distribution(decade):
    filtered_df = df[df["decade"] == decade]

    category_counts = filtered_df["artwork_type_title"].value_counts().reset_index()
    category_counts.columns = ["artwork_type_title", "count"]

    fig = px.bar(
        category_counts,
        x="artwork_type_title",
        y="count",
        title=f"Artwork Types in {decade}s",
        labels={"artwork_type_title": "Artwork Type", "count": "Number of Artworks"},
        color="count",
        color_continuous_scale="Blues",
        hover_data={"artwork_type_title": True, "count": True}
    )
    fig.update_layout(
        plot_bgcolor="lightgray",
        paper_bgcolor="#F8F7F7")
    return fig

#%% Function: Metadata Table - Artwork Details
def show_artwork_metadata(decade):
    filtered_df = df[df["decade"] == decade][["title", "artist_display", "place_of_origin", "medium_display", "dimensions"]]
    st.write(f"### Artworks from the {decade}s")
    st.dataframe(filtered_df, use_container_width=True)  # Full-width table


#%% TAB 1 Functions
def plot_origin_distribution1(selected_period):
    start_decade, end_decade = selected_period

    # Filter dataset within the selected time range
    filtered_df = df[(df["decade"] >= start_decade) & (df["decade"] <= end_decade)]

    origin_counts = filtered_df["place_of_origin"].value_counts().reset_index()
    origin_counts.columns = ["place_of_origin", "count"]

    # Create the choropleth map with color range explicitly set from 0 to 100+
    fig = px.choropleth(
        origin_counts,
        locations="place_of_origin",
        locationmode="country names",
        color="count",
        title=f"Artwork Origins from {start_decade} to {end_decade}",
        color_continuous_scale="Viridis",
        range_color=[0, 100],  # Set color scale but keep actual values unchanged
        hover_data={"place_of_origin": True, "count": True}  # Display actual count
    )

    # Set background colors
    fig.update_layout(
        plot_bgcolor="lightgray",
        paper_bgcolor="#F8F7F7"
    )
    
    return fig

# Adjusted function: Bar Chart for Artwork Category Distribution based on the selected time period range
def plot_category_distribution1(selected_period):
    start_decade, end_decade = selected_period

    # Filter dataset within the selected time range
    filtered_df = df[(df["decade"] >= start_decade) & (df["decade"] <= end_decade)]

    category_counts = filtered_df["artwork_type_title"].value_counts().reset_index()
    category_counts.columns = ["artwork_type_title", "count"]

    fig = px.bar(
        category_counts,
        x="artwork_type_title",
        y="count",
        title=f"Artwork Types from {start_decade} to {end_decade}",
        labels={"artwork_type_title": "Artwork Type", "count": "Number of Artworks"},
        color="count",
        color_continuous_scale="Blues",
        hover_data={"artwork_type_title": True, "count": True}
    )

    # Set background colors
    fig.update_layout(
        plot_bgcolor="lightgray",
        paper_bgcolor="#F8F7F7"
    )

    return fig

# This function now filters artworks **within a selected time range** instead of a single decade 🚀
# Adjusted function: Display Artwork Metadata based on the selected time period range
def show_artwork_metadata1(selected_period):
    start_decade, end_decade = selected_period

    # Filter dataset within the selected time range
    filtered_df = df[(df["decade"] >= start_decade) & (df["decade"] <= end_decade)][
        ["title", "artist_display", "place_of_origin", "medium_display", "dimensions"]
    ]

    # Display metadata with a dynamically updated title
    st.write(f"### Artworks from {start_decade} to {end_decade}")
    st.dataframe(filtered_df, use_container_width=True)  # Full-width table

# This function now filters artworks **within a selected time range** instead of a single decade 🚀


#%% Streamlit UI Setup----------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        .top-row {
            background-color: #B60235;
            padding: 50px;
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: white;
            border-radius: 1px;
        }
    </style>
    <div class="top-row">Interactive Analysis of the Art Institute of Chicago Art Collection</div>
    """,
    unsafe_allow_html=True
)
st.subheader("This project provides a multi-dimensional outlook of the Art Institute of Chicago collection in order to see potential trends and patterns in the types or time period of collected artworks.")
st.write("The page is split up into two major sections: The first section, seen in the first row of visualizations, display three representations of the overall amount of artworks collected and their different types. The second section allows the user to see specific time periods and decades in order to get a more specific analysis of the time period or decade.")
st.write("")
st.header("Overview of Artworks Across Time and Medium")
# Generate plots
fig_line = plot_artwork_trends()
fig_pie = plot_artwork_type_distribution()
fig_tree = plot_classification_distribution()

#%% Display First Row: Line Chart, Pie Chart, and Treemap
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_line, use_container_width=True)
    st.write("The line chart was created as an overal outlook on the distribution of artworks by their decade. The plot data was retrieved from the AIC database that had each individual artwork and their estimated start and end date of the creation process. The artwork start and end dates were averaged out and grouped by decade, followed by a count function that calculated how many artworks belonged to a certain decade. There were a few outliers that were removed where an end date would be past the present and the start date would be millions of years in the past for an artwork that did not fit that timestamp.")

with col2:
    if fig_pie:
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No artwork type title data available.")
    st.write("This pie chart serves to help visualize the makeup of artwork categories in the collection. There is an emphasis on categories as this display congrugated 43 artwork types into 10 categories. This was done to minimize the vast components making up the pie chart clouded the effectivity of the visualization. The categories were decided by artwork types that made sense together. For example, works on paper included prints, photographs, drawings, books, and graphic designs. Multimedia and Modern art includes installations, mixed media, time based media, digital arts, and audio-video works.")
with col3:
    if fig_tree:
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.warning("No classification titles found in dataset.")
    st.write("This treemap attemps to visualize all the artwork types present in the collection. This is an especially difficult task given the amount of artwork types there are along with the sheer range of distribution of types. Prints and photographs dominate the type makeup of the collection, which causes the other artwork types to seem insignificant in comparison. While that may be the case, it fails to take into consideration on the nature of production of these artworks. Prints and photographs are naturally faster to produce than furniture objects and armor. Nonetheless, while this representation is flawed, it provides a closer look at each artwork types to the user.")
st.write("")
st.write("All in all, there are some interesting observations to be made here. From the graphs, it becomes evident that most of the artworks in the collection were created in the 1800s and forward, with most of it in the 1960s and 1970s. As a result, the distribution of artworks became skewed towards artwork types prevelant in those periods like prints and photographs. Perhaps for the future it may be interesting to focus the analysis on these two decades or see how the distribution in the collection looks without this unbalance.")

st.header("Geographic and Categorical Distribution of Artworks by Time Period and Decade")
#%% Tabs
tab1, tab2 = st.tabs(["Time Period", "Individual Decades"])

with tab1:
    st.markdown("### Select a Time Period")

# Define time period clusters
    time_periods = {
    "Ancient & Classical Art (-5000 to 0)": (-5000, 0),
    "Medieval & Early Postclassical Art (0 to 1400)": (0, 1400),
    "Early Global Exchange (1400-1700)": (1400, 1700),
    "Art in the Age of Empires (1700-1900)": (1700, 1900),
    "Modern & Contemporary Art (1900-Present)": (1900, 2025)
}
# Create buttons for each period
    selected_period = None
    col1, col2, col3 = st.columns(3)

    for i, (label, (start, end)) in enumerate(time_periods.items()):
        if i % 3 == 0:
            with col1:
                if st.button(label):
                    selected_period = (start, end)
        elif i % 3 == 1:
            with col2:
                if st.button(label):
                    selected_period = (start, end)
        else:
            with col3:
                if st.button(label):
                    selected_period = (start, end)

# If no button has been pressed, default to the most recent period
    if selected_period is None:
        selected_period = (1900, 2025)

    # Filter the dataset based on the selected period
    filtered_df = df[(df["decade"] >= selected_period[0]) & (df["decade"] <= selected_period[1])]
    col4, col5 = st.columns(2)

    with col4:
            st.plotly_chart(plot_origin_distribution1(selected_period), use_container_width=True)
            st.write("This choropleth map displays the geographic distribution of artworks. The count is heavily skewed consistently to certain countries like the United States, China, and Germany. A limit of 100+ was implemented in the color scheme to prevent these three countries lighting up and leaving the rest as black. Generally, this worked, though the code has technical difficulties where sometimes the countries would show dark despite having over 10K artworks.")
    with col5:
            st.plotly_chart(plot_category_distribution1(selected_period), use_container_width=True)
            st.write("This bar plot serves a similar function to the pie chart and tree map in showing the types of artworks, just for the specific time period. The bar plot is good here as it allows the user to see every artwork type present, albeit most of these entries are tiny and hard to navigate compared to the first few. This plot, along with all the others, offer a fullscreen option which may help with that issue.")

#%% Display Third Row: Full-Width Metadata Table
    st.write("")
    st.write("There are some very interesting observations to be made. Firstly, going through the time periods it is revealed that prints have been a dominant art form in the collection since the 'Early Global Exchange' period, whereas the visualizations above suggested that most of the prints correlated with the giant collection in the 1960s and 1970s. This raises the question of how exactly prints were utilized as art forms throughout these periods and if they are just a bias of the Institute or potentially an indication to larger trends in art history. Nonetheless, this illuminates some limitations of this analysis: The most important limitation is that these are merely metadata and do not display the most important aspect of art which is the visual. This causes 'prints' to be an umbrella type that combines potentially many different expressions of the medium. Additionally, the data does not indicate any relation between the artworks and the museums, making it impossible to derive any conclusions on whether the collection of the Institute can be indicative of any larger trends in the arts. Finally, the time period buttons are a bit problematic as distinctions of time periods are difficult to make on a global scale as cultures develop in their own ways. These lables are meant for an effective visualization and is by no means a marker of period shifts.")
    st.write("As a potential future direction, it maybe interesting to produce some visualizations on artists. It would also be interesting to see how I could mathematically distinguish the time periods to give a more evenly distributed display. The dataset also included a column called classification titles that grouped multiple themes and mediums under the artwork. It would also be interesting to do a sankey diagram to see how these classifications converge into types and categories.")
    st.markdown("### Artwork Metadata")
    show_artwork_metadata1(selected_period)
#%% Decade Selection Slider (Centered Below First Row)
with tab2:
    st.write("This tab is meant to supplement the Time Period and Overall visualizations. It allows the users to query into individual decades to see a detailed breakdown on the artworks metadata. As the collection is spread throughout the centuries, the slider often shows little data save for 1960 and 1970s. Perhaps an addition in the future is other forms of visualization that takes advantage of the comparatively low amount of artworks per decade.")
    st.markdown("### Select a Decade")
    selected_decade = st.slider(
    "Select a decade",  # Provide an accessible label
    int(df["decade"].min()),
    int(df["decade"].max()),
    step=10,
    label_visibility="collapsed"  # Keeps the label hidden while maintaining accessibility
)

#%% Display Second Row: Choropleth & Bar Chart
    col4, col5 = st.columns(2)

    with col4:
        st.plotly_chart(plot_origin_distribution(selected_decade), use_container_width=True)

    with col5:
        st.plotly_chart(plot_category_distribution(selected_decade), use_container_width=True)



#%% Display Third Row: Full-Width Metadata Table
    st.markdown("### Artwork Metadata")
    show_artwork_metadata(selected_decade)

st.markdown("---")

st.markdown(
    """
    **Data Source:**  
    This analysis is based on data from the  
    [Art Institute of Chicago API Data](https://github.com/art-institute-of-chicago/api-data).
    """,
    unsafe_allow_html=True
)