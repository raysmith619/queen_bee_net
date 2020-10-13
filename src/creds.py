# creds.py
"""
A week attempt to provide my creds without
broadcasting them to the world
"""

cred_dir = ".."
unfn = f"{cred_dir}/uname.txt"
def get_username():
    tx = None
    try:
        with open(unfn) as f:
            tx = f.read()
            tx = ''.join(tx.split())
    except Exception as e:
        print(f"Can't get {unfn}: {str(e)}")
    return tx

unpwfn = f"{cred_dir}/upw.txt"
def get_psword():
    tx = None
    try:
        with open(unpwfn) as f:
            tx = f.read()
            tx = ''.join(tx.split())
    except Exception as e:
        print(f"Can't get {unpwfn}: {str(e)}")
    return tx

if __name__ == "__main__":
    print(get_username())
    print(get_psword())