# pipeline.py
from extract import extract
from transform import transform
# from load import save_to_csv

def run_pipeline():

    print("   TMDB MOVIE ETL PIPELINE")
    # Extract
    raw_df = extract()

    # Transform
    clean_df = transform(raw_df)

    # # Load
    # save_to_csv(clean_df)

    print("\n[PIPELINE] ETL Pipeline completed successfully.\n")


if __name__ == "__main__":
    run_pipeline()
