-- Membuat database jika belum ada
CREATE DATABASE IF NOT EXISTS company_directory;

-- Menggunakan database yang baru dibuat
USE company_directory;

-- Membuat tabel companies
CREATE TABLE IF NOT EXISTS companies (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    NameCompany VARCHAR(100),
    NoReg VARCHAR(20),
    Product VARCHAR(50),
    Address VARCHAR(100),
    PostCode VARCHAR(10),
    Email VARCHAR(100),
    UniqCode VARCHAR(4) UNIQUE
);



# Insert company data
INSERT INTO companies (NameCompany, NoReg, Product, Address, PostCode, Email, UniqCode) VALUES
('PT Bunga Mawar', '673657', 'Ikan Sarden', 'Jl Perning No 30', '61352', 'bunga_mawar@bm.co.id', 'A32K'),
('PT Berkah Indah', '463930', 'Minyak Goreng', 'Jl Rungkut No 79', '61385', 'berkah_indah@bi.co.id', 'B15G'),
('PT Sinar Terang', '373910', 'Susu Bubuk', 'Jl Ponokawan No 78', '68271', 'sinar_terang@st.co.id', 'R19U'),
('PT Bulan Bintang', '648201', 'Minyak Sawit', 'Jl Besuk No 56', '67371', 'bulan_bintang@bb.co.id', 'P19R'),
('PT Makmur Sejahtera', '492271', 'Udang Beku', 'Jl Tlogosari No 56', '67372', 'makmur_sejahtera@ms.co.id', 'G10B'),
('PT Kurnia Indah', '749104', 'Pengolahan Rumput Laut', 'Jl Kandangan No 78', '67361', 'kurnia_indah@ki.co.id', 'T67X'),
('PT Bangun Rajasa', '631936', 'Terasi Udang', 'Jl Tirta No 67', '64181', 'bangun_rajasa@br.co.id', 'K63L'),
('PT Kawah Mas', '361978', 'Ikan Teri Kering', 'Jl Subur No 89', '64153', 'kawah_mas@km.co.id', 'N96K'),
('PT Indah Caria', '173736', 'Tahu', 'Jl Kawi No 23', '62275', 'indah_ceria@ic.co.id', 'C16Y'),
('PT Karya Husada', '519136', 'Selai', 'Jl Sampung no 45', '59153', 'karya_husada@kh.co.id', 'B18V');

# Verify data insertion
SELECT * FROM companies;
