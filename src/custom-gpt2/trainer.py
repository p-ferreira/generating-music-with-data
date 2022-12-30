import os
import torch
from datasets import load_dataset
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import WhitespaceSplit
from tokenizers.trainers import WordLevelTrainer
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, GPT2Config, DataCollatorForLanguageModeling, \
    TrainingArguments, Trainer



TRAIN_TOKEN_SEQUENCES_PATH = '../../data/processed/train_data.txt'
VALIDATION_TOKEN_SEQUENCES_PATH = '../../data/processed/validation_data.txt'

TOKEN_SEQUENCES_PATHS = [TRAIN_TOKEN_SEQUENCES_PATH, VALIDATION_TOKEN_SEQUENCES_PATH]
TOKENIZER_PATH = 'tokenizer.json'

# Special Tokens
UNK_TOKEN = '[UNK]'
PAD_TOKEN = '[PAD]'
BOS_TOKEN = '[BOS]'
EOS_TOKEN = '[EOS]'

SPECIAL_TOKENS = [UNK_TOKEN, BOS_TOKEN, EOS_TOKEN, PAD_TOKEN]


def load_tokenizer() -> PreTrainedTokenizerFast:
    if not os.path.exists(TOKENIZER_PATH):
        print('Creating new tokenizer...')
        tokenizer = Tokenizer(WordLevel(unk_token=UNK_TOKEN))
        tokenizer.pre_tokenizer = WhitespaceSplit()
        trainer = WordLevelTrainer(special_tokens=SPECIAL_TOKENS)

        tokenizer.train(files=TOKEN_SEQUENCES_PATHS, trainer=trainer)

        tokenizer.save(TOKENIZER_PATH)

        print('Tokenizer created!')
    else:
        print('Using existing tokenizer...')

    pretrained_tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
    # Ensures PAD token is added
    pretrained_tokenizer.add_special_tokens({'pad_token': PAD_TOKEN})
    return pretrained_tokenizer


def tokenize(elements, tokenizer: PreTrainedTokenizerFast):
    outputs = tokenizer(
        elements['text'],
        truncation=True,
        max_length=50,
        return_overflowing_tokens=True,
        return_length=True
    )

    return {"input_ids": outputs["input_ids"]}


def create_model(tokenizer: PreTrainedTokenizerFast) -> GPT2LMHeadModel:
    vocab_size = len(tokenizer.get_vocab())

    bos_token_id = tokenizer.convert_tokens_to_ids(BOS_TOKEN)
    eos_token_id = tokenizer.convert_tokens_to_ids(EOS_TOKEN)
    pad_token_id = tokenizer.convert_tokens_to_ids(PAD_TOKEN)

    model_config = GPT2Config(
        vocab_size=vocab_size,
        pad_token_id=pad_token_id,
        bos_token_id=bos_token_id,
        eos_token_id=eos_token_id,
        # Hyper parameters
        n_head=8,
        n_layer=6,
        n_embd=512,
        n_positions=1024,
        n_ctx=1024,
    )

    model = GPT2LMHeadModel(model_config)
    return model


def get_training_args() -> TrainingArguments:
    return TrainingArguments(
        output_dir="gpt2_language_model",
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        evaluation_strategy="steps",
        eval_steps=5_000,
        logging_steps=5_000,
        gradient_accumulation_steps=8,
        num_train_epochs=20,
        weight_decay=0.1,
        warmup_steps=1_000,
        lr_scheduler_type="cosine",
        learning_rate=5e-4,
        save_steps=5_000,
        save_total_limit=5,
        load_best_model_at_end=True,
        overwrite_output_dir=True,
        fp16=True
    )


def main():
    print('Starting...')
    tokenizer = load_tokenizer()
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    print('Loading dataset...')

    raw_dataset = load_dataset(
        'text',
        data_files=
        {
            "train": TRAIN_TOKEN_SEQUENCES_PATH,
            "validation": VALIDATION_TOKEN_SEQUENCES_PATH
        })

    print(f'Raw dataset loaded:'
          f' train={len(raw_dataset["train"])} validation={len(raw_dataset["validation"])}')

    print('Tokenizing dataset...')

    tokenized_dataset = raw_dataset.map(
        lambda element: tokenize(element, tokenizer),
        batched=True,
        remove_columns='text')  # Remove the original text column

    print(f'Dataset created: '
          f'train={len(tokenized_dataset["train"])} validation={len(tokenized_dataset["validation"])}')

    model = create_model(tokenizer)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    training_args = get_training_args()

    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['validation'],
    )

    print('Start model training...')
    trainer.train()
    print('Model training finished!')


if __name__ == '__main__':
    main()
