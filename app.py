from flask import Flask, render_template, send_from_directory, request,session,redirect,url_for
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection setup
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection
def load_data():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Define the product table schema
    product_table_schema = """
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            description TEXT,
            price TEXT,
            marka TEXT,
            seri TEXT,
            model TEXT,
            yıl TEXT,
            yakıt TEXT,
            vites TEXT,
            ImageURL TEXT
        )
    """

    # Create the product table if it doesn't exist
    cursor.execute(product_table_schema)
    print("Table created successfully.")

    # Check the count of existing products
    existing_product_count = cursor.execute("SELECT COUNT(*) FROM product").fetchone()[0]

    # Only insert data if there are no existing products
    if existing_product_count == 0:
        # Insert data into the product table
        data_to_insert = [
            (1133658850, '2023 Maserati Grecale 2.0 Hybrid Modena 330HP Fer&Mas Bayi Çıkış',
             'Merhaba, Araç 2023 model ve Fer&Mas bayiden sıfır alınmıştır. 18 Ağustos 2023 tarihinde trafiğe çıkışlıdır. '
             '100.000₺ değerinde USA Inozetek - Snow Blue kaplaması İstanbul Kornit Design\'da yaptırılmıştır. '
             'Araç rengi normalde Füme (GRIGIO LAVA)\'dir. Kaza, boya, değişen, hata ve tramer yoktur.',
             '7,250,000 TL', 'Maserati', 'Seri', '2.0 Hybrid Modena', '2023', 'Hybrid', 'Otomatik',
             'https://i0.shbdn.com/photos/65/88/50/thmb_113365885006h.jpg'),
            (1122090164, '2016 MODEL VW PASSAT 2.0 TDİ 190 HP HİGHLİNE HATASIZ 145.000 KM',
            '2016 MODEL VW PASSAT 2.0 TDİ BMT 190 HP HİGHLİNE DSG HATASIZ - KAZASIZ - BOYASIZ TRAMER KAYDI YOK '
            'KM : ORJ 145.000 MUAYENE TARİHİ : 29.05.2025 ŞASE NO : WVWZZZ3CZHE116942​ HAYALET EKRAN F1 VİTES '
            'ELEKTRİKLİ ÖN KOLTUKLAR ISITMALI ÖN KOLTUKLAR KOLTUK HAFIZA KOLTUK MASAJI DERİ SİYAH KOLTUK AHŞAP İÇ TRİMLER '
            'YAĞMUR SENSÖRÜ FAR SENSÖRÜ Bİ-XENON FAR VS....',
            '1.553.000 TL', 'Volkswagen', 'Passat', '2.0 TDI BlueMotion Highline', '2016', 'Dizel', 'Otomatik',
            'https://i0.shbdn.com/photos/09/01/64/thmb_1122090164b5w.jpg'),
            (1142432345, '!!ACİLL SAHİBİNDEN HATASIZ AUDİ/A3/1.6 TDİ/LİMOUSİNE CAM TAVAN!!',
            'SAĞ İKİ KAPİ VE ARKA ÇAMURLUK LOKAL BOYALİ HARİCİ HATASİZ BOYASİZDİR. '
            'BÜTÜN AĞİR BAKIMLARI YAPILMIŞTIR UZUN YILLARCA KULLANİLABİLECEK AİLE ARACIDIR.',
            '985.000 TL', 'Audi', 'A3', 'A3 Sedan 1.6 TDI Limousine', '2014', 'Dizel', 'Otomatik',
            'https://i0.shbdn.com/photos/43/23/45/thmb_1142432345r73.jpg'),
            (1122770591, 'KÖSE MOTORS\'dan hatasız boyasız emalsiz temizlikte',
            'KÖSE MOTORS’dan 2017 MODEL BMW 3.18İ PREMIUM LINE 142.000KM\'DE SEDEFLİ BEYAZ '
            '4 FARKLI SÜRÜŞ MODU GERİ GÖRÜŞ KAMERASI HIZ SABİTLEYİCİ ŞERİT TAKİP ÇARPIŞMA '
            'ÖNLEYİCİ CRUISE CONTROL SUNROOF', '1.330.000 TL', 'BMW', '3 Serisi',
            '318i Premium Line', '2017', 'Benzin', 'Otomatik',
            'https://i0.shbdn.com/photos/77/05/91/thmb_1122770591mke.jpg'),
            (1121070772, 'TAKAS OLUR MERCEDES 2015 AMG A 180 DIZEL CAM TAVANLI TERTEMİZ',
            'ARACIM 2015 AMG A 180 OTOMATİK DIZEL Aracın içi dışı tertemizdir.',
            '1.069.000 TL', 'Mercedes-Benz', 'A Serisi',
            'A 180 CDI BlueEfficiency AMG', '2015', 'Dizel', 'Otomatik',
            'https://i0.shbdn.com/photos/07/07/72/thmb_1121070772wlt.jpg'),
            (1139066003, 'Mercedes Benz C118 CLA 45 AMG S 4MATIC MASLAK MODERN OTO ÇIKIŞLI',
            'AMG CLA 45 S 71200 KM SORUNSUZ ÜSTÜN PERFORMANS DİKKAT ÇEKİCİ RENK',
            '3.650.000 TL', 'Mercedes-Benz', 'CLA', '45 S AMG', '2020', 'Benzin', 'Otomatik',
            'https://i0.shbdn.com/photos/06/60/03/thmb_1139066003384.jpg'),
            (1142969895, 'MERCEDES GLS 350 4 MATİC AMG BAYİ ÇIKIŞLI',
            'TRAMER KAYDI YOKTUR. PARK HALINDE CARPMA SONUCU KAPUT BOYALI VE CAMURLUK 1 KARIS LOKAL BOYALI.',
            '6.850.000 TL', 'Mercedes-Benz', 'GLS', '350 D', '2016', 'Dizel', 'Otomatik',
            'https://i0.shbdn.com/photos/96/98/95/thmb_1142969895l5n.jpg'),
            (1135144744, 'Emsalsiz - M4 Dönüşüm - Verde Ermes',
            'ARACIM PROFESYONEL BİR ŞEKİLDE MOTOR YÜRÜYEN HARİÇ M4 DÖNÜŞTÜRÜLMÜŞTÜR. TÜM PARÇALAR ORJİNAL OLUP TÜM PARÇALARIN FATURALARI MEVCUTTUR',
            '2.450.000 TL', 'BMW', '4 Serisi', '428i M Sport', '2015', 'Benzin', 'Otomatik',
            'https://i0.shbdn.com/photos/14/47/44/thmb_11351447448h7.jpg'),
            (1137329390, 'mustang mach-E premium extended 360 kamera+bang&olufsen',
            'Araçta çizik dahi yok. Premium paket.Değişensiz boyasız hatasız extradan 2.000$ en iyi ithal şeffaf kaplamadan yapıldı.araç türkçe yazılımlı',
            '3.500.000 TL', 'Ford', 'Mustang Mach-E', 'Extended', '2021', 'Elektrik', 'Otomatik',
            'https://i0.shbdn.com/photos/32/93/90/thmb_1137329390fyk.jpg'),
            (1143557491, 'BARBARUS MOTORS\'DAN 2023 BMW M SPORT 50. M235İ XDRİVE 7 BİN KM',
            'AVANTAJLI KREDİ İMKANLARI İÇİN LÜTFEN İLETİŞİME GEÇİNİZ.',
            '2.750.000 TL', 'BMW', 'M Serisi', 'M235i xDrive', '2023', 'Benzin', 'Otomatik',
            'https://i0.shbdn.com/photos/55/74/91/thmb_1143557491gur.jpg')

        ]
        cursor.executemany("""
            INSERT INTO product (
                id, product_name, description, price, marka, seri, model, yıl, yakıt, vites, ImageURL
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data_to_insert)
        connection.commit()
        print("Data inserted successfully.")
    else:
        print("Data already exists in the product table.")

    connection.close()

# Run the load_data function
load_data()


# Route for the index page
@app.route('/')
def index():
    connection = get_db_connection()
    # Fetch products ordered by ID (you can change this based on your requirements)
    product = connection.execute("SELECT * FROM product ORDER BY id").fetchall()
    print("Product count:", len(product))  # Add this line for debugging
    connection.close()

    # Initialize an empty list in the session if it doesn't exist
    if 'product_list' not in session:
        session['product_list'] = []

    return render_template('index.html', product=product)

@app.route('/product/<int:id>/product_detail')
@app.route('/product/<int:id>')
def product_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    product = cursor.execute("SELECT * FROM product WHERE id = ?", (id,)).fetchone()
    connection.close()
    return render_template('product_detail.html', product=product)


...



@app.route('/search', methods=['GET', 'POST'])
def search():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        search_term = request.form.get('search_term', '')

        # Define the SQL query for searching
        sql_query = """
            SELECT * FROM product 
            WHERE product_name LIKE ? OR description LIKE ?
               OR marka LIKE ? OR seri LIKE ? OR model LIKE ? OR yıl LIKE ? 
               OR yakıt LIKE ? OR vites LIKE ?
        """

        # Use the '%' wildcard to search for partial matches
        search_results = cursor.execute(sql_query, (
            f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%",
            f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"
        )).fetchall()

        # Arama sonuçları kontrolü
        search_message = "Aranan ürün bulunamadı." if not search_results else ""

        if len(search_results) == 1:
            # If there is only one result, redirect to the product detail page
            connection.close()
            return redirect(url_for('product_detail', id=search_results[0]['id']))

    else:
        # Varsayılan olarak tüm ürünleri göster
        cursor.execute("SELECT * FROM product")
        search_results = cursor.fetchall()
        search_term = ''
        search_message = ""

    # Bağlantıyı kapatmayı template'e veriyi gönderdikten sonra yap
    connection.close()

    return render_template('search.html', product=search_results, search_term=search_term, search_message=search_message)






...




if __name__ == '__main__':
    app.run(debug=True)
