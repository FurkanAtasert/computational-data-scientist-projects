from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import sqlite3
from preprocess_text import preprocess_text
from jpype import getDefaultJVMPath, startJVM, shutdownJVM, JClass, JString

# Start the Java Virtual Machine
startJVM(getDefaultJVMPath(), "-ea", f"-Djava.class.path=\\zemberek-nlp-master\\morphology\\src\\test\\java\\zemberek\\morphology\\TurkishMorphologyFunctionalTests.java")

# Connect to the SQLite database
conn = sqlite3.connect('author_articles.db')
cursor = conn.cursor()

# Retrieve opinion columns from the database
cursor.execute("SELECT yazar, metin FROM author_articles")
kose_yazilari = cursor.fetchall()

# Preprocess the opinion columns
preprocessed_texts = [(yazar, preprocess_text(metin)) for yazar, metin in kose_yazilari]

# Close the database connection
conn.close()

# Shut down the Java Virtual Machine
shutdownJVM()

# Separate data and labels
authors, texts = zip(*preprocessed_texts)

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Create the classification model
clf = MultinomialNB()
clf.fit(X, authors)

# Predict the author of an unknown text
unknown_text = "Bir Gün Her Şey Biter” Değerli okuyucular, hayatın akışı bazen beklenmedik şekilde değişebilir. Bir gün her şey biter, ama bu bitiş aynı zamanda yeni başlangıçlara da kapı aralar. İşte bu yüzden umudu kaybetmemeliyiz. Geleceğe dair umutlarımızı korumalı, yaşadığımız anın değerini bilmeliyiz. İnsanlar arasındaki ilişkiler, anılar ve deneyimler, hayatın gerçek zenginlikleridir. Unutmayalım ki, her gün bir hediye ve bir fırsattır."
preprocessed_unknown_text = preprocess_text(unknown_text)
X_unknown = vectorizer.transform([preprocessed_unknown_text])

predicted_author = clf.predict(X_unknown)[0]
print(f"The text belongs to the author {predicted_author}.")