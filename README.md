Puppy MochaBot is a lite version of MochaBot that'll only check Torrey Pines.

Python@3.9

Installation:
  <Usage of venv is optional>
  
  pip3 install -r requirements<_windows>.txt
    - If fails, try pip3 install --upgrade wheel
  python3 bot_health_check.py

Usage:
  1. Update the credential/web_passwords.yaml with your torrey pines account.
  2. Update the settings in userdata/config.py

  Below will check the first tee time available that is before 1:15pm on everyday with available players of 4.
      # tee time thresholds for bot to check
      hold_tee_time = {
                    'latest_tee_time': '13:15', # Must be 24hr format
                    'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], # 'Mon','Tue','Wed','Thu','Fri','Sat','Sun'
                    'number_of_players': 4, # Minimum number of available players in the tee time
                      }

  Below will check the first tee time available that is before 10AM on all weekdays for a minimum of single player.
      # tee time thresholds for bot to check
      hold_tee_time = {
                    'latest_tee_time': '10:00', # Must be 24hr format
                    'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], # 'Mon','Tue','Wed','Thu','Fri','Sat','Sun'
                    'number_of_players': 1, # Minimum number of available players in the tee time
                      }
