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
        # print original_text
        # print cipher_text
        # x = "Along with a 93-year-old man who is savouring his last meeting with his family , sitting firmly wedged in his pillows while toasts are drunk in his honour , a 36-year-young man is dying tragically , surrounded by his parents , his wife and his two young children , after having tried everything to survive ."
        # print cipher_solver.languagemodel.score(x), x
        # x = "Showers continued throughout the week in the Bahia cocoa zone, alleviating the drought since early January and improving prospects for the coming temporao, although normal humidity levels have not been restored, Comissaria Smith said in its weekly review."
        # print cipher_solver.languagemodel.score(x), x
        # x = "aafsd wertwerewt sdgfhghertsd sgdftwrehr htrthsthere aegrergargr sdfjkhdsfjkh sr sdg trtyk udf rg rdfdgdsf"
        # print cipher_solver.languagemodel.score(x), x
        # x = "January potato herald dog phone execute"
        # print cipher_solver.languagemodel.score(x), x
        # return
        original_text = "Along with a 93-year-old man who is savouring his last meeting with his family , sitting firmly wedged in his pillows while toasts are drunk in his honour , a 36-year-young man is dying tragically , surrounded by his parents , his wife and his two young children , after having tried everything to survive ."
        key = util.generateKey()
        cipher_text = util.encrypt(original_text, key)
        # baseline_text, baseline_key = cipher_baseline.decrypt(cipher_text)
        guess_text, guess_key = cipher_solver.decrypt(cipher_text)
        score = score_guess(original_text, key, guess_text, guess_key)
        guess_scores.append(score)

        return

    print sum(guess_scores)/len(guess_scores)

if __name__ == '__main__':
    main()
