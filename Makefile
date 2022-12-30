JSB_CHORALES_URL=http://www-ens.iro.umontreal.ca/~boulanni/JSB%20Chorales.zip
MUSE_DATA_URL=http://www-ens.iro.umontreal.ca/~boulanni/MuseData.zip
MAESTRO_URL=https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip

RAW_DATA_DIR=data/raw

# Create maestro dataset
maestro-ds: maestro maestro-token-sequence-gpt2

########################################## GET RAW DATASETS ##########################################
maestro:
	echo 'Downloading and extracting MAESTRO dataset...'
	wget -O $(RAW_DATA_DIR)/maestro.zip $(MAESTRO_URL)
	unzip -o $(RAW_DATA_DIR)/maestro.zip -d $(RAW_DATA_DIR)/maestro
	rm $(RAW_DATA_DIR)/maestro.zip

########################################## PROCESS RAW DATASETS ##########################################

maestro-token-sequence-gpt2:
	echo 'Splitting MAESTRO dataset in training and validation...'
	python src/custom-gpt2/make_maestro_split_raw_dataset.py
	echo 'Creating token sequences...'
	python src/custom-gpt2/make_token_sequence_dataset.py


clean:
	echo Deleting raw data
	rm -r ./data/raw/*
