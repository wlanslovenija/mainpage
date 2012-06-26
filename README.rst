Wlan Slovenia main webpage
==========================
http://wlan-si.net/

How to install for development
------------------------------

1. Clone from GitHub::

    git clone https://github.com/wlanslovenija/mainpage.git

2. Create and activate new virtual environment::

    virtualenv ~/.virtualenv/mainpage
    source ~/.virtualenv/mainpage/bin/activate
    
3. Move to location where you cloned mainpage and run devsetup script::

    python scripts/devsetup.py
    
   This script will install all requirements and load data to local database.
4. Start developing!