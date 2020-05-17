import pickle
import Levenshtein as Lev
import torch
from e2e.modules.definition import logger


def char_distance(target, y_hat):
    """
    Calculating charater distance between target & y_hat

    Args:
        target: sequence of target
        y_hat: sequence of y_Hat

    Returns: distance, length
        - **dist**: distance between target & y_hat
        - **length**: length of target sequence
    """
    target = target.replace(' ', '')
    y_hat = y_hat.replace(' ', '')

    dist = Lev.distance(y_hat, target)
    length = len(target.replace(' ', ''))

    return dist, length


def get_distance(targets, y_hats, id2char, eos_id):
    """
    Provides total character distance between targets & y_hats

    Args:
        targets (torch.Tensor): set of ground truth
        y_hats (torch.Tensor): predicted y values (y_hat) by the model
        id2char (dict): id2char[id] = ch
        eos_id (int): identification of <end of sequence>

    Returns: total_dist, total_length
        - **total_dist**: total distance between targets & y_hats
        - **total_length**: total length of targets sequence
    """
    total_dist = 0
    total_length = 0

    for (target, y_hat) in zip(targets, y_hats):
        script = label_to_string(target, id2char, eos_id)
        pred = label_to_string(y_hat, id2char, eos_id)

        dist, length = char_distance(script, pred)

        total_dist += dist
        total_length += length

    return total_dist, total_length


def get_label(filepath, sos_id, eos_id, target_dict=None):
    """
    Provides specific file`s label to list format.

    Args:
        filepath (str): specific path of label file
        sos_id (int): identification of <start of sequence>
        eos_id (int): identification of <end of sequence>
        target_dict (dict): dictionary of filename and labels

    Returns: label
        - **label** (list): list of bos + sequence of label + eos
    """
    assert target_dict is not None, 'target_dict is None'

    key = filepath.split('/')[-1].split('.')[0]

    script = target_dict[key]
    tokens = script.split(' ')

    labels = list()
    labels.append(int(sos_id))
    for token in tokens:
        labels.append(int(token))
    labels.append(int(eos_id))

    return labels


def label_to_string(labels, id2char, eos_id):
    """
    Converts label to string (number => Hangeul)

    Args:
        labels (list): number label
        id2char (dict): id2char[id] = ch
        eos_id (int): identification of <end of sequence>

    Returns: sentence
        - **sentence** (str or list): Hangeul representation of labels
    """
    if len(labels.shape) == 1:
        sentence = str()
        for label in labels:
            if label.item() == eos_id:
                break
            sentence += id2char[label.item()]
        return sentence

    elif len(labels.shape) == 2:
        sentences = list()
        for batch in labels:
            sentence = str()
            for label in batch:
                if label.item() == eos_id:
                    break
                sentence += id2char[label.item()]
            sentences.append(sentence)
        return sentences


def save_pickle(save_var, savepath, message=""):
    """ Save variable using pickle """
    with open(savepath + '.bin', "wb") as f:
        pickle.dump(save_var, f)
    logger.info(message)


def print_args(args):
    """ Print arguments """
    logger.info('--mode: %s' % str(args.mode))
    logger.info('--use_multi_gpu: %s' % str(args.use_multi_gpu))
    logger.info('--init_uniform: %s' % str(args.init_uniform))
    logger.info('--use_bidirectional: %s' % str(args.use_bidirectional))
    logger.info('--input_reverse: %s' % str(args.input_reverse))
    logger.info('--use_augment: %s' % str(args.use_augment))
    logger.info('--use_pickle: %s' % str(args.use_pickle))
    logger.info('--use_cuda: %s' % str(args.use_cuda))
    logger.info('--model_path: %s' % str(args.model_path))
    logger.info('--augment_num: %s' % str(args.augment_num))
    logger.info('--hidden_dim: %s' % str(args.hidden_dim))
    logger.info('--dropout: %s' % str(args.dropout))
    logger.info('--n_head: %s' % str(args.num_heads))
    logger.info('--label_smoothing: %s' % str(args.label_smoothing))
    logger.info('--listener_layer_size: %s' % str(args.listener_layer_size))
    logger.info('--speller_layer_size: %s' % str(args.speller_layer_size))
    logger.info('--conv_type: %s' % str(args.conv_type))
    logger.info('--rnn_type: %s' % str(args.rnn_type))
    logger.info('--k: %s' % str(args.k))
    logger.info('--batch_size: %s' % str(args.batch_size))
    logger.info('--num_workers: %s' % str(args.num_workers))
    logger.info('--max_epochs: %s' % str(args.num_epochs))
    logger.info('--lr: %s' % str(args.lr))
    logger.info('--min_lr: %s' % str(args.min_lr))
    logger.info('--lr_factor: %s' % str(args.lr_factor))
    logger.info('--lr_patience: %s' % str(args.lr_patience))
    logger.info('--teacher_forcing_ratio: %s' % str(args.teacher_forcing_ratio))
    logger.info('--valid_ratio: %s' % str(args.valid_ratio))
    logger.info('--max_len: %s' % str(args.max_len))
    logger.info('--seed: %s' % str(args.seed))
    logger.info('--sr: %s' % str(args.sr))
    logger.info('--window_size: %s' % str(args.window_size))
    logger.info('--stride: %s' % str(args.stride))
    logger.info('--n_mels: %s' % str(args.n_mels))
    logger.info('--normalize: %s' % str(args.normalize))
    logger.info('--del_silence: %s' % str(args.del_silence))
    logger.info('--feature_extract_by: %s' % str(args.feature_extract_by))
    logger.info('--time_mask_para: %s' % str(args.time_mask_para))
    logger.info('--freq_mask_para: %s' % str(args.freq_mask_para))
    logger.info('--time_mask_num: %s' % str(args.time_mask_num))
    logger.info('--freq_mask_num: %s' % str(args.freq_mask_num))
    logger.info('--save_result_every: %s' % str(args.save_result_every))
    logger.info('--checkpoint_every: %s' % str(args.checkpoint_every))
    logger.info('--print_every: %s' % str(args.print_every))
    logger.info('--resume: %s' % str(args.resume))
