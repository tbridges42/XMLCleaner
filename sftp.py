import pysftp
from time import sleep
from tqdm import tqdm


# TODO get info from config file


def download(hostname, username, password, localpath):
    with pysftp.Connection(hostname, username=username, password=password) as sftp:
        files = [file for file in sftp.listdir_attr(path) if file.st_size > 104]
        total_size = 0
        for file in files:
            total_size = total_size + file.st_size
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading files') as progress_bar:
            for file in files:
                sftp.get(path + '/' + file.filename, localpath=localpath+file.filename)
                progress_bar.update(file.st_size)


def main():
    download(hostname, username, password, localpath)


if __name__ == "__main__":
    main()
