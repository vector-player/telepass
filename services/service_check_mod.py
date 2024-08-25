import importlib



def check_install_mod(mod_name):
    try:
        spec = importlib.util.find_spec(mod_name)
    except (ModuleNotFoundError, ValueError, AttributeError): 
        print(mod_name,"is not installed")           
        return False

    # only accept it as valid if there is a source file for the module - not bytecode only.
    if issubclass(type(spec), importlib.machinery.ModuleSpec):
        print(mod_name,"is installed")         
        return True

    print(mod_name,"is not installed")  
    return False


if __name__ == "__main__":
    mod_name = 'webview'
    check_install_mod(mod_name)