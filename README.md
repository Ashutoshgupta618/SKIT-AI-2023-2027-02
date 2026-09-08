# Vocal-X
final year project

# // git request// 

opencmd:
Step 1: Git Repository Setup Karein (Pehli Baar)
Bash
# Apne local system par repository clone karne ke liye
git clone https://github.com/Ashutoshgupta618/Vocal-X.git
# Project folder ke andar jane ke liye
cd Vocal-X 

Step 2: Nayi Feature Branch Banayein
Direct main me kaam na karke ek nayi branch banayein:

Bash
# Nayi branch banakar uspar switch karne ke liye
git checkout -b feature/new-folder-name

Step 3: Local Folder Banayein Aur Code Add Karein
apni files us folder me daalo

Step 4: Changes Staging Aur Commit Karein
Bash
# Naye folder aur saari nayi files ko add karne ke liye
git add .
# Changes ko message ke saath commit karne ke liye
git commit -m "Added new module folder"

Step 5: Nayi Branch Ko GitHub Par Push Karein
Bash
# Apni nayi branch ko GitHub par upload karne ke liye
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
