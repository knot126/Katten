<?php

define("KATTEN_LOADED", 1);

// It's ../ here, so this is a little hack :|
$gDatabasePathOverride = "../katten.db/";

// Include the required stuff
require_once "../Utilities.php";
require_once "../Context.php";
require_once "../Endpoint.php";
require_once "../Database.php";
require_once "../Users.php";

// Some contants for returning
define("KAT_ERROR_NOT_AUTHED", "Not authenticated");
define("KAT_ERROR_WRONG_VERSION", "Wrong version");
define("KAT_ERROR_SERVER_DOWN", "Server unavailable");
define("KAT_ERROR_INVALID_RECEIPT", "Invalid receipt");

// Log the post data
KtLog("Post data to touchpet/index.php:\n" . file_get_contents("php://input"));

// Player endpoint
$gEndpoints->add("player", function (Context $context) {
	$info = "<players>";
	$info .= "<player>";
	// It seems like the game initialises a lot of things much further than if this
	// is set than it isn't set.
	$info .= '<property category="10" id="0">1</property>';
	
	for ($i = 0; $i < 10000; $i++) {
		$info .= '<inventory inventoryID="' . "$i" . '" known="1" rewarded="0" owned="1" gifted="0" timeacquired="1692404008" quantity="99" decaystate="0"/>';
	}
	
	$info .= "</player>";
	$info .= "</players>";
	
	$context->sendXml($info);
});

$gEndpoints->add("setplayerproperty", function (Context $context) {
	$session = new Session($context->fromPost("sessionToken"));
	$user = new User($session->user_id);
	
	$igt = $context->fromPost("ifgreaterthan");
	$value = $context->fromPost("propertyvalue");
	$cat = $context->fromPost("categoryID");
	$id = $context->fromPost("propertyID");
	
	if ($igt === null || $value > ((int) $igt)) {
		$user->data->pset($cat, $id, $value);
		$user->save();
	}
	
	$context->sendXml("<players></players>");
});

$gEndpoints->add("pets", function (Context $context) {
	$context->sendXml("<pets></pets>");
});

// $gEndpoints->add("@default", function (Context $context) {
// 	$context->sendXml("<results></results>"); // see what this does ...
// });

// Run the endpoint
$context = new Context();
$context->useXml();
$gEndpoints->run($context->fromPost("cmd"), $context);
