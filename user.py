#method 1
print("Enter your start date")
sdate = input()
#method 1
print("Enter your end date")
edate = input()

#method 2

print("Enter your 10 pain levels separated by spaces and date")
print("Enter end if you are done")

arr = []
while True:
    inp = input()
    if (inp == "end"):
        break
    array = []
    inp=inp.split()
    for i in inp:
        array.append(int(i))
    arr.append(array)

print (sdate)
print (edate)
print (arr)