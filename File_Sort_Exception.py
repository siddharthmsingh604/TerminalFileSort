class InputSplitError(Exception):
    def __init__(self,message,error_type):
        super().__init__(message)
        self.error_type = error_type
    
    def handleError(self):
        if(self.error_type == "ParameterError"):
            return(self.paramterCountError())
        else:
            return(f'Invalid Input Error')
    def paramterCountError(self):
        return(f'{self.args[0]}: Invalid number of Arguments')

class InputCheckError(Exception):
    def __init__(self,message,error_type):
        super().__init__(message)
        self.error_type = error_type

    def handleError(self):
        if(self.error_type == "PathError"):
            return(self.parameterPathError())  
        elif(self.error_type == "ExtensionError"):
            return(self.parameterExtensionError())
        elif(self.error_type == "ConditionError"):
            return(self.parameterConditionError())
        else:
            return(f'Invalid Parameter Error')

    def parameterPathError(self):
        return(f'{self.args[0]}: Invalid Path')
    
    def parameterExtensionError(self):
        return(f'{self.args[0]}: Invalid Extension')
    
    def parameterConditionError(self):
        return(f'{self.args[0]}: Invalid Condition')