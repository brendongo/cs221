import re,  mmap


class InputFile():
    def __init__(self, filename):
        self.texts = []
        self.index = 0
        with open(filename, 'r+') as f:
            data = mmap.mmap(f.fileno(),0)
            bodyRegex = re.compile("<BODY>([^<]*)</BODY>", re.IGNORECASE)
            matches = bodyRegex.findall(data)
            for match in matches:
                text = "%s" % match
                self.texts.append(text)

    def next_string(self):
        if self.index < len(self.texts):
            index = self.index
            self.index += 1
            return self.texts[index]
        

def main():
    inputs_file = InputFile("reut2-000.sgm")
    print inputs_file.next_string()




if __name__ == '__main__':
    main()