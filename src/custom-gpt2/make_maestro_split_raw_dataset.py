import pandas as pd
import shutil
import os

MAESTRO_PATH = 'data/raw/maestro/maestro-v3.0.0/'
OUTPUT_FOLDER_PATH = 'data/interim/maestro/'


def copy_and_clean_filename(df, group_name: str):
    output_path = OUTPUT_FOLDER_PATH + group_name + '/'

    # create folder if it doesn't exists
    if not os.path.exists(output_path):
        print('creating directory: ' + output_path)
        os.mkdir(output_path)

    for index, row in df.iterrows():
        original_file_path = MAESTRO_PATH + row['midi_filename']
        new_file_name = f"{row['year']}-{index}.midi"

        output_file_path = output_path + new_file_name

        # copy and rename file
        shutil.copy(original_file_path, output_file_path)


def organize_files():
    maestro_df = pd.read_csv(MAESTRO_PATH + 'maestro-v3.0.0.csv')
    grouped_df = maestro_df.groupby('split')

    for group_name, grouped_df in grouped_df:

        # Merge validation dataset with train dataset (For Language modeling training purposes)
        if group_name == 'validation':
            group_name = 'train'

        # Uses test dataset as the validation dataset (since we don't need a test set)
        elif group_name == 'test':
            group_name = 'validation'

        copy_and_clean_filename(grouped_df, group_name)


def main():
    if not os.path.exists(OUTPUT_FOLDER_PATH):
        print('creating directory: ' + OUTPUT_FOLDER_PATH)
        os.mkdir(OUTPUT_FOLDER_PATH)

    organize_files()


if __name__ == '__main__':
    main()