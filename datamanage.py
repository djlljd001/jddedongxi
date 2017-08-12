import io
import os
import base64
import datetime


exit()
exit()
exit()

# Way to use base64:
# file_name_string = base64.urlsafe_b64encode("***$^%^(&&^$%&%*^(&*^?<>{}:>?<***")
# print file_name_string
# file_name_string = base64.urlsafe_b64decode(file_name_string)
# print file_name_string
# exit()

# Way to use datetime:
# print(datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S'))


# filename = "behav_history_20170101_20170630"
filename = "behav_history_20170101_20170630"
files = io.open(filename, "r", encoding='utf8')
lines = files.read().splitlines()
totalLines = len(lines)
userid = None

# ================= percentage ========
z = totalLines / 100.0          # =====
a = 0                           # =====
i = 0                           # =====
# ================= percentage ========

def convertUnixDateToDate(i, a):
    print "Start"
    NewFilename = "user_cart_history_converted"
    newFile = io.open(NewFilename, "a", encoding='utf8')
    for line in lines:
        # ================= percentage ========
        if i / z > a + 1:  # =====
            a = int(i / z)  # =====
            print a, "%"  # =====
        i = i + 1
        # ================= percentage ========
        splited = line.split("\t")
        date = datetime.datetime.fromtimestamp(int(splited[2])).strftime('%Y-%m-%d %H:%M:%S')
        newFile.write(splited[0] + "\t" +splited[1] + "\t" +  date  + "\n" )
    newFile.close()

def splitFile(i, a):

    for line in lines:
        # ================= percentage ========
        if i / z > a + 1:  # =====
            a = int(i / z)  # =====
            print a, "%"  # =====
        i = i + 1
        # ================= percentage ========

        splited = line.split("\t")
        if "2017-01-" in splited[5] or "2017-02-" in splited[5]:
            userid =  base64.urlsafe_b64encode(splited[1])
            NewFilename = "DispatchedData/newnewnfwefcwewvce/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()

def mergeData(i, a):
    pass



def cleanUselessData(i,a):
    for line in lines:
        # ================= percentage ========
        if i / z > a + 1:  # =====
            a = int(i / z)  # =====
            print a, "%"  # =====
        i = i + 1
        # ================= percentage ========

# convertUnixDateToDate(i, a)
splitFile(i, a)

files.close()