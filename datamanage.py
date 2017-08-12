import io
import os
import base64
import datetime

#
# exit()
# exit()
# exit()

# Way to use base64:
# file_name_string = base64.urlsafe_b64encode("***$^%^(&&^$%&%*^(&*^?<>{}:>?<***")
# print file_name_string
# file_name_string = base64.urlsafe_b64decode(file_name_string)
# print file_name_string
# exit()

# Way to use datetime:
# print(datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S'))


# filename = "behav_history_20170101_20170630"
filename = "user_cart_history_converted"
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
        month = "UserAddToCartJune"
        nummonth = "06"
        if "2017-" + nummonth + "-01" in splited[2]:
            userid =  base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/01/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-02" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/02/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-03" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/03/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-04" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/04/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-05" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/05/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-06" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/06/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-07" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/07/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-08" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/08/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-09" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/09/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-10" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/10/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-11" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/11/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-12" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/12/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-13" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/13/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-14" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/14/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-15" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/15/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-16" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/16/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-17" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/17/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-18" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/18/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-19" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/19/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-20" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/20/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-21" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/21/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-22" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/22/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-23" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/23/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-24" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/24/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-25" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/25/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-26" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/26/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-27" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/27/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-28" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/28/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-29" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/29/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-30" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/30/" + userid
            newFile = io.open(NewFilename, "a", encoding='utf8')
            newFile.write(line + "\n")
            newFile.close()
        elif "2017-" + nummonth + "-31" in splited[2]:
            userid = base64.urlsafe_b64encode(splited[0])
            NewFilename = "NewDispatchedData/" + month + "/31/" + userid
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
