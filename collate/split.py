import numpy as np
data = np.load('new_data.npy')

test_set_f = open('test_set.txt', 'r')
test_set = set([l.strip() for l in test_set_f.readlines()])
test_set_f.close()

print(test_set)

order_ids = data[...,0]
train_inds = []
test_inds = []
for i in range(len(order_ids)):
    if str(int(order_ids[i])) in test_set:
        test_inds.append(i)
    else:
        train_inds.append(i)

train = data[train_inds]
test = data[test_inds]

print(train.shape, test.shape)
