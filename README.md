Views + Votes for https://coinmarketcap.com working with or without proxies.

INSTRUCTIONS:

- Install Docker and Docker-compose
    - https://docs.docker.com/install/
    - https://docs.docker.com/compose/install/

- if you have proxies add your proxies in proxies.txt on every new line, proxy:port, example:
    1.1.1.1:8000
    2.2.2.2:8000
    
- in config.env you can edit the number of workers to be used in parallel, the link to visit, and the sleep time on every url:

Run the project:
    - in terminal got inside the folder where the main.py is,  and run:
        - docker-compose build
        - docker-compose up(after he installs it will start working)

You can view what is happening using VNC, use a vnc app, connect to 127.0.0.1:5901, the password is `secret`

---------------

Donations: PornRocket Address: 0xcd29123f16C9476520F59dD132A7Fd8EC5EC0259