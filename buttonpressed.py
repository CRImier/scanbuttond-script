#!/usr/bin/env python
import os
import sys
import subprocess
import datetime

flag = "/tmp/scanbuttond.lock"

def execute(*args):
    """Comfortable subprocess wrapper to call external programs"""
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
        return [0, output]
    except subprocess.CalledProcessError as e:
        return [int(e.returncode), e.output]

def get_file_dir():
    """Pybssort wrapper to get scanning directory"""
    output = execute("pybssort dir")
    if output[0] == 0:
        return output[1].strip('\n') #In case of successful call directory name is in output[1]
    else:
        log("Problem while executing 'pybssort', output enclosed:")
        log(repr(output))
        return None

def convert(filename):
    """Uses CLI imagemagick 'convert' to convert images"""
    output = execute("convert "+filename+".tiff "+filename+".jpg")
    os.remove(filename+".tiff")
    if output[0] == 0:
        return True
    else:
        log("Problem while executing 'convert', output enclosed:")
        log(repr(output))
        return None

def scan(filename):
    """Executes scanimage with given parameters"""
    scan_command = 'scanimage --format=tiff --resolution 300 --mode Gray --gamma-correction "High contrast printing" > '+filename+'.tiff'
    output = execute(scan_command)
    if output[0] == 0:
        return True
    else:
        log("Problem while executing 'scanimage', output enclosed:")
        log(repr(output))
        return None

def choose_filename():
    """Chooses filename for an image file from all the available filenames """
    try:
        filenames = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    except KeyError:
        filenames = []
    counter = 0
    new_filename = 'scan_000.jpg'
    while new_filename in filenames:
        counter +=1
        new_filename = 'scan_'+str(counter).zfill(3)+'.jpg'
    log(new_filename)
    return 'scan_'+str(counter).zfill(3)

def log(data):
    """Writes data into a logfile adding a timestamp """
    f = open("/etc/scanbuttond/buttonpressed.log", "a")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(timestamp+"    "+str(data)+"\n")
    f.close()

def make_success_sound():
    """Makes a success sound """
    execute("aplay /etc/scanbuttond/success.wav")

def make_failure_sound():
    """so sad
    many tears
    poor program
    wow"""
    execute("aplay /etc/scanbuttond/error.wav")

def make_flag():
    """ Makes a lockfile to prevent race conditions"""
    open(flag, 'a').close()

def flag_exists():
    """Checks if the lockfile exists"""
    return os.path.isfile(flag)

def delete_flag():
    """Deletes the lockfile"""
    try:
        os.remove(flag)
    except OsError:
        pass

def logger(message):
    """Executes system 'logger' to log important data"""
    execute("logger "+message)

def exit(num):
    """Exits doing some necessary things"""
    delete_flag()
    if num == 0:
        make_success_sound()
        log("Successfully scanned file")
        sys.exit(0)
    else:
        make_failure_sound()
        log("Something went wrong, error code: "+str(num))
        sys.exit(num)

#And now for the main routine.
if __name__ == "__main__":
    #Check for a flag, if exists, exit.
    if flag_exists():
        log("Called while already running")
        exit(2)

    #Make a temporary flag file so that 2 instances don't run at the same time
    make_flag()
    
    #Get a directory
    directory = get_file_dir()
    if not directory:
        log("Terminating because of pybssort problem")
        exit(3)

    #Change current path to that directory
    os.chdir(directory)

    #Generate the filename
    filename = choose_filename()

    #Scan the image
    result = scan(filename)
    if not result:
        log("Terminating because of scanimage failure")
        exit(4)

    #Convert the image
    result = convert(filename)
    if not result:
        log("Terminating because of convert failure")
        exit(5)

    #Everything has been OK - so let's finish!
    logger(filename)
    exit(0)


