<?php
/**
 * This code was taken from another project.
 */

if (!defined("KATTEN_LOADED")) {
	die("Should not be loading utils directly, or <code>KATTEN_LOADED</code> not defined.");
}

/**
 * TODO:
 * 
 * - Database locks. These are important!
 */

$gDatabasePath = "./katten.db/";

class RDBObject {
	/**
	 * RevisionDB object container
	 */
	
	public $revisions;
	public $rdb_;
	
	function __construct(object $source) {
		// Check if RevisionDB is already supported. If not enable it.
		if (property_exists($source, "rdb_")) {
			$this->revisions = $source->revisions;
			$this->rdb_ = 1;
		}
		else {
			$this->revisions = array($source);
			$this->rdb_ = 1;
		}
	}
	
	function at(int $index = -1) {
		/**
		 * Return the revision at the given index. If index is -1, then the newest
		 * revision is returned.
		 */
		
		if ($index == -1) {
			$index = sizeof($this->revisions) - 1;
		}
		
		return $this->revisions[$index];
	}
	
	function top() {
		/**
		 * Return the top (current) revision
		 */
		
		return $this->at();
	}
	
	function add($item) {
		/**
		 * Add a new revision.
		 */
		
		$this->revisions[] = $item;
	}
	
	function revert(int $index) {
		/**
		 * Revert to the revision at index.
		 */
		
		$this->add($this->at($index));
	}
	
	function size() {
		/**
		 * Return the number of revisions.
		 */
		
		return sizeof($this->revisions);
	}
}

class Collection {
	/**
	 * Represtnation of a database collection and various actions on it.
	 */
	
	public $path;
	
	function __construct(string $name) {
		global $gDatabasePath;
		
		$this->path = $gDatabasePath . $name . "/";
		
		// Make database folder if it doesn't exist
		if (!file_exists($this->path)) {
			mkdir($this->path, 0777, true);
		}
	}
	
	function get_item_path(string | int $item) : string {
		/**
		 * Get the path to the file in the database.
		 */
		
		return $this->path . str_replace("/", "", "$item");
	}
	
	function load(string | int $item) : object | array | null {
		/**
		 * Load a database object
		 */
		
		$path = $this->get_item_path($item);
		
		$file = fopen($path, "r");
		
		// Need to clear cache to make sure things work; otherwise there are bugs.
		clearstatcache();
		
		$json_data = fread($file, filesize($path));
		
		$data = json_decode($json_data);
		
		fclose($file);
		
		return $data;
	}
	
	function save(string | int $item, $data) : void {
		/**
		 * Save a database object
		 */
		
		$file = fopen($this->get_item_path($item), "w");
		fwrite($file, json_encode($data));
		fclose($file);
	}
	
	function delete(string | int $item) : void {
		/**
		 * Remove a database object
		 */
		
		unlink($this->get_item_path($item));
	}
	
	function has(string | int $item) : bool {
		$path = $this->get_item_path($item);
		
		return file_exists($path) && !is_dir($path);
	}
	
	function enumerate() : array {
		$array = scandir($this->get_item_path(""));
		array_shift($array);
		array_shift($array);
		return $array;
	}
}

class RevisioningCollection {
	/**
	 * A collection which supports revisioing. It can be used as a drop in replacement
	 * for the normal Collection.
	 */
	
	public $db;
	
	function __construct(string $name) {
		$this->db = new Collection($name);
	}
	
	function load(string $item, int $index = -1) {
		/**
		 * Load a revision (or the latest if not specified)
		 */
		
		$data = $this->db->load($item);
		
		// RDBObject's constructor will take care of the case that this isn't
		// already an RDBObject for us :)
		$obj = new RDBObject($data);
		
		return $obj->at($index);
	}
	
	function save(string $item, $newdata) : void {
		/**
		 * Save a new revision
		 */
		
		// Load current version info
		$data = null;
		
		if ($this->db->has($item)) {
			$data = $this->db->load($item);
		}
		else {
			$data = new stdClass();
			$data->rdb_ = 1;
			$data->revisions = array();
		}
		
		// Constuct the RDB Object
		// We can do this transparently since RDBObject will auto-create itself
		// if this isn't already an RDBObject
		$obj = new RDBObject($data);
		
		// Add the new revision
		$obj->add($newdata);
		
		// Save the new RDBObject
		$this->db->save($item, $obj);
	}
	
	function delete(string $item) : void {
		$this->db->delete($item);
	}
	
	function has(string $item) : bool {
		return $this->db->has($item);
	}
	
	function enumerate() : array {
		return $this->db->enumerate();
	}
	
	function history(string $item) : array {
		/**
		 * Return the revision history for a given item as
		 * 
		 * array(
		 *     object(
		 *         author: string,
		 *         updated: int,
		 *         reason: string
		 *     ),
		 *     ...
		 * )
		 */
		
		$data = $this->db->load($item);
		
		// Array to hold history info
		$history = array();
		
		$obj = new RDBObject($data);
		
		for ($i = 0; $i < $obj->size(); $i++) {
			$revision = $obj->at($i);
			
			// Check if there is an author feild, if so use it instead
			$author = "Unknown author";
			
			if (property_exists($revision, "author")) {
				$author = $revision->author;
			}
			
			// Check if there is an updated feild, and use if so
			$updated = 0;
			
			if (property_exists($revision, "updated")) {
				$updated = $revision->updated;
			}
			
			// Check if there is a reason feild, and use if so
			$reason = "No reason given";
			
			if (property_exists($revision, "reason")) {
				$reason = $revision->reason;
			}
			
			// Create the info object
			$info = new stdClass();
			$info->author = $author;
			$info->updated = $updated;
			$info->reason = $reason;
			
			$history[] = $info;
		}
		
		return $history;
	}
}

function enumerate_stores() {
	/**
	 * Enumerate available database stores
	 */
	
	global $gDatabasePath;
	
	$array = scandir($gDatabasePath);
	array_shift($array);
	array_shift($array);
	return $array;
}

function backup_database() : string {
	/**
	 * Back up the databse to a zip file
	 */
	
	global $gDatabasePath;
	
	$zip = new ZipArchive();
	
	$filename = "../data/store/smashhitlab_" . date("Y-m-d_His", time()) . ".zip";
	
	$zip->open($filename, ZIPARCHIVE::CREATE);
	$zip->addEmptyDir("db");
	
	$stores = enumerate_stores();
	
	for ($j = 0; $j < sizeof($stores); $j++) {
		$db = new Collection($stores[$j]);
		$files = $db->enumerate();
		
		$zip->addEmptyDir("db/" . $stores[$j]);
		
		for ($i = 0; $i < sizeof($files); $i++) {
			$zip->addFile($gDatabasePath . "/" . $stores[$j] . "/" . $files[$i], "db/" . $stores[$j] . "/" . $files[$i]);
		}
	}
	
	$zip->close();
	
	return $filename;
}
