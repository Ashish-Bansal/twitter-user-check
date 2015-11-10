<!DOCTYPE html>
<html lang="en">

<head>
	<base href="/">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Twitter Spy</title>
	<link href="css/bootstrap.min.css" rel="stylesheet">
	<link href="css/style.css" rel="stylesheet">

	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="js/jquery-1.11.3.min.js"></script>
	<!-- Include all compiled plugins (below), or include individual files as needed -->
	<script src="js/bootstrap.min.js"></script>
</head>

<body ng-app='app'>
	<div class="container-fluid header-bg" id="header">
		<div class="row">
			<div class="col-md-12" style="background-color:#000">
				<div class="col-md-4">
					<img src="twitter-bird-light-bgs.png" class="img-responsive">
				</div>
			</div>
		</div>
	</div>


	<div id="main" ng-controller="ViewController" class="clearfix overflow-hidden">
		<!-- xhr content would be added here -->
		<div data-ng-view class="view-fade-in"></div>
	</div>

	<div class="container-fluid footer-bg" id="footer">
		<div class="row">
			<div class="col-md-12 text-white">
				<h5><span class="glyphicon glyphicon-copyright-mark"></span>Copyright 2015.</h5>
			</div>
		</div>
	</div>
</body>

<script type="text/javascript" src="js/angular.js"></script>
<script type="text/javascript" src="js/angular-route.js"></script>
<script type="text/javascript" src="js/app.js"></script>

</html>
