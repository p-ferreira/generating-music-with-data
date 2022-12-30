import os
import torch
import itertools, os
import numpy as np
from progress.bar import Bar

import config
import utils
from sequence import EventSeq, ControlSeq

# pylint: disable=E1101
# pylint: disable=W0101

class Dataset:
    def __init__(self, root, verbose=False):
        assert os.path.isdir(root), root
        paths = utils.find_files_by_extensions(root, ['.data'])
        self.root = root
        self.samples = []
        self.seqlens = []
        if verbose:
            paths = Bar(root).iter(list(paths))
        for path in paths:
            eventseq, controlseq = torch.load(path)
            controlseq = ControlSeq.recover_compressed_array(controlseq)
            assert len(eventseq) == len(controlseq)
            self.samples.append((eventseq, controlseq))
            self.seqlens.append(len(eventseq))
        self.avglen = np.mean(self.seqlens)
    
    def batches(self, batch_size, window_size, stride_size):
        indeces = [(i, range(j, j + window_size))
                   for i, seqlen in enumerate(self.seqlens)
                   for j in range(0, seqlen - window_size, stride_size)]
        while True:
            eventseq_batch = []
            controlseq_batch = []
            n = 0
            for ii in np.random.permutation(len(indeces)):
                i, r = indeces[ii]
                eventseq, controlseq = self.samples[i]
                eventseq = eventseq[r.start:r.stop]
                controlseq = controlseq[r.start:r.stop]
                eventseq_batch.append(eventseq)
                controlseq_batch.append(controlseq)
                n += 1
                if n == batch_size:
                    yield (np.stack(eventseq_batch, axis=1),
                           np.stack(controlseq_batch, axis=1))
                    eventseq_batch.clear()
                    controlseq_batch.clear()
                    n = 0
    
    def __repr__(self):
        return (f'Dataset(root="{self.root}", '
                f'samples={len(self.samples)}, '
                f'avglen={self.avglen})')
