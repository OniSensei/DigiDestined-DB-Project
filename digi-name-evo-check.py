import sqlite3

# Connect to the digimon database
conn = sqlite3.connect('digimon.db')
c = conn.cursor()

# Retrieve digimon records with event 'none' and non-null evolutions
c.execute("SELECT * FROM digi WHERE Event = 'None' AND Evolutions != 'None'")
digimon_records = c.fetchall()

discrepancy_found = False  # Flag to track if any spelling discrepancy is found

# Iterate over the digimon records
for record in digimon_records:
    name = record[1]
    evolutions = record[13]
    
    # Split the evolutions column into individual evolution names
    evolution_names = evolutions.split(',')
    
    for evolution_name in evolution_names:
        evolution_name = evolution_name.strip()  # Remove leading/trailing whitespace
        
        # Check spelling similarity of evolution name with the digimon names (excluding current digimon)
        c.execute("SELECT Name FROM digi WHERE Name != ? AND Name = ?", (name, evolution_name))
        matching_names = c.fetchall()
        
        if not matching_names:
            discrepancy_found = True
            print(f"Spelling issue detected: {name} -> {evolution_name}")

# Print "no issues found" message if no discrepancies are found
if not discrepancy_found:
    print("No spelling issues found.")

# Close the database connection
conn.close()
