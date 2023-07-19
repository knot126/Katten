<?php

if (!defined("KATTEN_LOADED")) {
	die("Should not be loading utils directly, or <code>KATTEN_LOADED</code> not defined.");
}

function KtDateTime() : string {
	return date("Y-m-d H:i:s", time());
}

function KtLog(string $what) : void {
	$dt = KtDateTime();
	$ip = KtGetClientIP();
	$host = $_SERVER["SERVER_NAME"];
	
	$file = fopen((is_dir("Logs") ? "Logs/katten.log" : "../../Logs/touchpet.log"), "a");
	
	if (!$file) {
		return;
	}
	
	fwrite($file, "$dt $host $ip -- $what\n");
	fclose($file);
}

function KtGetHeader(string $what) : ?string {
	$i = 'HTTP_' . str_replace("-", "_", strtoupper($what));
	
	return array_key_exists($i, $_SERVER) ? $_SERVER[$i] : null;
}

function KtGetClientIP() {
	return $_SERVER["REMOTE_ADDR"];
}

function KtRespondWithJson(object | array $data) : void {
	header("Content-Type: application/json");
	$s = json_encode($data);
	echo $s;
	KtLog("Response content: " . $s);
	die();
}

function KtError(string $message) : void {
	KtRespondWithJson([
		"success" => false,
		"error_msg" => $message,
	]);
}

function KtLoadObject(object &$to, object $from) {
	/**
	 * Load everything from object $from into object $to
	 */
	
	foreach (get_object_vars($from) as $key => $value) {
		$to->$key = $value;
	}
}

function KtRandomToken() : string {
	/**
	 * Cryptographically secure random token
	 */
	
	return bin2hex(random_bytes(32));
}

function KtCounterNext(string $id, int $first = 1) : int {
	/**
	 * For a global counter, get the next value.
	 */
	
	$c = new Collection("katten");
	
	// Setup counters on new install
	if (!$c->has("counters")) {
		$c->save("counters", ["_global" => 1]);
	}
	
	// Load counter data
	$counters = $c->load("counters");
	
	// If the counter exists, increment it
	if (property_exists($counters, $id)) {
		$counters->$id += 1;
	}
	// If it doesn't, initalise it
	else {
		$counters->$id = $first;
	}
	
	// Save global counters
	$c->save("counters", $counters);
	
	// Return current value
	return $counters->$id;
}
