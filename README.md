# SSH Manager
![Main menu](https://github.com/Yarosvet/SSH-Manager/raw/master/screenshots/menu.png)

**A simple and convenient ssh manager written on Python3.**
___
*You can use a compiled binary from releases.*
# Run
```bash
pip3 install -r requirements.txt
python3 main.py
```
# Build
Install *pyinstaller*
```bash
pip3 install pyinstaller
```
And build binary
```bash
pyinstaller -F main.py -n sshman
```
The binary file will be exported to *dist* directory

You can add it to /bin
```bash
sudo cp sshman /usr/local/bin/sshman
```
