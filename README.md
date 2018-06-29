**README**

**server.py** is a minimal web server to perform remote operations on the Raspberry Pi via a web interface. Main operations are clean shutdown; restart; upload a file; view a log file.

**steering.py** is a tethered control script, using two wired buttons to manage steering via an H-Bridge on each wheel motor. Configuration of GPIO pins is via config.py

Both of these scripts are run on startup by the RPi, using the script /etc/rc.local

   sudo python3 /home/python/server/server.py &
   sudo python3 /home/python/server/steering.py &
   exit 0

