set -e
cd online_install
pip install requirements.txt
python install_database.py
cd ..
cp -r online/* ./
curl 'localhost/login.php'
