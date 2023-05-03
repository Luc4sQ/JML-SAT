def hello():
    print("hello")
    pass

def FileReader(url):
    if url == "sometype":
        knfData = open(url)
    else:
        print("please retry, with a proper file")
        return 0
    
