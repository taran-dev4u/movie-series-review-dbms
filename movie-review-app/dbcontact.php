<?php
include "database.php"; // Using database connection file here

if(isset($_POST['submit']))
{		
    $fullname = $_POST['name'];
    $email = $_POST['email'];
    $suggestion = $_POST['message']

    $insert = mysqli_query($db,"INSERT INTO `feedback`(`feedback_id`, `feedback_pname`, 'feedback_pemail', 'feedback_pmessage') VALUES (null,'$fullname','$email', '$suggestion')");

    if(!$insert)
    {
        echo mysqli_error();
    }
    else
    {
        echo "Records added successfully.";
    }
}

mysqli_close($db); // Close connection
?>