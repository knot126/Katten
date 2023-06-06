<?php

class EndpointManager {
	/**
	 * An manager for endpoints which allows endpoints to be registered in the
	 * file that they were created so we don't have to keep editing main.php to
	 * add new endpoints.
	 */
	
	private $endpoints;
	
	function __construct() {
		$this->endpoints = array();
	}
	
	function add(string $name, /*function*/ $func) {
		/**
		 * Add an endpoint function.
		 */
		
		$this->endpoints[$name] = $func;
	}
	
	function run(string $name, $context = null) : bool {
		/**
		 * Run an endpoint given a name for one. Returns if calling was
		 * successful.
		 */
		
		if (isset($this->endpoints[$name])) {
			$this->endpoints[$name]($context);
			return true;
		}
		else {
			return false;
		}
	}
}

$gEndpoints = new EndpointManager();
