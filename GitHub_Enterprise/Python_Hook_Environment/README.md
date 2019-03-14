# GHE Hook Environment & Pre-receive Hook Script
Run 'create_image.sh' to build/rebuild the python3 docker image.

Note: you cannot build the dockerfile while connected to the office wifi (the guest wifi seems fine, though).

Building the Hook environment:
    1. Download everything from [your actual repo](https://gitserver.com/organisation/repo/github)
    2. To generate a new docker image:
        1. Remove existing tar.gz tarball
        2. Ensure that Docker is installed and running
        3. If you’ve done this before:
            1. Remove existing Docker image (`docker image rm -f pre-receive.python3.alpine-3.3`. ?)
            2. Remove any pre-existing containers using `docker container prune` (note: that will remove **all** non-running containers)
        4. To add python libraries to be installed, add them in **./hook-env/requirements.txt**
        5. Get the current ELK SSH-keys from [your elk repo](https://gitserver.com/organisation/repo/certs)
        6. Run create_image.sh to generate new tarball
        7. If you want an interactive login shell to test the docker image,
            check that python libraries are installed, etc, run:
                    `docker run -it pre-receive.python3.alpine-3.3 /bin/bash`
    3. Upload the tarball to your GitHub infrastructure:
        5. Use SCP to upload the tarball to your GHE server
        7. Create the new hook environment on GitHub, either by:
            1. From your SSH session to the GHE server, run `ghe-hook-env-create Python3 /home/admin/alpine-3.3.tar.gz`
            2. Or from the GitHub Enterprise website, Site Admin -> Admin Centre -> Hooks -> Manage Environments -> Add Environment (URL should be /home/admin/alpine-3.3.tar.gz)



As to why this is necessary .. by default, GHE only supports BASH scripts. To use anything else you need to create a new hook environment to support the language you wish to use (in this case Python, but presumably you can do something similar for any language). The hook environment is simply a tarballed docker image running alpine+python3.

NOTE:
-----
ghe-hook-env-create WILL NOT overwrite an existing hook environment.
Create a new one, move any existing hooks over and then delete the old one.

NOTE2:
------
All of this was written for a client; I've stripped out any client-specific
steps and information and uploaded without testing; it's intended to point 
you in the right direction, but it'll probably need work.
