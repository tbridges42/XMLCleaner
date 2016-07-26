import my_xml
import time
import os
from os import walk
from tqdm import tqdm


agencies = [115, "Department of Agriculture",
144, "Department of Financial Institutions",
145, "Commissioner of Insurance",
155, "Public Service Commission",
165, "Department of Safety and Professional Services",
190, "State Fair Park Board",
192, "Wisconsin Economic Development Corporation",
220, "Wisconsin Artistic Endowment Foundation",
225, "Educational Communications Board",
235, "Higher Educational Aids Board",
245, "Historical Society",
250, "Medical College of Wisconsin",
255, "Department of Public Instruction",
285, "University of Wisconsin System",
292, "Technical College System Board",
320, "Environmental Improvement Program",
360, "Lower Wisconsin State Riverway Board",
370, "Department of Natural Resources",
373, "Fox River Navigational System Authority",
375, "Lower Fox River Remediation Authority",
380, "Department of Tourism",
385, "Kickapoo Reserve Management Board",
395, "Department of Transportation",
410, "Department of Corrections",
425, "Employment Relations Commission",
432, "Board on Aging and Long-Term Care",
433, "Child Abuse and Neglect Prevention Board",
435, "Department of Health Services",
437, "Department of Children and Families",
438, "Board for people with Developmental Disabilities",
440, "Health and Educational Facilities Authority",
445, "Department of Workforce Development",
455, "Department of Justice",
465, "Department of Military Affairs",
475, "District Attorneys",
485, "Department of Veterans Affairs",
490, "Wisconsin Housing and Economic Development Authority",
505, "Department of Administration",
507, "Board of Commissioners of Public Lands",
510, "Elections Commission",
511, "Government Accountability Board",
515, "Department of Employee Trust Funds",
521, "Ethics Commission",
525, "Office of the Governor",
536, "Investment Board",
540, "Office of the Lieutenant Governor",
550, "Public Defender Board",
566, "Department of Revenue",
575, "Secretary of State",
585, "Treasurer",
625, "Circuit Courts",
660, "Court of Appeals",
670, "Judicial Council",
680, "Supreme Court",
765, "Legislature",
]

# get all files to be merged
def getunmergedfiles():
    files = []
    for (dirpath, dirnames, filenames) in walk(os.path.dirname(os.path.abspath(__file__))):
        for (filename) in filenames:
            if filename.startswith('upload') and filename.endswith('.xml'):
                files.append(filename)
        break
    return files


def main():
    agency_collection = {}
    files = getunmergedfiles()
    with tqdm(total=len(files), unit_scale=True, desc='Merging files') as progress_bar:
        for (filename) in getunmergedfiles():
            # the agency abbreviation is the third section of a hyphen-separated filename
            agency = filename.split('-')[2]
            agencyset = set()
            if agency in agencies:
                agencyset = agency_collection[agency]
            agencyset |= my_xml.to_set(my_xml.from_file(filename))
            agency_collection[agency] = agencyset
            progress_bar.update(1)

    for (agency) in agencies:
        print(agency)
        my_xml.print_as_xml(agency_collection[agency], "upload-" + agencies[int(agency)] + "-" + time.strftime("%y%m%d") +
                            "-merged.xml", "wb")


if __name__ == "__main__":
    main()