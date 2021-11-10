<center>
<form action="" method="post">
     <input type="submit" name="start" value="start" style="height:50%; width:100%" />
     <input type="submit" name="stop" value="stop" style="height:50%; width:100%" />
</form>
</center>

<?php
    if(isset($_POST['start'])){
        exec('sudo -u pi /usr/bin/python3 /home/pi/cat-laser/src/laser.py');
        exec('sudo -u pi touch /home/pi/cat-laser/src/start-script');
    }
    if(isset($_POST['stop'])){
        exec('sudo -u pi touch /home/pi/cat-laser/src/stop-script');
    }
?>
