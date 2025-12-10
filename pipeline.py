# pipeline.py
from extract import extract
from transform import transform
from load import save_to_csv
from visualization import generate_all_visualizations

def run_pipeline():

    print("   TMDB MOVIE ETL PIPELINE")
    # Extract
    raw_df = extract()

    # Transform
    clean_df = transform(raw_df)

    #  Load
    save_to_csv(clean_df)

    print("ETL Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
