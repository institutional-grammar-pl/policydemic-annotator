import joblib
from pathlib import Path
import pandas as pd

model_path = Path('sentence_type_classifier.joblib')

model_pipeline = joblib.load(model_path)


def split(in_path, out_path):
    with open(in_path, 'r') as input_:
        file_text = input_.read()

    sentences = file_text.split('\n\n')

    df = pd.DataFrame({
        'text': sentences
    })

    is_regulative = model_pipeline.predict(df.text)

    constitutive = []
    regulative = []

    for label, sentence in zip(is_regulative, sentences):
        if label:
            regulative.append(sentence)
        else:
            constitutive.append(sentence)

    out_path = Path(out_path)
    constitutive_path = out_path.parent / (out_path.stem + '_constitutive.txt')
    regulative_path = out_path.parent / (out_path.stem + '_regulative.txt')

    with open(constitutive_path, 'w+') as cont_file:
        cont_file.write('\n\n'.join(constitutive))

    with open(regulative_path, 'w+') as reg_file:
        reg_file.write('\n\n'.join(regulative))

