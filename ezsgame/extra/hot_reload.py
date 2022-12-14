from ..global_data import get_screen

class Reload:
    def __init__(self, file, _globals, _locals):
        self.file = file
        self._globals = _globals
        self._locals = _locals
        self.code = ""
        self._start_code = ""
                      
        self.screen = get_screen()
        
        with open (self.file, "r") as f:
            file_content = f.read()        
            try:
                # code goes from ::reload to  ::endreload
                code = file_content.split('::reload')[1].split('::endreload')[0]     
                                
            except IndexError:
                raise SyntaxError(f"No code division found at: {self.file} \n\t Need to have ::reload and ::endreload")

            except Exception as e:
                raise e
            
            else:
                self._start_code = code
        
        self.__call__()

    def __call__(self, globals=None, locals=None):
        if globals:
            self._globals = globals
            self._locals = locals

        
        with open (self.file, "r") as f:
            file_content = f.read()        
            try:
                # code goes from ::reload to  ::endreload
                code = file_content.split('::reload')[1].split('::endreload')[0]     
                                
            except IndexError:
                if self._start_code:
                    code = self._start_code
                else: 
                    raise SyntaxError(f"No code division found at: {self.file}")

            except Exception as e:
                raise e
        
            if code != self.code:  
                try: 
                    exec(code, self._globals, self._locals)     
                                
                except Exception as e:
                    try:
                        # tries most recent saved code
                        exec(self.code, self._globals, self._locals)
                    except:   
                        # tries original code
                        exec(self._start_code, self._globals, self._locals)
                        
                        self.code = self._start_code
                else:
                    self.code = code 
                
             