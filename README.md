## DSP Support Data Copy No Protobuf implementation
-------------------------------------------------------------------------
- App copies files from a data directory to a destination (NAS) directory

- To run open 2 terminals
    - Run in 1st terminal: $ python server.py
    - Run in 2nd terminal: cd app/      &&     $ python file_manager.py
- To run tests 2 terminals
    - Run in 1st terminal: $ python server.py
    - Run in 2nd terminal: cd test/      &&     $ python test_file_manager.py

- To clean out project
    - Run in terminal: cd app/      &&     $ _setup.sh  >   clean
- To build project
    - Run in terminal: $ _setup.sh  >   build