import mysql.connector

# Fungsi untuk menghubungkan ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",     # Ganti dengan username MySQL Anda
        password="Marklee080",  # Ganti dengan password MySQL Anda
        database="data_company"
    )

def header():
    print("==========================================================================================================================================\n"
          "============================= Direktori Pencarian Perusahaan Industri di Kota Surabaya ==================================\n"
          "==========================================================================================================================================\n")

def main_menu():
    print(""" 
                       ******************** Main Menu *************************
                        ----------------- Nomor Option ------------------------
                        1 = display company-----(Melihat semua data yang sudah tersedia)
                        2 = add company --------(Membuat data baru yang belum tersedia)
                        3 = update company------(Memperbarui data yang sudah tersedia)
                        4 = delete company------(Menghapus data yang sudah tersedia)
                        5 = exit ---------------(Meninggalkan Program)
                      **********************************************************
            """)

def user_input(text, valid_options=None, max_length=None, is_unique_code=False):
    attempts = 0
    while attempts < 3:
        input_value = input(text)
        
        if max_length and len(input_value) > max_length:
            print(f"Input tidak boleh lebih dari {max_length} karakter.")
            attempts += 1
            continue
        
        if is_unique_code and (len(input_value) != 4 or not input_value.isalnum() or not input_value.isupper()):
            print("Kode unik harus 4 karakter, kombinasi huruf kapital dan angka.")
            attempts += 1
            continue

        if valid_options and input_value not in valid_options:
            print("Input tidak valid. Silakan masukkan salah satu dari: ", ', '.join(valid_options))
            attempts += 1
            continue

        return input_value
    
    print("Terlalu banyak percobaan yang salah. Kembali ke menu utama.")
    return None 

def display_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    cursor.close()
    conn.close()

    print("  NameCompany        NoReg         Product                   Address              PostCode            Email                 UniqCode")
    print("=" * 135)

    for company in companies:
        print(f"{company[1]:20} {company[2]:10} {company[3]:25} {company[4]:25} {company[5]:10} {company[6]:30} {company[7]:10}")

def display_company():
    print(""" 
                     ******************** 1. Display Company Menu **********************
                        ----------------- Nomor Option ------------------------
                        1 = Shown All Product Company 
                        2 = Shown All Name Company 
                        3 = Back to Main Menu  
                    ****************************************************************
            """)

    option = user_input("Masukkan nomor option yang ingin anda jalankan: ", ["1", "2", "3"])  
    if option is None:
        return  
    if option == "1":
        display_data()
    elif option == "2":
        company_name = input("Masukkan nama perusahaan yang ingin dicari: ")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies WHERE NameCompany LIKE %s", ('%' + company_name + '%',))
        companies = cursor.fetchall()
        cursor.close()
        conn.close()

        if companies:
            for company in companies:
                print(f"{company[1]:20} {company[2]:10} {company[3]:25} {company[4]:25} {company[5]:10} {company[6]:30} {company[7]:10}")
        else:
            print("Perusahaan tidak ditemukan.")

def manage_company(action):
    uniq_code = user_input(f"Masukkan kode unik perusahaan yang ingin {action}: ", max_length=4, is_unique_code=True)
    if uniq_code is None:
        return 

    conn = connect_db()
    cursor = conn.cursor()

    if action == "create":
        cursor.execute("SELECT * FROM companies WHERE UniqCode = %s", (uniq_code,))
        company = cursor.fetchone()
        if company:
            print("Kode unik sudah ada. Silakan gunakan kode unik lain.")
            return False

        new_company = {
            "NameCompany": user_input("Masukkan nama perusahaan: ", max_length=100),
            "NoReg": user_input("Masukkan nomor registrasi: ", max_length=20),
            "Product": user_input("Masukkan produk: ", max_length=50),
            "Address": user_input("Masukkan alamat: ", max_length=100),
            "PostCode": user_input("Masukkan kode pos: ", max_length=10),
            "Email": user_input("Masukkan email: ", max_length=100),
            "UniqCode": uniq_code
        }
        cursor.execute("INSERT INTO companies (NameCompany, NoReg, Product, Address, PostCode, Email, UniqCode) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (new_company["NameCompany"], new_company["NoReg"], new_company["Product"], new_company["Address"],
                        new_company["PostCode"], new_company["Email"], new_company["UniqCode"]))
        conn.commit()
        print("Data berhasil ditambahkan.")

    elif action == "update":
        cursor.execute("SELECT * FROM companies WHERE UniqCode = %s", (uniq_code,))
        company = cursor.fetchone()
        if company:
            print("Data yang tersedia:")
            for key, value in zip(["NameCompany", "NoReg", "Product", "Address", "PostCode", "Email"], company[1:]):
                print(f"  {key}: {value}")

            if user_input(f"Apakah anda ingin melanjutkan update data? (1.Ya / 2.Tidak): ", ["1", "2"]) == "1":
                updates = {
                    "NameCompany": user_input("Masukkan nama perusahaan baru (tekan Enter untuk tetap): ", max_length=100),
                    "NoReg": user_input("Masukkan nomor registrasi baru (tekan Enter untuk tetap): ", max_length=20),
                    "Product": user_input("Masukkan produk baru (tekan Enter untuk tetap): ", max_length=50),
                    "Address": user_input("Masukkan alamat baru (tekan Enter untuk tetap): ", max_length=100),
                    "PostCode": user_input("Masukkan kode pos baru (tekan Enter untuk tetap): ", max_length=10),
                    "Email": user_input("Masukkan email baru (tekan Enter untuk tetap): ", max_length=100),
                }
                cursor.execute("""
                    UPDATE companies 
                    SET NameCompany = COALESCE(NULLIF(%s, ''), NameCompany),
                        NoReg = COALESCE(NULLIF(%s, ''), NoReg),
                        Product = COALESCE(NULLIF(%s, ''), Product),
                        Address = COALESCE(NULLIF(%s, ''), Address),
                        PostCode = COALESCE(NULLIF(%s, ''), PostCode),
                        Email = COALESCE(NULLIF(%s, ''), Email)
                    WHERE UniqCode = %s
                """, (updates["NameCompany"], updates["NoReg"], updates["Product"], updates["Address"], updates["PostCode"], updates["Email"], uniq_code))
                conn.commit()
                print("Data berhasil diupdate.")
        else:
            print("Data tidak ditemukan dengan kode unik tersebut.")

    elif action == "delete":
        cursor.execute("SELECT * FROM companies WHERE UniqCode = %s", (uniq_code,))
        company = cursor.fetchone()
        if company:
            print("Data yang akan dihapus:")
            for key, value in zip(["NameCompany", "NoReg", "Product", "Address", "PostCode", "Email"], company[1:]):
                print(f"  {key}: {value}")

            if user_input("Apakah anda ingin menghapus data ini? (1.Ya / 2.Tidak): ", ["1", "2"]) == "1":
                cursor.execute("DELETE FROM companies WHERE UniqCode = %s", (uniq_code,))
                conn.commit()
                print("Data berhasil dihapus.")
        else:
            print("Data tidak ditemukan dengan kode unik tersebut.")

    cursor.close()
    conn.close()

# Loop utama program
header()
while True:
    main_menu()
    option = user_input("Masukkan nomor option yang ingin anda jalankan: ", ["1", "2", "3", "4", "5"])
    
    if option is None:
        continue 
    if option == "1":
        display_company()  
    elif option == "2":
        manage_company("create")
    elif option == "3":
        manage_company("update")
    elif option == "4":
        manage_company("delete")
    elif option == "5":
        print("Anda akan keluar dari program.")
        break
