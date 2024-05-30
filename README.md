# Bulk Tag Assignment for Stack Overflow for Teams
A Python script that uses the Stack Overflow for Teams API to assign a specified tag to all existing questions

## Table of Contents
* [Requirements](https://github.com/jklick-so/so4t_bulk_tag_assignment?tab=readme-ov-file#requirements)
* [Setup](https://github.com/jklick-so/so4t_bulk_tag_assignment?tab=readme-ov-file#setup)
* [Usage](https://github.com/jklick-so/so4t_bulk_tag_assignment?tab=readme-ov-file#usage)
* [Support, security, and legal](https://github.com/jklick-so/so4t_bulk_tag_assignment?tab=readme-ov-file#support-security-and-legal)


## Requirements
* Stack Overflow Enterprise or Business
* Python 3.8 or higher ([download](https://www.python.org/downloads/))
* Operating system: Linux, MacOS, or Windows

## Setup

[Download](https://github.com/jklick-so/so4t_bulk_tag_assignment/archive/refs/heads/main.zip) and unpack the contents of this repository

**Installing Dependencies**

* Open a terminal window (or, for Windows, a command prompt)
* Navigate to the directory where you unpacked the files
* Install the dependencies: `python3 -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org`

> NOTE: Depending on your installation of Python, you may need to use `python` or `py` instead of `python3` in the command above. If `python3` is not a recognized command, you can check which command to use by running `python --version` or `py --version` in your terminal and seeing which responds with the installed Python version.

**API Authentication**

To authenticate with the Stack Overflow API, you will need to generate a valid access token with write permissions. To generate an access token, follow the instructions in the KB article titled [Secure API Token Generation Using OAuth with PKCE](https://support.stackenterprise.co/support/solutions/articles/22000286119-secure-api-token-generation-using-oauth-with-pkce)

> NOTE: you'll need to make sure to include the `write_access` scope when generating your token, otherwise you will not be able to make the necessary updates to content via the API.

## Usage

In a terminal window, navigate to the directory where you unpacked the script. Run the script with the following format, replacing the `SUBDOMAIN`, `YOUR_TOKEN`, and `TAG_NAME` with your own values.

`python3 main.py --url "https://SUBDOMAIN.stackenterprise.co" --token "YOUR_TOKEN" --tag "TAG_NAME"`

* SUBDOMAIN: The subdomain of your Stack Overflow Enterprise site. For example, if your site is `https://stackoverflow.enterprise.com`, then the subdomain would be `stackoverflow`.
* YOUR_TOKEN: The token you generated in the previous step.
* TAG_NAME: The name of the tag you want to assign to existing content.

> WARNING: As currently designed, this will assign the given tag to ALL existing questions. If a subset of questions is desired, feel free modify the script to accept a list of questions or question IDs. 


## Support, security, and legal
Disclaimer: the creator of this project works at Stack Overflow, but it is a labor of love that comes with no formal support from Stack Overflow. 

If you run into issues using the script, please [open an issue](https://github.com/jklick-so/so4t_bulk_tag_assignment/issues). You are also welcome to edit the script to suit your needs, steal the code, or do whatever you want with it. It is provided as-is, with no warranty or guarantee of any kind. If the creator wasn't so lazy, there would likely be an MIT license file included.
