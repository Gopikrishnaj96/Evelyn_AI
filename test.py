import sqlite3
import speech_recognition as sr
from ui import get_user_correction  # ✅ Import UI correction prompt

# ✅ Initialize SQLite Database
conn = sqlite3.connect("corrections.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ Create Corrections Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS corrections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_text TEXT UNIQUE,
        corrected_text TEXT,
        count INTEGER DEFAULT 1,
        last_corrected TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# ✅ Create or Verify the Accuracy Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accuracy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_attempts INTEGER DEFAULT 0,
        correct_attempts INTEGER DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# ✅ Ensure there is at least one entry in the accuracy table
cursor.execute("SELECT * FROM accuracy")
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO accuracy (total_attempts, correct_attempts) VALUES (0, 0)")
conn.commit()

# ✅ Log the current tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

def update_corrections(original, corrected):
    """Store user corrections in the database and ensure they are committed."""
    conn = sqlite3.connect("corrections.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT count FROM corrections WHERE original_text=?", (original,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE corrections 
            SET corrected_text=?, count=count+1, last_corrected=CURRENT_TIMESTAMP 
            WHERE original_text=?""",
            (corrected, original)
        )
    else:
        cursor.execute("""
            INSERT INTO corrections (original_text, corrected_text, count, last_corrected) 
            VALUES (?, ?, 1, CURRENT_TIMESTAMP)""", 
            (original, corrected)
        )
    
    conn.commit()
    conn.close()

def get_boosted_phrases():
    """Retrieve frequently corrected words for boosting accuracy."""
    conn = sqlite3.connect("corrections.db", check_same_thread=False)
    cursor = conn.cursor()

    # ✅ Fetch phrases corrected more than twice
    cursor.execute("SELECT corrected_text FROM corrections WHERE count > 2")
    boosted_words = [row[0] for row in cursor.fetchall()]

    conn.close()
    return boosted_words

def update_accuracy(is_correct):
    """Update accuracy metrics in the database."""
    conn = sqlite3.connect("corrections.db", check_same_thread=False)
    cursor = conn.cursor()

    # Increment total attempts
    cursor.execute("UPDATE accuracy SET total_attempts = total_attempts + 1")

    # Increment correct attempts if the recognition was correct
    if is_correct:
        cursor.execute("UPDATE accuracy SET correct_attempts = correct_attempts + 1")

    # Update timestamp
    cursor.execute("UPDATE accuracy SET last_updated = CURRENT_TIMESTAMP")
    conn.commit()
    conn.close()

def get_accuracy():
    """Fetch and calculate the accuracy of speech recognition."""
    conn = sqlite3.connect("corrections.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT total_attempts, correct_attempts FROM accuracy")
    result = cursor.fetchone()
    conn.close()

    if result:
        total_attempts, correct_attempts = result
        if total_attempts == 0:
            return 0.0  # Avoid division by zero
        accuracy = (correct_attempts / total_attempts) * 100
        return round(accuracy, 2)
    return 0.0

def takecommand():
    """Capture voice input, boost accuracy using adapted words, and adapt dynamically."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        # Increase listening duration by setting a longer timeout and phrase time limit
        audio = r.listen(source, timeout=15, phrase_time_limit=30)

    try:
        print("Recognizing...")
        boosted_phrases = get_boosted_phrases()  # ✅ Fetch frequent corrections

        # ✅ Use Google STT for recognition
        query = r.recognize_google(audio, language='en-in')

        print(f"User said: {query}")

        # ✅ Check if the phrase matches boosted corrections
        if query in boosted_phrases:
            print(f"Boosted phrase detected: {query}")
            update_accuracy(is_correct=True)  # Recognition is correct
            return query.lower()

        # ✅ Ask for correction for non-boosted phrases
        correction = get_user_correction(query)

        if correction and correction.lower() != "yes":
            update_corrections(query, correction)  # Save corrected phrase
            update_accuracy(is_correct=False)  # Recognition required correction
            query = correction.lower()
        else:
            update_accuracy(is_correct=True)  # Recognition was correct

        return query.lower()

    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
    while True:
        command = takecommand()
        if command == "exit":
            break

        # Display the current accuracy after each command

        accuracy = get_accuracy()
        print(f"Current Accuracy: {accuracy}%")
