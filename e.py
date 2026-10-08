class Check:
    def __init__(self, FileName : str):
        self.fn = FileName
        
    def Read(self):
        f = open(self.fn, 'r')
        data = f.read()
        f.close()
        return data
    
    def Write(self):
        f = open(self.fn, 'w')
        f.write('nn')
        f.close()
        
if __name__ == '__main__':
    try:
        c = Check('snd.py')
        print(c.Read())
        c.Write()
    except Exception as e:
        print(f'the error was {e}')
    finally:
        pass