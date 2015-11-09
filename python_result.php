<?php
$search_item = $_REQUEST['search_user'];

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

//$cmd_str = 'python2 crawler.py --handle '.$search_item.' --resultfile '.$resultfile.' --tweetfile '.$tweetfile.' --max 6';
//echo $cmd_str;

// $cmd_exec = exec($cmd_str);

// $file = fopen($resultfile,"r");
// while(!feof($file)) {
// 		$result_array = fgetcsv($file);
// }
// fclose($file);

$result_array = array("2401982971","ashish_bansal96","","Ashish Bansal","Chandigarh","1","17","16","2014-03-21","597");
echo "<div class='thumbnail'>Total Tweets<hr><h2>".$result_array[5]." <small>TWEETS</small></h2></div>"

?>