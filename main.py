import cleaner
import merge
import sftp
import scraper
import config


def main():
    creds = config.get_creds()
    sftp.download(creds.get("sftp_url"), creds.get("sftp_username"), creds.get("sftp_password"), creds.get("localpath"))
    cleaner.clean(creds.get("localpath"))
    merge.merge(creds.get("localpath"))
    scraper.scrape(creds)


if __name__ == "__main__":
    main()
