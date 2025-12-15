import pandas as pd
import matplotlib.pyplot as plt
import os


#Helper function to save plots to output directory
def save_plot(filename, output_dir='output/visualizations'):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    print(f"Saved: {filepath}")
    plt.close()

#Scatter plot for revenue vs Budget
def plot_revenue_vs_budget(clean_df):
    plt.figure(figsize=(8, 5))
    plt.scatter(clean_df['budget_musd'], clean_df['revenue_musd'])
    plt.xlabel("Budget (Million USD)")
    plt.ylabel("Revenue (Million USD)")
    plt.title("Revenue vs Budget")
    save_plot('revenue_vs_budget.png')


# Expand genres into separate rows
def plot_roi_by_genre(clean_df):
    genre_df = clean_df[['genres', 'roi']].dropna()
    genre_df = genre_df.assign(genres=genre_df['genres'].str.split('|')).explode('genres')

    plt.figure(figsize=(8, 5))
    plt.boxplot([genre_df[genre_df['genres'] == g]['roi'].dropna()
                 for g in genre_df['genres'].unique()],
                labels=genre_df['genres'].unique(),
                vert=True)

    plt.xticks(rotation=90)
    plt.title("ROI Distribution by Genre")
    plt.ylabel("ROI")
    save_plot('roi_by_genre.png')


    #Scatter plot of Popularity vs Rating (vote_average)
def plot_popularity_vs_rating(clean_df):
    plt.figure(figsize=(8, 5))
    plt.scatter(clean_df['popularity'], clean_df['vote_average'])
    plt.xlabel("Popularity")
    plt.ylabel("Rating (vote_average)")
    plt.title("Popularity vs Rating")
    save_plot('popularity_vs_rating.png')


    #Line plot showing average revenue trends over years
def plot_yearly_avg_revenue(clean_df):
    clean_df_copy = clean_df.copy()
    clean_df_copy['release_year'] = clean_df_copy['release_date'].dt.year

    yearly = clean_df_copy.groupby('release_year')['revenue_musd'].mean()

    plt.figure(figsize=(8, 5))
    plt.plot(yearly.index, yearly.values)
    plt.xlabel("Year")
    plt.ylabel("Average Revenue (M USD)")
    plt.title("Yearly Box Office Performance")
    plt.grid(True)
    save_plot('yearly_avg_revenue.png')


#Bar plot comparing average revenue between franchise and standalone movies
def plot_franchise_vs_standalone(clean_df):
    franchise_df = clean_df[clean_df['belongs_to_collection'].notna()]
    standalone_df = clean_df[clean_df['belongs_to_collection'].isna()]

    labels = ["Franchise", "Standalone"]
    avg_revenue = [
        franchise_df['revenue_musd'].mean(),
        standalone_df['revenue_musd'].mean()
    ]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, avg_revenue)
    plt.title("Franchise vs Standalone: Average Revenue")
    plt.ylabel("Average Revenue (M USD)")
    plt.show()


#Print detailed statistics comparing franchise and standalone movies
def franchise_vs_standalone_stats(clean_df):
    franchise_df = clean_df[clean_df['belongs_to_collection'].notna()]
    standalone_df = clean_df[clean_df['belongs_to_collection'].isna()]

    franchise_stats = franchise_df[['revenue_musd', 'roi', 'budget_musd', 'popularity', 'vote_average']].mean()
    standalone_stats = standalone_df[['revenue_musd', 'roi', 'budget_musd', 'popularity', 'vote_average']].mean()

    print("Franchise Stats:\n", franchise_stats)
    print("\nStandalone Stats:\n", standalone_stats)


#Aggregate franchise statistics grouped by collection name
def franchise_group_analysis(clean_df):
    franchise_df = clean_df[clean_df['belongs_to_collection'].notna()]   
    franchise_group = franchise_df.groupby('belongs_to_collection').agg({
        'id': 'count',
        'budget_musd': ['sum', 'mean'],
        'revenue_musd': ['sum', 'mean'],
        'vote_average': 'mean'
    })

    franchise_group = franchise_group.sort_values(('revenue_musd', 'sum'), ascending=False)
    
    return franchise_group.head()


    #Aggregate director statistics
def director_group_analysis(clean_df):
   
    director_group = clean_df.groupby('director').agg({
        'id': 'count',
        'revenue_musd': 'sum',
        'vote_average': 'mean'
    }).sort_values('revenue_musd', ascending=False)

    return director_group.head()


    #Search for Science Fiction and Action movies with Bruce Willis
def search_bruce_willis_scifi_action(clean_df):
    search1 = clean_df[
        clean_df['genres'].str.contains("Science Fiction", na=False) &
        clean_df['genres'].str.contains("Action", na=False) &
        clean_df['cast'].str.contains("Bruce Willis", na=False)
    ]

    search1 = search1.sort_values(by='vote_average', ascending=False)
    
    return search1[['title', 'genres', 'vote_average']]


    #Search for Uma Thurman movies directed by Quentin Tarantino
def search_uma_thurman_tarantino(clean_df):
    search2 = clean_df[
        clean_df['cast'].str.contains("Uma Thurman", na=False) &
        (clean_df['director'] == "Quentin Tarantino")
    ]

    search2 = search2.sort_values(by='runtime')
    
    return search2[['title', 'runtime', 'director']]


    #Generate all visualizations from the notebook
def generate_all_visualizations(clean_df):
    print("Generating Revenue vs Budget plot...")
    plot_revenue_vs_budget(clean_df)
    
    print("\nGenerating ROI by Genre plot...")
    plot_roi_by_genre(clean_df)
    
    print("\nGenerating Popularity vs Rating plot...")
    plot_popularity_vs_rating(clean_df)
    
    print("\nGenerating Yearly Average Revenue plot...")
    plot_yearly_avg_revenue(clean_df)
    
    print("\nGenerating Franchise vs Standalone plot...")
    plot_franchise_vs_standalone(clean_df)
    
    print("\nFranchise vs Standalone Statistics:")
    franchise_vs_standalone_stats(clean_df)
    
    print("\nFranchise Group Analysis:")
    print(franchise_group_analysis(clean_df))
    
    print("\nDirector Group Analysis:")
    print(director_group_analysis(clean_df))
    
    print("\nBruce Willis - Science Fiction & Action Movies:")
    print(search_bruce_willis_scifi_action(clean_df))
    
    print("\nUma Thurman - Quentin Tarantino Movies:")
    print(search_uma_thurman_tarantino(clean_df))


    # Example usage - load data and generate visualizations
if __name__ == "__main__":
    
    try:
        clean_df = pd.read_csv('output/clean_movies.csv', parse_dates=['release_date'])
        generate_all_visualizations(clean_df)
    except FileNotFoundError:
        print("Error: output/clean_movies.csv not found. Please ensure the data pipeline has been run.")
