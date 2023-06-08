# TerminalFileSort
A python file that can sort files in folders based on extensions so for a .jpeg file a JPEG folder will be made which will consists of all jpeg files
In order to run the command first set the current working directory of terminal to the path where File_Sort.py file is 
command is: cd {path}
To sort the file
command is: python File_Sort.py {path} {extensions} {condition}
path*:- The path of the folder where the sorting is to be performed path needs to be in inverted commas eg. "D:/New Folder/Test"
extension:- If only seleceted files need to be sorted then enter the extensions name eg: .jpeg pdf .mp4 here only these three files will be sorted rest will remain unaltered. If all files need to be sorted then dont enter any exception skip the part.
condition:- The condition for exist_ok can be either True or False.
            Condition specifies wheather the sorting to be done is in new folders or in pre-existing folders if there is any.
            "True" means sort in existing folders if any.
            "False" means sort in new folders
eg:
For selective sort command is: python File_Sort.py "D:\New folder\Test" .jpeg pdf  "exist_ok = True"
For complete sort command is: python File_Sort.py "D:\New folder\Test" "exist_ok = True"
