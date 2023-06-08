# python File_Sort.py "D:\New folder\Test" arg1 arg2 arg3  "exist_ok = True"

import os
import sys
import numpy as np
import re
import shutil
import File_Sort_Exception as errors


class InputSplit:
    def __init__(self,terminal_input):
        self.terminal_input = terminal_input

    def inputSplitNoExtension(self):
        argument1 = self.terminal_input[0]
        argument2 = self.terminal_input[-1]
        return(argument1,argument2)
    
    def inputSplitWithExtension(self):
        argument1 = self.terminal_input[0]
        argument2 = self.terminal_input[1:len(self.terminal_input)-1]
        argument3 = self.terminal_input[-1]
        return(argument1,argument2,argument3)


class InputCheck:
    def __init__(self,input):
        self.path = input[0]
        self.condition = input[-1]
        if(len(input) == 2):
            pass
        else:
            self.extensions = input[1] 

    def checkPath(self):
        if(os.path.exists(self.path)):
            return(True)
        else:
            return(False)
        
    def checkExtension(self):
        dir_extension = []
        for file in os.listdir(self.path):
            if(os.path.isfile(self.path+"/"+file)):
                dir_extension.append(file.split(".")[-1])
            else:
                pass
        self.extensions = [re.sub(r'^\.',"",ext) for ext in self.extensions]
        repeat_check = {ext:self.extensions.count(ext) for ext in self.extensions}
        for count in repeat_check.values():
            if(count == 1):
                pass
            else:
                return(False)
        for extension in self.extensions:
            if(extension in dir_extension):
                pass
            else:
                return(False)
        return(True)

    def checkCondition(self):
        temp = self.condition.split("=")
        temp = [i.strip() for i in temp]
        if(len(temp) == 2):
            if(temp[0] == "exist_ok"):
                if(temp[-1] == "True" or temp[-1] == "False"):
                    return(True)
                else:
                    return(False)
            else:
                return(False)
        else:
            return(False)
        
        
class MiniFunctionSort:

    #say we want to know if the folder exist in our current working directory    
    def checkIfFolder(path,folder):
        if(os.path.isdir(os.path.join(path,folder))):
            return(True)
        else:
            return(False)
        
    #say we want to know if its a file or not but the given path and and name of file/folder

    def checkIfFile(path,file):
        if(os.path.isfile(os.path.join(path,file))):
            return(True)
        else:
            return(False)
        
    #say we want to filter the extension and obtain it without '.'
    def filterExtensions(extensions):
        return [re.sub(r'^\.', '', extension).upper() for extension in extensions]
    
    #say we want to create a folder and obtain the path for it
    def folderMakingPath(path,folder_name):
        return(os.path.join(path,folder_name))
    
    #say we want to check if the 
    def checkIfExist(path,folder):
        return(os.path.exists(MiniFunctionSort.folderMakingPath(path,folder)))
        
    #say we want to obtain all the extensions in the given path
    def obtainAllExtension(path):
        extensioninpath = set()
        for content in os.listdir(path):
            if(MiniFunctionSort.checkIfFile(path,content)):
                extensioninpath.add(os.path.splitext(content)[1].lower())
        return(extensioninpath)

    #say we want to know if the latest folder that exists in the directory
    def obtainLatestFolder(path,folder):
        folder = folder.upper()
        input_format = r'^{}\(\d+\)(?![()])(?<!\(\))$'.format(re.escape(folder))
        pattern_object = re.compile(input_format)
        contents = os.listdir(path)
        folders_match = []
        for content in contents:
            if(MiniFunctionSort.checkIfFolder(path,content)):
                if(pattern_object.match(content)):
                    folders_match.append(content)
                else:
                    pass
            else:
                pass
        if(len(folders_match) == 0):
            return(None)
        return (max(folders_match , key = lambda temp: int(re.search(r'\d+',temp).group())))
    
    #say we obtain the next folder by passing the path and current 
    def obtainNextFolder(path,folder):
        latest_folder = MiniFunctionSort.obtainLatestFolder(path,folder)
        if(latest_folder == None):
            return(folder.upper()+"(1)")
        else:
            latest_folder_pattern = r'\((\d+)\)'
            digits = int(re.search(latest_folder_pattern,latest_folder).group(1))
            return(folder.upper()+ "(" + str(digits+1) + ")")

    def createFolder(path,folder):
        if(MiniFunctionSort.checkIfExist(path,folder)):
            pass
        else:
            os.makedirs(MiniFunctionSort.folderMakingPath(path,folder))

    def conditionHandle(condition):
        if(condition.split("=")[-1].strip() == "True"):
            return(True)
        else:
            return(False)

    def sort(path,working_folder):
        for file in os.listdir(path):
            if(MiniFunctionSort.checkIfFile(path,file)):
                current_extension = os.path.splitext(file)[1].upper().split(".")[-1]
                if(current_extension in working_folder.keys()):
                    shutil.move(os.path.join(path,file),os.path.join(path,working_folder[current_extension],file))
                else:
                    pass
            else:
                pass


