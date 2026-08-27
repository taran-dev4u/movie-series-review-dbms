 <?php

@session_start();
 ?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title><?php echo $page_title; ?></title>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	<link rel="stylesheet" href="beautify/css/main.css"/>
	<link rel="icon" href="images/favicon.png">

</head>
<body>


<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
	<div class="container">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</button>
			<a href="about.php" class=" navbar-brand"><i class="fa fa-clock-o fa-lg"></i> Taran Mamidala</a>
		</div>
		<div class="navbar-right">
			<div id="navbar" class="navbar-collapse collapse">
				
					<ul class="nav navbar-nav">
						
						<li class="dropdown">
							<a href="" class="dropdown-toggle navbar-brand" data-toggle="dropdown" role="button" aria-expanded="false"> MENU <i class="fa fa-caret-down"></i></a>
							<ul class="dropdown-menu" role="menu">
								<li><a href="index.php">HOME</a></li>
								<li><a href="movies.php">MOVIES</a></li>
								<li><a href="reviews.php">REVIEWS</a></li>
								<li><a href="about.php">ABOUT ME</a></li>
								<li><a href="addreview.php">ADD REVIEW</a></li>
							</ul>
					</ul>
				

			</div>
		</div>
	</div>
</nav>