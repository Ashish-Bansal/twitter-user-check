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
$userfile = generateRandomString();

$cmd_str = '/usr/bin/python2.7 crawler.py --handle '.$search_item.' --resultfile '.$resultfile.' --tweetfile '.$tweetfile.' --userfile '.$userfile;
echo $cmd_str;
$cmd_exec = exec($cmd_str);
echo $cmd_exec;
die();
$base_path = "fetched/";
$file = fopen($base_path.$resultfile,"r");
print_r(fgetcsv($file));
fclose($file);

?>

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Twitter Crawler</title>
	<link href="css/bootstrap.min.css" rel="stylesheet">

	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="js/jquery-1.11.3.min.js"></script>
	<!-- Include all compiled plugins (below), or include individual files as needed -->
	<script src="js/bootstrap.min.js"></script>
</head>

<section>
	<div class="container">
		<div class="row">
			<div class="col-md-12" style="background-color:#5dc9e4">&nbsp;<br><br><br><br></div>
		</div>
		<div class="row" style="top:-60px">
			<div class="col-md-2">
				<img src="user.jpg" class="img-circle img-responsive">
			</div>
			<div class="col-md-5">
				<h3><?php echo $result_array[3];?></h3>
				<small>@<?php echo $result_array[1];?></small>
			</div>
		</div>
	</div>
</section>
