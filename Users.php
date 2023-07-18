<?php

$cUsers = new Collection("users");
$cSessions = new Collection("sessions");

class User {
	public $id;
	public $password;
	public $age_restricted;
	public $lite;
	public $gamertag;
	public $email;
	public $motto;
	public $first_name;
	public $last_name;
	public $birth_date;
	public $gender;
	public $opt_in;
	public $distribution_name;
	
	function __construct(?string $id = null) {
		global $cUsers;
		
		if ($id && $cUsers->has($id)) {
			KtLoadObject($this, $cUsers->load($id));
		}
		else if ($id) {
			die("Cannot load user by id $id: user does not exist");
		}
	}
	
	function save() : void {
		global $cUsers;
		$cUsers->save($this->id, $this);
	}
	
	function create(array $info) : ?string {
		/**
		 * Create the user data. Returns null on sucess, string with error
		 * details on failure.
		 */
		
		$this->id = KtCounterNext("userid");
		
		// Password
		if (!user_password_is_good($info["password"])) {
			return "Password must be at least 4 characters";
		}
		
		if ($info["password"] != $info["password_confirmation"]) {
			return "Password confirmation does not match";
		}
		
		$this->set_password($info["password"]);
		
		// Age restriction
		$this->age_restricted = (int) $info["age_restricted"];
		
		// Decide between lite and non-lite user info
		if (array_key_exists("lite", $info)) {
			$this->lite = (int) $info["lite"];
		}
		else {
			$this->lite = 0;
			
			// Gamertag
			if (strlen($info["gamertag"]) < 4) {
				return "Gamername should be at least 4 characters";
			}
			
			$this->gamertag = $info["gamertag"];
			
			// Everything else
			$this->email = $info["email"];
			$this->motto = $info["motto"];
			$this->first_name = $info["first_name"];
			$this->last_name = $info["last_name"];
			$this->birth_date = $info["birth_date"];
			$this->gender = $info["gender"];
			$this->opt_in = $info["opt_in"];
			
			if (array_key_exists("distribution_name", $info)) {
				$this->distribution_name = $info["distribution_name"];
			}
		}
		
		$this->save();
		
		return null;
	}
	
	function set_password(string $password) {
		$this->password = password_hash($password, PASSWORD_ARGON2ID);
	}
	
	function check_password(string $guess) {
		return password_verify($guess, $this->password);
	}
}

function user_exists(string $id) : bool {
	global $cUsers;
	
	return $cUsers->has($id);
}

function user_password_is_good(string $password) : bool {
	return strlen($password) >= 4;
}
