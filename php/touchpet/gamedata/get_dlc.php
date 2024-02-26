<?php

define("KATTEN_LOADED", 1);
require_once "Utilities.php";

header("Content-Type: text/plain"); // used to be text/xml
// If we just put nothing here, the game is okay with that.

// Log info
KtLog("Servered DLC info to client (IP = " . KtGetClientIP() . ", User-Agent = " . KtGetHeader("User-Agent") . ").");
