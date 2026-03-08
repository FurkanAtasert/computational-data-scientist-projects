from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM
import sqlite3
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import requests

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Start JVM for Zemberek
ZEMBEREK_PATH = '\\zemberek-nlp-master'
startJVM(getDefaultJVMPath(), "-ea", f"-Djava.class.path={ZEMBEREK_PATH}")

# Load Java classes
TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
TurkishTokenizer = JClass('zemberek.tokenization.TurkishTokenizer')

# Create SQLite database
conn = sqlite3.connect('kose_yazi_veritabani.db')
cursor = conn.cursor()

# Create the opinion articles table
cursor.execute('''CREATE TABLE IF NOT EXISTS kose_yazilari
                (yazar TEXT, metin TEXT)''')

# Insert sample opinion articles into the database
kose_yazilari = [
    ("Yılmaz Özdil", "Türkiye’nin Geleceği: Demokrasi ve Eğitim..."),
    ("Emin Çölaşan", "Bürokrasideki Saçma Sapan Atamalar..."),
    ("Hıncal Uluç", "Futbolun Günahları ve Kutsallıkları..."),
    ("Ahmet Altan", "Özgürlük ve Adalet Arayışı..."),
    ("Fatih Altaylı", "Türkiye’nin Dış Politikası ve Geleceği...")
]

cursor.executemany('INSERT INTO kose_yazilari VALUES (?, ?)', kose_yazilari)

# Save changes
conn.commit()

# Close the database
conn.close()

# Shut down the JVM for Zemberek
shutdownJVM()