from tabulate import tabulate
from db import get_connection
import mysql.connector
import hashlib

def kembali():
    input("\nTekan ENTER untuk kembali...")

def cari_karyawan(nip):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM employees WHERE nip = %s"
    cursor.execute(query, (nip,))
    emp = cursor.fetchone()

    conn.close()
    return emp

def login():
    while True:
        print("\n===== LOGIN =====")
        user_id = input("User ID : ").strip()
        password = input("Password: ").strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM accounts WHERE user_id = %s",
            (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            print("User tidak ditemukan")
            conn.close()
            continue

        if user["status"] != "approved":
            print("Account belum di-approve oleh Super Admin.")
            conn.close()
            continue

        if user["blocked"] == 1:
            print("Account anda terblokir.")
            conn.close()
            continue

        if password == user["password"]:
            cursor.execute("""
                UPDATE accounts
                SET fail = 0
                WHERE user_id = %s
            """, (user_id,))
            conn.commit()
            conn.close()

            print("Login berhasil.")
            return user["user_id"], user["role"]

        else:
            fail_count = user["fail"] + 1
            blocked_status = 1 if fail_count >= 3 else 0

            cursor.execute("""
                UPDATE accounts
                SET fail = %s,
                    blocked = %s
                WHERE user_id = %s
            """, (fail_count, blocked_status, user_id))

            conn.commit()

            print("Password salah!")

            if blocked_status:
                print("Account anda terblokir karena 3x gagal login.")

            conn.close()

def lihat_data_karyawan():
    print("DATA KARYAWAN")
    keyword = input("Cari berdasarkan NIP / Nama (kosongkan untuk semua): ").strip().lower()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if keyword == "":
        query = "SELECT nip, nama, ttl, hp, departemen FROM employees"
        cursor.execute(query)
    else:
        query = """
            SELECT nip, nama, ttl, hp, departemen 
            FROM employees
            WHERE LOWER(nip) LIKE %s OR LOWER(nama) LIKE %s
        """
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword))

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Data tidak ditemukan")
        kembali()
        return

    rows = []
    for e in data:
        rows.append([
            e["nip"],
            e["nama"],
            e["ttl"],
            e["hp"],
            e["departemen"]
        ])

    print(tabulate(
        rows,
        headers=["NIP", "Nama", "TTL", "HP", "Departemen"],
        tablefmt="simple_grid"
    ))

    kembali()

def lihat_pangkat_gaji():
    nip = input("Masukkan NIP: ")
    emp = cari_karyawan(nip)

    if emp:
        rows = [[
            emp["nip"],
            emp["nama"],
            emp["pangkat"],
            f"Rp {emp['gaji']:,}"
        ]]

        print(tabulate(
            rows,
            headers=["NIP", "Nama", "Pangkat", "Gaji"],
            tablefmt="simple_grid"
        ))
    else:
        print("Data tidak ditemukan")

    kembali()

