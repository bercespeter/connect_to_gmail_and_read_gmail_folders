# -*- coding: utf-8 -*-
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
#-----------------------------------------------------------------------------#
# Parameters
#-----------------------------------------------------------------------------#
# Sending: SMTP Server
SMTP_SERVER = "smtp.gmail.com" # this parameter is correct as of 2024.10.25.
SMTP_PORT   = 465              # this parameter is correct as of 2024.10.25.

# Reading: IMAP server
IMAP_SERVER = "imap.gmail.com" # this parameter is correct as of 2024.10.25.
IMAP_PORT   = 993              # this parameter is correct as of 2024.10.25.

# Account credentials
GMAIL_USERNAME = "your_username@gmail.com" # your_username@gmail.com: change it to yours
GMAIL_PASSWORD = "ABCD ABCD ABCD ABCD"     # your App password: change it to yours

#-----------------------------------------------------------------------------#
# List of Gmail account folders in English Gmail version 
# NOTE: Names are different in other languages, except the INBOX folder
GMAIL_FOLDERS = ['"INBOX"',             #item: [0]
                 '"[Gmail]/All Mail"',  #item: [1]
                 '"[Gmail]/Drafts"',    #item: [2]
                 '"[Gmail]/Important"', #item: [3]
                 '"[Gmail]/Sent Mail"', #item: [4]
                 '"[Gmail]/Spam"',      #item: [5]
                 '"[Gmail]/Starred"',   #item: [6]
                 '"[Gmail]/Trash"']     #item: [7]

#-----------------------------------------------------------------------------#
# Developer / Author rights:  Peter Berces (bercespeter@gmail.com) - License: Apache 2.0
def connect_to_gmail(p_username = GMAIL_USERNAME, p_password = GMAIL_PASSWORD):
    """Connect to the Gmail IMAP server"""
    
    try:
        
        # Package import
        import imaplib
        # Connect to the server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        # Login
        mail.login(p_username, p_password)
        
    except Exception as e_all:
        
        msg = "\nERROR: The following error(s) occured in the connect to Gmail procedure: " + str(e_all) + " !"
        print(msg)
        
    finally:
        
        if mail:
            
            msg = "\nNOTE: Successfull gmail connection attempt with the user: " + p_username + " !"
            print(msg)
            return mail
        
        else:
            
            msg = "\nERROR: Failed gmail connection attempt with the user: " + p_username + " !"
            print(msg)
            
