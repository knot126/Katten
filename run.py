#!/usr/bin/env python3
"""
Script to start Plus+ and Touch Pets servers
"""

import os
import subprocess
import tomllib
import time
from sys import argv, exit
from pathlib import Path

katten_dir = str(Path(__file__).parent)

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
	
	if '-h' in argv or '--help' in argv:
		print(f"""Start Katten Server\n\n{argv[0]} [OPTIONS]\n\nAvailable options:
	--no-touch-pets     Do not start the touch pets server(s)
	--mitm <exec>       Run with mitmproxy, using command <exec> to start mitmproxy""")
		exit(127)
	
	touch_pets = "--no-touch-pets" not in argv
	mitm_exec = (argv[argv.index("--mitm")+1]) if "--mitm" in argv else None
	router_port = '5000' if mitm_exec else '8080'
	
	# if mongo: mgr.run([config['mongo_exec'], '--quiet', '--dbpath', config['mongo_db']])
	mgr.run(['flask', 'run', '--debug', '--port', '5100'], 'plus')
	if touch_pets: mgr.run(['flask', 'run', '--debug', '--port', '5200'], 'touchpet')
	mgr.run(['flask', 'run', '--debug', '--host', '0.0.0.0', '--port', router_port], 'router')
	if mitm_exec: mgr.run([mitm_exec, '--mode=reverse:http://localhost:5000'])
	
	try:
		while True:
			mgr.poll()
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("Exiting...")
	
	mgr.stop()

if __name__ == "__main__":
	main()
