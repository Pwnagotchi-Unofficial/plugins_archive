from multiprocessing.connection import Client
import sys

if (len(sys.argv) != 2):
    print 'no powerutil command given. Try shutdown/restart-auto/restart-manual/reboot-auto/reboot-manual'
    sys.exit()

cmd = sys.argv[1]
print 'cmd = ' + cmd
if cmd not in ('shutdown', 'restart-auto', 'restart-manual', 'reboot-auto', 'reboot-manual'):
    print 'invalid menu command given. Try shutdown/restart-auto/restart-manual/reboot-auto/reboot-manual'
    sys.exit()

address = ('localhost', 6799)
conn = Client(address)
conn.send(cmd)
conn.close()

