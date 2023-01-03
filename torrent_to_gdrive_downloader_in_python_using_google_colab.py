# -*- coding: utf-8 -*-
"""Torrent_To_Gdrive_Downloader_In_Python_Using_Google_Colab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qy7TNIA5OgGAPP6WVVzbPvlutEFoK7PX

# **Steps to download files into Gdrive**

**1 : Install The Python  Libraries**

**2 : Mount Your Google Drive Where You Want To Store The Data**

**3 : Start the Server**

### **Following steps for Google Drive Upload (Personal Drive)**

**4 : Upload .torrent File Or Paste Magnet Link [for GDrive]** 

**Note :- You can upload multiple files simultaneously**

**4 : Upload .torrent File Or Paste Magnet Link [for Team Drive]**

**5 : Start Cloud Upload**
"""

#@title # **1 : Install The Python  Libraries**
#@markdown <h3>⬅️ Click Here to Start Installing the Libraries</h3>
# Hiding the warnings
import warnings
warnings.filterwarnings("ignore")

# Installing the libraries
!pip install qiskit ipywidgets
!python -m pip install --upgrade pip setuptools wheel
!python -m pip install lbry-libtorrent
!pip install folium==0.2.1

#@title **2 : Mount Your Google Drive Where You Want To Store The Data**
#@markdown <h3>⬅️ Click Here to Start Mounting the drive</h3>
#@markdown <br><center><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Google_Drive_logo.png/600px-Google_Drive_logo.png' height="50" alt="Gdrive logo"/></center>
#@markdown <center><h3>Mount Gdrive to /content/drive</h3></center><br>

MODE = "MOUNT" #@param ["MOUNT", "UNMOUNT"]
#Mount your Gdrive! 

from google.colab import drive

drive.mount._DEBUG = False

if MODE == "MOUNT":
  drive.mount('/content/drive', force_remount=True)

elif MODE == "UNMOUNT":
  try:
    drive.flush_and_unmount()
    
  except Exception as e:
    print("Not able mount the Gdrive please run the cell again..!")
  
  get_ipython().system_raw("rm -rf /root/.config/Google/DriveFS")

#@title **3 : Start the Server**
#@markdown <h3>⬅️ Click Here to START server</h3>

!apt install python3-libtorrent

import libtorrent as lt

ses = lt.session()
ses.listen_on(6881, 6891)
downloads = []

from IPython.display import HTML, clear_output

clear_output()

print("Server Started Successfully")

"""# **Following steps for Google Drive Upload (Personal Drive)**
<br><center><img src='https://drive.google.com/uc?id=1iqeDl-Jdv6FyeswW4Jt7bDN-e6VdHMb2' height="100" /></center>

#**4 : Upload .torrent File Or Paste Magnet Link [for GDrive]**
"""

#@title **4 : Upload .torrent File [for GDrive]** 
#@markdown <h3>⬅️ Click Here to </h3>
#@markdown <h3>Upload torrent file</h3>
#@markdown <h5>You can run this cell to add more files as many times as you want</h5>
#@markdown <h5>No parallel downloading using .torrent files, use magnet for that</h5><br>


from google.colab import files

source = files.upload()
params = {
    "save_path": "/content/drive/My Drive/Torrent",
    "ti": lt.torrent_info(list(source.keys())[0]),
}
downloads.append(ses.add_torrent(params))

#@title **4 : Paste Magnet Link [for GDrive]** 
#@markdown <h3>⬅️ Click Here to </h3>
#@markdown <h3>Add From Magnet Link</h3>
#@markdown <h5>You can run this cell to add more files as many times as you want</h5><br>


params = {"save_path": "/content/drive/My Drive/Torrent"}

while True:
    magnet_link = input("Enter Magnet Link Or Type Exit: ")
    if magnet_link.lower() == "exit":
        break
    downloads.append(
        lt.add_magnet_uri(ses, magnet_link, params)
    )

"""# **Following steps for Team Drive Upload (Shared Drive)**
<br><center><img src='https://drive.google.com/uc?id=1AC4hpO-pE2FyHzTQBrwq27kGbZDOeVuO' height="100" /></center>

# **4 : Upload .torrent File Or Paste Magnet Link [for Team Drive]**

# **Provide a specific path / Location where you want to download the file**
"""

#@title **4 : Upload .torrent File [for Team Drive]**
#@markdown <h3>⬅️ Click Here to </h3>
#@markdown <h3>Upload torrent file</h3>
#@markdown <h5>You can run this cell to add more files as many times as you want</h5>
#@markdown <h5>Doesn't support parallel downloding, use magnet method for that</h5><br>

#@markdown <h3>Enter the path where you want to download the file :</h3>
path = "/content/drive/Shareddrives/Aman" #@param {type:"string"}
check=[]


from google.colab import files

source = files.upload()
params = {
    "save_path": path,
    "ti": lt.torrent_info(list(source.keys())[0]),
}
downloads.append(ses.add_torrent(params))

clear_output()

print("Started Successfully")

#@title **4 : Paste Magnet Link [for Team Drive]**
#@markdown <h3>⬅️ Click Here to </h3>
#@markdown <h3>Add From Magnet Link</h3>
#@markdown <h5>You can run this cell to add more files as many times as you want</h5><br>

#@markdown <h3>Enter the path where you want to download the file :</h3>
path = "/content/drive/Shared drives/Aman" #@param {type:"string"}
check=[]
params = {"save_path": path}

while True:
    magnet_link = input("Enter Magnet Link Or Type Exit: ")
    if magnet_link.lower() == "exit":
        break
    downloads.append(
        lt.add_magnet_uri(ses, magnet_link, params)
    )

clear_output()

print("Started Successfully")

#@title **5 : Start Cloud Upload**
#@markdown <h3>⬅️ Click Here to Start Download</h3>
import time
from IPython.display import display
import ipywidgets as widgets

state_str = [
    "queued",
    "checking",
    "downloading metadata",
    "downloading",
    "finished",
    "seeding",
    "allocating",
    "checking fastresume",
]

layout = widgets.Layout(width="auto")
style = {"description_width": "initial"}
download_bars = [
    widgets.FloatSlider(
        step=0.01, disabled=True, layout=layout, style=style
    )
    for _ in downloads
]
display(*download_bars)

while downloads:
    next_shift = 0
    for index, download in enumerate(downloads[:]):
        bar = download_bars[index + next_shift]
        if not download.is_seed():
            s = download.status()

            bar.description = " ".join(
                [
                    download.name(),
                    str(s.download_rate / 1000),
                    "kB/s",
                    state_str[s.state],
                ]
            )
            bar.value = s.progress * 100
        else:
            next_shift -= 1
            ses.remove_torrent(download)
            downloads.remove(download)
            bar.close() # Seems to be not working in Colab (see https://github.com/googlecolab/colabtools/issues/726#issue-486731758)
            download_bars.remove(bar)
            print(download.name(), "complete")
    time.sleep(1)