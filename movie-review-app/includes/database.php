<?php
	
	$host = "localhost";
	$port;
	$username = "ronny";
	$password = "1234567890";
	$database = "movie_data";
	$tblMovies = "movies";
	$tblReviews = "reviews";
	$tblfeedback = "feedback";
	
	$conn = @new mysqli($host, $username, $password, $database, $port);
	if (mysqli_connect_errno() != 0) {
	    $errno = mysqli_connect_errno();
	    $errmsg = mysqli_connect_error();
	    die("Connect Failed with: ($errno) $errmsg<br/>\n");
	}
?>