import csv, util, solver, baseline, LanguageModel, string
from itertools import izip

def score_accuracy(encryption_key, decryption_key, cipher_text, original_text):
    ''' 
    Scores how accurate a decryption key was in decrypting a given cipher_text encrypted using a given encryption_key
    The score is given as a percent of correct letters in the encryption key that are mapped back to their original letters
    '''
    true_decryption_key = util.getDecryptionKey(encryption_key)
    original_text_noised = util.encryptCase(cipher_text, true_decryption_key)
    decrypted_text_noised = util.encryptCase(cipher_text, decryption_key)
    num_same_all = [1 for x,y,z in zip(original_text_noised, decrypted_text_noised, original_text) if x == z and x == y and x != " "]
    num_same_original = [1 for x,z in zip(original_text_noised, original_text) if x == z and x != " "]
    return sum(num_same_all)/float(sum(num_same_original))

def main():
    learnfile = "ngrams.txt"
    testfile = "europarl-v7.es-en.en"
    verbose = False
    noise = 0.05
    numIterations = 0
    minLength = 100

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
        original_text_noised = util.add_noise(original_text, noise)
        cipher_text = util.encryptCase(original_text_noised, encryption_key)

        if verbose:
            print "Original Text", original_text
            print "Original Text Noised", original_text_noised
            print "Key", encryption_key
            print "Cipher Text Noised", cipher_text
            
        
        baseline_text, baseline_decryption_key = cipher_baseline.decrypt(cipher_text)
        guess_text, guess_decryption_key, num_guesses = cipher_solver.decrypt(cipher_text)

        baseline_score = score_accuracy(encryption_key, baseline_decryption_key, cipher_text, original_text)
        baseline_accuracy.append(baseline_score)
        solver_score = score_accuracy(encryption_key, guess_decryption_key, cipher_text, original_text)
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
