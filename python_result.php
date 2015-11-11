<?php

$search_item = $_GET['search_user'];

if (empty($search_item)) {
	echo "User handle not passed";
	die();
}

function generateRandomString($length = 8) {
	$characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	$charactersLength = strlen($characters);
	$randomString = '';
	for ($i = 0; $i < $length; $i++) {
		$randomString .= $characters[rand(0, $charactersLength - 1)];
	}
	return $randomString;
}

$resultfile = generateRandomString();
$tweetfile = generateRandomString();
$userfile = generateRandomString();
$probfile = generateRandomString();

putenv("LD_PRELOAD=/usr/lib/libcrypto.so.1.0.0:/usr/lib/libssl.so.1.0.0:/usr/lib/libcurl.so");
$cmd_str = '/usr/bin/python2.7 crawler.py --handle '.$search_item.' --resultfile '.$resultfile.' --tweetfile '.$tweetfile.' --userfile '.$userfile.' --probabilityfile '.$probfile.' 2>&1';
$op=array();
$cmd_exec = exec($cmd_str, $op);

// PYTHON DEBUG!!!
// echo $cmd_str;
// $arrlength = count($op);
// for($x = 0; $x < $arrlength; $x++) {
//     echo $op[$x];
//     echo "<br>";
// }

$base_path = "fetched/";
$file = fopen($base_path.$userfile,"r");
$result_userinfo = fgets($file);
fclose($file);

$final_result = file_get_contents($base_path.$probfile);

header('Content-Type: application/json');
echo $result_userinfo;

?>
