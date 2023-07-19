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

$gDefaultMessages = [
	[
		"times_to_display" => 1000000,
		"title" => "Welcome to Katten Server!",
		"text" => "Welcome to the Katten Server project! Please remember you may find bugs or missing features.",
		"url" => "http://example.com",
		"alert" => true,
		"web_view" => false,
	]
];

function katten_unchecked_login(int $user_id, string $password) : array {
	global $gDefaultMessages;
	
	// Check if the user exists
	if (!user_exists($user_id)) {
		return [
			"success" => false,
			"error_msg" => "Wrong username or password?",
		];
	}
	
	// Open user and try to create session
	$user = new User($user_id);
	$session = new Session();
	
	$success = $session->create($user, $password);
	
	// Failed!
	if (!$success) {
		return [
			"success" => false,
			"error_msg" => "Wrong username or password?",
		];
	}
	
	// It worked!!
	$response = $session->package();
	$response["success"] = true;
	$response["profile"] = $user;
	$response["messages"] = $gDefaultMessages;
	
	return $response;
}

$gEndpoints->add("users", function (Context $context) {
	$user = new User();
	$user_data = $context->fromPost("user");
	$error = $user->create($user_data);
	
	// If there was an error, report it and stop
	if ($error) {
		$context->sendJson([
			"success" => false,
			"error_msg" => $error,
		]);
	}
	
	// Do a basic user login
	$response = katten_unchecked_login($user->id, $user_data["password"]);
	
	// Respond!
	$context->sendJson($response);
});

$gEndpoints->add("session", function (Context $context) {
	/**
	 * Oh dear god. This endpoint is used in so many ways and it's not the most
	 * consistent thing ever.
	 */
	
	global $gDefaultMessages;
	
	// Sign in using existing session
	if ($context->fromPost("auth_token")) {
		$auth_token = $context->fromPost("auth_token");
		
		if (session_exists($auth_token)) {
			$session = new Session($auth_token);
			$user = new User($session->user_id);
			
			// Why do we need this and why the fuck does this work???
			$user->success = true;
			$user->user_id = $user->id;
			
			$response = $session->package();
			$response["success"] = true;
			$response["profile"] = $user;
			$response["messages"] = $gDefaultMessages;
			
			$context->sendJson($response);
		}
		else {
			$context->sendJson([
				"success" => false,
			]);
		}
	}
	// Update device_token for push notifications (we dont do those)
	else if ($context->fromPost("device_token")) {
		$context->sendJson([
			"success" => true,
		]);
	}
	else {
		$context->sendJson([
			"success" => false,
			"error_msg" => "Katten Server does not support using this endpoint like that",
		]);
	}
});

$gEndpoints->add("oauth/authorize_new", function (Context $context) {
	/**
	 * Theoretically this does something with game-specific oauth tokens, but
	 * really I can't be bothered to implement that so it's not game specific
	 */
	
	$key = $context->fromPost("key");
	$fake = sha256("I don't know what I'm doing");
	
	$context->sendJson([
		"success" => true,
		"oauth_token" => $fake,
		"oauth_secret" => $fake,
	]);
});

function main() : void {
	global $gEndpoints;
	
	$context = new Context();
	
	$target = $context->fromGet("request");
	
	KtLog($context->fromGet("appname") . " -- Request for $target");
	KtLog("Data (json): " . json_encode($_POST));
	KtLog("Data (raw): " . file_get_contents("php://input"));
	// KtLog("Server info: " . json_encode($_SERVER));
	
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
