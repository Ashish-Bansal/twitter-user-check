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
$result_array = fgetcsv($file);
fclose($file);

$final_result = file_get_contents($base_path.$probfile);

?>

<section>
	<div class="container">
		<div class="row">
			<div class="col-md-12" style="background-color:#5dc9e4">&nbsp;<br><br><br><br></div>
		</div>
		<div class="row" >
			<div class="col-md-2">
				<img src="<?php echo $result_array[9]; ?>" class="img-circle img-responsive" style="margin-top:-60px">
			</div>
			<div class="col-md-4" style="margin-top:-20px">
				<h3><?php echo $result_array[3];?></h3>
				<small>@<?php echo $result_array[1];?></small>
				<br>
				<h5><span class="glyphicon glyphicon-map-marker"></span> <?php echo $result_array[4];?></h5>
				<h6>Joined on <?php echo $result_array[8];?></h6>
			</div>
			<div class="col-md-4" style="margin-top:-20px">
				<h3><?php echo $result_array[5]; ?> <small>TWEETS</small></h3>
				<h3><?php echo $result_array[6]; ?> <small>FOLLOWERS</small></h3>
				<h3><?php echo $result_array[7]; ?> <small>FOLLOWING</small></h3>
			</div>
			<div class="col-md-2">
				<br>
				<button class="btn btn-primary btn-lg" type="button">
					<?php echo $final_result; ?>
				</button>
			</div>
		</div>
	</div>
</section>
