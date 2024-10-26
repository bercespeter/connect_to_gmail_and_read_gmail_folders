# -*- coding: utf-8 -*-
# connect_to_gmail_and_read_gmail_folders
"""
#-----------------------------------------------------------------------------#
# Description: Read Gmail messages with Python code
#              Connect to Gmail and read any Gmail folders from Python code.
#              The results will be displayed in the standard ouput.
#              You just have to change your username and password in the parameters section.
#-----------------------------------------------------------------------------#
# Created: 2024.10.25. 06:47:11
# Copyright: 2024, Peter Berces
# License: Apache 2.0 
# Developer:  Peter Berces (bercespeter@gmail.com)
# Name:    connect_to_gmail_and_read_gmail_folders.py
# 
# https://github.com/bercespeter/connect_to_gmail_and_read_gmail_folders/blob/main/LICENSE
#-----------------------------------------------------------------------------#
# Pre-requisit steps for setting up access for your Gmail account
# 
# Setup Step 1.: Enable IMAP access for your Gmail account from the Gmail settings.
#                1. Sign in to your Gmail account in a browser
#                2. Click the Gmail gear icon on the top right corner.
#                3. Choose Settings > Forwarding and POP/IMAP.
#                4. Select Enable IMAP, and then choose Save Changes.
#                
# Setup Step 2.: Set up an App Password after you have "2-Step Verification" enabled
#                1. Sign in to your Gmail account in a browser
#                2. Click the Gmail profile picture icon on the top right corner, select "Manage your Google Account"
#                3. Under your "Google Account" choose the "Security" tab
#                4. Go to the "How you sign in to Google" pane and click on "2-Step Verification"
#                5. Turn it on
#                6. Go to the "App passwords" pane and generate an App Password
#-----------------------------------------------------------------------------#
# Pre-requisit steps for setting up Python code
# 
# Base setup steps: Make sure email and imaplib packages are installed. If not then run command 
#                   from Anaconda prompt: "pip install email" after that "pip install imaplib".
# 
# Additional Steps: If your language display setting in Gmail is using special
#                   characters (like german or hungarian) then you have to install
#                   re and base64 packages with "pip install re" after that 
#                   "pip install base64".
#-----------------------------------------------------------------------------# 
# Parameter setup: Change your GMAIL_USERNAME and GMAIL_PASSWORD (your App Password)
#-----------------------------------------------------------------------------#
"""
