import csv, util, solver, baseline, LanguageModel, string
from itertools import izip

def score_accuracy(key, guess_key):
    return sum([1 for i in xrange(len(key.strip())) if key[i] == guess_key[i]])/float(26)

def main():
    learnfile = "newstest2012.en"
    testfile = "original"
    verbose = False
    noise = 0.0

    languagemodel = LanguageModel.LanguageModel(learnfile)
    original_text_file = open(testfile, "r")

    cipher_solver = solver.Solver(languagemodel)
    cipher_baseline = baseline.Baseline()
    solver_accuracy = []
    baseline_accuracy = []

    counter = 0
    for original_text in original_text_file:
        counter += 1
        if counter == 0 or counter == 1: continue
        if counter == 4: break
        key = util.generateKey()
        cipher_text = util.encryptCase(original_text, key)
        cipher_text_noised = util.add_noise(cipher_text, noise)

        if verbose:
            print "Original Text", original_text
            print "Key"
            print "Cipher Text", cipher_text
            print "Noised", cipher_text_noised
        
        # baseline_text, baseline_key = cipher_baseline.decrypt(cipher_text_noised)
        # baseline_accuracy.append(score_accuracy(original_text, key, baseline_text, baseline_key));

        guess_text, guess_key = cipher_solver.decrypt(cipher_text_noised)
        
        print util.encrypt(string.ascii_uppercase, key)
        print util.encrypt(util.encrypt(string.ascii_uppercase, key), guess_key)
        decrypted_alpha = util.encrypt(util.encrypt(string.ascii_uppercase, key), guess_key)
        solver_accuracy.append(score_accuracy(string.ascii_uppercase, decrypted_alpha))

    # print "Average Accuracy of Baseline: ", sum(baseline_accuracy)/len(baseline_accuracy)
    print "Average Accuracy of Solver: ", sum(solver_accuracy)/len(solver_accuracy)
    print "Over %d cipher texts" % len(solver_accuracy)

if __name__ == '__main__':
    main()
