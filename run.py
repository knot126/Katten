#!/usr/bin/env python3
"""
Script to start Plus+ and Touch Pets servers
"""

import os
import subprocess
import tomllib
import time
from sys import argv
from pathlib import Path

katten_dir = str(Path(__file__).parent)

try:
	config = tomllib.loads(Path(katten_dir + "/runconfig.toml").read_text())
except:
	print("""You need to create a runconfig.toml next to this script with:
	- 'mongo_exec' set to the mongod executable name/path
	- 'mongo_db' set to the mongodb database path (folder)
	- 'mitmproxy_exec' set to the mitmproxy executable name/path""")
	os.exit(127)

def run(args, runpath=None):
	if runpath:
		print(f" -- chdir to {runpath}")
		os.chdir(runpath)
	
	print(f" -- execute {' '.join(args)}")
	return subprocess.Popen(args)

class RunMgr:
	def __init__(self):
		self.processes = []
		self.orig_cwd = os.getcwd()
	
	def run(self, cmd, runpath=None):
		self.processes.append(run(cmd, katten_dir + "/" + runpath if runpath else None))
	
	def poll(self):
		for proc in self.processes:
			proc.poll()
	
	def stop(self):
		for proc in self.processes:
			print(f' -- terminate pid {proc.pid}')
			
			proc.terminate()
			
			while proc.poll() == None:
				time.sleep(0.1)
		
		os.chdir(self.orig_cwd)

def main():
	mgr = RunMgr()
	
	mongo = "--no-mongo" not in argv
	touch_pets = "--no-touch-pets" not in argv
	mitm = "--no-mitmproxy" not in argv
	
	if mongo: mgr.run([config['mongo_exec'], '--quiet', '--dbpath', config['mongo_db']])
	mgr.run(['flask', 'run', '--debug', '--port', '5100'], 'plus')
	if touch_pets: mgr.run(['flask', 'run', '--debug', '--port', '5200'], 'touchpet')
	mgr.run(['flask', 'run', '--debug', '--host', '0.0.0.0', '--port', '5000'], 'router')
	if mitm: mgr.run([config['mitmproxy_exec'], '--mode=reverse:http://localhost:5000'])
	
	try:
		while True:
			mgr.poll()
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("Exiting...")
	
	mgr.stop()

if __name__ == "__main__":
	main()
