# Some Notes ✏️🗒

This submission was written in Python 3 (3.5.1). This change can also be seen in the run.sh file, as I have explicitly used the command "python3". 

The imported packages are as follows (all of which are standard)
  * os
  * sys
  * datetime
  * bisect
  * operator

The first line in the main method uses an encoding of 'latin-1'. This is due to the fact that Python 3 automatically uses utf-8 when reading in the file. The problem with this is there is a symbol (0x80) that isn't defined in this encoding that appeared in the ~500MB file that could be downloaded. Having the file being read in as a byte would negatively affect many of the commonly used python functions such as split() and str(), which is why I used latin-1. 
