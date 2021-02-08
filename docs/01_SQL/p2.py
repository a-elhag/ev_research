## Part 0: Initializing
import io
import numpy as np
import sqlite3

## Part 1: BoilerPlate NumPy
# Converts np.array to TEXT when inserting
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())          

sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
def convert_array(text):                   
    out = io.BytesIO(text)                       
    out.seek(0)                                  
    return np.load(out)                          

sqlite3.register_converter("array", convert_array)

## Part 2: Opening Database
conn = sqlite3.connect("P2.db",
                            detect_types=sqlite3.PARSE_DECLTYPES)

cursor = conn.cursor()

## Part 3: Creating a Table
cursor.execute("""CREATE TABLE IF NOT EXISTS data (arr ARRAY);""")

## Part 4: Inserting Arrays
x = np.random.rand(10)
cursor.execute("INSERT INTO data (arr) values (?)", (x, ))

## Part 5: Commiting
conn.commit()


## Part 6: Select
cursor.execute(f"SELECT id, arr FROM data LIMIT 2")
data = cursor.fetchall()
data
