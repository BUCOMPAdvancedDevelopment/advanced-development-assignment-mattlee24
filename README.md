# Advanced Devlopement Unit Coursework - Matt Lee s5207970

### Coursework for Advanced Dev Unit, Final Year (Year 3)

#### To access Site on the cloud, use the following link: 

https://ad-gamezone.ew.r.appspot.com  (Not optimised for mobile!...yet)

# Local Server Commands
                  
#### To run in a local environment, run the following commands:

Create a local virtual environment with flask installed.

Copy contents of git folder inside virtual enviroment.

pip3 install -r requirements.txt
      
1. set FLASK_APP=main.py
2. set FLASK_DEBUG=1 (Devlopment Only)
3. flask run
4. ctrl-c (Shut down local server)

### Important - Don't forget: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (r"Path to Credentials file on YOUR machine") 
### It will not run unless this is changed accordingly.

#
        
#### To run unit tests

- run command "test.py" in terminal

   
