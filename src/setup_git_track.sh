export git_activity_path=$(pwd)
cd $git_activity_path
chmod +x main.py
cp main.py github-activity
chmod +x github-activity
echo "export PATH=\"\$PATH:$git_activity_path\"" >> ~/.bashrc
bash