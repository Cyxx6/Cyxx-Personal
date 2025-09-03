# f = open("cyxx.txt" , "w")
# f = open("name.txt" , "w")  this is how u create files in pyhon
import os
f=open("cyxx.txt")
print(f.read())  # This coommabd opens a file..
f.close()        # = this command closes the file after it is done opening..

f=open("name.txt")
print(f.read(2)) # this command prints the first letters of the filel...as indicated in the bracket
f.close()

f=open("cyxx.txt")
print(f.readline()) # this reads the first line in the file
print(f.readline()) # this will also print the second line when done this way... <-
f.close()

f=open("name.txt")
for line in f:
    print(line)   #this will also print the file for u but with spaces...
f.close() 

# Opening a file that doesnt exist... u use the try block...
try:
    f=open("mil.txt")
    print(f.read())
except:
    print("does not exist")
f.close()

#APPENDING to files

f=open("cyxx.txt","a")
f.write("Hilda")
f.close()

#Openeing a file for writing..(ie. changes everything in the file and replaces it with what u want)
""""
f=open("name.txt","w")
f.write("ive deleted everything")  #thats why ive commented it
"""

if os.path.exists("dave.txt"):
    os.remove("dove.txt")
else:
    print("cant delete")


