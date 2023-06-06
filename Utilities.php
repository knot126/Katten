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
	
	$file = fopen("katten.log", "a");
	fwrite($file, "$dt $ip -- $what\n");
	fclose($file);
}

function KtGetHeader(string $what) : string {
	return $_SERVER['HTTP_' . str_replace("-", "_", strtoupper($what))];
}

function KtGetClientIP() {
	return $_SERVER["REMOTE_ADDR"];
}

function KtRespondWithJson(object | array $data) : void {
	header("Content-Type: application/json");
	echo json_encode($data);
	die();
}
