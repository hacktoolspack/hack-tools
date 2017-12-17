Random Occurence Algorithm
==========================

Copyright SavSec RoA © 2017

# About RoA

RoA started out as a basic visual algorithm. With this algorithm I decided to make an encryption based application that could allow for more security in python based communications! This lead to the development of a Python-Base Advanced AES Extension which adds more security to AES Encryption! The methods employed into this application make it 3 times more secure then regular AES on it's own! Risk of decryption via Ciphers is reduced due to the usage of multiple keys, data shifting, and advanced salting! Multiple keys are used to encrypt the unpacking information and the message being sent! The unpacking information lets the recipient rearrange the current data in order to reveal the second layer of encryption (This makes it so Encryption Cracking Applications not be able realize they got through the first layer if they get it correct) Once the second piece of data is revealed the program will decrypt that message by rearranging it to form the final message!

# Using RoA

RoA is extremely simple to use! All the main processes are taken care of automatically so you don't need to worry about messing things up while trying to decrypt or encrypt data with RoA! Here is an example:

```python
import RoA, time

Ro = RoA.RoA(True) # True activates verbose mode for advanced information

en_data = Ro.encrypt("Follow @Russian_Otter on Instagram!", Ro.generate_key("PythonRo"*4))
# The first argument for RoA.encrypt is your message that you want to encrypt!
# The second argument is your RoA Key which can be made by running RoA.generate_key followed by a 32bit key

# After this RoA will return a list of different values!:
#		Master Encrypted Dictionary
#		Rokey
#		AES Key

time.sleep(1)

decrypted = Ro.decrypt(en_data[0],en_data[1], en_data[2]) # The decrypt function interprets Master Encrypted Dictionary, The Ro Key, and The AES Key inorder to reverse the process and give you the text!
```
