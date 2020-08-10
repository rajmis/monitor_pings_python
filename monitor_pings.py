import subprocess  # For executing a shell command.
import argparse # For taking systems arguments.
import csv # For writing to csv files.
import time # For getting current time.

def ping(host,mode):
    """
    Monitors PINGs to a host address for a UNIX-like system. Requires Python 3.5+.
    By default, the program pings 'google.com' if no address argument is passed via '-a'

    For one shot [-m 'one'] monitoring, the code prints response time if the PING succeeds, otherwise, prints w.r.t the scenarios.
	    Case 1: In case a host does not respond to a ping (ICMP) request even if the host name is valid.
	    		Output: 'Timeout. Host did not respond.'

	    Case 2: No active internet connection exists.
	    		Output: 'Network not reachable.'

	    Case 3: PING succeeds.
	    		Output: 'PING successful. Response time: XX.X ms'
	
	For continous logging [-m 'log'], the code saves the timestamped data in 'data.csv' file.
		Case 1: In case a host does not respond to a ping (ICMP) request even if the host name is valid.
				Logged as XXXXXXX, YYYYYY, -1

		Case 2: No active internet connection exists.
				Logged as XXXXXXX, YYYYYY, -99

		Case 1: PING succeeds.
				Logged as XXXXXXX, YYYYYY, ZZ.Z
		
		where XXXXXXX is timestamp, YYYYYY is the host address, ZZ.Z is the response time.
    """

    # Similar to running "ping -c 1 -w 2 google.com"
    command = ['ping', '-c', '1', '-w', '2', host]
    run_cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res_str = str(run_cmd.stdout)
    if run_cmd.returncode == 0:
    	res_tm = res_str[res_str.find('time=') + len('time='): res_str.find('ms')]
    	if mode == 0:
    		print("PING successful. Response time: " + res_tm + " ms")
    	else:
    		return res_tm

    else:
    	if 'connect' in res_str:
    		if mode == 0:
    			print("Network not reachable.")
    		else:
    			return -99
    	else:
    		if mode == 0:
    			print("Timeout. Host did not respond.")
    		else:
    			return -1


parser = argparse.ArgumentParser()
parser.add_argument('-m', help='Define mode of monitoring - \'log\' for loggin and \'one\' for oneshot data.')
parser.add_argument('-a', help='Host Address to PING.')
args = parser.parse_args()


#Checking if a host address was given.
if args.a == None:
	host_addr = "google.com"
else:
	host_addr = args.a


if args.m is None or args.m == 'one':
	print("Pinging " + host_addr +"..")
	ping(host_addr,0)

elif args.m == 'log':
	try:
		with open('data.csv', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(['timestamp'] + ['host address'] + ['response time'])
			while(1):
				ping_res = ping(host_addr,1)
				writer.writerow([str(int(time.time()))] + [host_addr] + [ping_res])
				time.sleep(2)
	except KeyboardInterrupt:
		print("Monitoring stopped by the user. Check \'data.csv\' file for details.")

else:
	print("The selected mode does not exists currently.\nPlease either select \'log\' for loggin and \'one\' for oneshot data.")