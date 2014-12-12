####################################
## Server authentication details. ##
####################################
##Set these variable before executing
ftp_host="YOUR_FTP_HOST"
ftp_username="YOUR_FTP_USERNAME"
ftp_passwd="YOUR_FTP_PASSWORD"

##############################
## Written by Kousthub Raja ##
##############################
from ftplib import FTP
import glob
import os

folder=os.getcwd().split(os.sep)[-1]

def upload(con):
	flist=con.nlst()
	if folder not in flist:
		con.mkd(folder)

	con.cwd(folder)

	files=glob.glob("*")
	for fil in files:
		print "[+] Uploading : "+fil
		try:
			con.storbinary("STOR "+fil,open(fil,"rb"))
		except:
			print "Could not upload : %s" % fil

def download(con):
	con.cwd(folder)
	flist=con.nlst()
	for fil in flist:
		if fil!="." and fil!="..":
			print "[+] Downloading : "+fil
			try:
				con.retrbinary("RETR "+fil,open(fil,"wb").write)
			except:
				print "Could not download : %s" % fil
	
##################
## Main program ##
##################
def main():
  print "Connecting to server. Please wait..."
  con=FTP(ftp_host,ftp_username,ftp_passwd)
  try:
    con.cwd("public_html")
  except:
    print "No public_html folder found, using root folder."

  flist=con.nlst()
  if 'sync' not in flist:
    con.mkd('sync')

  stype=raw_input("Upload to server/Download [U/D]: ")
  stype=stype.lower().strip()

  if(stype=="u"):
    upload(con)
  elif(stype=="d"):
    download(con)
  else:
    print "Invalid Option"


  con.close()
  print "\n    Done!"
  raw_input("Press enter to exist..")

def first_run():
  source_code=open(__file__,'r').read()
  source_head=source_code[0:300]
  source_body=source_code[300:-1]
  if 'YOUR_FTP_HOST' in source_head:
    print "You need to enter your FTP server's login details for the first time use. This can be later changed easily by editing source.\n\n"
    ftp_host=raw_input("Enter your Host name [eg: ftp.mysite.com ] : ")
    ftp_username=raw_input("Enter your User name [eg: sasi ]           : ")
    ftp_passwd=raw_input("Enter your Password [eg: secret ]          : ")
    source_head=source_head.replace('YOUR_FTP_HOST',ftp_host)
    source_head=source_head.replace('YOUR_FTP_USERNAME',ftp_username)
    source_head=source_head.replace('YOUR_FTP_PASSWORD',ftp_passwd)
    source_code=source_head+source_body
    print ftp_host
    open(__file__,'w').write(source_code)
    print "Server Setup done. You dont have to repeat this. Execute once again to sync."
    # print source_code
    
if __name__=='__main__':
  first_run()
  main()
 
