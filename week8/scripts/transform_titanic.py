import os 
import pandas as pd 
from extract_titanic import extract_data

def transform_data(raw_path):
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_dir=os.path.join(base_dir,"data","staged")
    os.makedirs(staged_dir,exist_ok=True)
    df=pd.read_csv(raw_path)
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    cat_cols = df.select_dtypes(include=['object']).columns
    df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

    df.drop(columns=[],inplace=True,errors='ignore')

    staged_path=os.path.join(staged_dir,'titanic_transformed.csv')
    df.to_csv(staged_path,index=False)
    print(f"Data transformed and saved at : {staged_path}")

    return staged_path

if __name__=="__main__":
    from extract_titanic import extract_data
    raw_path=extract_data()
    transform_data(raw_path)