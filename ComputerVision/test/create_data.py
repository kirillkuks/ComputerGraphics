import numpy as np
import cv2

IM_SHAPE = (200, 300)

class Transform:
    def __init__(self, obj):
        self.scale = obj['scale'] if 'scale' in obj else 1
        self.angle = obj['angle'] * np.pi / 180.0 if 'angle' in obj else 0
        self.dx = obj['dx'] if 'dx' in obj else 0
        self.dy = obj['dy'] if 'dy' in obj else 0
        self.shape = obj['shape']

    def draw(self, inpt, gt, color=255):
        assert (inpt.shape == gt.shape)

        new_shape = self.shape.copy().astype(np.float)

        # Scale
        new_shape *= self.scale

        # Rotation
        tmp = new_shape.copy()
        for i in [0, 1]:
           new_shape[:, i] = np.cos(self.angle) * tmp[:, i] \
                             - ((-1) ** i) * np.sin(self.angle) * tmp[:, 1 - i]

        #Shift
        new_shape[:, 0] += self.dx
        new_shape[:, 1] += self.dy

        cv2.fillPoly(gt, [new_shape.astype(np.int32)], color)
        cv2.polylines(inpt, [new_shape.astype(np.int32)], True, color)


def read_topology(file):
    in_shapes = []

    with open(file) as fp:
        N = int(fp.readline())
        for line in fp:
            in_shapes.append(line[:-1].split(', '))

    for i, shape in enumerate(in_shapes):
        in_shape_x = shape[0::2]
        in_shape_y = shape[1::2]

        in_shapes[i] = np.array(list(zip(in_shape_x, in_shape_y)))

    return in_shapes


def read_transform(file, in_shapes):
    out_transform = []
    with open(file) as fp:
        M = int(fp.readline())
        for line in fp:
            data_items = line[:-1].split(', ')
            obj = {
                'shape': in_shapes[int(data_items[0])],
                'dx': int(data_items[1]),
                'dy': int(data_items[2]),
                'scale': int(data_items[3]),
                'angle': int(data_items[4])
            }
            out_transform.append(Transform(obj))

    return out_transform

def draw_transform(out_transform):
    inpt = np.zeros(IM_SHAPE).astype(np.uint8)
    gt = np.zeros(IM_SHAPE).astype(np.uint8)
    for transform in out_transform:
        transform.draw(inpt, gt)

    return inpt, gt

if __name__ == '__main__':
    BASE_FILE = '000_pure'
    in_shapes = read_topology(f'data/{BASE_FILE}_in.txt')
    out_transform = read_transform(f'data/{BASE_FILE}_out.txt', in_shapes)
    inpt, gt = draw_transform(out_transform)

    cv2.imshow('inpt', inpt)
    cv2.imshow('result', gt)

    cv2.waitKey(0)
