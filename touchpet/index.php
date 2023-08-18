<?php

define("KATTEN_LOADED", 1);

require_once "../Utilities.php";
require_once "../Context.php";
require_once "../Endpoint.php";
require_once "../Database.php";

// It's ../ here, so this is a little hack :|
$gDatabasePath = "../katten.db/";

// Some contants for returning
define("KAT_ERROR_NOT_AUTHED", "Not authenticated");
define("KAT_ERROR_WRONG_VERSION", "Wrong version");
define("KAT_ERROR_SERVER_DOWN", "Server unavailable");
define("KAT_ERROR_INVALID_RECEIPT", "Invalid receipt");

// Log the post data
KtLog("Post data to touchpet/index.php:\n" . file_get_contents("php://input"));

// Player endpoint
$gEndpoints->add("player", function (Context $context) {
	$context->sendXml("<players></players>");
});

$gEndpoints->add("pets", function (Context $context) {
	$context->sendXml("<cats></cats>");
});

// Run the endpoint
$context = new Context();
$context->useXml();
$gEndpoints->run($context->fromPost("cmd"), $context);
