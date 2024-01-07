from termcolor import cprint


class Detection:
    def __init__(self,Host,Url,Status,Title,Length):
        self.host=Host
        self.url=Url
        self.status=Status
        self.title=Title
        self.length=Length

def banner():
    cprint('                          ', 'green', attrs=['bold', 'underline'])
    cprint('''
    三思而行，再行而思''', 'green', attrs=['bold'])
    cprint('                          ', 'green', attrs=['bold', 'underline'])
    print()
