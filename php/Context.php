<?php

class Context {
	public $request_body;
	public $response_body;
	public $content_type;
	
	function __construct() {
		$this->request_body = "";
		$this->response_body = "";
		$this->content_type = "application/json";
		
		if (KtGetHeader("Content-Type") == "multipart/form-data") {
			$this->request_body = $_POST;
		}
	}
	
	function fromGet(string $key) : null | string | array {
		$value = null;
		
		if (array_key_exists($key, $_GET)) {
			$value = $_GET[$key];
		}
		
		return $value;
	}
	
	function fromPost(string $key) : null | string | array {
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
	
	function useXml() : Context {
		$this->content_type = "text/xml";
		return $this;
	}
	
	function setBody(string $body) : Context {
		$this->response_body = $body;
		return $this;
	}
	
	function sendJson(object | array $data) : void {
		$this->toJson($data)->send();
	}
	
	function sendXml(string $data) : void {
		$this->useXml()->setBody($data)->send();
	}
}
