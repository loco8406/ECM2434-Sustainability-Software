# ECM2434-Sustainability-Software

## ! Important Information !
This project is currently in the prototyping phase and the current state of the application may not accurately represent its final iteration. Subject to change.\
As a result, only the following basic functionality is included at this time:\
-Login/Registration System\
-Referral System\
-Points Tallying\
-Leaderboard Tracking\
-Water Station Generation Gamekeepers\
-Water Station Scanning/Point accumulation

While we have made efforts to make the experience stable enough for basic usage, please expect bugs and errors.

## How to Run

### Prerequisites
Please ensure that you have the correct version of Python installed.\
Python Version: **3.10.11**

*This software is not garuanteed to be compatible with other versions than the one listed above*

The following Python packages are also required for operation:\
-**Django** (Version: 5.1.6)\
-**Pillow** (Version: 11.1.0)\
-**qrcode** (Version: 8.0)

### Running the application
1. Clone the repository using your preferred method.\
2. Ensure that you have installed the prerequisite modules listed above via pip.
3. Navigate to the 'WebsiteRoot' directory
4. Run python manage.py makemigrations
5. Run python manage.py migrate
6. Run python manage.py runserver

The application should now be running on your machine.

### Admin can assign gamekeepers functionality 
1. Create django superuser run python manage.py createsuperuser
2. Acess django admin pannel and click on a registered user
3. Scroll down and type "gamekeeper" instead of "user" in the box for role

Now when this account logs in they will be directed to the gamekeeper dashbaord where they can implement game features

