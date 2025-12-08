# import os 
# import pandas as pd 
# from supabase import create_client,Client
# from dotenv import load_dotenv

# #initialize supabase client

# def get_supabase_client():
#     load_dotenv()
#     url=os.getenv("SUPABASE_URL")
#     key=os.getenv("SUPABASE_KEY")
#     if not url or not key :
#         raise ValueError("missing supabase key or url")
#     return create_client(url,key)

# def create_table():
#     try:
#         supabase=get_supabase_client()
#         create_table_sql="""
#           CREATE TABLE IF NOT EXISTS iris_data(id bigserial primary key,sepal_length float,sepal_width float,petal_length float,petal_width float,species text,sepal_ratio float,petal_ratio float,is_petal_long integer)"""
#         try:
#             supabase.rpc('execute_sql',{'query':create_table_sql}).execute()
#             print("table iris datset  created")
#         except Exception as e:
#             print(f"Note:{e}")
#             print(f"table will be created automatically")
#     except Exception as e:
#         print(f"error while creating a table :{e}")
#         print("Con..with insertion ")

# def load_to_supabase(staged_path:str,table_name:str="iris_data"):
#     if not os.path.isabs(staged_path):
#         staged_path=os.path.abspath(os.path.join(os.path.dirname(__file__),staged_path))
#         print("looking for the data fill at : {staged_path}")
#         if not os.path.exists(staged_path):
#             print(f"Error : file not found at {staged_path}")
#             print("Return the transform_iris.py")
#             return 
#         try:
#             supabase=get_supabase_client()
#             df=pd.read_csv(staged_path)
#             total_rows=len(df)
#             batch_size=50
#             print(f"loading {total_rows} rows into '{table_name}'..")
#             for i in range (0,total_rows,batch_size):
#                 batch=df.iloc[i:i+batch_size].copy
#                 batch = batch.where(pd.notnull(batch), None)
#                 records=batch.to_dict("records")
#                 try:
#                    response = supabase.table(table_name).insert(records).execute()
#                    end = min(i + batch_size, total_rows)
#                    print(f"Inserted rows {i + 1} – {end} of {total_rows}")
#                 except Exception as e:
#                    print(f"Error in batch {i // batch_size + 1}: {str(e)}")
#                    continue
#                 print(f"Finished loading iris data into '{table_name}'")
#         except Exception as e:
#             print(f"Error loading data:{e}")
        







# if __name__ == "__main__":
 
#     staged_csv_path = os.path.join("..", "data", "staged", "iris_transformed.csv")
 
    
#     load_to_supabase(staged_csv_path)


import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
 
# Initialize Supabase Client
def get_supabase_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Missing Supabase URL or Supabase KEY in .env")
    return create_client(url, key)
 
def load_to_supabase(staged_path: str, table_name: str = "iris_data"):
 
    if not os.path.isabs(staged_path):
        base_dir = os.path.dirname(__file__)
        staged_path = os.path.abspath(os.path.join(base_dir, staged_path))
 
    print(f"Looking for the data file at: {staged_path}")
    if not os.path.exists(staged_path):
        print(f"Error: file not found at: {staged_path}")
        print("Run transform_iris.py first to generate iris_transformed.csv")
        return
 
    try:
        supabase = get_supabase_client()
 
        df = pd.read_csv(staged_path)
 
        total_rows = len(df)
        batch_size = 50
        print(f"Loading {total_rows} rows into '{table_name}'")
 
        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i:i + batch_size].copy()
 
            batch = batch.where(pd.notnull(batch), None)
 
            records = batch.to_dict("records")
 
            try:
                response = supabase.table(table_name).insert(records).execute()
                end = min(i + batch_size, total_rows)
                print(f"Inserted rows {i + 1} – {end} of {total_rows}")
            except Exception as e:
                print(f"Error in batch {i // batch_size + 1}: {str(e)}")
                continue
 
        print(f"Finished loading Iris dataset into '{table_name}'")
 
    except Exception as e:
        print(f"Error loading data: {e}")
 
if __name__ == "__main__":
    staged_csv_path = os.path.join("..", "data", "staged", "iris_transformed.csv")
    load_to_supabase(staged_csv_path)