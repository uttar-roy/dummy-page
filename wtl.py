import paramiko as pm
import os, time
import sys,csv

#Define Missing Host Keys:
class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


#Define Lists for I/O:
mac,already_done,auth,done=([] for i in range(4))

USER = 'admin'
PASSWORD = 'Aruba@123'
with open('input.csv', 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        mac.append(row[0])
for i in mac:

   HOST = str(i)
   print(HOST +'\n###############')
   client = pm.SSHClient()
   client.load_system_host_keys()
   client.set_missing_host_key_policy(pm.AutoAddPolicy())
   try:
    client.connect('10.68.126.210', username=USER, password=PASSWORD, timeout=1000)
	
    channel = client.invoke_shell() 
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    channel.send('en\n')
    time.sleep(2)
    output=stdout.readlines()
    print('\n'.join(output))
    channel.send('Aruba123\n')
    time.sleep(2)
    channel.send('whitelist-db rap add mac-address '+i+' ap-group iapvpn\n')
    time.sleep(2)
    channel.send('iap trusted-branch-db add mac-address '+i+'\n')
    time.sleep(2)
    stdout.close()
    stdin.close()
    client.close()
    done.append(i)
   except (pm.ssh_exception.AuthenticationException,pm.ssh_exception.NoValidConnectionsError,TimeoutError,
   pm.ssh_exception.SSHException,OSError,ConnectionResetError) as error:
    auth.append(i)
    continue

#write output Files:   
print(done)   
with open('done.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(done) 
	
print(auth)
with open('autherr.csv', 'w+') as mf:
    wr = csv.writer(mf, quoting=csv.QUOTE_ALL)
    wr.writerow(auth)
