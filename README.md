Puppy MochaBot is a lite version of MochaBot that'll only check Torrey Pines.

Python@3.9

# <ins>**Installation:**<ins>
<Usage of venv is optional>
  
1. pip3 install -r requirements<_windows>.txt
    - If fails, try pip3 install --upgrade wheel


# <ins>**Usage:**<ins>
1. Update the credential/web_passwords.yaml with your torrey pines account.
2. Update the settings in userdata/config.py (See examples below)
3. Run 'python3 bot_health_check.py'

- Below will check the first tee time available that is before 1:15pm on everyday with available players of 4.
  - tee time thresholds for bot to check
    ```python
      hold_tee_time = {
                        'latest_tee_time': '13:15',
                        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        'number_of_players': 4,
                      }


- Below will check the first tee time available that is before 10AM on all weekdays for a minimum of single player.
  - tee time thresholds for bot to check
    ```python
      hold_tee_time = {
                        'latest_tee_time': '10:00',
                        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                        'number_of_players': 1,
                      }
