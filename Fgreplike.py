'''
File: Fgreplike.py
File Create: 30th October 2014
Author: Abhijit
-----
 Python script to perform like fgrep in a bash script
 
 Usage: Fgreplike.py <Textual search string> {list of file names}

-----
Last Modified: 27th April 2020 4:19:03 pm
Modified By: Stephen Byers
-----
No Copyright 2020
'''

import re
import sys


if len(sys.argv) < 3:
    sys.exit( "Insufficient command line arguments: Usage: Fgreplike.py <search term> <{file or file list}>")

ReadFiles = 0
FoundFiles = 0
Srch = r'{}'.format(sys.argv[1])
for f in sys.argv[2:]:   
    #print("Attempting to open file: {}".format(f))
    #setting latin-1 encoder keeps binary files from illegal codes
    with open(f, encoding="latin-1") as origin_file:
        ReadFiles += 1
        lcnt = 0
        for line in origin_file:
            line = re.findall(Srch, line)
            lcnt += 1
            if line:
                print("Found {} in {} line {}".format(line[0],f,lcnt))
                FoundFiles += 1
                break
print("Reviewed {} file(s) for pattern: '{}' and found {}".format(ReadFiles,Srch,FoundFiles))