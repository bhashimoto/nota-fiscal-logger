from nf_fetch import NFFetcher
from qr_reader import QRReader
from database import DBManager

def main():
    qrr = QRReader()
    dbm = DBManager()
    nff = NFFetcher()

    qrr.read()

    for url in qrr.codes.keys():
        data = nff.fetch_nf(url)

        dbm.insert_nf(data["header"])
        
        for item in data["items"]:
            dbm.insert_item(item)




if __name__ == "__main__":
    main()
