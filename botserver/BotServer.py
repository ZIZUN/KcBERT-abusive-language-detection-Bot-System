﻿import os
import logging
import argparse
import mysql.connector
from tqdm import tqdm, trange

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import AutoModelForSequenceClassification

from utils import init_logger, load_tokenizer

import time

import re
import emoji
from soynlp.normalizer import repeat_normalize

def clean(x):
    x = pattern.sub(' ', x)
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)
    return x

emojis = ''.join(emoji.UNICODE_EMOJI.keys())
pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-힣{emojis}]+')
url_pattern = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

logger = logging.getLogger(__name__)

mysql_con = None

def softmax(a) :
    exp_a = np.exp(a)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    
    return y

def select_comment(idvalue):
    try:
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='django_web', user='root', password='root')
                                            
        mysql_cursor = mysql_con.cursor(dictionary=True)

        sql = "select * from blog_comment where id = " + str(idvalue) + ";"
        
        mysql_cursor.execute(sql)
        i = 0

        for row in mysql_cursor:
            i = i+1
            
            
        mysql_cursor.close()

        if i>=1:
            return 1
        else:
            return 0

    except Exception as e:
        print(e.message)


    finally:
        if mysql_con is not None:
            mysql_con.close()


def print_comment(idvalue):
    try:

        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='django_web', user='root', password='root')
                                            
        mysql_cursor = mysql_con.cursor(dictionary=True)

        sql = "select * from blog_comment where id = " + str(idvalue) + ";"
        
        mysql_cursor.execute(sql)
        
        
        for row in mysql_cursor:
            return(str(row['text']))

        mysql_cursor.close()

    except Exception as e:
        print(e.message)


    finally:
        if mysql_con is not None:
            mysql_con.close()   
            
def update_comment(idvalue, str_):
    try:

        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='django_web', user='root', password='root')
                                            
        mysql_cursor = mysql_con.cursor(dictionary=True)      
        
        sql = "UPDATE blog_comment SET text = '" + str_ + "' WHERE id = "+ str(idvalue) + ";"
        
        mysql_cursor.execute(sql)
            
        mysql_con.commit()
            
        mysql_cursor.close()

    except Exception as e:
        print(e.message)


    finally:
        if mysql_con is not None:
            mysql_con.close()   
            
def search_comment_idvalue():  # 
    i = 1
    while(1):
        if select_comment(i) == 1:
            i= i+1
            continue
        else:
            return i-1

def get_device(pred_config):
    return "cuda" if torch.cuda.is_available() and not pred_config.no_cuda else "cpu"


def get_args(pred_config):
    return torch.load(os.path.join(pred_config.model_dir, 'training_args.bin'))


def load_model(pred_config, args, device):
    # Check whether model exists
    if not os.path.exists(pred_config.model_dir):
        raise Exception("Model doesn't exists! Train first!")

    try:
        model = AutoModelForSequenceClassification.from_pretrained(args.model_dir)  # Config will be automatically loaded from model_dir
        model.to(device)
        model.eval()
        logger.info("***** Model Loaded *****")
    except:
        raise Exception("Some model files might be missing...")

    return model




def convert_input_file_to_tensor_dataset(pred_config,
                                         args,
                                         first_,
                                         last_,
                                         cls_token_segment_id=0,
                                         pad_token_segment_id=0,
                                         sequence_a_segment_id=0,
                                         mask_padding_with_zero=True):
    tokenizer = load_tokenizer(args)

    # Setting based on the current model type
    cls_token = tokenizer.cls_token
    sep_token = tokenizer.sep_token
    pad_token_id = tokenizer.pad_token_id

    all_input_ids = []
    all_attention_mask = []
    all_token_type_ids = []

    for i in range(first_, last_+1):
        line = print_comment(i)
        line = clean(line) #전처리
        line = line.strip()
        tokens = tokenizer.tokenize(line)
        # Account for [CLS] and [SEP]
        special_tokens_count = 2
        if len(tokens) > args.max_seq_len - special_tokens_count:
            tokens = tokens[:(args.max_seq_len - special_tokens_count)]

        # Add [SEP] token
        tokens += [sep_token]
        token_type_ids = [sequence_a_segment_id] * len(tokens)

        # Add [CLS] token
        tokens = [cls_token] + tokens
        token_type_ids = [cls_token_segment_id] + token_type_ids

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real tokens are attended to.
        attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # Zero-pad up to the sequence length.
        padding_length = args.max_seq_len - len(input_ids)
        input_ids = input_ids + ([pad_token_id] * padding_length)
        attention_mask = attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
        token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)

        all_input_ids.append(input_ids)
        all_attention_mask.append(attention_mask)
        all_token_type_ids.append(token_type_ids)

    # Change to Tensor
    all_input_ids = torch.tensor(all_input_ids, dtype=torch.long)
    all_attention_mask = torch.tensor(all_attention_mask, dtype=torch.long)
    all_token_type_ids = torch.tensor(all_token_type_ids, dtype=torch.long)

    dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids)

    return dataset

if __name__ == "__main__":
    init_logger()
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", default="sample_pred_in.txt", type=str, help="Input file for prediction")
    parser.add_argument("--output_file", default="sample_pred_out.txt", type=str, help="Output file for prediction")
    parser.add_argument("--model_dir", default="./model", type=str, help="Path to save, load model")

    parser.add_argument("--batch_size", default=32, type=int, help="Batch size for prediction")
    parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")

    pred_config = parser.parse_args()



    # load model and args
    args = get_args(pred_config)
    device = get_device(pred_config)
    model = load_model(pred_config, args, device)
    logger.info(args)

    # Convert input file to TensorDataset

    first_ = search_comment_idvalue() 
    
    while(1):
        time.sleep(3)
        
        last_ = search_comment_idvalue()

        
        if first_==last_ :
            continue
        
        
        dataset = convert_input_file_to_tensor_dataset(pred_config, args, first_+1, last_)

        # Predict
        sampler = SequentialSampler(dataset)

        data_loader = DataLoader(dataset, sampler=sampler, batch_size=pred_config.batch_size)

        preds = None

        for batch in tqdm(data_loader, desc="Predicting"):
            batch = tuple(t.to(device) for t in batch)
            with torch.no_grad():
                inputs = {"input_ids": batch[0],
                          "attention_mask": batch[1],
                          "labels": None}
                #if args.model_type != "distilkobert":
                inputs["token_type_ids"] = batch[2]

                outputs = model(**inputs)

                logits = outputs[0]

                if preds is None:
                    preds = logits.detach().cpu().numpy()
                else:
                    preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)

        preds = np.argmax(preds, axis=1)


        temp_num = 0
        
        for i in range(first_+1 , last_+1):
            
            if preds[temp_num] == 0:
                update_comment(i, "※ 탐지봇에 의해 악성댓글이 감지됨 ※")
                temp_num = temp_num + 1
            
        first_ = last_