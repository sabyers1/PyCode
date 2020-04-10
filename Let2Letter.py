#Let2Letter file renaming script
import os
pathname = "/Users/sabyers1/Dropbox/Job Search Info/"
savepathname = os.getcwd()
os.chdir(pathname)      # change working director for os.rename to work
cnt = 0
for fname in os.listdir(pathname):
    newfname=fname.replace("Leter","Letter",1)
    if newfname != fname :
        print("From: {} To: {}".format(fname, newfname))
        os.rename(fname,newfname)
        cnt += 1
print("Changed {} file(s)\n".format(cnt))
os.chdir(savepathname) # restore working directory