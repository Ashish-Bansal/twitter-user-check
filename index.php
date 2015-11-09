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

<body ng-app='app'>
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-12" style="background-color:#000">
				<img src="twitter-bird-light-bgs.png" class="img-responsive">
			</div>
		</div>
	</div>
<br>
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-2">
				
			</div>
			<div class="col-md-10">
				
				<form id="search_form" name="search_form" method="get" action="//python_result.php" class="form-inline">
					<div class="form-group">
						<label class="sr-only" for="search_user">Search User</label>
						<div class="input-group">
							<input type="text" class="form-control" id="search_user" name="search_user" 
							ng-minlength=3 
							ng-maxlength=20 
							ng-pattern="[a-zA-Z0-9]" 
							placeholder="Search User" required>
							<div class="input-group-addon"><span class="glyphicon glyphicon-search"></span> </div>
						</div>
					</div>
					<button type="submit" class="btn btn-primary">Analyze</button>
				</form>	

			</div>
		</div>
		<div id="main" class="clearfix overflow-hidden">
	        <!-- xhr content would be added here -->
	        <div data-ng-view class="view-fade-in"></div>
	    </div>
	</div>
	<base href="/">
</body>

<script type="text/javascript" src="js/angular.js"></script>
<script type="text/javascript" src="js/angular-route.js"></script>
<script type="text/javascript" src="js/app.js"></script>

</html>