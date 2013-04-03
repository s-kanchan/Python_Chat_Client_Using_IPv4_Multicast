import sys,getopt
import os
import socket
import string
import struct
import threading
from threading import Thread
from time import sleep


mutual_lock=threading.Lock()
MCAST_GRP = '224.1.1.1' 		# default value taken  if not given
MCAST_PORT = 5007;
chat_name="abcxyz123"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)  # for sending msg

def main():
	try:
        	opts, args = getopt.getopt(sys.argv[1:], "m:p:n:",['multicast','port','name'])
	except getopt.GetoptError:
		print "Please read this:\nUsage : python <file.py> -m <Multicast-IP> -p <Multicast-Port> -n <Chatter-Name>"
        	os._exit(1)

    	try:
		for o,a in opts:
        		if o in ("-m"):
				msgSplit=a.split('.')
				if((int(msgSplit[0])!=224)|(int(msgSplit[1])>255)|(int(msgSplit[2])>255)|(int(msgSplit[3])>255)|(len(msgSplit)>4)):
              				raise Exception;#taking care of incorrect multicast ipv4 addresses.
	    			else:
					global MCAST_GRP
            				MCAST_GRP = a
        		elif o in ("-p"):
				global MCAST_PORT
				MCAST_PORT = int(a)
				try:
					sock.bind(('', MCAST_PORT))
				except SocketException:
					raise Exception
	    			
            		elif o in ("-n"):
	    			global chat_name
            			chat_name = a
			else:
				assert False
	except Exception:
		print("please enter valid input parameters");
        	os._exit(1)
		

if __name__ == "__main__":
    main()


#sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

msg= chat_name+"\@/**************** "+string.upper(chat_name)+ " has joined the room **********************\@/welcome"
sock.sendto(msg.strip(), (MCAST_GRP, MCAST_PORT))

class bc:
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    cyan = '\033[36m'
    ion = '\033[3m'
    ioff = '\033[23m'
    bon = '\033[1m'
    boff = '\033[22m'
    reset = '\033[0m'


def interrupt():
	import sys, tty, termios

	fd = sys.stdin.fileno()
	# save original terminal settings 
	old_settings = termios.tcgetattr(fd)

	# change terminal settings to raw read
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	# restore original terminal settings 
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch;
        



def receive_msg(sock):
	while True:
  		msg,(addr,port) =sock.recvfrom(10240)
		if(msg):
			try:
				mutual_lock.acquire()
				msg=msg.split('\@/')
				if not (msg[0] == chat_name):
					if not (msg[2]):
						print bc.bon+bc.blue+string.upper(msg[0])+" <<< "+bc.boff+bc.cyan+msg[1]+bc.reset
					else:
						if(msg[2]=="welcome"):
							print bc.green+msg[1]+bc.reset
						else:
							print bc.red+msg[1]+bc.reset
			finally:
				mutual_lock.release()
		print "\r"

'''if __name__ == "__main__":
    main() '''

if __name__ == "__main__":
    thread = Thread(target = receive_msg, args = (sock, ))
    thread.start()
    #print "thread finished...exiting"

print bc.green+"################################ WELCOME TO CHAT ROOM #####################################"
print "Press any key,then type your message \nType 'quit' to leave the room"
print "###########################################################################################"+bc.reset
if(chat_name == "abcxyz123"):
	chat_name=raw_input(bc.red+"Name required : "+bc.blue);
	print bc.reset
while 1:
	ch_val = '';
	ch_val = interrupt();
	if(ch_val):
		try:
			mutual_lock.acquire()
			
			msg=raw_input(bc.bon+bc.green+"ME >>> "+bc.boff+bc.cyan)
			print bc.reset
			if(string.upper(msg) == "QUIT"):
				print bc.yellow+"################### Leaving the chat room, BYE :)  ########################  "+bc.reset
				msg= chat_name+"\@/**************** "+string.upper(chat_name)+ " has left the room **********************\@/action"
				sock.sendto(msg.strip(), (MCAST_GRP, MCAST_PORT))
				os._exit(1)
				 
			if msg:
				msg= chat_name+"\@/"+msg+"\@/"
				sock.sendto(msg.strip(), (MCAST_GRP, MCAST_PORT))
			
			
		finally:
			mutual_lock.release()
	
	#print "\r"
