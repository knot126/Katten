<?php

class Context {
	public $request_body;
	public $response_body;
	public $content_type;
	
	function __construct() {
		$this->request_body = "";
		$this->response_body = "";
		$this->content_type = "application/json";
	}
	
	function fromGet(string $key) : ?string {
		$value = null;
		
		if (array_key_exists($key, $_GET)) {
			$value = $_GET[$key];
		}
		
		return $value;
	}
	
	function fromPost(string $key) : ?string {
		$value = null;
		
		if (array_key_exists($key, $_POST)) {
			$value = $_POST[$key];
		}
		
		return $value;
	}
	
	function toJson(object | array $data) : Context {
		$this->response_body .= json_encode($data);
		
		return $this;
	}
	
	function send() : void {
		header("Content-Type: $this->content_type");
		echo $this->response_body;
		die();
	}
	
	function sendJson(object | array $data) : void {
		$this->toJson($data)->send();
	}
}