# Sample call
# mail = connect_to_gmail()
#-----------------------------------------------------------------------------#
# Developer / Author rights:  Peter Berces (bercespeter@gmail.com) - License: Apache 2.0
def read_mailbox(p_username = GMAIL_USERNAME, p_password = GMAIL_PASSWORD, p_folder_name = GMAIL_FOLDERS[0]):
    """Lists all the Gmail message in the selected IMAP folder."""
    
    try:
        
        mail = connect_to_gmail(p_username, p_password)

        status, folders = mail.list()
    
        # for using other language display in Gmail then english uncomment this line
        # encoded_for_imap = utf_7_str_to_IMAP_modified_utf_7_str(p_folder_name) # uncomment this line in case of eg. german 
        encoded_for_imap = p_folder_name # comment out this line in case you use other language
        
        status, messages = mail.select(encoded_for_imap)
        
        if status != "OK":
            
            print("\nERROR: Failed to access the input folder.")
            
        else:
            
            # Fetch all email IDs from the input folder
            status, msg_nums = mail.search(None, "ALL")
            
            if status != "OK":
                
                print("\nERROR: Failed to retrieve email IDs.")
                
            else:
                
                print("\nNOTE: Process each email by ID in the input folder.")
                for num in msg_nums[0].split():
                    
                    # Fetch the email by ID
                    status, msg_data = mail.fetch(num, "(RFC822)")
                    
                    if status != "OK":
                        
                        print(f"\nERROR: Failed to fetch email with ID {num}")
                        continue
                    
                    # Parse the email content
                    try:
                        
                        # Package import
                        import email
                        msg = email.message_from_bytes(msg_data[0][1])
                    
                    except Exception as e:
                        
                        print(f"\nERROR: Could not import email or email content parsing failed: {e}")
                    
                    # Decode email sender
                    sender = msg["From"]
                    
                    # Decode email receiver
                    receiver = msg["To"]
                    
                    # Decode email subject
                    try:
                        
                        # Package import
                        from email.header import decode_header
                        subject, encoding = decode_header(msg["Subject"])[0]
                    
                    except Exception as e:
                        
                        print(f"\nERROR: Could not import email header or decoding header failed: {e}")
                        
                        
                    if isinstance(subject, bytes):
                        
                        subject = subject.decode(encoding if encoding else "utf-8")
                        
                    # Decode email date
                    date = msg["Date"]
                    parsed_date = email.utils.parsedate_to_datetime(date)
                    date_str = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Initialize attachment flag
                    attachment_flag = False
                    # Initialize email body
                    body = ""
                    
                    # Iterate through the email parts
                    if msg.is_multipart():
                        
                        for part in msg.walk():
                            
                            # Check for attachments
                            content_disposition = part.get("Content-Disposition", "")
                            if "attachment" in content_disposition:
                                
                                attachment_flag = True
                                
                            # Extract the email body
                            if part.get_content_type() == "text/plain" and "attachment" not in content_disposition:
                                
                                try:
                                    
                                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                                    
                                except Exception as e:
                                    
                                    print(f"\nERROR: Could not decode body: {e}")
                                    
                    else:
                        
                        # If the email is not multipart, extract the payload directly
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
                    
                    # Print the email details
                    print("\n")
                    print("-" * 40)
                    print("Sender: " + sender)
                    print("Receiver: " + receiver)
                    print("Date: " + date_str)
                    print("Has attachment: " + ("Yes" if attachment_flag else "No") )
                    print("-" * 40)
                    print("Subject :" + subject)
                    print("-" * 40)
                    print("Body: \n-----\n" + body[:5000] + "...")  # Print only first 5000 chars of the body
                    print("-" * 40)
                    print("\n")
                    print("*" * 75)  # Separator
                    
    except Exception as e_all:
        
        msg = "\nERROR: The following error(s) occured in the e-mail reading operation: " + str(e_all) + " !"
        print(msg)

"""
#-----------------------------------------------------------------------------#
# Sample calls of the procedure to list messages in different folders
#-----------------------------------------------------------------------------#
"""


read_mailbox(p_folder_name = GMAIL_FOLDERS[0]) # Uncomment line to read INBOX Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[1]) # Uncomment line to read  [Gmail]/All Mail Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[2]) # Uncomment line to read  [Gmail]/Drafts Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[3]) # Uncomment line to read  [Gmail]/Important Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[4]) # Uncomment line to read  [Gmail]/Sent Mail Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[5]) # Uncomment line to read  [Gmail]/Spam Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[6]) # Uncomment line to read  [Gmail]/Starred Folder
# read_mailbox(p_folder_name = GMAIL_FOLDERS[7]) # Uncomment line to read  [Gmail]/Trash Folder


