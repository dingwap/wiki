# Setting up and testing comms between the server and client(s)

## Setting up SSH access

The Ansible server will connect to the clients via SSH to send commands and receive responses. SSH is good to use because it's standard, well supported and provides an encrypted channel between the client and the server so that anything transmitted between the two devices can't be intercepted.

When you connect to a device with SSH by default it will ask for a username and password. This is fine for normal access, but when using Ansible it will be a pain to have to keep typing in passwords and it won't be great for automation! So, we'll set up passwordless access by configuring the Ansible clients to trust the Ansible server.

### SSH key generation

You should've already completed this when you set up the ansible server with the **ssh-keygen** command in **step 8**. This creates the SSH key which we'll share with the clients so they trust the server.

### Copying SSH key to the client machine

The **openssh** package contains a command which allows us to copy our public key to the client hosts.

In the example below we'll use the user **joe** and an Ansible client with ip address **10.10.10.3**. *You'll need to change the user and ip address for the ones relevant to your clients.*

    ssh-copy-id joe@10.10.10.3

When this command is run for the first time (and if you haven't connected to the client before) you'll see a message like this:

    /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/xxx/.ssh/id_rsa.pub"
    The authenticity of host '10.10.10.3 (10.10.10.3)' can't be established.
    ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
    This key is not known by any other names
    Are you sure you want to continue connecting (yes/no/[fingerprint])?

This is fine, as it's just the SSH client letting you know that it's the first time that you've connected to this client and makes sure that you're aware of this.

When you confirm that you're happy with this (by typing **yes**) you'll then be prompted to enter the password for the client.

Once you've successfully authenticated you'll see the following message:

    Number of key(s) added: 1

    Now try logging into the machine, with:   "ssh 'joe@10.10.10.3'"
    and check to make sure that only the key(s) you wanted were added.

If you now try to connect to the Ansible client with the following command:

    ssh joe@10.10.10.3

you'll be connected to the Ansible client without needing to enter your password, as the Ansible client now trusts the Ansible server.

This activity also updates some files on your Ansible server and Ansible client so that both sides *know* about each other and remember for the next time they connect.

**Ansible server**

*known_hosts* (within the .ssh directory from the home directory) will now include the SSH key fingerprint for the client you've just added. This means that it's now known to the Ansible server and the warning message from earlier won't be shown again.

**Ansible client**

*authorized_keys* (within the .ssh directory from the home directory) contains the public key and username for the Ansible server. As the name suggests, keys within this file are authorised to acess the client and will be trusted for access.

## Setting up the Ansible Hosts file

Now we need to tell the Ansible server about the Ansible client(s) which have been configured. The hosts file is used to create groups of clients which will be managed by Ansible.

In the following example I'll use the same client as before with IP address *10.10.10.3*.

This is just a simple activity of editing the */etc/ansible/hosts* file (created in step 7 for the Ansible server setup). You can do this with your preferred text editor (vi/nano etc).

    nano /etc/ansible/hosts

This will open the file in nano, and you'll then need to add the name of the group and the ip address(es) of the clients which will be managed by Ansible.

    [test]
    10.10.10.3

In my example I've created a single group called **test** and added a single client within the group with IP address **10.10.10.3**.

## Testing access to the Ansible clients

We can now run a simple command against the Ansible clients to ensure that our Ansible server can communicate with them. The following will just send a simple 'hello' command to the Ansible client.

    ansible test -m ping

- **Ansible** is the command used to initiate communications to the client(s)
- **test** is name of the group of client(s) we'll be testing
- **-m ping** tells the Ansible command to use the ping *module* to communicate with the cilent(s)

If successful you'll see the following message confirming that Ansible has communicated with your clients and run the **ping** module


    10.10.10.3 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
    }
