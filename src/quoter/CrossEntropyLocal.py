# Code by Tobin South
# https://github.com/tobinsouth/ProcessEntropy

from numba import jit, prange
import numpy as np
from quoter.ProcessEntropyPreprocessing import tweet_to_hash_array


@jit(nopython=True)
def find_lambda_jit(target, source):
    """
    Finds the longest subsequence of the target array,
    starting from index 0, that is contained in the source array.
    Returns the length of that subsequence + 1.
    i.e. returns the length of the shortest subsequence starting at 0
    that has not previously appeared.

    Args:
        target: NumPy array, perferable of type int.
        source: NumPy array, perferable of type int.
    Returns:
        Integer of the length.
    """

    source_size = source.shape[0] - 1
    target_size = target.shape[0] - 1
    t_max = 0
    c_max = 0

    for si in range(0, source_size + 1):
        if source[si] == target[0]:
            c_max = 1
            for ei in range(1, min(target_size, source_size - si + 1)):
                if source[si + ei] != target[ei]:
                    break
                else:
                    c_max = c_max + 1

            #                 if(si+ei>=source_size):
            #                     break

            if c_max > t_max:
                t_max = c_max

    return t_max + 1


@jit(parallel=True, nopython=True)
def get_all_lambdas(target, source, relative_pos, lambdas):
    """
    Finds all the the longest subsequences of the target,
    that are contained in the sequence of the source,
    with the source cutoff at the location set in relative_pos.
    See function find_lambda_jit for description of Lambda_i(target|source)
    Args:
        target: Array of ints, usually corresponding to hashed words.
        source: Arry of ints, usually corresponding to hashed words.
        relative_pos: list of integers with the same length as target denoting the
            relative time ordering of target vs. source. These integers tell us the
            position relative_pos[x] = i in source such that all symbols in source[:i]
            occurred before the x-th word in target.
        lambdas: A premade array of length(target), usually filled with zeros.
            Used for efficiency reasons.
    Return:
        A list of ints, denoting the value for Lambda for each index in the target.
    """

    for i in prange(0, len(target)):
        if not relative_pos[i] == 0:
            lambdas[i] = find_lambda_jit(target[i:], source[: relative_pos[i]])
        else:
            lambdas[i] = 1

    return lambdas


def timeseries_cross_entropy(
    time_tweets_target, time_tweets_source, please_sanitize=True, get_lambdas=False
):
    """
    Finds the cross entropy H_cross(target|source) where the processes are embedded in time.
    i.e. How many bits we would need to encode the data in target
    using information in the source that is before the current time.
    This is described mathematically in [1] as,
    T = target
    S = source
    
    \hat{h}_{ \times}(T | S)=\frac{N_{T} \log _{2} N_{S}}{\sum_{i=1}^{N_{T}} \Lambda_{i}(T | S)}
    
    Args:
        time_tweets_target: A list of tuples with (time, tweet_content).
            This is the stream of new information that we can testing the ability to encode.
            If please_sanitize = True (default) then tweet_content can be a string.
        time_tweets_source: A list of tuples with (time, tweet_content).
            This is the stream of previous information from which we try to encode the target.
        please_sanitize: Option to have the tweet string converted to numpy int arrays for speed.
            If False, please santize tweet into a list of tokenzied words, ideally converting these to ints,
            via a hash.
        get_lambdas: Boolean choice to return the list of all calculated Lambda values for each point
            in target. Usually used for debugging.
    Return:
        The cross entropy as a float
    [1] I. Kontoyiannis, P.H. Algoet, Yu.M. Suhov, and A.J. Wyner. Nonparametric entropy
    esti mation for stationary processes and random fields, with applications to English text.
    IEEE Transactions on Information Theory, 44(3):1319–1327, May 1998.
    Credit to Bagrow and Mitchell for code ideas that I've stolen for this function.
    """

    # Decorate tweets (so we can distinguish the users), before sorting in time:

    if (
        please_sanitize
    ):  # Option to have the tweet string converted to numpy int arrays for speed.
        # tweet_to_hash_array fucntion can be found in package.
        decorated_target = [
            (time, "target", tweet_to_hash_array(tweet))
            for time, tweet in time_tweets_target
        ]
        decorated_source = [
            (time, "source", tweet_to_hash_array(tweet))
            for time, tweet in time_tweets_source
        ]
    else:
        decorated_target = [
            (time, "target", tweet) for time, tweet in time_tweets_target
        ]
        decorated_source = [
            (time, "source", tweet) for time, tweet in time_tweets_source
        ]

    # Join time series:
    time_tweets = decorated_target + decorated_source

    # Sort in place by time:
    time_tweets.sort()

    # Loop over combined tweets and build word vectors and target->source relative_pos:
    target, source, relative_pos = [], [], []
    for time, user, tweet in time_tweets:
        words = tweet
        if user == "target":
            target.extend(words)
            relative_pos.extend([len(source)] * len(words))
        else:
            source.extend(words)

    target = np.array(target, dtype=np.uint32)
    source = np.array(source, dtype=np.uint32)
    relative_pos = np.array(relative_pos, dtype=np.uint32)
    lambdas = np.zeros(len(target), dtype=np.uint32)  # Premake for efficiency

    lambdas = get_all_lambdas(target, source, relative_pos, lambdas)

    if get_lambdas:
        return lambdas
    return len(target) * np.log2(len(source)) / np.sum(lambdas)
