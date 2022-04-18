import os
import cv2

from create_data import *

EXECUTABLE = 'C:/Users/CHUKDANIIL/Documents/algsingraphics/LabCV/labs/2021/Krupkina/Computer_vision_challenge-cv_shape_finder/shape_finder.py'
BASE_DIR = 'data'

VERBOSE = True

scores = []
for ind in ['000', '001', '002', '003']:
    for n_type in ['pure', 'noise', 'line']:
        print(f'PROCESSING FILE: {ind}_{n_type}')

        in_topology_file = os.path.join(BASE_DIR, f'{ind}_{n_type}_in.txt')
        in_image_file = os.path.join(BASE_DIR, f'{ind}_{n_type}_src.png')
        in_gt_file = os.path.join(BASE_DIR, f'{ind}_{n_type}_gt.png')

        exec_line = f'{EXECUTABLE} -s {in_topology_file} -i {in_image_file} > out.txt'
        os.system(exec_line)

        out_image_file = 'out.txt'

        in_topology = read_topology(in_topology_file)
        result = read_transform(out_image_file, in_topology)

        _, result_img = draw_transform(result)
        gt = cv2.imread(in_gt_file, 0)

        union = np.sum(np.bitwise_or(gt, result_img) > 0)
        intersection = np.sum(np.bitwise_and(gt, result_img) > 0)
        local_score = float(intersection) / float(union)

        scores.append(local_score)

        if VERBOSE:
            cv2.imshow('gt', gt)
            cv2.imshow('result', result_img)

            cv2.waitKey(0)

print(f'SCORES: {scores}')
total = float(sum(scores)) / float(len(scores))
print(f'mIoU result: {total}')