# Basic commands

## Basics

Structure of Powershell

Verbs and Nouns

```pwsh
get-verb
```

- Add
- New
- Remove
- Get
- Set
- Show
- Import
- Start
- Stop

etc!

The verb is followed by the action

```pwsh
get-azaduser
get-service
stop-service
```

### Getting help

Follow the command with -? to get basic help for a specific command

```pwsh
get-azaduser -?
get-service -?
```

Prefix a command with get-help for more detailed help

```pwsh
get-help get-service
```

### Checking which modules are installed

```pwsh
get-module -listavailable
```

### Reviewing the commands within a module

```pwsh
get-command
```

Shows all commands installed and available.

```pwsh
get-command -verb get
```

Shows all commands which use the verb get

```pwsh
get-command -noun service
```

Shows all commands related to the noun service

You can combine these to narrow down further

```pwsh
get-command -noun service -verb get
```

#### Listing all commands within a module

*if you want to understand what you can do with a module*

```pwsh
get-command -module az.accounts
```

#### Listing specific verbs within a module

*if you want to only look at commands which gather information but do not change anything*

```pwsh
get-command -module az.accounts -verb get
```

### Installing modules

Installing Powershell modules using **install-module**

Install-module by default will install for all users, and will need local admin to install.

You can use the following the avoid the need for local admin and install for the current user

```pwsh
install-module -scope currentuser

Install-Module -Name MicrosoftTeams -scope currentuser
```

*you will see this command if it's the first time you've used a repository*

```shell
Untrusted repository. You are installing the modules from an untrusted repository. If you trust this repository, change its InstallationPolicy value by running the Set-PSRepository cmdlet. Are you sure you want to install the modules from 'PSGallery'?
```

### Trust a repository

*You can throw caution to the wind and change the installation policy to untrusted, so all repositories are trusted by default. **However**, it's probably best not to do this, and consciously enable the repositories you want to trust*

```pwsh
set-psrepository psgallery -installationpolicy trusted
```

### Modules are installed in the following locations

"All User" modules

```shell
C:\Program Files\WindowsPowerShell\Modules
C:\Windows\system32\WindowsPowerShell\v1.0\Modules
```

"Local User" modules

```shell
C:\Users\vagrant\Documents\WindowsPowerShell\Modules
C:\Users\vagrant\OneDrive\Documents\WindowsPowerShell\Modules
```

*Note* - the second location shown above normally only occurs if you have OneDrive folder redirection enabled.

### Finding modules

```pwsh
find-module -name powershellget

find-module -name *account*

find-module -filter proxmox

find module -name *account* -repository
```

### Updating modules

Powershell doesn't automatically update its modules by default. If there's a newer version of a module which has some new features you need you can update it with the following command:

```pwsh
update-module az
```

### Getting more information an object's properties and actions

#### Get-member

You can use get-member to expand the properties and actions of an object. Firstly you need to get the object and then pipe it to the get-member cmdlet.

```pwsh
get-service w32time |get-member
```

This will report the **properties** and **methods** for the object and helps to build up a query or action with the relevant verb and object.

#### Example output

| Name    | MemberType | Definition |
| --- | --- | --- |
|Name | AliasProperty |Name = ServiceName |
|RequiredServices | AliasProperty |RequiredServices = ServicesDependedOn |
|Disposed |Event |System.EventHandler Disposed(System.Object, System.EventArgs) |
|Close |Method |void Close() |
|Continue |Method |void Continue() |
| CreateObjRef |Method |System.Runtime.Remoting.ObjRef CreateObjRef(type requestedType)|
|GetType |Method | type GetType() |
|Start |Method |void Start(), void Start(string[] args) |
|Stop |Method |void Stop() |
|CanPauseAndContinue |Property |bool CanPauseAndContinue {get;} |
|CanShutdown |Property |bool CanShutdown {get;} |
|CanStop |Property |bool CanStop {get;} |
|Container |Property |System.ComponentModel.IContainer Container {get;}|
|DependentServices |Property |System.ServiceProcess.ServiceController[] DependentServices {get;} |
|DisplayName |Property |string DisplayName {get;set;} |
|MachineName |Property |string MachineName {get;set;} |
StartType |Property |System.ServiceProcess.ServiceStartMode StartType {get;} |
Status |Property |System.ServiceProcess.ServiceControllerStatus Status {get;} |
|ToString |ScriptMethod |System.Object ToString(); |

The properties can then be used to struture a command which shows the relevant properties for two services.

```pwsh
get-service w32time, netman |select name, servicetype, starttype, status
```

|Name |ServiceType |StartType |Status |
| --- | --- | --- | --- |
|netman |Win32OwnProcess Win32ShareProcess |Manual |Stopped |
|w32time |Win32OwnProcess, Win32ShareProcess |Manual |Running |


https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-string-substitutions?view=powershell-7.4
