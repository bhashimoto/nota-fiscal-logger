from nf_fetch import NFFetcher
from qr_reader import QRReader

def main():
    qrr = QRReader()
    qrr.read()
    print(qrr.codes)
    nff = NFFetcher()
    for url in qrr.codes.keys():
        data = nff.fetch_nf(url)
        print(data)


if __name__ == "__main__":
    main()
