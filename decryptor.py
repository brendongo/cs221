import csv, util, solver, baseline, LanguageModel, string
from itertools import izip

def score_accuracy(encryption_key, decryption_key, cipher_text):
    ''' 
    Scores how accurate a decryption key was in decrypting a given cipher_text encrypted using a given encryption_key
    The score is given as a percent of correct letters in the encryption key that are mapped back to their original letters
    '''
    true_decryption_key = util.getDecryptionKey(encryption_key)
    matches = [(true_decryption_key[i] == decryption_key[i]) for i in xrange(len(string.ascii_uppercase)) if string.ascii_uppercase[i] in cipher_text or string.ascii_lowercase[i] in cipher_text]
    return sum(matches)/float(len(matches))

def main():
    learnfile = "ngrams.txt"
    testfile = "europarl-v7.es-en.en"
    verbose = False
    noise = 0.05
    numIterations = 0
    minLength = 100

    print "Learning..."
    languagemodel = LanguageModel.LanguageModel(learnfile)
    original_text_file = open(testfile, "r")

    cipher_solver = solver.Solver(languagemodel)
    cipher_baseline = baseline.Baseline()
    solver_accuracy = []
    baseline_accuracy = []
    max_counts = []

    for original_text in original_text_file:
        if len(original_text) < minLength: continue
        numIterations += 1
        if numIterations == 1: continue
        if numIterations > 30: break
        encryption_key = util.generateKey()
        cipher_text = util.encryptCase(original_text, encryption_key)
        cipher_text_noised = util.add_noise(cipher_text, noise)

        if verbose:
            print "Original Text", original_text
            print "Key", encryption_key
            print "Cipher Text", cipher_text
            print "Noised", cipher_text_noised
        
        baseline_text, baseline_decryption_key = cipher_baseline.decrypt(cipher_text_noised)
        guess_text, guess_decryption_key, num_guesses = cipher_solver.decrypt(cipher_text_noised)
        baseline_score = score_accuracy(encryption_key, baseline_decryption_key, cipher_text)
        baseline_accuracy.append(baseline_score)
        solver_score = score_accuracy(encryption_key, guess_decryption_key, cipher_text)
        solver_accuracy.append(solver_score)
        max_counts.append(num_guesses)

        print "Baseline Accuracy: ", baseline_score
        print "Average Accuracy of Baseline: ", sum(baseline_accuracy)/len(baseline_accuracy)
        print "Solver Accuracy: ", solver_score
        print "Average Accuracy of Solver: ", sum(solver_accuracy)/len(solver_accuracy)
        print "Reached same thing many times", max_counts

    print "Average Accuracy of Baseline: ", sum(baseline_accuracy)/len(baseline_accuracy)
    print "Average Accuracy of Solver: ", sum(solver_accuracy)/len(solver_accuracy)
    print "Over %d cipher texts" % len(solver_accuracy)

if __name__ == '__main__':
    main()
