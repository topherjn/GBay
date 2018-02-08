Running GT_Bay on Ubuntu Server 16.04 follow the below guidelines:

1. Install on Ubuntu Server 16.04
    follow and standard install practice

2. Start the ubuntu instance and login (Install required packages)
   * `sudo apt-get update`
   * `sudo apt-get -y upgrade`
   * `sudo apt-get -y install mysql-server` (create root password as passw0rd)
   * `sudo apt-get -y install python3-pip python3-dev`
   * `sudo apt-get -y install python3-venv`
   * `pip3 install --upgrade pip setuptools`

3. Create a virtual environment for GT_Bay project (Install required python packages)
   * `mkdir ~/Applications`
   * `python3 -m venv Applications/python_envs`
   * `source ~/Applications/python_envs/bin/activate`
   * `pip install --upgrade pip`
   * `pip install pymysql`
   * `pip install wheel`
   * `pip install flask`
   * `pip install flask-wtf`
   * `pip install gunicorn`
   * `pip install gevent`

4. Git clone code to Ubuntu Instance (Code is currently under dev-dan branch)
   * `sudo service mysql start`
   * `mysql -u root -p`
        mysql> CREATE DATABASE GT_BAY;
        mysql -h localhost -u root GT_BAY < ./gt_bay_initialize.sql
   * `source ~/Applications/python_envs/bin/activate`
   * `cd gt_bay;nohup ./run.sh &`


5. Test web app
   * visit http://34.206.176.170:9000/


6. Kill the running server
   * for d in `ps -auxww|grep python|cut -d' ' -f4`;do echo $d; done
   * kill -9 `cat thermo_ui/gunicorn.pid`




   also had to symlink the mysql client library on my Mac
   sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.18.dylib

