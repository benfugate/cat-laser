<form action="" method="post">
     <input type="submit" name="start" value="start" />
     <input type="submit" name="stop" value="stop" />
</form>

<?php
    if(isset($_POST['start'])){
        system('sudo -u root -S python3 /laser/src/laser.py');
    }
    if(isset($_POST['stop'])){
        system('sudo -u root -S touch /laser/stop-script');
    }
?>