class CompleteSort:
    def __init__(self,input):
        self.path = input[0]
        self.condition = input[-1]

    def handleCompleteSort(self):
        if(MiniFunctionSort.conditionHandle(self.condition)):
            CompleteSort.existTrue(self)
        else:
            CompleteSort.existFalse(self)

    def existTrue(self):
        ext_folder = MiniFunctionSort.filterExtensions(MiniFunctionSort.obtainAllExtension(self.path))
        working_folder = {folder:MiniFunctionSort.obtainLatestFolder(self.path,folder) for folder in ext_folder}
        for folder in working_folder.keys():
            if(working_folder[folder] == None):
                working_folder[folder] = MiniFunctionSort.obtainNextFolder(self.path,folder)
            else:
                pass
        for folder in working_folder.values():
            MiniFunctionSort.createFolder(self.path,folder)
        MiniFunctionSort.sort(self.path,working_folder)

    def existFalse(self):
        ext_folder = MiniFunctionSort.filterExtensions(MiniFunctionSort.obtainAllExtension(self.path))
        working_folder = {folder:MiniFunctionSort.obtainNextFolder(self.path,folder) for folder in ext_folder}
        for folder in working_folder.values():
            MiniFunctionSort.createFolder(self.path,folder)        
        MiniFunctionSort.sort(self.path,working_folder)

class SelectiveSort:
    def __init__(self,input):
        self.path = input[0]
        self.condition = input[2]
        self.extension = input[1]

    def handleSelectiveSort(self):
        if(MiniFunctionSort.conditionHandle(self.condition)):
            SelectiveSort.existTrue(self)
        else:
            SelectiveSort.existFalse(self)

    def existTrue(self):
        ext_folder = MiniFunctionSort.filterExtensions(self.extension)
        working_folder = {folder:MiniFunctionSort.obtainLatestFolder(self.path,folder) for folder in ext_folder}
        for folder in working_folder.keys():
            if(working_folder[folder] == None):
                working_folder[folder] = MiniFunctionSort.obtainNextFolder(self.path,folder)
            else:
                pass
        for folder in working_folder.values():
            MiniFunctionSort.createFolder(self.path,folder)
        MiniFunctionSort.sort(self.path,working_folder)
        

    def existFalse(self):
        ext_folder = MiniFunctionSort.filterExtensions(self.extensions)
        working_folder = {folder:MiniFunctionSort.obtainNextFolder(self.path,folder) for folder in ext_folder}
        for folder in working_folder.values():
            MiniFunctionSort.createFolder(self.path,folder)
        MiniFunctionSort.sort(self.path,working_folder)
        

if __name__ == "__main__":
    terminal_input = sys.argv[1:]
    terminal_input = np.array(terminal_input,dtype="U")
    inputsplit = InputSplit(terminal_input)
    try:
        if(len(terminal_input)<2):
            raise errors.InputSplitError("ParameterError","ParameterError")
        elif(len(terminal_input) == 2):
            path,condition = inputsplit.inputSplitNoExtension()
            inputcheck = InputCheck([path,condition])
            try:
                if(inputcheck.checkPath()):
                    try:
                        if(inputcheck.checkCondition()):
                            completesort = CompleteSort([path,condition])
                            completesort.handleCompleteSort()
                        else:
                            raise errors.InputCheckError("ConditionError","ConditionError")
                    except errors.InputCheckError as error:
                        print(error.handleError())
                else:
                    raise errors.InputCheckError("PathError","PathError")
            except errors.InputCheckError as error:
                print(error.handleError())
        else:
            path,extensions,condition = inputsplit.inputSplitWithExtension()
            inputcheck = InputCheck([path,extensions,condition])
            try:
                if(inputcheck.checkPath()):
                    try:
                        if(inputcheck.checkExtension()):
                            try:
                                if(inputcheck.checkCondition()):
                                    selectivesort = SelectiveSort([path,extensions,condition])
                                    selectivesort.handleSelectiveSort()
                                else:
                                    raise errors.InputCheckError("ConditionError","ConditionError")
                            except errors.InputCheckError as error:
                                print(error.handleError())
                        else:
                            raise errors.InputCheckError("ExtensionError","ExtensionError")
                    except errors.InputCheckError as error:
                        print(error.handleError())
                else:
                    raise errors.InputCheckError("PathError","PathError")
            except errors.InputCheckError as error:
                print(error.handleError())
    except errors.InputSplitError as error:
        print(error.handleError())