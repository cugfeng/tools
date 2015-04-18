import os
import os.path
import shutil

Files = [ "._.DS_Store", ".DS_Store" ]
Dirs  = [ ".AppleDouble" ]
Roots = [ "C:\\", "D:\\" ]

# If file listed in $Files, dir listed in $Dirs, exist in $Roots, delete it

def main():
    for Root in Roots:
        for root, dirs, files in os.walk(Root):
            for file in Files:
                if file in files:
                    path = os.path.join(root, file)
                    print "Remove file %s" % path
                    os.remove(path)
            for dir in Dirs:
                if dir in dirs:
                    path = os.path.join(root, dir)
                    print "Remove directory %s" % path
                    shutil.rmtree(path)

main()
