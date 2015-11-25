BASEDIR="/home/easyctf/easyctf"
HTTPDIR="/var/www"
EASTEREGGS="$BASEDIR/extras/easter_eggs"

echo "-- EXTRAS --"

echo "Easter Egg: 1337"
tmux kill-session -t egg1337 2> /dev/null
tmux new-session -s egg1337 -d "cd $EASTEREGGS/1337 && node app"

echo "Easter Egg: Ubuntu"
cd $EASTEREGGS/ubuntu
sudo npm install --save &> /dev/null
tmux kill-session -t eggubuntu 2> /dev/null
tmux new-session -s eggubuntu -d "cd $EASTEREGGS/ubuntu && node app"

echo "PHP Sites"
sudo rm -rf $HTTPDIR/*
sudo rm -rf /etc/apache2/sites-available/*
sudo rm -rf /etc/apache2/sites-enabled/*
sudo cp -r $BASEDIR/extras/apache_conf/* /etc/apache2/sites-available
sudo ln -s /etc/apache2/sites-available/* /etc/apache2/sites-enabled
sudo cp -r $BASEDIR/extras/apache/* $HTTPDIR
sudo chmod -R a+rx $HTTPDIR
sudo service apache2 restart

echo "Node Apps"
for app in "infinity_star"
do
	echo "Loading $app..."
	cd $BASEDIR/extras/$app
	# sudo rm -rf node_modules
	sudo npm install --save &> /dev/null
	tmux kill-session -t $app 2> /dev/null
	tmux new-session -s $app -d "cd $BASEDIR/extras/$app && node app"
done