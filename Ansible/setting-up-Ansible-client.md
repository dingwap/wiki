# Setting up my Ansible environment - Ansible client

## Ansible Client
The Ansible Client is any host which will be controlled by the Ansible Master server. This device will accept commands via the server and will carry out these activities, enabling centralised and repeatable automation from the Ansible Server.

Clients can be Windows and Linux, I'm starting with Linux as it's easier to set up and manage. Windows appears to be hellishly complicated, requiring lots of firewall ports and the use of WinRM (yuck), but support for SSH might make it easier in the future, we'll see!

Setting up the client is very similar to the [*server guide*](../Ansible/setting-up-Ansible-master.md). You'll need to follow all steps from 1-6, which will give you a client which:

1 - Is configured with a non-root user

2 - Has been set up for Sudo access from the non-root user

3 - Has Ansible installed and ready to go

You will need to carry this out on all hosts which will be managed by Ansible. Once complete you can continue with the [Testing Comms guide](../Reference/Testing-Ansible-Comms.md)