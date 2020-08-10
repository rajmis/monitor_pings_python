import subprocess  # For executing a shell command.
import argparse # For taking systems arguments.

def ping(host):
    """
    Monitors PINGs to a host address for a UNIX-like system. Requires Python 3.5+.
    By default, the program pings 'google.com' if no address argument is passed via '-a'

    Prints response time if the PING succeeds, otherwise, prints w.r.t the scenarios.

    Case 1: In case a host does not respond to a ping (ICMP) request even if the host name is valid.
    		Output: 'Timeout. Host did not respond.'

    Case 2: No active internet connection exists.
    		Output: 'Network not reachable.'

    Case 3: PING succeeds.
    		Output: 'PING successful. Response time: XX.X ms'
    """

    # Similar to running "ping -c 1 -w 2 google.com"
    command = ['ping', '-c', '1', '-w', '2', host]
    a = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res_str = str(a.stdout)
    if a.returncode == 0:
    	print("PING successful. Response time: "+res_str[res_str.find('time=') + len('time='): res_str.find('ms') + len('ms')])
    else:
    	if 'connect' in res_str:
    		print("Network not reachable.")
    	else:
    		print("Timeout. Host did not respond.")


parser = argparse.ArgumentParser()
parser.add_argument('-a', help='Host Address to PING.')
args = parser.parse_args()
if args.a == None:
	print("Pinging google.com..")
	ping("google.com")
else:
	print("Pinging " + args.a +"..")
	ping(args.a)