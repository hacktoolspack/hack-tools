<?php

$con = mysqli_connect("127.0.0.1","username","password","database");

if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$rows = mysqli_query($con,"SELECT username FROM users where id=" . $_GET['id']);

if (mysqli_num_rows($rows) == 0) {
    echo 0;
} else {
    echo 1;
}

mysqli_close($con);

?>
