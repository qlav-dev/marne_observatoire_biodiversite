conda env create -f environment.yml
conda activate marne_observatoire


# Si pip:
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate sur Windows
pip install -r requirements.txt