# CJExploiter
CJExploiter is drag and drop ClickJacking exploit development assistance tool. First open the "index.html" with your browser locally and enter target URL and click on "View Site". You can dynamically create your own inputs. Finally by click the "Exploit It" you can see the P0C.

Feel free to make pull requests, if there's anything you feel we could do better.
![ScreenShot](https://raw.githubusercontent.com/enddo/CJExploiter/master/main.png)
##Summery
Clickjacking, also known as a "UI redress attack", is when an attacker uses multiple transparent or opaque layers to trick a user into clicking on a button or link on another page when they were intending to click on the the top level page. Thus, the attacker is "hijacking" clicks meant for their page and routing them to another page, most likely owned by another application, domain, or both.

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker. [OWASP](https://www.owasp.org/index.php/Clickjacking)

You can use this tool to generate dynamic P0C.
