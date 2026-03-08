import sqlite3

# Create SQLite database
conn = sqlite3.connect('author_articles.db')
cursor = conn.cursor()

# Create the opinion articles table
cursor.execute('''CREATE TABLE IF NOT EXISTS author_articles
                (yazar TEXT, metin TEXT)''')

# Insert sample opinion articles into the database
author_articles = [
    ("Yılmaz Özdil", "Türkiye’nin Geleceği: Demokrasi ve Eğitim” Değerli okurlar, bugün sizlere Türkiye’nin geleceği hakkında düşüncelerimi paylaşmak istiyorum. Demokrasi ve eğitim, ülkemizin temel taşlarıdır. Ancak son yıllarda bu alanlarda yaşanan sorunlar, geleceğimizi tehdit ediyor. Demokrasimizi güçlendirmeli, eğitim sistemimizi yeniden yapılandırmalıyız. Unutmayalım ki, geleceğimiz bugünkü kararlarımızla şekilleniyor."),
    ("Emin Çölaşan", "Bürokrasideki Saçma Sapan Atamalar” Sevgili okurlar, son günlerde bürokraside yaşanan atamaları gözlemliyorum ve şaşkınlığımı gizleyemiyorum. Hangi kriterlere göre bu atamalar yapılıyor, anlamak gerçekten zor. Saçma sapan atamaların ülkeye ne gibi zararlar verdiğini düşünmek bile istemiyorum."),
    ("Hıncal Uluç", "Futbolun Günahları ve Kutsallıkları” Sayın okurlar, futbolun toplum üzerindeki etkisi büyüktür. Hem günahları hem de kutsallıkları vardır. Kulüpler, taraftarlar, yöneticiler, futbolcular… Her biri bu büyük oyunun parçasıdır. Ancak bazen bu kutsal oyunun içinde yaşanan günahları görmemiz gerekiyor."),
    ("Ahmet Altan", "Özgürlük ve Adalet Arayışı” Değerli okuyucular, özgürlük ve adalet, insan haklarının temelidir. Ülkemizde bu değerlere olan inancımızı kaybetmemeliyiz. Adaletin sağlanması için hep birlikte mücadele etmeliyiz. Unutmayalım ki, özgürlük ve adalet olmadan bir toplum ilerleyemez."),
    ("Fatih Altaylı", "Türkiye’nin Dış Politikası ve Geleceği” Sayın okurlar, Türkiye’nin dış politikası son yıllarda önemli değişiklikler geçirdi. Gelecekte bu politikanın nasıl şekilleneceği, ülkemizin uluslararası ilişkileri açısından kritik bir konudur. Diplomasi ve strateji, geleceğimizi belirleyen unsurlardır.")
]

cursor.executemany('INSERT INTO author_articles VALUES (?, ?)', author_articles)

# Save changes
conn.commit()

# Close the database
conn.close()