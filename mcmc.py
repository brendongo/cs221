def mcmc():
  best_cipher_key = 
  best_score = 
  curr_cipher_key =
  curr_score = 
  for i in xrange(maxiter):
    temp = swap(currBestCipherKey)
    temp_score = score(temp)
    if temp_score > curr_score:
      curr_cipher_key = temp
      curr_score = temp_score

      if temp_score > best_score:
        best_cipher_key = temp
        best_score = temp_score

    else if random.random < temp_score/best_score:
      curr_cipher_key = temp
      curr_score = temp_score

  return best_cipher_key








  distances = [0] * maxiter
  park_list = list(parks.keys())
  random.shuffle(park_list)
  rt = (park_list, total_distance(park_list, parks))
  best = rt
  for i in range(maxiter):
    tmp = switch_successive (rt) if method == 0 else switch_random (rt)
    rt_new = (tmp, total_distance(tmp, parks))
    delta = rt_new[1] - rt[1]
    if delta < 0 or (t > 0 and random.random() < math.e ** (-delta / t)):
      rt = rt_new
    if rt[1] < best[1]:
      best = rt
    distances[i] = rt[1]
  print best[1]
  return distances