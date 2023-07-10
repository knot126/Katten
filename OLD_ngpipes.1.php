<?php

define("KATTEN_LOADED", 1);
require_once "Utilities.php";
require_once "Endpoint.php";

// Fake profile info
$gFakeProfile = [
	"user_id" => 1,
	"gamertag" => "Katten Server",
	"badge_id" => 0,
	"photo_url" => null,
	"motto" => "Katten Server!",
	"email" => "kitty@cat.net",
	"email_hash" => md5("kitty@cat.net"),
	"phone_number" => "000-000-0000",
	"password" => "letmein",
	"first_name" => "Katten",
	"last_name" => "Server",
	"fullname_privacy" => true,
	"age_restricted" => true,
	"new_buddy" => false,
	"mutual_friends" => false,
	// "capabilities" => [], -- seems to crash the game
	"hide_presence" => false,
	"friend_only_notification" => false,
	"lite" => false,
	"gamerscore" => 0,
	"level_position" => 1,
	"level_name" => "Unknown",
	"level_points" => 0,
	"level_next_points" => 10000,
	"games" => ["PetCat"],
];

// Log the body of the request
$method = $_GET["real_url"];
KtLog("real_url = $method");

if ($contents = file_get_contents("php://input")) {
	KtLog("POST body: " . urldecode($contents));
}

//die();

// Respond to it
switch ($method) {
	// This seems to be the user creation endpoint, for some reason.
	// Any way, I am not currently RE'ing the login endpoint.
	case "users":
		KtLog("Respond to /users");
		KtRespondWithJson([
			"success" => true,
			"auth_token" => "letmein",
			"oauth_token" => "letmein",
			"oauth_secret" => "letmein",
			// i added these and they seem to crash but it might be due
			// to me already having a user account created
			//"configuration" => [],
			//"messages" => [],
		]);
		break;
	
	// !!! PROBABLY DOESNT WORK !!! //
	case "oauth/authorize_new":
		KtLog("Respond to /oauth/authorize_new");
		KtRespondWithJson([
			"target" => null,
			"action" => null,
			"tokens" => [
				"oauth_token" => "letmein",
				"oauth_secret" => "letmein",
				"user_id" => 1,
			],
			//"error" => false,
		]);
		break;
	
	case "session":
		if (array_key_exists("auth_token", $_POST)) {
			KtLog("Respond to /session (auth token)");
			KtRespondWithJson([
				"success" => false,
			]);
			// KtRespondWithJson([
			// 	"success" => true,
			// 	"gamertag" => "none",
			// 	"badge_id" => 0,
			// ]);
			// KtRespondWithJson([
			// 	"success" => true,
			// 	"auth_token" => "letmein",
			// 	"gamertag" => "none", // <- don't know if this does anything
			// 	"badge_id" => 0,
			// 	"oauth_token" => "letmein",
			// 	"oauth_secret" => "letmein",
			// 	"profile" => $gFakeProfile,
			// ]);
		} else if (array_key_exists("device_token", $_POST)) {
			KtLog("Respond to /session (device token)");
			KtRespondWithJson([
				"success" => true,
			]);
		}
		break;
	
	// The 1 here should really be the user id but oh well :-)
	case "users/1":
		KtLog("Respond to /users/1");
		KtRespondWithJson($gFakeProfile);
		break;
	
	case "users/1/achievements":
		KtLog("Respond to /users/1/achievements");
		KtRespondWithJson([
			"success" => true,
			"user_id" => 1,
			"achievements" => [],
		]);
		break;
	
	case "users/1/buddies":
		KtLog("Respond to /users/1/buddies");
		KtRespondWithJson([
			"success" => true,
			"list" => [],
			"offset" => 0,
			"total" => 0,
		]);
		break;
	
	// I think it doesn't really like this either ...
	case "user_updates":
		KtLog("Respond to /user_updates");
		KtRespondWithJson([
			"success" => true,
			"update_interval" => 10.0,
			"online_friends" => [],
			"updates" => [],
		]);
		break;
	
	case "social_accounts/search":
		KtLog("Respond to /social_accounts/search");
		KtRespondWithJson([
			"success" => true,
			"social_accounts" => [],
		]);
		break;
	
	// Not really sure what it's used for ...
	case "games":
		// KtLog("Respond to /games");
		// KtRespondWithJson([
		// 	"success" => true,
		// 	"games" => [],
		// ]);
		$host = KtGetHeader("Host");
		KtRespondWithJson([
			"success" => true,
			"games" => [
				[
					"app_key" => "PetCat",
					"name" => "PetCat",
					"icon_url" => "http://$host/PetCat.png",
					"publisher" => "ngmoco",
					"catalog_url" => "http://none.invalid/",
					"feed_url" => "http://none.invalid/",
					"app_store_url" => "http://none.invalid/",
					"master_product_id" => "PetCat",
					"featured" => false,
					"leaderboards_count" => 0,
					"achievements_count" => 0,
				],
			],
			
		]);
		break;
}

// just in case
// UPDATE: The game does not like this change and crashes.
// KtRespondWithJson([]);
