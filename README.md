# Vocal-X
final year project

# // git request// 

opencmd:
Step 1: Git Repository Setup Karein (Pehli Baar)
Bash
# for clone
git clone https://github.com/Ashutoshgupta618/Vocal-X.git
cd vocal_X

#  BY Direct ( from your system to git)
cd vocal-X
git init

git remote add origin https://github.com/Ashutoshgupta618/Vocal-X.git


Step 2 (optional : Latest Code Download Karein from github (git pull) ) 
Ab main branch ka saara code apne system par lene ke liye pull chalayein:
# Code download aur merge karne ke liye
git pull origin main

--pull request or to paste your code in git
# Nayi branch banakar uspar switch karne ke liye
git checkout -b feature/new-folder-name

-- put all files on this--
git add .

git commit -m "Added new module folder"

git push -u origin feature/new-folder-name

Step 6: GitHub Par Pull Request (PR) Bana Kar Merge Karein
Apne browser me repository Vocal-X kholein.
"Compare & pull request" -> click kare -> Title write  -> fir "Create pull request" ->click kare
"Merge pull request" -> "Confirm merge" par click kar dein.

Step 7: Main Branch Ko Local Par Update Karein
Merge hone ke baad apne computer par wapas main branch ko update kar lein:
Bash
# Wapas main branch par aane ke liye
git checkout main
# GitHub se latest changes local system par lene ke liye
git pull origin main


Aage jab bhi koi naya folder ya code append karna ho, Step 2 se Step 7 tak ke steps dobara repeat karein.
