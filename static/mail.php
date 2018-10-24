<?php 
    $to = "houlier.nicolas@outlook.fr";
    $from= $_POST['email']; 
    $name = $_POST['name'];
    $subject = "twitmining_contact_" . $name;
    $message = $_POST['message'];

    $headers = "From:" . $from;
    mail($to,$subject,$message,$headers);

    echo "Mail Sent. Thank you " . $name . ", we will contact you shortly.";
?>