# Ddos-http-layer-7-using-python
Bypass 503 clodflare  and launch attack from different elastic public ip's
there is two method

before follow this instructions https://github.com/Anorov/cloudflare-scrape <br/>
# AMI Linux user

 
 sudo yum update <br/>
 sudo yum install python<br/>
 sudo easy_install pip<br/>
 sudo pip install cfscrape <br/>
 sudo pip install requests_toolbelt<br/>
 curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.32.0/install.sh | bash <br/>
 . ~/.nvm/nvm.sh <br/>
 nvm install 4.4.5 <br/>
 node -v <br/>
 vi thread.txt (save as empty) <br/>


# ubuntu user
sudo apt-get update<br/>
sudo apt-get install python<br/>
sudo apt-get install python-pip<br/>
pip install cfscrape<br/>
apt-get install nodejs<br/>
pip install requests_toolbelt<br/>
vi thread.txt (empty) <br/>

# method 1
  usage :<br/>
  python tr503_alternative.py <first-private-ip-of-n/w-interface> <how-much-ip> <no-of-threads> <br/>
  example : python tr503_alternative.py 172.31.42.22 30 100
  
# method 2
  usage :<br/>
  mkdir session <br/>
  
  
  if the site is not under dos attack mode (503 checking your browser before accessing site)<br/>
  python tr200.py "first-private-ip-of-n/w-interface" "how-much-ip" <br/>
  
  After 503<br/>
  python scraper503.py "first-private-ip-of-n/w-interface" "how-much-ip"  "char" <br/>
  python tr503.py "first-private-ip-of-n/w-interface" 'how-much-ip"  <br/>
  
  To increase thread level at Runtime <br/>
  change the values in thread.txt to increase threads 
  
  
  
  
