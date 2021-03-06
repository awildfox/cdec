from __future__ import division
import math
import sym

def contextless(feature):
    feature.compute_contextless_score = feature
    return feature

MAXSCORE = 99

def EgivenF(fphrase, ephrase, paircount, fcount, fsample_count): # p(e|f)
    return -math.log10(paircount/fcount)

def CountEF(fphrase, ephrase, paircount, fcount, fsample_count):
    return math.log10(1 + paircount)

def SampleCountF(fphrase, ephrase, paircount, fcount, fsample_count):
    return math.log10(1 + fsample_count)

def EgivenFCoherent(fphrase, ephrase, paircount, fcount, fsample_count):
    prob = paircount/fsample_count
    return -math.log10(prob) if prob > 0 else MAXSCORE

def CoherenceProb(fphrase, ephrase, paircount, fcount, fsample_count):
    return -math.log10(fcount/fsample_count)

def MaxLexEgivenF(ttable):
    def feature(fphrase, ephrase, paircount, fcount, fsample_count):
        fwords = [sym.tostring(w) for w in fphrase if not sym.isvar(w)] + ['NULL']
        ewords = (sym.tostring(w) for w in ephrase if not sym.isvar(w))
        def score():
            for e in ewords:
              maxScore = max(ttable.get_score(f, e, 0) for f in fwords)
              yield -math.log10(maxScore) if maxScore > 0 else MAXSCORE
        return sum(score())
    return feature

def MaxLexFgivenE(ttable):
    def feature(fphrase, ephrase, paircount, fcount, fsample_count):
        fwords = (sym.tostring(w) for w in fphrase if not sym.isvar(w))
        ewords = [sym.tostring(w) for w in ephrase if not sym.isvar(w)] + ['NULL']
        def score():
            for f in fwords:
              maxScore = max(ttable.get_score(f, e, 1) for e in ewords)
              yield -math.log10(maxScore) if maxScore > 0 else MAXSCORE
        return sum(score())
    return feature

def IsSingletonF(fphrase, ephrase, paircount, fcount, fsample_count):
    return (fcount == 1)

def IsSingletonFE(fphrase, ephrase, paircount, fcount, fsample_count):
    return (paircount == 1)

def IsNotSingletonF(fphrase, ephrase, paircount, fcount, fsample_count):
    return (fcount > 1)

def IsNotSingletonFE(fphrase, ephrase, paircount, fcount, fsample_count):
    return (paircount > 1)

def IsFEGreaterThanZero(fphrase, ephrase, paircount, fcount, fsample_count):
    return (paircount > 0.01)