def tambah_karyawan():
    print("TAMBAH KARYAWAN")

    nip = input("Masukkan NIP: ").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT nip FROM employees WHERE nip = %s", (nip,))
    existing = cursor.fetchone()

    if existing:
        print("NIP sudah terdaftar! Tidak bisa duplicate.")
        conn.close()
        kembali()
        return

    print("NIP tersedia. Silakan isi biodata.\n")

    nama = input("Nama: ")
    ttl = input("TTL: ")
    alamat_ktp = input("Alamat KTP: ")
    alamat_tinggal = input("Alamat Tinggal: ")
    hp = input("No HP: ")
    rumah = input("No Rumah: ")
    emergency = input("Emergency Contact: ")
    riwayat = input("Riwayat Kerja: ")
    pangkat = input("Pangkat: ")
    gaji = int(input("Gaji: "))
    departemen = input("Departemen: ")

    confirm = input("Yakin tambah data? (Y/N): ").upper()

    if confirm == "Y":
        query = """
            INSERT INTO employees
            (nip, nama, ttl, alamat_ktp, alamat_tinggal, hp, rumah,
             emergency, riwayat, pangkat, gaji, departemen)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            nip, nama, ttl, alamat_ktp, alamat_tinggal, hp,
            rumah, emergency, riwayat, pangkat, gaji, departemen
        ))

        conn.commit()
        print("Data karyawan berhasil ditambahkan")
    else:
        print("Penambahan dibatalkan")

    conn.close()
    kembali()

def update_karyawan():
    nip = input("Masukkan NIP: ").strip()
    emp = cari_karyawan(nip)

    if not emp:
        print("Data tidak ditemukan")
        kembali()
        return

    print("UPDATE DATA KARYAWAN")
    print("Kosongkan jika tidak ingin mengubah data.\n")

    new_nama = input(f"Nama ({emp['nama']}): ").strip()
    new_ttl = input(f"TTL ({emp['ttl']}): ").strip()
    new_alamat_ktp = input(f"Alamat KTP ({emp['alamat_ktp']}): ").strip()
    new_alamat_tinggal = input(f"Alamat Tinggal ({emp['alamat_tinggal']}): ").strip()
    new_hp = input(f"No HP ({emp['hp']}): ").strip()
    new_rumah = input(f"No Rumah ({emp['rumah']}): ").strip()
    new_emergency = input(f"Emergency ({emp['emergency']}): ").strip()
    new_riwayat = input(f"Riwayat Kerja ({emp['riwayat']}): ").strip()
    new_pangkat = input(f"Pangkat ({emp['pangkat']}): ").strip()
    new_gaji = input(f"Gaji ({emp['gaji']}): ").strip()
    new_departemen = input(f"Departemen ({emp['departemen']}): ").strip()

    confirm = input("Yakin update data? (Y/N): ").upper()

    if confirm != "Y":
        print("Update dibatalkan")
        kembali()
        return

    nama = new_nama if new_nama else emp["nama"]
    ttl = new_ttl if new_ttl else emp["ttl"]
    alamat_ktp = new_alamat_ktp if new_alamat_ktp else emp["alamat_ktp"]
    alamat_tinggal = new_alamat_tinggal if new_alamat_tinggal else emp["alamat_tinggal"]
    hp = new_hp if new_hp else emp["hp"]
    rumah = new_rumah if new_rumah else emp["rumah"]
    emergency = new_emergency if new_emergency else emp["emergency"]
    riwayat = new_riwayat if new_riwayat else emp["riwayat"]
    pangkat = new_pangkat if new_pangkat else emp["pangkat"]
    gaji = int(new_gaji) if new_gaji else emp["gaji"]
    departemen = new_departemen if new_departemen else emp["departemen"]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE employees
        SET nama = %s,
            ttl = %s,
            alamat_ktp = %s,
            alamat_tinggal = %s,
            hp = %s,
            rumah = %s,
            emergency = %s,
            riwayat = %s,
            pangkat = %s,
            gaji = %s,
            departemen = %s
        WHERE nip = %s
    """

    cursor.execute(query, (
        nama, ttl, alamat_ktp, alamat_tinggal,
        hp, rumah, emergency, riwayat,
        pangkat, gaji, departemen,
        nip
    ))

    conn.commit()
    conn.close()

    print("Data karyawan berhasil diupdate")
    kembali()

def tambah_resign():
    nip = input("Masukkan NIP resign: ")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees WHERE nip = %s", (nip,))
    emp = cursor.fetchone()

    if not emp:
        print("Data tidak ditemukan")
        conn.close()
        kembali()
        return

    confirm = input("Yakin resign-kan? (Y/N): ").upper()

    if confirm == "Y":

        insert_query = """
            INSERT INTO resign_employees
            (nip, nama, ttl, alamat_ktp, alamat_tinggal, hp, rumah,
             emergency, riwayat, pangkat, gaji, departemen)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        data = (
            emp["nip"], emp["nama"], emp["ttl"], emp["alamat_ktp"],
            emp["alamat_tinggal"], emp["hp"], emp["rumah"],
            emp["emergency"], emp["riwayat"], emp["pangkat"],
            emp["gaji"], emp["departemen"]
        )

        cursor.execute(insert_query, data)
        cursor.execute("DELETE FROM employees WHERE nip = %s", (nip,))
        conn.commit()

        print(f"{emp['nama']} dipindahkan ke daftar resign")

    conn.close()
    kembali()


def lihat_resign():
    print("DATA KARYAWAN RESIGN")
    keyword = input("Cari berdasarkan NIP / Nama (kosongkan untuk semua): ").strip().lower()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if keyword == "":
        query = """
            SELECT nip, nama, ttl, departemen, hp
            FROM resign_employees
        """
        cursor.execute(query)
    else:
        query = """
            SELECT nip, nama, ttl, departemen, hp
            FROM resign_employees
            WHERE LOWER(nip) LIKE %s OR LOWER(nama) LIKE %s
        """
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword))

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Data tidak ditemukan")
        kembali()
        return

    rows = []
    for e in data:
        rows.append([
            e["nip"],
            e["nama"],
            e["ttl"],
            e["departemen"],
            e["hp"]
        ])

    print(tabulate(
        rows,
        headers=["NIP", "Nama", "TTL", "Departemen", "HP"],
        tablefmt="simple_grid"
    ))

    kembali()



def request_account(action, request_by):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    target_user_id = input("Masukkan User ID target: ").strip().lower()

    cursor.execute("""
        SELECT id FROM account_requests
        WHERE target_user_id = %s AND status = 'pending'
    """, (target_user_id,))
    
    if cursor.fetchone():
        print("Sudah ada request pending untuk user tersebut.")
        conn.close()
        return

    role = None
    password = None

    if action == "add":
        role = input("Masukkan role (user/admin/supervisor): ").strip().lower()
        password = input("Masukkan password: ").strip()

        if role not in ["user", "admin", "supervisor"]:
            print("Role tidak valid.")
            conn.close()
            return

    cursor.execute("""
        INSERT INTO account_requests 
        (request_by, target_user_id, action, role, password, status)
        VALUES (%s, %s, %s, %s, %s, 'pending')
    """, (request_by, target_user_id, action, role, password))

    conn.commit()
    conn.close()

    print("Request berhasil dikirim ke Super Admin.")

def lihat_account_pending():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, request_by, target_user_id, action, role
        FROM account_requests
        WHERE status = 'pending'
    """)

    results = cursor.fetchall()

    if not results:
        print("Tidak ada request pending.")
    else:
        print("\n=== REQUEST ACCOUNT PENDING ===")
        for r in results:
            print(f"""
ID Request : {r['id']}
Request By : {r['request_by']}
Target     : {r['target_user_id']}
Action     : {r['action']}
Role       : {r['role']}
--------------------------
""")

    conn.close()

