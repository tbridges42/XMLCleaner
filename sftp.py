import pysftp
from tqdm import tqdm


def get_creds():
    creds = {}
    with open("config.txt") as file:
        for line in file:
            (key, val) = [x.strip() for x in line.split('=')]
            creds[key] = val
    return creds


def download(hostname, username, password, localpath):
    with pysftp.Connection(hostname, username=username, password=password) as sftp:
        files = [file for file in sftp.listdir_attr(path) if file.st_size > 104]
        total_size = 0
        for file in files:
            total_size = total_size + file.st_size
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading files') as progress_bar:
            for file in files:
                sftp.get(creds["path"] + '/' + file.filename, localpath=creds["localpath"]+file.filename)
                progress_bar.update(file.st_size)


def main():
    download(hostname, username, password, localpath)


if __name__ == "__main__":
    main()
