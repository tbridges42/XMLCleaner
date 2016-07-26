from os import walk, sep, path
import my_xml


def get_files():
    files = []
    canon = ""
    for (dirpath, dirnames, filenames) in walk(get_working_directory()):
        for (currentfile) in filenames:
            if "canon" in currentfile:
                canon = currentfile
            else:
                if currentfile.endswith('.xml'):
                    files.append(dirpath + sep + currentfile)
        break
    return canon, files


def get_working_directory():
    for (dirpath, dirnames, filenames) in walk(path.dirname(path.abspath(__file__))):
        for (dirname) in dirnames:
            return dirname


def get_missing_records():
    canon_file, files = get_files()
    canon_xml = my_xml.to_set(my_xml.from_file(canon_file))
    files_xml = set()
    for file in files:
        files_xml |= my_xml.to_set(my_xml.from_file(canon_file))
    return files_xml - canon_xml


def main():
    print("Working...")
    missing = get_missing_records()
    my_xml.print_as_xml(missing, "missing.xml", "wb")
    print("Found " + str(len(missing)) + " records")
    result = input(":")


if __name__ == "__main__":
    main()
