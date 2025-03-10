#%%
import pandas as pd

#%%
df = pd.read_csv("datasets/artworks.csv") 


df["date_start"] = pd.to_numeric(df["date_start"], errors="coerce")
df = df.dropna(subset=["date_start"])
df["avg_year"] = ((df["date_start"] + df["date_end"]) / 2).round()
df["decade"] = (df["avg_year"] // 10) * 10  # Group by decade

df = df[df["title"] != "Indian on Horse Attacked by Bears"] #this particular point had an unusual work start date in the millions, causing issues
df = df[df["date_end"] <= 2025] #some data points had a date end of over a few thousand. This is used to limit it to 2025.


#%% Function for Artwork Type sorting. This creates a CSV file
# Count occurrences of each artwork type
artwork_type_counts = df["artwork_type_title"].value_counts().reset_index()
artwork_type_counts.columns = ["artwork_type", "count"]

artwork_type_counts.to_csv("artwork_type_counts.csv", index=False)

artwork_type_counts.head()

#%%
artwork_type_counts = pd.read_csv("artwork_type_counts.csv")

# was mapping the artwork types to bigger categories.
category_mapping = {
    "Works on Paper": ["Print", "Photograph", "Drawing and Watercolor", "Architectural Drawing", "Book", "Graphic Design"],
    "Textiles, Fashion, and Accessories": ["Textile", "Costume and Accessories", "Coverings and Hangings"],
    "Paintings and Miniatures": ["Painting", "Miniature Painting"],
    "Sculptures, Ceramics, and Glass": ["Sculpture", "Ceramics", "Glass", "Decorative Arts", "Metalwork"],
    "Architecture and Furniture": ["Architectural Drawing", "Furniture", "Architectural fragment", "Miniature room"],
    "Objects of Daily Life and Ritual": ["Vessel", "Coin", "Religious/Ritual Object", "Mask", "Funerary Object", "Medals", "Icon"],
    "Arms, Armor, and Equipment": ["Arms", "Armor", "Equipment"],
    "Multimedia and Modern Art": ["Installation", "Mixed Media", "Time Based Media", "Film, Video, New Media", "Digital Arts", "Audio-Video"],
    "Industrial and Design Objects": ["Design", "Prototypes"],
    "Archives and Miscellaneous": ["Archives (groupings)", "non-art", "Materials"]
}

category_counts = {}

for index, row in artwork_type_counts.iterrows():
    artwork_type = row["artwork_type"]
    count = row["count"]

    for category, types in category_mapping.items():
        if artwork_type in types:
            if category in category_counts:
                category_counts[category] += count
            else:
                category_counts[category] = count
            break

category_counts_df = pd.DataFrame(list(category_counts.items()), columns=["Category", "Count"])
category_counts_df.to_csv("artwork_category_counts.csv", index=False)


category_counts_df.head()