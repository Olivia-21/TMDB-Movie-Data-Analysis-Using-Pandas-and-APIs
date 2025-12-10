# transform.py
import pandas as pd

# Extraction Functions 
def extract_cast(credits):
    if isinstance(credits, dict) and "cast" in credits:
        return "|".join([p["name"] for p in credits["cast"][:10]])
    return None

def extract_director(credits):
    if isinstance(credits, dict) and "crew" in credits:
        for p in credits["crew"]:
            if p.get("job") == "Director":
                return p["name"]
    return None

def extract_cast_size(credits):
    if isinstance(credits, dict) and "cast" in credits:
        return len(credits["cast"])
    return None

def extract_crew_size(credits):
    if isinstance(credits, dict) and "crew" in credits:
        return len(credits["crew"])
    return None

def extract_names(value):
    if isinstance(value, list):
        return "|".join([v.get("name","") for v in value])
    return None

def extract_collection(value):
    if isinstance(value, dict):
        return value.get("name")
    return None


# Main Transformation Function 

def transform(df):
    print("[TRANSFORM] Starting transformation..")

    clean_df = df.copy()

    # Drop unwanted columns
    cols_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
    clean_df = clean_df.drop(columns=cols_to_drop, errors="ignore")

    # Extract credits-list fields
    clean_df["cast"]       = clean_df["credits"].apply(extract_cast)
    clean_df["director"]   = clean_df["credits"].apply(extract_director)
    clean_df["cast_size"]  = clean_df["credits"].apply(extract_cast_size)
    clean_df["crew_size"]  = clean_df["credits"].apply(extract_crew_size)

    # Extract names from JSON columns
    json_columns = ['genres','production_countries','production_companies','spoken_languages']
    for col in json_columns:
        clean_df[col] = clean_df[col].apply(extract_names)

    clean_df['belongs_to_collection'] = df['belongs_to_collection'].apply(extract_collection)

    # Convert numeric columns
    numeric_cols = ['budget', 'revenue', 'popularity', 'vote_count', 'vote_average', 'runtime']
    for col in numeric_cols:
        clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")

    clean_df['release_date'] = pd.to_datetime(clean_df['release_date'], errors="coerce")

    # Replace 0 with NaN
    clean_df[['budget','revenue','runtime']] = clean_df[['budget','revenue','runtime']].replace(0, pd.NA)

    # Convert to million USD
    clean_df["budget_musd"] = clean_df["budget"] / 1_000_000
    clean_df["revenue_musd"] = clean_df["revenue"] / 1_000_000

    # Remove rows with too many missing fields
    clean_df = clean_df.dropna(thresh=10)

    # Final selected columns
    final_columns = [
        'id','title','tagline','release_date','genres','belongs_to_collection',
        'original_language','budget_musd','revenue_musd','production_companies',
        'production_countries','vote_count','vote_average','popularity','runtime',
        'overview','spoken_languages','poster_path','cast','cast_size','director','crew_size'
    ]
    clean_df = clean_df[[c for c in final_columns if c in clean_df.columns]]

    # KPI Calculations 
    clean_df["profit"] = clean_df["revenue_musd"] - clean_df["budget_musd"]
    clean_df["roi"] = clean_df["revenue_musd"] / clean_df["budget_musd"]
    clean_df["roi"] = clean_df["roi"].replace([float("inf"), -float("inf")], pd.NA)

    print("[TRANSFORM] Transformation completed.")
    return clean_df
