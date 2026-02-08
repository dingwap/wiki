# Python Modules

## Understanding modules

Modules contain functions which can be used for specific actions.

## Checking which modules are installed

You can check which modules are installed with:

>help("modules")

This will show a complete list of all modules installed.

## Finding Modules

The main repository is the [Python Package Index](pypi.org). You can search for specific words or types of modules you're looking for, and often the functions and how to use the modules are shown within the repository.

When they're not identitied you can find a link to the website for the specific module, which will provide futher info for their use.

## Installing

Before any module you have to install it onto the device where the script is being run from.

You can do this with:

>python -m pip install PackageName

**Example**

    python -m pip install langdetect

## Listing out the module

You can check which modules are installed with

>help("modules")

This will show a complete list of all modules installed.

## Understanding modules

Modules contain functions which can be used for specific actions.

## Finding Modules

The main repository is the [Python Package Index](pypi.org). You can search for specific words or types of modules you're looking for, and often the functions and how to use the modules are shown within the repository.

When they're not identitied you can find a link to the website for the specific module, which will provide futher info for their use.

**Listing out the module**

>dir (module)

**Getting help for a module**

To view the help file for a specific module:

>help (module)

**Example**

    from textblob import TextBlob
    dir(TextBlob)
    help(TextBlob)
