# SplitFileDate.py
import os

pathname = "/Users/sabyers1/Documents/Archive/Huntington"
savepathname = os.getcwd()
os.chdir(pathname)      # change working director for os.rename to work
for fname in os.listdir(pathname):
    if fname.startswith("Huntington"):
            if fname[10:].split(' ')[0] == fname[10:]:
                newfname = fname[:14] + ' ' + fname[14:]
                print("From: " + fname + ',' + newfname)
                os.rename(fname,newfname)
os.chdir(savepathname) # restore working directory