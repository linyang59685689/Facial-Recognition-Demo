# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/1/5 下午10:08
# @Author: LiLinYang
# @File  : generate_train_and_test.txt.py

import cv2 as cv


def gen_train_test_text(from_path, to_path, train_text_path="../data/train.txt",
                        test_text_path="../data/test.txt", train_nums=800,is_append=True):
    with open(from_path + "label.txt") as f:
        line1 = f.readline().split(" ")
        last_img = None
        img_count = 0
        last_img_name = ''

        if is_append:
            train_f = open(train_text_path, 'a')
            test_f = open(test_text_path, 'a')
        else :
            train_f = open(train_text_path, 'w')
            test_f = open(test_text_path, 'w')

        while len(line1) > 2:
            img_name = line1[0]
            left_top_x = float(line1[1])
            left_top_y = float(line1[2])
            right_bottom_x = float(line1[3])
            right_bottom_y = float(line1[4])
            width = right_bottom_x - left_top_x
            height = right_bottom_y - left_top_y
            left_top_x = int(left_top_x - width * 0.125)
            right_bottom_x = int(right_bottom_x + width * 0.125)
            left_top_y = int(left_top_y - height * 0.125)
            right_bottom_y = int(right_bottom_y + height * 0.125)

            if img_count < train_nums:
                write_file = train_f
            else:
                write_file = test_f

            if last_img_name != img_name:
                if last_img is not None:
                    cv.imwrite(to_path + last_img_name, last_img)
                    img_count += 1
                last_img_name = img_name
                last_img = None

            if last_img is None:
                last_img = cv.imread(from_path + img_name)
                img = last_img

            points = []
            for i in (range((len(line1) - 5) // 2)):
                points.append(float(line1[2 * i + 5]))
                points.append(float(line1[2 * i + 1 + 5]))
                x = int(float(line1[2 * i + 5]))
                y = int(float(line1[2 * i + 1 + 5]))
                if x <= left_top_x:
                    left_top_x = x - 1
                if x >= right_bottom_x:
                    right_bottom_x = x + 1
                if y <= left_top_y:
                    left_top_y = y - 1
                if y >= right_bottom_y:
                    right_bottom_y = y + 1

                cv.circle(img, (x, y),
                          1, (0, 0, 255), thickness=-1)

            if left_top_x < 0:
                left_top_x = 0
            if left_top_y < 0:
                left_top_y = 0
            if right_bottom_x > img.shape[1]:
                right_bottom_x = img.shape[1] - 1
            if right_bottom_y > img.shape[0]:
                right_bottom_y = img.shape[0] - 1

            new_line = from_path + img_name + ' ' \
                       + str(left_top_x) + ' ' \
                       + str(left_top_y) + ' ' \
                       + str(right_bottom_x) + ' ' \
                       + str(right_bottom_y) + ' '
            for i in points:
                if i is points[-1]:
                    new_line += str(i) + '\n'
                else:
                    new_line += str(i) + ' '

            write_file.write(new_line)

            img = cv.rectangle(img, (left_top_x, left_top_y), (right_bottom_x, right_bottom_y),
                               (0, 255, 0), 1)

            last_img = img
            line1 = f.readline().split(" ")

        cv.imwrite(to_path + last_img_name, last_img)


def draw_img_by_txt(text_path, to_path):
    with open(text_path) as f:
        line1 = f.readline().split(" ")
        last_img = None
        last_img_name = ''

        while len(line1) > 2:
            img_name = line1[0]
            left_top_x = int(float(line1[1]))
            left_top_y = int(float(line1[2]))
            right_bottom_x = int(float(line1[3]))
            right_bottom_y = int(float(line1[4]))
            real_name = img_name[img_name.rfind('/')+1:]
            print(line1)

            if last_img_name != img_name:
                if last_img is not None:
                    cv.imwrite(to_path + real_name, last_img)
                last_img_name = img_name
                last_img = None

            if last_img is None:
                last_img = cv.imread(img_name)
                img = last_img

            for i in (range((len(line1) - 5) // 2)):
                x = int(float(line1[2 * i + 5]))
                y = int(float(line1[2 * i + 1 + 5]))
                cv.circle(img, (x, y),
                          4, (0, 0, 255), thickness=-1)

            img = cv.rectangle(img, (left_top_x, left_top_y), (right_bottom_x, right_bottom_y),
                               (0, 255, 0), 1)
            last_img = img
            line1 = f.readline().split(" ")

        real_name = img_name[img_name.rfind('/'):]
        cv.imwrite(to_path + real_name, last_img)


gen_train_test_text('../data/I/', '../data/trainA/',is_append=False)
gen_train_test_text('../data/II/', '../data/testA/')

draw_img_by_txt("../data/train.txt","../data/trainB/")

# a=open('a.txt','w')
# for i in range(100):
#     a.writelines('a\n')
#     a.writelines(' ')


