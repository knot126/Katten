<?php

function match_to_key(array $regexes, string $value) : mixed {
	/**
	 * Return the first regex that matches with the given value
	 */
	
	for ($i = 0; $i < sizeof($regexes); $i++) {
		$match = preg_match("~^" . $regexes[$i] . "$~", $value);
		
		if ($match) {
			return $regexes[$i];
		}
	}
	
	return null;
}

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
		
		$first_match = match_to_key(array_keys($this->endpoints), $name);
		
		if ($first_match) {
			$this->endpoints[$first_match]($context);
			return true;
		}
		else {
			// Run the default enpoint if it exists
			if (array_key_exists("@default", $this->endpoints)) {
				$this->endpoints["@default"]($context);
			}
			
			return false;
		}
	}
}

$gEndpoints = new EndpointManager();
