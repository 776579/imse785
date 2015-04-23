Three Tricks to Operate on Your VM
===
*-MAC WANG*

We have noticed that recently some students encountered problems when operating on our Cloudera Quickstart VM. Here I am going to mention three practical techniques that you might need when working on your VM. They are not required, though. I tested these tricks on *Windows 8.1 Pro*; I believe they work well on other versions of Windows. Please let me know otherwise. 

For those of you who are using UNIX-based operating systems, e.g. Mac OS or Ubuntu, life is much easier for you: please contact me and I will show you some special recipes. 

Also, I will integrate these configurations into our customized Cloudera VM and update the image recently. I will keep you posted. 

## 1. View Web Interface on Windows

Who would not prefer viewing web interfaces on their own OS than squeezing in the tiny Virtual Machine window? No problem, let's make it happen:

**Step 1. Change Network Adapter Settings (on Windows)**

1. With your VM _powered off_, locate to *Settings* -> *Network* -> *Adapter 1*;
2. Change *Attached to:* option to *Bridged Adapter*;
3. You can specify the interface you want to use, but usually it works by default.

**Step 2. Get IP of the VM (on Cloudera)**

1. Open *Terminal*;
2. Type in the following command: 

	```
	[cloudera@quickstart ~]$ ifconfig
	```
3. Find your IP address, it is labeled by *"inet addr"* and starting with *"192."* or *"10."*, please notice *"127.0.0.1"* is not what we need. Mine is *192.168.1.106*, I will use that in my following steps;

**Step 3. Use your browser instead of the VM's (on Windows)**

1. Open your local browser and paste your IP address with the port numbers to access the web interfaces (you may replace the IP address with your own) :

	* Cloudera Manager: *192.168.1.106*
	* Hue: *192.168.1.106:8888*
	* Hadoop HDFS Namenode: *192.168.1.106:50070*
	* Hadoop HDFS Secondary Namenode: *192.168.1.106:50090*
	* Hadoop HDFS Datanode: *192.168.1.106:50073*
	* YARN Resource Manager: *192.168.1.106:8088*
	* YARN Node Manager: *192.168.1.106:8042*
	* HBASE Region Server: *192.168.1.106:60030*
	* HBASE Master: *192.168.1.106:60010*

	
## 2. Enter Commands on Windows

Sometimes it is difficult to operate within Virtual Machine, since you had to frequently switch back and forth between your Windows and our VM. So I will show you how to interact with our VM without clicking into it. The technique we are about to use here is called [Secure Shell (SSH)](http://en.wikipedia.org/wiki/Secure_Shell). I assume you have read *1. View Web Interfaces on Windows* and understand how to get your VM's IP. I hereby use my VM's IP, *192.168.1.106*, in the following steps. 

**Step 1. Install Putty (on Windows)**

1. Download [Putty](http://en.wikipedia.org/wiki/PuTTY) from this [link](http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe);
2. Execute the installation package.

**Step 2. SSH into your VM (on Windows)**

1. Open *Putty*;
2. Put in your VM's IP, which is *192.168.1.106* in my case;
3. Click *"Yes"* to add the key to your system;
4. Enter *"cloudera"* for *"login as:"*, and *"cloudera"* for the password;
5. Now you have control of your VM.


## 3. File Transferring

Although *WinScp* is a feasible solution, nothing could be easier than a simple drag'n'drop. So let's start out creating a shared folder via [SMB](http://en.wikipedia.org/wiki/Server_Message_Block). You only need to do the following steps one time. 

**Step 1. Install Samba (on Cloudera)**

1. Open *Terminal*;
2. Enter this command: `sudo yum install -y samba`
3. It takes a while to install, but eventually you will see messages like these: 
	
	```
	...
	Installed:
		samba.x86_64 0:3.6.23-12.el6
	
	Complete!
	[cloudera@quickstart ~]$
	```

**Step 2. Create Shared Folder (on Cloudera)**

1. Open *Terminal*;
2. Enter the following command: 

	```
	[cloudera@quickstart ~]$ mkdir ~/Desktop/Share
	[cloudera@quickstart ~]$ sudo chmod -R 777 ~/Desktop/Share
	```

3. Check if a folder is created on your Desktop (I can hardly believe if it isn't, but just in case you type something wrong);

**Step 3. Configure SMB (on Cloudera)**

1. Open *Terminal*;
2. Enter the following commands to download our customized configuration file:

	```
	[cloudera@quickstart ~]$ cd ~/Desktop
	[cloudera@quickstart Desktop]$ wget https://raw.githubusercontent.com/90hours/imse785/master/smb.conf
	--2015-02-20 12:58:42--  https://raw.githubusercontent.com/90hours/imse785/master/smb.conf
	Resolving raw.githubusercontent.com... 23.235.40.133
	Connecting to raw.githubusercontent.com|23.235.40.133|:443... connected.
	HTTP request sent, awaiting response... 200 OK
	Length: 9980 (9.7K) [text/plain]
	Saving to: “smb.conf”

	100%[===================================================================================================================================>] 9,980       --.-K/s   in 0s

	2015-02-20 12:58:42 (25.3 MB/s) - “smb.conf” saved [9980/9980]

	[cloudera@quickstart Desktop]$ sudo mv smb.conf /etc/samba/smb.conf 
	```

**Step 4. Start *SMB* and *NMB* services (on Cloudera)**

*Unfortunately, you need to conduct this step every time you reboot your VM. :(*

1. Open *Terminal*;
2. Enter the following commands to start SMB and NMB services:

	```
	[cloudera@quickstart Desktop]$ sudo service smb start; sudo service nmb start
	Starting SMB services:                                     [  OK  ]
	Starting NMB services:                                     [  OK  ]
	```

**Step 5. Enjoy (on Windows)**

1. Go back to your Windows;
2. Press Windows Key + R to open *Run* Dialogue; 
3. Enter `"\\"` followed by your VM's IP, for example: `\\192.168.1.106` in my case;
4. You can start transferring files to/from this shared folder, which is also viewable on your VM's Desktop.
5. If you cannot connect after reboot, please double-check your VM's IP to make sure you are using the correct one. 

## Another notice: 

There is a new version of Virtual Box recently, we recommend all of  you to install the new release and keep your Virtual Box updated. 

<hr>
COPYRIGHT @ IMSE 785 by Dr. Shing-I Chang, KANSAS STATE UNIVERSITY