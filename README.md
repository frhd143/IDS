# IDS - File Integrity Checker


## Overview
This Python script is designed to check the integrity of files within a directory and its subdirectories. It accomplishes this by generating a hash value for each file and storing the hash value in a log file. By comparing the hash values of the current set of files with the hash values stored in the previous log file, the script can detect if any files have been modified, added, or removed.


## Requirements
- Python 3.x
- hashlib library


## Usage
1.  Place the `ids.py` file in the directory that you want to check.
2.  Open the terminal in that directory and run the script:
```sh
python3 ids.py
```
The script will generate a log file: hash_data_0.txt. hash_data_0.txt contains the current set of hash values for all files in the directory and its subdirectories.

3.  Add some files, delete some files, or modify some files.
4.  Run the script again:
```sh
python3 ids.py
```
The script will generate a log file hash_data_1.txt. This file is now considered the current set of hash values. The hash_data_0.txt is considered the previous set of hash values.  
The script will compare the hash values in hash_data_1.txt with those in hash_data_0.txt and print out any files that have been modified, added, or removed.
