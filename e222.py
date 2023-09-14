import sqlite3
import pandas as pd

# Read the file and copy content to a list
df = pd.read_csv('stephen_king_adaptations.txt', header=None, names=['movieID', 'movieName', 'movieYear', 'imdbRating'])
stephen_king_adaptations_list = df.values.tolist()

# Establish SQLite connection and create table
conn = sqlite3.connect('stephen_king_adaptations_pandas.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
             (movieID TEXT, movieName TEXT, movieYear INTEGER, imdbRating REAL)''')
conn.commit()

# Insert data into table
df.to_sql('stephen_king_adaptations_table', conn, if_exists='replace', index=False)

# Function to handle user input and perform searches
def main_loop():
    while True:
        print("\nOptions:")
        print("1. Search by movie name")
        print("2. Search by movie year")
        print("3. Search by movie rating")
        print("4. STOP")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter the name of the movie: ")
            query = f"SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE '%{name}%'"
        elif choice == '2':
            year = int(input("Enter the year of the movie: "))
            query = f"SELECT * FROM stephen_king_adaptations_table WHERE movieYear = {year}"
        elif choice == '3':
            rating = float(input("Enter the minimum rating of the movie: "))
            query = f"SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= {rating}"
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")
            continue
        
        df_query = pd.read_sql_query(query, conn)
        
        if df_query.empty:
            print("No matching records found.")
        else:
            print(df_query)

if __name__ == "__main__":
    main_loop()
