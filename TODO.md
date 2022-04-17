- Workflow
    - Function to coordinate all synthesis, editing, trimming
    - When 'Export New Audio' button is clicked
        - Transcript from p tag is taken -> compared to original transcript with timestamps
        - If words have been deleted they appear in red crossed out font and removed from audio
        - If words have been added they appear in green and synthesized after that timestamp in audio
    
Setup reminders
- pip install -e . (to install voicedoc package)
- install requirements