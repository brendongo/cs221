import csv, util, solver, baseline
from itertools import izip

def score_guess(original_text, key, guess_text, guess_key):
    # TODO
    return 0.0

def main():
    verbose = False
    keys_file = open("keys", 'r')
    cipher_text_file = open("substitute", 'r') # or open("substitute_noise", 'r')
    original_text_file = open("original", "r")

    cipher_solver = solver.Solver()
    cipher_baseline = baseline.Baseline()
    guess_scores = []


    for original_text, key, cipher_text in izip(original_text_file, keys_file, cipher_text_file):
        baseline_text, baseline_key = cipher_baseline.decrypt(cipher_text)
        guess_text, guess_key = cipher_solver.decrypt(cipher_text)
        score = score_guess(original_text, key, guess_text, guess_key)
        guess_scores.append(score)

    print sum(guess_scores)/len(guess_scores)

if __name__ == '__main__':
    main()