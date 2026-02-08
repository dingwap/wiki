# Managing secrets in Ansible

I've been using Ansible to create some test environments in my homelab. All was going well until I almost uploaded my secret passwords into GitHub when I was synchronising my changes back.

In the playbook below, I'm ok to show the password used to set up the container in Proxmox as that's changed after container creation, but the api_password is the main password I use to access my ProxMox server, so didn't want that being uploaded into GitHub or sat in plaintext in a Playbook.


    - name: ProxMox
      hosts: proxmox
       tasks:
      - name: Create new container automatically selecting the next available vmid
        community.general.proxmox:
           api_user: 'root@pam'
           api_password: 'SecretPassword'
           api_host: 'ProxMox-Host'
           hostname: 'new-container'
           ostemplate: 'local:vztmpl/alpine-3.16-default_20220622_amd64.tar.xz'
           storage: local
           password: changeme


## Using Prompt to gather the secret

The simplest method of managing secrets in an Ansible Playbook is to use an interactive prompt which gathers a variable and then uses that in the playbook.

In the example below we're using **prompt** within the playbook to gather a variable called **api_key** and then using that with the **api_password** section instead of the password in plain text.

*The variable is contained within quotation marks and curly brackets*

    ---
    - name: ProxMox
      hosts: proxmox
      vars_prompt:
      - name: api_key
        prompt: Enter the API Key
      tasks:
      - name: Create new container.
        community.general.proxmox:
        node: 'ProxMox-Host'
        api_user: 'root@pam'
        api_password: "{{ api_key }}"
        api_host: 'proxmox-host.example.com'
 
When you run the playbook with you'll be promoted with **Enter the API Key**, and once you enter the password it will be saved as the api_key variable and used within the Playbook.

Whilst this works fine, it requires interaction so not ideal if I wanted to run a regular scheduled activity such as updating or patching servers.

## Using Ansible Vault to hold the secrets securely

Ansible Vault can also be used to hold the passwords securely in an encrypted file. With this method you need to create a file which contains the variables called within your playbook and the corresponsing secret/password. For this I created a single file called defaults.enc, I thought calling it 'secrets' or 'passwords' might be a little too obvious!

> nano defaults.enc

With this new file you need to add each variable with the password.

    api_key: SecretPassword

Once you've done this, save the file.

Next, you need to encrypt the file so the secrets within are protected. There's an Ansible command for that...

> ansible-vault encrypt defaults.enc

You'll be prompted to add a password for the vault, **remember this** as you'll need it when editing the file and when using when you run the Playbook.

when you edit the file now you'll see the file has been encrypted and just contains a lot numbers. Don't worry, you can still edit it if you need to with the following command.

> ansible-vault edit defaults.enc

This will open the file securely, using **vi** as the editor, and it will remain encrypted and secured after you save it.

The Playbook will look similar to the previous one, but without the **vars_prompt:** section. The api_key variable is still in-place, but this will be taken from the **defaults.enc** file rather than via a prompt for the key.

    ---
    - name: ProxMox
      hosts: proxmox

      tasks:
      - name: Create new container.
        community.general.proxmox:
        node: 'ProxMox-Host'
        api_user: 'root@pam'
        api_password: "{{ api_key }}"
        api_host: 'proxmox-host.example.com'

All sounds good so far, it's run with the following command:
> ansible-playbook -e @defaults.enc --ask-vault-pass test.yaml

However, whilst the secrets are encrypted and secured, you'll notice the **--ask-vault-pass** option in the command, meaning that you're still prompted for a password (the vault password) when it runs.
