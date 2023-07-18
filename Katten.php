<?php

define("KATTEN_LOADED", 1);

require_once "Database.php";
require_once "Utilities.php";
require_once "Endpoint.php";
require_once "Context.php";
require_once "Users.php";

$gEndpoints->add("katten/test/getparams", function (Context $context) {
	$context->sendJson($_GET);
});

$gEndpoints->add("katten/ping", function (Context $context) {
	$context->sendJson([
		"success" => true,
	]);
});

$gEndpoints->add("users", function (Context $context) {
	$context->sendJson([
		"success" => true,
	]);
});

function main() : void {
	global $gEndpoints;
	
	$context = new Context();
	
	$target = $context->fromGet("request");
	$status = $gEndpoints->run($target, $context);
	
	if (!$status) {
		$context->sendJson([
			"success" => false,
			"error_msg" => "Katten Server does not support '$target'."
		]);
	}
	else {
		$context->send();
	}
}

main();
