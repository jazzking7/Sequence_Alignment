# Author: Jasper Wang
# Date: 20 Dec 2021
# Goal: Sequence Aligner

import numpy as np

class Aligner:

    def __init__(self):
        self.match = 1
        self.mismatch = -1
        self.gap = 1

    def set_parameters(self, match, mismatch, gap):
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

    def substitution(self, a, b):
        return self.match if a == b else self.mismatch

    def NW(self, seq1, seq2):
        ls1, ls2 = len(seq1), len(seq2)
        scores = np.zeros((ls1+1, ls2+1), dtype="int32")
        path = np.zeros((ls1+1, ls2+1), dtype="int32")
        for i in range(1, ls1+1):
            scores[i, 0] = i*-1
            path[i, 0] = 1
        for j in range(1, ls2+1):
            scores[0, j] = j*-1
            path[0, j] = 2

        for i in range(0, ls1):
            for j in range(0, ls2):
                scores[i+1, j+1] = max(self.substitution(seq1[i], seq2[j]) + scores[i, j],  # No gap
                                       scores[i, j+1] + self.gap,  # seq2 matches with a gap
                                       scores[i+1, j] + self.gap)  # seq1 matches with a gap
                if scores[i+1, j+1] == self.substitution(seq1[i], seq2[j]) + scores[i, j]:
                    path[i+1, j+1] = 0
                elif scores[i+1, j+1] == scores[i, j+1] - 1:
                    path[i+1, j+1] = 2
                else:
                    path[i+1, j+1] = 1

        i, j = ls1, ls2
        S, T = "", ""
        while not (i == 0 or j == 0):
            if path[i, j] == 0:
                S = seq1[i-1] + S
                T = seq2[j-1] + T
                i -= 1
                j -= 1
            elif path[i, j] == 1:
                S = "_" + S
                T = seq2[j - 1] + T
                j -= 1
            else:
                S = seq1[i - 1] + S
                T = "_" + T
                i -= 1
        if i > 0:
            while i >= 1:
                S = seq1[i-1] + S
                T = "_" + T
                i -= 1
        if j > 0:
            while j >= 1:
                S = "_" + S
                T = seq2[j-1] + T
                j -= 1
        return S, T

    def analyze(self, filename):
        try:
            data = open(filename, "r")
            data = data.readlines()
            seqs = []
            for line in data:
                if line[0] == ">":
                    continue
                seqs.append(line.strip())
            return self.NW(seqs[0], seqs[1])
        except:
            return "Unable to analyze your given data, verify if\n your file respects the format mentioned in readme."


