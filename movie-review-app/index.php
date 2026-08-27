<?php
	$page_title = "TARAN";
	include_once('includes/header.php');
?>

	<div id="myCarousel" class="carousel slide" data-ride="carousel">
		
		<ol class="carousel-indicators">
			<li data-target="#myCarousel" data-slide-to="0" class="active"></li>
			<li data-target="#myCarousel" data-slide-to="1"></li>
			<li data-target="#myCarousel" data-slide-to="2"></li>
		</ol>
		<div class="carousel-inner" role="listbox">
			<div class="item active">
				<img src="images\movie_wallpaper.jpg" alt="First slide">
				<div class="jumbotron">
					<div class="container">
						<div class="carousel-caption">
							<h1>READ MOVIE DETAILS</h1>
							<p>you can see a list of movie titles along with ratings, years, a short synopsis of it , and even reviews!</p>
							<p><a class="btn btn-lg btn-info" href="movies.php" role="button">READ MOVIE DETAILS&raquo;</a></p>
						</div>
					</div>
				</div>
			</div>
			<div class="item">
				<img src="https://wallpapercave.com/wp/wp4922390.jpg" alt="Second slide">
				<div class="jumbotron">
					<div class="container">
						<div class="carousel-caption">
							<h1>Rate Movies</h1>
							<p>Create an account to review your favorite movies</p>
							<p><a class="btn btn-lg btn-info" href="moviesdetails.php" role="button">RATE MOVIES&raquo;</a></p>
						</div>
					</div>
				</div>
			</div>
			<div class="item">
				<img src="images\movie_read.jpg" alt="Third slide">
				<div class="jumbotron">
					<div class="container">
						<div class="carousel-caption">
							<h1>Read Reviews</h1>
							<p>Check all of our reviews and find out more about what others thought of your favorite movies!</p>
							<p><a class="btn btn-lg btn-info" href="reviews.php" role="button">VIEW REVIEWS &raquo;</a></p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="container">
		
		<div class="row">
			<div class="col-md-4">
				<h2>LIST OF MOVIES</h2>
				<p>It contains a list of movie titles along with ratings, years, a short synopsis of it , and even reviews!</p>
				<p><a class="btn btn-default" href="movies.php" role="button">VIEW MOVIES &raquo;</a></p>
			</div>
			<div class="col-md-4">
				<h2>LIST OF REVIEWS</h2>
				<p>Browse all of our reviews and find out more about what others thought of your favorite movies!</p>
				<p><a class="btn btn-default" href="reviews.php" role="button">VIEW REVIEWS &raquo;</a></p>
			</div>
			<div class="col-md-4">
				<h2>ADD REVIEWS</h2>
				<p>give the rating for your favourite movies which you experienced, in your own way!</p>
				<p><a class="btn btn-default" href="addreview.php" role="button">ADD REVIEW &raquo;</a></p>
			</div>
		</div>

	</div> 


<?php
	include_once('includes/footer.php');