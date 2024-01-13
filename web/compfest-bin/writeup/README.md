# COMPFEST-Bin | Web (500 pts)

**POC**

1. Given a web service which is stated to be a clone of `pastebin`. After inspecting the feature, it seems that it used older `Weasyprint module` which is can be used to do a Local File Inclusion (LFI). 
2. By using the LFI approach, we can start to enumerate the source code inside `/proc/sef/cwd/app.py`
3. There, we found another vulnerability which is SQLite Injection inside `edit_profile` route. Furthermore, it can be used to enumerate the `notes` table which is likely to be encrypted
4. Fortunately, the encryption/decryption function can be found inside the `controllers/Utils.py`, so that we can just make use of it in order to decrypt the admin's note
