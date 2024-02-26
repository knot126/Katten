<?php

$cUsers = new Collection("users");
$cSessions = new Collection("sessions");

#[AllowDynamicProperties]
class User {
	/**
	 * Info about a user and some auth info
	 */
	
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
	public $data;
	
	function __construct(null | string | int $id = null) {
		global $cUsers;
		
		if ($id && $cUsers->has($id)) {
			KtLoadObject($this, $cUsers->load($id));
			$this->data = new DataItems($this->data);
		}
		else if ($id) {
			KtError("Cannot load user by id $id: user does not exist");
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
			$this->gamertag = "Player$this->id";
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
		
		$this->data = new DataItems();
		
		$this->save();
		
		return null;
	}
	
	function set_password(string $password) : void {
		$this->password = password_hash($password, PASSWORD_ARGON2ID);
	}
	
	function check_password(string $guess) : bool {
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

class Session {
	/**
	 * Account session
	 */
	
	public $id;
	public $user_id;
	
	function __construct(?string $id = null) {
		global $cSessions;
		
		if ($id && $cSessions->has($id)) {
			KtLoadObject($this, $cSessions->load($id));
		}
		else if ($id) {
			KtError("Cannot load session by name $id: session does not exist");
		}
	}
	
	function save() : void {
		global $cSessions;
		$cSessions->save($this->id, $this);
	}
	
	function create(User $user, string $password) : bool {
		/**
		 * Create a new session using the user's name and password
		 */
		
		if (!$user->check_password($password)) {
			return false;
		}
		
		$this->id = KtRandomToken();
		$this->user_id = $user->id;
		
		$this->save();
		
		return true;
	}
	
	function package() : array {
		/**
		 * Package sessions info into the format the games want
		 * 
		 * This will include the user's id and oauth tokens
		 */
		
		return [
			"user_id" => $this->user_id,
			"oauth_token" => $this->id,
			"oauth_secret" => $this->id,
			"oauth2_token" => $this->id,
			"auth_token" => $this->id,
		];
	}
}

function session_exists(string $id) : bool {
	global $cSessions;
	
	return $cSessions->has($id);
}

#[AllowDynamicProperties]
class DataItems {
	public $items;
	
	function __construct(null | array | object $items = null) {
		if (is_array($items)) {
			$this->items = $items;
		}
		else if (is_object($items)) {
			$this->items = get_object_vars($items);
		}
		else {
			$this->items = ["__items__" => null];
		}
	}
	
	function getRealPath(array $path) : string {
		return join(".", $path);
	}
	
	function get(array $path, mixed $default = null) : mixed {
		$path = $this->getRealPath($path);
		return array_key_exists($path, $this->items) ? $this->items[$path] : $default;
	}
	
	function set(array $path, mixed $data) : string {
		$path = $this->getRealPath($path);
		$this->items[$path] = $data;
		return $path;
	}
	
	function pget(int $cat, int $prop, mixed $default = null) : mixed {
		return $this->get(["PetCat.$cat.$prop"], $default);
	}
	
	function pset(int $cat, int $prop, mixed $val) : void {
		$this->set(["PetCat.$cat.$prop"], $val);
	}
}
