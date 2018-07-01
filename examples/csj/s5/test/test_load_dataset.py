#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import unittest

sys.path.append(os.path.abspath('../../../../'))
from src.dataset.loader import Dataset
from src.utils.measure_time_func import measure_time


class TestLoadDataset(unittest.TestCase):

    def test(self):

        # self.check(label_type='character_wb_left', data_type='eva1')
        # self.check(label_type='character_wb_right', data_type='eva1')
        # self.check(label_type='character_wb_both', data_type='eva1')
        # self.check(label_type='character_wb_remove', data_type='eva1')

        # data_type
        self.check(label_type='character_wb', data_type='train')
        self.check(label_type='word', data_type='train')
        self.check(label_type='word', data_type='dev')
        self.check(label_type='word', data_type='eval1')
        self.check(label_type='word', data_type='eval2')
        self.check(label_type='word', data_type='eval3')

        # data_size
        self.check(label_type='word', data_type='dev', data_size='aps_other')
        self.check(label_type='word', data_type='dev', data_size='all')

        # label_type
        self.check(label_type='character')
        self.check(label_type='character_wb')
        self.check(label_type='pos')
        self.check(label_type='phone')
        self.check(label_type='phone_wb')

        # sort
        self.check(label_type='word', sort_utt=True)

    @measure_time
    def check(self, label_type, data_type='dev', data_size='aps_other',
              shuffle=False, sort_utt=True, sort_stop_epoch=None):

        print('========================================')
        print('  label_type: %s' % label_type)
        print('  data_type: %s' % data_type)
        print('  data_size: %s' % data_size)
        print('  shuffle: %s' % str(shuffle))
        print('  sort_utt: %s' % str(sort_utt))
        print('  sort_stop_epoch: %s' % str(sort_stop_epoch))
        print('========================================')

        dataset = Dataset(
            corpus='csj',
            data_save_path='/n/sd8/inaguma/corpus/csj/kaldi',
            input_freq=80, use_delta=False, use_double_delta=False,
            data_size=data_size, data_type=data_type,
            label_type=label_type, batch_size=64, max_epoch=1,
            shuffle=shuffle, sort_utt=sort_utt,
            reverse=True, sort_stop_epoch=sort_stop_epoch,
            tool='htk', num_enque=None)

        print('=> Loading mini-batch...')
        if label_type == 'word':
            map_fn = dataset.idx2word
        elif 'character' in label_type:
            map_fn = dataset.idx2char
        elif 'phone' in label_type:
            map_fn = dataset.idx2phone

        for batch, is_new_epoch in dataset:
            str_ref = batch['ys'][0]
            if not dataset.is_test:
                str_ref = map_fn(str_ref)

            print('----- %s (epoch: %.3f, batch: %d) -----' %
                  (batch['input_names'][0], dataset.epoch_detail, len(batch['xs'])))
            print(str_ref)
            print('x_lens: %d' % (len(batch['xs'][0]) / 8))
            if not dataset.is_test:
                print('y_lens: %d' % (len(batch['ys'][0])))

            if dataset.epoch_detail >= 1:
                break


if __name__ == '__main__':
    unittest.main()