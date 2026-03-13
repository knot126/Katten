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

def run(args, runpath=None, env_vars={}):
	if runpath:
		print(f" -- chdir to {runpath}")
		os.chdir(runpath)
	
	procenv = dict(os.environ) | env_vars
	
	print(f" -- execute {' '.join(args)}")
	return subprocess.Popen(args, env=procenv)

class RunMgr:
	def __init__(self):
		self.processes = []
		self.orig_cwd = os.getcwd()
	
	def run(self, cmd, runpath=None, env_vars={}):
		self.processes.append(run(cmd, katten_dir + "/" + runpath if runpath else None, env_vars))
	
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
	--no-touch-pets        Do not start the touch pets server(s)
	--touch-pets <apps>    Start instances of touch pets for given game names (ex: cats,dogs2) instead of the default (only cats)
	--mitm <exec>          Run with mitmproxy, using command <exec> to start mitmproxy""")
		exit(127)
	
	touch_pets = "--no-touch-pets" not in argv
	tp_instances = (argv[argv.index("--touch-pets")+1]).split(",") if "--touch-pets" in argv else {"cats"}
	mitm_exec = (argv[argv.index("--mitm")+1]) if "--mitm" in argv else None
	router_port = '5000' if mitm_exec else '8080'
	
	mgr.run(['flask', 'run', '--debug', '--port', '5100'], 'plus')
	
	if touch_pets:
		if "cats" in tp_instances:
			mgr.run(['flask', 'run', '--debug', '--port', '5200'], 'touchpet')
		
		if "dogs2" in tp_instances:
			mgr.run(['flask', 'run', '--debug', '--port', '5201'], 'touchpet', {"TP_APPNAME": "dogs2"})
		
		if "dogs" in tp_instances:
			mgr.run(['flask', 'run', '--debug', '--port', '5202'], 'touchpet', {"TP_APPNAME": "dogs"})
	
	mgr.run(['flask', 'run', '--no-debug', '--host', '0.0.0.0', '--port', router_port], 'router')
	
	if mitm_exec:
		mgr.run([mitm_exec, '--mode=reverse:http://localhost:5000'])
	
	try:
		while True:
			mgr.poll()
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("Exiting...")
	
	mgr.stop()

if __name__ == "__main__":
	main()
