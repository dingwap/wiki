# Setting up my Ansible environment - Ansible Master

## Ansible Master

Ansible operates in a standard hub-and-spoke model with a client/server relationship.

The Ansible Master is the server which will host the playbooks which will be used by Ansible to carry out activities on Ansible clients. It will be the **hub** for all management activities for the clients.


Firstly, I created an Alpine container on my virtualisation platform. It's an Alpine 3.16 container with a root user.

*The example commands explained below are for Alpine but are very similar for Ubuntu-based distributions (mostly just a case of switching out **apk add** to **apt install**)*

1 - Login as root and install Sudo

    apk add sudo

2 - Add a new user with adduser (*using Joe as an example user*)

    adduser joe

3 - Enable sudo access for the user

    echo '%wheel ALL=(ALL) ALL' > /etc/sudoers.d/wheel 
    adduser joe wheel 

4 - Logout root user and login as new user.

Test sudo access with the following command to open an interactive shell

    sudo -i

Do everything else as your new user, **not as root**.

5 - Install openssh for remote access with your new sudo powers and make sure it starts at boot

    sudo apk add openssh
    sudo rc-update add sshd

6 - Install ansible and python

    sudo apk add ansible
    sudo apk add python3

7 - Create your ansible hosts file

    sudo nano touch /etc/ansible/hosts

8 - Create ssh keys for passwordless login to Ansible-managed devices

    ssh-keygen

This will create SSH keys in .ssh (from your home directory) called id_rsa and id_rsa.pub. We'll need these later on.

**Now, go and configure your clients** with the [*client guide*](../Reference/setting-up-Ansible-client.md)