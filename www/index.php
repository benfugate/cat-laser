<form action="" method="post">
     <input type="submit" name="start" value="start" />
     <input type="submit" name="stop" value="stop" />
</form>

<?php
    if(isset($_POST['start'])){
        system('sudo -u root -S python3 /home/pi/cat-laser/src/stop-script');
    }
    if(isset($_POST['stop'])){
        system('sudo -u root -S touch /home/pi/cat-laser/src/stop-script');
    }
?>