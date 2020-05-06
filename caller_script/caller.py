import sys
import importlib
import os

if __name__ == "__main__":
    # The order of the arguments is the same as in the PythonCaller class
    _, script_path, script_name, classname, methodname, jsonarg = sys.argv

    cmd_folder = os.path.realpath(os.path.abspath(script_path))
    
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    # import module with model-class
    themodule = importlib.import_module(script_name)
    # Get the class itself and create an instance
    theclass = getattr(themodule, classname)
    obj = theclass()
    # Get the method to be called
    thefunc = getattr(obj, methodname)
    # Result of the invoked method is printed to the stdout and caught by the PythonCaller class
    print(thefunc(jsonarg))