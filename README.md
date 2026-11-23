# AIS Association Rule Mining — Groceries Dataset

Implementasi algoritma **AIS (Agrawal, Imielinski, Swami)** klasik dari nol menggunakan Python untuk menemukan *frequent itemset* dan *association rules* pada data transaksi belanja bahan makanan. Proyek ini juga memuat eksperimen pengaruh nilai *minimum support* dan *minimum confidence* terhadap jumlah itemset dan rules yang dihasilkan.

## Fitur

- Implementasi AIS tanpa library data mining (hanya `pandas` untuk pengolahan data)
- Preprocessing: konversi tanggal, penghapusan duplikasi produk, dan pembentukan transaksi
- Pembentukan association rules dengan metrik **support**, **confidence**, dan **lift**
- Eksperimen otomatis pada berbagai kombinasi *minimum support* dan *confidence*
- Ringkasan jumlah kandidat dan frequent itemset di setiap level

## Struktur Repository

```
.
├── ais_association_rules.py   # Program utama
├── Groceries_dataset.csv      # Dataset transaksi
├── requirements.txt
└── README.md
```

## Dataset

File `Groceries_dataset.csv` harus berada di direktori yang sama dengan program dan memiliki kolom berikut:

| Kolom             | Deskripsi                                   |
|-------------------|---------------------------------------------|
| `Member_number`   | ID anggota/pelanggan                        |
| `Date`            | Tanggal transaksi (format `dd-mm-YYYY`)     |
| `itemDescription` | Nama produk yang dibeli                     |

Satu **transaksi** didefinisikan sebagai kombinasi unik `Member_number` + `Date`, dan seluruh produk di dalamnya membentuk satu himpunan item (*itemset*).

## Instalasi

```bash
git clone https://github.com/<username>/<nama-repository>.git
cd <nama-repository>

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Isi `requirements.txt`:

```
pandas
```

## Cara Menjalankan

```bash
python ais_association_rules.py
```

Program akan menjalankan eksperimen untuk setiap nilai *minimum support* lalu menampilkan ringkasan dan 10 rules teratas berdasarkan confidence.

## Konfigurasi

Parameter eksperimen dapat diubah pada konstanta di bagian atas file:

| Konstanta           | Default                      | Keterangan                                |
|---------------------|------------------------------|-------------------------------------------|
| `DATASET_PATH`      | `Groceries_dataset.csv`      | Lokasi file dataset                       |
| `DATE_FORMAT`       | `%d-%m-%Y`                   | Format tanggal pada dataset               |
| `SUPPORT_VALUES`    | `[0.005, 0.01, 0.02, 0.03]`  | Nilai minimum support yang diuji          |
| `CONFIDENCE_VALUES` | `[0.05, 0.10, 0.15, 0.20]`   | Ambang confidence untuk menghitung rules  |
| `TOP_N_RULES`       | `10`                         | Jumlah rules teratas yang ditampilkan     |

## Cara Kerja

### 1. Preprocessing
1. Kolom `Date` dikonversi ke tipe datetime.
2. Duplikasi produk pada transaksi yang sama dihapus.
3. Data dikelompokkan per `Member_number` dan `Date` menjadi daftar transaksi.

### 2. Algoritma AIS
1. Hitung support setiap item dan ambil **frequent 1-itemset** (count ≥ `ceil(min_support × jumlah transaksi)`).
2. Untuk setiap transaksi, perluas frequent itemset yang terkandung di dalamnya dengan item lain pada transaksi yang sama untuk membentuk **kandidat** `k+1`.
3. Hitung support kandidat (maksimal satu kali per transaksi), lalu pertahankan yang memenuhi minimum support.
4. Ulangi hingga tidak ada kandidat atau frequent itemset baru.

> **Catatan:** AIS membangkitkan kandidat dari isi transaksi, sehingga jumlah kandidatnya cenderung jauh lebih besar dibanding Apriori yang memangkas kandidat dengan sifat *anti-monotone*.

### 3. Pembentukan Rules
Untuk setiap frequent itemset berukuran ≥ 2, setiap item bergantian menjadi **konsekuen** (satu item) dan sisanya menjadi **antecedent**.

| Metrik         | Rumus                                         |
|----------------|-----------------------------------------------|
| **Support**    | `count(A ∪ B) / N`                            |
| **Confidence** | `count(A ∪ B) / count(A)`                     |
| **Lift**       | `confidence / (count(B) / N)`                 |

Keterangan: `A` = antecedent, `B` = consequent, `N` = jumlah transaksi.

## Contoh Output

```
Minimum Support: 0.01
Minimum Count: <jumlah>
Frequent Itemsets: {1: <n>, 2: <n>}
Candidates: {2: <n>}
Confidence: 0.05 | Jumlah Rules: <n>
...

Top Association Rules:
antecedent  consequent  support  confidence  lift
...
```

Nilai aktual bergantung pada dataset dan parameter yang digunakan.

## Keterbatasan

- Pada *minimum support* rendah (misalnya 0.005), jumlah kandidat dan waktu komputasi dapat meningkat tajam.
- Rules yang dibentuk hanya memiliki **satu item pada konsekuen**.
- Tidak ada pemangkasan kandidat sehingga kurang efisien untuk dataset besar.

## Pengembangan Selanjutnya

- Perbandingan performa dengan Apriori dan FP-Growth
- Ekspor hasil rules ke CSV
- Antarmuka argumen CLI untuk parameter eksperimen

## Lisensi

Tentukan lisensi proyek ini (misalnya MIT) dengan menambahkan file `LICENSE`.