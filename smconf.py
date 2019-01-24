import paramiko as pm
import os, time
import sys,csv

#Define Missing Host Keys:
class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


#Define Lists for I/O:
ip,pingfail,auth,done=([] for i in range(4))

USER = 'admin'
PASSWORD = 'admin'
with open('input.csv', 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        ip.append(row[0])
for i in ip:
  response = os.system("ping " + i)

  #and then check the response...
  if response == 0:
   HOST = str(i)
   print(HOST)
   client = pm.SSHClient()
   client.load_system_host_keys()
   client.set_missing_host_key_policy(pm.AutoAddPolicy())
   try:
    client.connect(HOST, username=USER, password=PASSWORD, timeout=1000)
	
    channel = client.invoke_shell() 
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    channel.send('config set wirelessCellSizeUnit 2\n')
    time.sleep(2)
    channel.send('config set wirelessInterfaceScanFrequencyBandwidth 15\n')
    time.sleep(2)
    channel.send('config set wirelessInterfaceScanFrequencyListFive "5730 5735 5740 5745 5750 5755 5760 5765 5770 5775 5780 5785 5790 5795 5800 5805 5810 5815 5820 5825 5830 5835 5840 5845 5850 5855 5860 5865 5870"\n')
    time.sleep(2)
    channel.send('config set wirelessInterfaceScanFrequencyListTen "5730 5735 5740 5745 5750 5755 5760 5765 5770 5775 5780 5785 5790 5795 5800 5805 5810 5815 5820 5825 5830 5835 5840 5845 5850 5855 5860 5865 5870"\n')
    time.sleep(2)
    channel.send('config set wirelessInterfaceScanFrequencyListTwenty "5730 5735 5740 5745 5750 5755 5760 5765 5770 5775 5780 5785 5790 5795 5800 5805 5810 5815 5820 5825 5830 5835 5840 5845 5850 5855 5860 5865 5870"\n')
    time.sleep(2)
    channel.send('config set wirelessInterfaceScanFrequencyListForty "5730 5735 5740 5745 5750 5755 5760 5765 5770 5775 5780 5785 5790 5795 5800 5805 5810 5815 5820 5825 5830 5835 5840 5845 5850 5855 5860 5865 5870"\n')
    time.sleep(2)
    channel.send('config set wirelessTXPowerManualLimit 0\n')
    time.sleep(2)
    channel.send('config set wirelessAcceptableAPRSSIThreshold -90\n')
    time.sleep(2)
    channel.send('config set wirelessAcceptableAPSNRThreshold 0\n')
    time.sleep(2)
    channel.send('config set powerSequenceFactoryDefault 0\n')
    time.sleep(2)
    channel.send('config commit\n')
    time.sleep(2)            
    channel.send('exit\n')

    stdout.close()
    stdin.close()
    client.close()
    done.append(i)
   except (pm.ssh_exception.AuthenticationException,pm.ssh_exception.NoValidConnectionsError,TimeoutError,
   pm.ssh_exception.SSHException,OSError,ConnectionResetError) as error:
    auth.append(i)
    continue
   
  else:
   pingfail.append(i)

#write output Files:   
print(done)   
with open('done.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(done) 
print(pingfail)   
with open('pingfail.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(pingfail)
print(auth)
with open('autherr.csv', 'w+') as mf:
    wr = csv.writer(mf, quoting=csv.QUOTE_ALL)
    wr.writerow(auth)
