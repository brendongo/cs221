import csv, util, solver, baseline, LanguageModel, string
from itertools import izip

def score_accuracy(encryption_key, decryption_key, cipher_text):
    decrypted_alpha = util.encrypt(util.encrypt(string.ascii_uppercase, encryption_key), decryption_key)
    usedletters = [i in cipher_text.upper() for i in string.ascii_uppercase]
    return sum([1 for i in xrange(len(string.ascii_uppercase)) if string.ascii_uppercase[i] == decrypted_alpha[i] and usedletters[i]])/float(sum(usedletters))

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

    numIterations = 0

    for original_text in original_text_file:
        numIterations += 1
        if numIterations == 1: continue
        if numIterations > 30: break
        encryption_key = util.generateKey()
        cipher_text = util.encryptCase(original_text, encryption_key)
        cipher_text_noised = util.add_noise(cipher_text, noise)

        if verbose:
            print "Original Text", original_text
            print "Key"
            print "Cipher Text", cipher_text
            print "Noised", cipher_text_noised
        
        baseline_text, baseline_decryption_key = cipher_baseline.decrypt(cipher_text_noised)
        guess_text, guess_decryption_key = cipher_solver.decrypt(cipher_text_noised)
        

        baseline_score = score_accuracy(encryption_key, baseline_decryption_key, cipher_text_noised)
        baseline_accuracy.append(baseline_score)
        solver_score = score_accuracy(encryption_key, guess_decryption_key, cipher_text_noised)
        solver_accuracy.append(solver_score)
        print "Baseline Accuracy: ", baseline_score
        print "Average Accuracy of Baseline: ", sum(baseline_accuracy)/len(baseline_accuracy)
        print "Solver Accuracy: ", solver_score
        print "Average Accuracy of Solver: ", sum(solver_accuracy)/len(solver_accuracy)

    print "Average Accuracy of Baseline: ", sum(baseline_accuracy)/len(baseline_accuracy)
    print "Average Accuracy of Solver: ", sum(solver_accuracy)/len(solver_accuracy)
    print "Over %d cipher texts" % len(solver_accuracy)

if __name__ == '__main__':
    main()
