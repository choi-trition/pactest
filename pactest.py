import pacparser as pac
import sys, requests
import os.path

wd = os.path.dirname(os.path.realpath(__file__))
os.chdir(wd)

usage = '''
--USAGE--

python.exe pactest.py [PAC File Location] [URL to Check]

 - PAC File Location : on-line address or local file
    ex)
        http://my-pac.net/proxy.pac
        proxy.pac (if the file is in the same location as the python script)
        D:/my-folder/proxy.pac

 - URL : URL to check with the PAC Script. If omitted, only PAC script evaluation will processed.
    ex)
        https://www.example.com

'''


def get_pac(location):
    print(f'\n<Target PAC File>\n - Target PAC : "{location}"')
    if location.find('http', 0, 4) == -1:
        try:
            if location.find('/') > 0:
                # in case of full path input, replace / to // as python format
                file_path = location.replace('/', '//')
                f = open(file_path, "r")
            else:
                # in case of that the pac file is located in the same folder
                file_path = wd + f'\{location}'
                location = file_path
                f = open(file_path, "r")
        except:
            print('\nCan NOT open the PAC File.\nPlease check PAC file location.\n')
            sys.exit(1)
        else:
            script = f.read()
            f.close()
    else:
        try:
            res = requests.get(location)
            if res.history: print(f' - Real Target : "{res.url}"')
            if res.status_code == 200:
                script = res.text
            else:
                print("Can NOT download PAC file.")
                print(' URL :', res.url, '\n response status :', res.status_code, '\n response reason :', res.headers)
                sys.exit(1)
        except:
            print("\nSomething went wrong.\nCan NOT download PAC file.\n")
            sys.exit(1)
    print()
    return script


def pac_evaluation(script):
    pac.init()
    pac.enable_microsoft_extensions()
    try:
        print("<PAC Script Check>")
        pac.parse_pac_string(script)
    except:
        pac.cleanup()
        sys.exit(1)
    else:
        print(" - No Syntax Error found.\n")


def check_url(url):
    try:
        proxy = pac.find_proxy(url)

        # USAGE
        # proxy = pac.find_proxy("FULL-URL", "HOSTNAME_Can be omitted")
        # proxy = pac.find_proxy("https://www.example.com","www.example.com")
        # Or simply,
        # print(pac.just_find_proxy("PAC-FILE", "FULL-URL", "HOSTNAME_Can be omitted"))
        # print(pac.just_find_proxy("E:\py\project\pactest\proxy.pac", "https://www.example.com"))
    except:
        print(f'Something went wrong.\nCan Not Check the URL.\nINPUT URL - "{url}"')
        sys.exit(1)
    else:
        print(f'<Check result>\n - URL : "{url}"\n - Result : "{proxy}"\n')


if __name__ == "__main__":

    try:
        input = sys.argv
    except:
        print(usage)
    else:
        if len(input) < 2:
            print(usage)
            sys.exit(1)
        elif len(input) == 2:
            pac_script = get_pac(input[1])
            pac_evaluation(pac_script)
        else:
            pac_script = get_pac(input[1])
            pac_evaluation(pac_script)
            check_url(input[2])