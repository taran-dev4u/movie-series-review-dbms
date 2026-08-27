<?php


$page_title = "Delete Review";

require_once ('includes/header.php');
require_once('includes/database.php');


$review_id = $_GET['id'];


$query_str = "DELETE FROM reviews WHERE review_id = '" . $review_id . "'";

//execut the query
$result = $conn->query($query_str);


if (!$result) {
  $errno = $conn->errno;
  $errmsg = $conn->error;
  echo "Selection failed with: ($errno) $errmsg<br/>\n";
  $conn->close();
  exit;
}?>
//confirming delete
<div class="container wrapper">
  <h1 class="text-center text-danger">Your review has been deleted</h1>
</div>

<?php

$conn->close();

include ('includes/footer.php');
?>

