#!/usr/bin/python
import os
import psutil
import time
import sys
import notify2
from PyQt5 import QtCore, QtGui, QtWidgets


DEBUG = False
LOG = False
TRAY_TOOLTIP = 'Wireguard applet' 
TRAY_ICON_CONNECTED = '/home/fdlsifu/Documents/tools/wireguard-applet/vpn-on.png' 
TRAY_ICON_NOTCONNECTED = '/home/fdlsifu/Documents/tools/wireguard-applet/vpn-off.png'

TUN_PATH = '/sys/class/net/wgclient'

state = {'RUNNING':0,'NOTRUNNING':1}


def log(msg,type='info'):
    output = ''
    if type == 'info':
        output += '[INFO]'
    elif type == 'error':
        output += '[ERROR]'
    elif DEBUG and type == 'debug':
        output += '[DEBUG]'
    output +='Wireguard-applet: ' + msg
    
    if LOG == True:
        print(output)

def dlog(msg):
    log(msg,type='debug')


class Worker(QtCore.QRunnable):

    def run(self):
        dlog("main loop start")
        time.sleep(1)
        dlog("main loop end")

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)

        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(self.exit)

        self.setContextMenu(self.menu)
        
        # Thread work 
        self.timer = QtCore.QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.work)
        self.timer.start()

        self.vpn_connected = SystemTrayIcon.check_vpn_connected()
        try:
            notify2.init("Wireguard init")
            self.notif = True
        except:
            self.notif = False
            pass

    def changeIcon(self,icon):
        self.setIcon(QtGui.QIcon(TRAY_ICON_CONNECTED))

    def run(self):
        dlog("SystemTrayIcon started")
        return

    def exit(self):
        QtCore.QCoreApplication.exit()

    def work(self):
        # check vpn connection
        # change icon accordingly
        # popup on connection
        # popup on disconnect

        new_state = SystemTrayIcon.check_vpn_connected()
        
        if not self.vpn_connected and new_state:
            self.setIcon(QtGui.QIcon(TRAY_ICON_CONNECTED))
            self.vpn_connected = new_state
            if self.notif:
                n = notify2.Notification("Wireguard VPN Connected")
                # Set the urgency level
                n.set_urgency(notify2.URGENCY_NORMAL)
                # Set the timeout
                n.set_timeout(1000)
                n.show()

        elif self.vpn_connected and not new_state:
            self.setIcon(QtGui.QIcon(TRAY_ICON_NOTCONNECTED))
            self.vpn_connected = new_state
            if self.notif:
                n = notify2.Notification("Wireguard VPN disconnected")
                # Set the urgency level
                n.set_urgency(notify2.URGENCY_NORMAL)
                # Set the timeout
                n.set_timeout(1000)
                n.show()
        dlog("wake up to work")
        return
    
    @staticmethod
    def check_vpn_connected():
        if os.path.isdir(TUN_PATH):
            log('vpn connected')
            return True
        log('vpn not connected')
        return False


def parseargs():
    global LOG
    if len(sys.argv) == 1:
        return
    if sys.argv[1] == "-v":
        LOG = True
        log("log activated")

def launch_app():
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    if SystemTrayIcon.check_vpn_connected():
        trayIcon = SystemTrayIcon(QtGui.QIcon(TRAY_ICON_CONNECTED), w)
    else:
        trayIcon = SystemTrayIcon(QtGui.QIcon(TRAY_ICON_NOTCONNECTED), w)

    trayIcon.show()
    trayIcon.run()
    sys.exit(app.exec_())


def main():
    parseargs()
    
    time.sleep(1)
    launch_app()

if __name__ == '__main__':
    main()
