class LogSearcher:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.f.seek(0,2)
        self.length = self.f.tell()
        
    def find(self, string, plusLines = 0):
        low = 0
        high = self.length

        while low < high:
            mid = (low+high)//2
            p = mid
            self.f.seek(p)
            
            while p >= 0:
                self.f.seek(p)

                char = self.f.read(1)
                if char == b'\n':
                    break

                p -= 1
            
            if p < 0: self.f.seek(0)
            
            line = self.f.readline()
            line = str(line, 'latin-1')
            date_start = line.find('"time": ') + 9
            line = line[date_start: date_start + 19 ]
            
            print ('--', mid, line)
            
            if line < string:
                low = mid+1
            else:
                high = mid
        
        p = low

        while p >= 0:
            self.f.seek(p)
            if self.f.read(1) == b'\n': break
            p -= 1

        if p < 0: self.f.seek(0)

        result = [ ]
        count = 0;   
        while True:
            line = self.f.readline()
            line = str(line, 'latin-1')
            if not line or (plusLines > 0 and count >= plusLines): break
            result.append(line)
            count += 1


        return result