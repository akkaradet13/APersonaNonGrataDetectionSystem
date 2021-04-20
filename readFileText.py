def read():
    f = open("./LevelSecurity.txt", "r")
    print(f.read())
    
def write():
    f = open("./LevelSecurity.txt", "w")
    f.write("1")
    f.close()
    
read()
write()
read()