import os, subprocess

keys = {
    '1':            '\x31',
    '2':            '\x32',
    's':            '\x73',
    'w':            '\x77',
    'x':            '\x78',
    'p':            '\x70',
    'z':            '\x7a',
    '+':            '\x2b',
    '-':            '\x2d',
    '.':            '\x2e',
    'space':        '\x20',
    'left-arrow':   '\x1b\x5b\x44',
    'right-arrow':  '\x1b\x5b\x43',
    'up-arrow':     '\x1b\x5b\x41',
    'down-arrow':   '\x1b\x5b\x42',
}

def checkForPipe(pipe_path):
    pipe_dir = os.path.dirname(pipe_path)
    if not os.path.exists(pipe_dir):
        os.makedirs(pipe_dir)

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
        print 'OMXPlayer: created new pipe', pipe_path

def isPlayerRunning():
    process = subprocess.Popen('ps cax | grep omxplayer', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout_list = filter(None, process.communicate()[0].split('\n'))

    return len(stdout_list) > 0

def sendCommand(cmd, pipe_path):
    cmd = cmd + ' > ' + pipe_path + ' &'
    return os.system(cmd) == 0

def sendKey(key, pipe_path):
    if key not in keys:
        return False

    return sendCommand('echo -n "' + keys[key] + '"', pipe_path)

def killPlayer():
    if isPlayerRunning():
        os.system('killall omxplayer.bin')

def playFile(path, omx_path, pipe_path):
    if isPlayerRunning():
        killPlayer()

    if not os.path.exists(path):
        return False

    s1 = os.system('sudo ' + omx_path + ' -p -o hdmi "' + path + '" <' + pipe_path + ' &') == 0
    s2 = sendKey('z', pipe_path)

    return s1 and s2
