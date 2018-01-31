To install on EC2 follow the below guidelines:
1. Create a free micro instance
    I'm using Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
    expose port 9000 for gunicorn
    add an elastic ip (in case we need to dump this instance but dont want to change IP's)

2. Start the instance and login with ssh
   * `ssh -i "Tomcat-key.pem" ubuntu@34.206.176.170`
       -- Tomcat-key.pem is my AWS permissions key file
   * `sudo apt-get update`
   * `sudo apt-get -y upgrade`
   * `sudo apt-get -y install python3-pip python3-dev`
   * `sudo apt-get -y install python3-venv`
   * `pip3 install --upgrade pip setuptools`

3. Create a virtual environment for our project
   * `mkdir ~/Applications`
   * `python3 -m venv Applications/python_envs`
   * `source ~/Applications/python_envs/bin/activate`
   * `pip install --upgrade pip`
   * `pip install wheel`
   * `pip install flask`
   * `pip install flask-wtf`
   * `pip install gunicorn`
   * `pip install gevent`

4. copy tar file from project to the EC2 Instance
   * `tar -cvf gt_bay.tar gt_bay`
   * `scp -i "Tomcat-key.pem" /Users/danhiggins/Code/GATech/CS6400_Database_Design/project/GT_Bay/gt_bay.tar ubuntu@34.206.176.170:~/Applications`
   * `ssh -i "Tomcat-key.pem" ubuntu@34.206.176.170`
   * `source ~/Applications/python_envs/bin/activate`
   * `cd Applications;tar -xvf gt_bay.tar`
   * `cd gt_bay;nohup ./run.sh &

5. Run web app
   * visit http://34.206.176.170:9000/


   for d in `ps -auxww|grep python|cut -d' ' -f4`;do echo $d; done
   kill -9 `cat thermo_ui/gunicorn.pid`