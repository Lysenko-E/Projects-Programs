\# Local DICOM Receiver Scripts (DCMTK STORE SCP)
----

These are two simple Windows batch scripts that start a local DICOM Store SCP server on your PC. They allow you to receive DICOM files from any DICOM viewer or modality and save them into a folder of your choice. The scripts automatically display the server’s IP, AE Title, and Port so you can configure your sender easily.

Both scripts use DCMTK’s `storescp.exe` to listen for incoming C‑STORE requests.

They were created for local testing only, such as verifying DICOM export functionality or checking how a system handles incoming files.

# What These Scripts Do

 Start a local DICOM Store SCP server:
```bash
&nbsp; - AE Title: STORE\_SCP
```
```bash
&nbsp; - Port: 10500
```
\- Automatically detect and display your local IPv4 address

\- Show server information in the console

\- Run continuously until stopped with Ctrl + C

\- Save incoming files into a user‑defined folder

# Two versions are included:

1\. \*\*Send Server.cmd\*\*  

&nbsp;  Renames incoming files and forces the `.dcm` extension.

&nbsp;  Command used:

&nbsp;  storescp.exe -v -aet STORE\_SCP 10500 -od "<output\_folder>" --rename --filename-extension .dcm



2\. \*\*start-dicom-server-SaveAnyFormat.cmd\*\*  

&nbsp;  Saves files exactly as received (no renaming).

&nbsp;  Command used:

&nbsp;  storescp.exe -v -aet STORE\_SCP 10500 -od "<output\_folder>"

# Useful For

\- Testing DICOM export from viewers

\- Simulating a simple PACS receiver

\- Verifying network connectivity

\- Local development and debugging

# What You Can Edit

You can safely modify the following parts of the scripts:

\- AE Title:
```bash
&nbsp; -aet STORE\_SCP
```

\- Port:
```bash
&nbsp; 10500
```
\- Output directory:

&nbsp; -od "C:\\Users\\...\\received"

\- Path to DCMTK:

&nbsp; "C:\\path\\to\\dcmtk\\bin\\storescp.exe"

These are the only areas most users will need to change.

# Requirements

# ! DCMTK (DICOM Toolkit)

You must have DCMTK installed.

Download: https://dicom.offis.de/dcmtk.php.en

Required component:

\- storescp.exe (Store SCP server)

 Windows

These scripts are standard .bat files and run natively in Windows Command Prompt.

# How to Run

1\. Install DCMTK

2\. Edit the script paths if needed

3\. Double‑click the .bat file

4\. The server will start and wait for incoming DICOM files

5\. Configure your DICOM sender with:

&nbsp;  - AE Title: STORE\_SCP

&nbsp;  - IP: shown in the console

&nbsp;  - Port: 10500

6\. Incoming files will appear in your chosen output folder

<!--
    DLL Dependencies (DCMTK Runtime)
To run storescp.exe successfully, the following DLLs must be present in the same folder:
- dcmdata.dll
- dcmnet.dll
- dcmtls.dll
- ofstd.dll
- oflog.dll

Tested path:
C:\Users\Egidijus\Desktop\Dicom_Receive_files_testing\dcmtk-3.6.9-win32-dynamic\dcmtk-3.6.9-win32-dynamic\bin

These DLLs are part of the DCMTK dynamic build and are required for storescp.exe to function.
Do not delete or move them separately.
-->

# Notes \& Safety

\- These scripts run locally only — no network exposure unless you configure it.

\- They do not modify system settings or registry entries.

\- Intended for testing and development, not clinical or production use.

\- Ensure the selected port is allowed through Windows Firewall if needed.

# Why Two Versions?

\- \*\*Renaming version:\*\*  

&nbsp; Useful when the sender does not provide meaningful filenames or when you want consistent `.dcm` extensions.

in clinical settings this is a common problem, where received/sent files are not read by the PACS/DICOM archive system.

\- \*\*Save‑as‑received version:\*\*  

&nbsp; Useful for debugging, preserving original filenames, or testing how different systems send data.




