import pysftp


hostname = 'secureftp01.wi.gov'
path = '511_prd/PFNPRD/outbound/PO_INT_006'
localpath = 'H:\\Contract Sunshine\\XML Files For Import\\STAR\\'


def download():
    with pysftp.Connection(hostname, username=username, password=password) as sftp:
        sftp.get_d(path, localpath)


def main():
    download()


if __name__ == "__main__":
    main()
