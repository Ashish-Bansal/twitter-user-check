<div class="container-fluid first-page-center-bg" id="dynamic">
	<div class="row">
		<div class="col-md-12">
			<section id="padding-dynamic">
				<h1 class="text-center text-white">Search out a TWITTER USER to know if it is a spammer</h1>
				<form ng-submit="submit()" ng-controller="FormController" id="search_form" name="search_form" class="form-inline text-center">

					<div class="form-group">
						<label class="sr-only" for="search_user">Search User</label>
						<div class="input-group">
							<input type="text" class="form-control input-lg zero-border-radius" id="search_user" name="search_user" ng-model="search_user"
							ng-minlength=3
							ng-maxlength=20
							placeholder="Search User" required>

							<div class="input-group-addon add-on">
								<button type="submit" class="btn btn-lg btn-primary zero-border-radius">Analyze</button>
							</div>
						</div>
					</div>
				</form>
			</section>
		</div>
	</div>
</div>

<script type="text/javascript">
var header_ht = $("#header").height();
var footer_ht = $("#footer").height();
var total_ht = $(window).height();
var actual_ht = total_ht-(header_ht+footer_ht);
document.getElementById('dynamic').style.height = actual_ht+"px";
document.getElementById('padding-dynamic').style["padding-top"] = (actual_ht/3)+"px";
</script>