def approve_account():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    target = input("Masukkan target user_id yang akan di-approve: ").strip().lower()

    cursor.execute("""
        SELECT * FROM account_requests
        WHERE target_user_id = %s
        AND status = 'pending'
        ORDER BY id DESC
        LIMIT 1
    """, (target,))

    request = cursor.fetchone()

    if not request:
        print("Request tidak ditemukan atau tidak ada yang pending.")
        conn.close()
        return

    if request["action"] == "add":

        cursor.execute("SELECT user_id FROM accounts WHERE user_id = %s", (target,))
        existing = cursor.fetchone()

        if existing:
            print("User sudah ada di tabel accounts.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO accounts
            (user_id, password, role, status, fail, blocked)
            VALUES (%s, %s, %s, 'approved', 0, 0)
        """, (
            target,
            request["password"],
            request["role"]
        ))

        print("Account berhasil dibuat dan di-approve.")

    elif request["action"] == "delete":

        cursor.execute("SELECT user_id FROM accounts WHERE user_id = %s", (target,))
        existing = cursor.fetchone()

        if not existing:
            print("User tidak ditemukan.")
            conn.close()
            return

        cursor.execute("""
            DELETE FROM accounts
            WHERE user_id = %s
        """, (target,))

        print("Account berhasil dihapus.")

    cursor.execute("""
        UPDATE account_requests
        SET status = 'approved'
        WHERE id = %s
    """, (request["id"],))

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def reject_account():
    conn = get_connection()
    cursor = conn.cursor()

    request_id = input("Masukkan ID request yang akan di-reject: ")

    cursor.execute("""
        UPDATE account_requests
        SET status = 'rejected'
        WHERE id = %s AND status = 'pending'
    """, (request_id,))

    if cursor.rowcount > 0:
        print("Request berhasil di-reject.")
    else:
        print("Request tidak ditemukan atau sudah diproses.")

    conn.commit()
    conn.close()

def super_admin_menu():
    while True:
        print("\n=== SUPER ADMIN MENU ===")
        print("1. Lihat Request Pending")
        print("2. Approve Request")
        print("3. Reject Request")
        print("0. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_account_pending()

        elif pilihan == "2":
            approve_account()

        elif pilihan == "3":
            reject_account()

        elif pilihan == "0":
            print("Logout berhasil.")
            break

        else:
            print("Pilihan tidak valid!")

def menu_user():
    while True:
        print("1. Lihat Data Karyawan")
        print("2. Lihat Karyawan Resign")
        print("0. Logout")
        p = input("Pilih: ")

        if p == "1":
            lihat_data_karyawan()
        elif p == "2":
            lihat_resign()
        elif p == "0":
            break

def menu_admin(username):
    while True:
        print("""
MENU ADMIN
1. Lihat Data Karyawan
2. Lihat Pangkat & Gaji
3. Tambah Karyawan
4. Lihat Resign
5. Tambah Resign
6. Update Data
7. Request Add Account
8. Request Delete Account
0. Logout
""")
        p = input("Pilih: ")

        if p == "1":
            lihat_data_karyawan()

        elif p == "2":
            lihat_pangkat_gaji()

        elif p == "3":
            tambah_karyawan()

        elif p == "4":
            lihat_resign()

        elif p == "5":
            tambah_resign()

        elif p == "6":
            update_karyawan()

        elif p == "7":
            request_account("add", username)

        elif p == "8":
            request_account("delete", username)

        elif p == "0":
            print("Logout berhasil.")
            break

        else:
            print("Pilihan tidak valid!")

def menu_supervisor():
    while True:
        print("MENU SUPERVISOR")
        print("1. Lihat Data Karyawan")
        print("2. Lihat Pangkat & Gaji")  
        print("3. Lihat Karyawan Resign")
        print("0. Logout")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            lihat_data_karyawan()

        elif pilih == "2":
            lihat_pangkat_gaji()   

        elif pilih == "3":
            lihat_resign()

        elif pilih == "0":
            break

        else:
            print("Menu tidak tersedia")

def main():
    while True:
        user_id, role = login()

        if role == "admin":
            menu_admin(user_id)

        elif role == "user":
            menu_user()

        elif role == "supervisor":
            menu_supervisor()

        elif role == "super_admin":
            super_admin_menu()

main()

