<?php
$servername = "sql300.epizy.com";
$databasename = "epiz_28753003_details";
$username = "epiz_28753003"; // For MYSQL the predifined username is root
$password = "a4o076cUIKYSQqp"; // For MYSQL the predifined password is " "(blank)

// Create connection
$conn = new mysqli($servername, $username, $password, $databasename);

 
// Check connection

 if ($conn->connect_error) {

    die("Connection failed: " . $conn->connect_error);
}

echo "Connected successfully";

?>