"""
#-----------------------------------------------------------------------------#
# Appendix - for using other language display in Gmail with special character set
#            like hungarian (é,á,ö,...), german (ä, ö, ü, ẞ) or greek (𝛼,...) or 
#            other languages with special character sets.
#-----------------------------------------------------------------------------#
# Explanation - The "Sent Mail" or other folders except "INBOX" are translated
#               in the gmail account, so they have to be refferred as the original
#               display language writtes. Probaly it is weird, but when you use
#               forexample hungarian, your "Sent Mail" is "Elküldött levelek" and
#               you have to reffer it in hungarian, but the problem is that it
#               contains two special characters: 'ü' and 'ö'. It is listed like
#               'Elk&APw-ld&APY-tt levelek' if we chech Gmail folder's with the
#               procedure 'check_mailboxes()' (what you can find below). However this
#               can not be used to download the outbox folder because as an
#               input you have to translate it back and forth, so the result will be 
#               in the ouput:   'Elk&APw=-ld&APY=-tt levelek' - when you call the
#               check_mailboxes('Elk&APw-ld&APY-tt levelek') procedure. So I have
#               noticed, that it contains two equal ('=') signs in addition. And
#               every special chaaracter is a bit differrent in differrent encodings.
#-----------------------------------------------------------------------------#
"""
# Developer / Author rights:  Peter Berces (bercespeter@gmail.com) - License: Apache 2.0
def utf_7_str_to_IMAP_modified_utf_7_str(p_encoded_str_in_utf_7 = GMAIL_FOLDERS[0], p_silent_flg = 'No'):
    """Decodes a string from IMAP modified UTF-7 encoding to UTF-8 encoded string."""
    
    try:
        
        try:
            
            # Package imports
            import re
            import base64
            
        except Exception as e:
            
            print(f"\nERROR: Could not import regular expression or base64 package: {e}")
        
        encoded_string = p_encoded_str_in_utf_7.replace("&", "+").replace(",", "/")
    
        def decode_match(match):
            b64_str = match.group(1)
            utf16_bytes = base64.b64decode(b64_str + "===")
            result_in_utf16 = utf16_bytes.decode("utf-16-be")
            return result_in_utf16
    
        encoded_str_in_utf_8 = re.sub(r"\+([A-Za-z0-9+/]+)-", decode_match, encoded_string)
    
        """Encodes a UTF-8 string into IMAP modified UTF-7 encoded string."""
        def encode_match(match):
            utf16_bytes = match.group(0).encode('utf-16-be')
            b64_str = base64.b64encode(utf16_bytes).decode('ascii').replace('/', ',')
            result_in_b64_str = f'+{b64_str}-'
            return result_in_b64_str
        
        IMAP_modified_utf_7_str = re.sub(r'[^\x20-\x7E]+', encode_match, encoded_str_in_utf_8).replace('+', '&')

    except Exception as e_all:
        
        msg = "\nERROR: The following error(s) occured in the encoding procedure: " + str(e_all) + " !"
        print(msg)
        
    finally:
        
        if IMAP_modified_utf_7_str:
            
            if (p_silent_flg == 'Yes'):
                return IMAP_modified_utf_7_str   
            else:
                msg = "\nNOTE: Successfully initialized utf-7 coded folder string: " + str(IMAP_modified_utf_7_str) + " !"
                print(msg)
                return IMAP_modified_utf_7_str
        
        else:
            
            msg = "\nERROR: Failed to initialize utf-7 coded folder string."
            print(msg)

# Sample call
# folder_name = utf_7_str_to_IMAP_modified_utf_7_str('Elk&APw-ld&APY-tt levelek')
#-----------------------------------------------------------------------------#
# Developer / Author rights:  Peter Berces (bercespeter@gmail.com) - License: Apache 2.0
def check_mailboxes(p_username = GMAIL_USERNAME, p_password = GMAIL_PASSWORD):
    """List all the Gmail IMAP server's folders."""

    try:
        
        # Connect to Gmail
        mail = connect_to_gmail()
        status, folders = mail.list()

        # If folders retrieved successfully, print them
        if status == "OK":
            print("\nNOTE: Folders in your Gmail account are the following:\n")
            for folder in folders:
                print(utf_7_str_to_IMAP_modified_utf_7_str(folder.decode(), 'Yes'))  # Decode from bytes to string
        
    except Exception as e_all:
        
        print(f"\nERROR: An unexpected error occurred: {e_all}")
        
    finally:
        
        # Log out and close the connection if mail was initialized
        if 'mail' in locals():
            mail.logout()
        print("\nNOTE: See the folders listed above!")
        
# Sample call
# check_mailboxes()
#-----------------------------------------------------------------------------#
# Copyright [2024] [Peter Berces]

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    http://www.apache.org/licenses/LICENSE-2.0
"""
#-----------------------------------------------------------------------------#
#                              End of file
#-----------------------------------------------------------------------------#
"""