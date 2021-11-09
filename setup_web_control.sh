#!/bin/bash
sudo apt install -y apache2 php
sudo cp www/index.php /var/www/html/
sudo rm /var/www/html/index.html
sudo service apache2 restart
echo "www-data ALL=(ALL) NOPASSWD: /usr/bin/python3" | sudo tee -a /etc/sudoers
echo "www-data ALL=(ALL) NOPASSWD: /usr/bin/touch" | sudo tee -a /etc/sudoers