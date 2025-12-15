
#  Final Report: TMDB Movie Analysis

## 1. Introduction
This project analyzed movie data collected from the TMDB API. The goal was to clean the dataset, transform key fields, and extract insights about movie performance over the years.

## 2. Methodology

### Data Collection
- Data was gathered using the TMDB API.
- Results were loaded into a Pandas DataFrame for cleaning and analysis.

### Data Cleaning Steps
- Removed rows missing essential fields such as 'title', 'id', and 'release_date'.
- Filled missing values in fields like 'runtime' and 'overview'.
- Converted important columns such as 'budget', 'popularity', and 'release_date' to proper datatypes.
- Extracted the movie 'release_year' for trend analysis.

### Exploratory Data Analysis
- Identified trends in movie releases.
- Examined popular movies and revenue patterns.
- Investigated runtime, ratings, and production budgets.
- Looked for correlations among key metrics (budget, revenue, popularity, vote_average).


## 3. Key Insights

### 1. Movie Release Trends
- There has been a consistent rise in movie releases over the years.
- More movies were produced between 2000 and 2020 than earlier decades.

### 2. Revenue and Budget Patterns
- Higher budgets generally correlate with higher revenue.
- Some low-budget movies still performed extremely well, showing strong ROI potential.

### 3. Ratings and Popularity
- Popular movies tend to receive higher vote counts.
- High vote averages do not always mean high popularity — audience size matters.

### 4. Movie Runtime
- Most movies fall within a 90–120 minute range.
- Runtime does not necessarily predict popularity or revenue.


## 4. Conclusion
The TMDB dataset provides rich information for understanding trends in the movie industry. By cleaning and structuring the data properly, we can uncover patterns in audience preferences, budget strategies, and film success rates.

Future improvements could include:
- Joining more TMDB endpoints (genres, cast, crew).
- Building a recommendation engine.
- Performing machine learning predictions (e.g., box office success).

