import psutil
import re

for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'cmdline', 'name', 'username'])
    except psutil.NoSuchProcess:
        pass
    else:

        cur_cmdline = pinfo['cmdline']

        r = re.compile('.*python.*')
        if any(r.match(line) for line in cur_cmdline):
            print(pinfo['pid'])
            print(cur_cmdline)

