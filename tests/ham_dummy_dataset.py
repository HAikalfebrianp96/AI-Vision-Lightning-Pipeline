import os
import random
import deeplake
import numpy as np
import pytest


@pytest.fixture(scope='session')
def ham_dummy_dataset_dir(tmp_path_factory):
    label_img = ['ak', 'bcc', 'bkl','df','mel','nv','vasc']

    root_dir = tmp_path_factory.mktemp('temp_ham_dummy_dataset')

    num_samples = 30
    for split in ['train', 'val', 'test']:
        output_dir = os.path.join(str(root_dir), f'dummy-{split}')
        print(output_dir)
        ds = deeplake.dataset(output_dir)
        with ds:
            ds.create_tensor('images', htype='image',
                             sample_compression='jpeg')
            # Classification
            ds.create_tensor('labels', htype='class_label',
                             class_names=label_img)

        with ds:
            for i in range(num_samples):
                dummy_label = random.choice(label_img)  # nosec
                label_num = label_img.index(dummy_label)

                ds.append({
                    'images': np.random.randint(0, 256, size=(256, 256), dtype='uint8'),
                    'labels': np.uint32(label_num)
                })

    return str(root_dir)


@pytest.fixture(scope='session')
def ham_dummy_train_dataset_dir(tmp_path_factory):
    label_img = ['ak', 'bcc', 'bkl','df','mel','nv','vasc']

    root_dir = tmp_path_factory.mktemp('temp_ham_dummy_dataset_train')

    num_samples = 547
    ds = deeplake.dataset(root_dir)
    with ds:
        ds.create_tensor('images', htype='image',
                         sample_compression='jpeg')
        ds.create_tensor('labels', htype='class_label',
                         class_names=label_img)

    with ds:
        for i in range(num_samples):
            dummy_label = random.choice(label_img)  # nosec
            label_num = label_img.index(dummy_label)

            ds.append({
                'images': np.random.randint(0, 256, size=(256, 256), dtype='uint8'),
                'labels': np.uint32(label_num)
            })

    return str(root_dir)


@pytest.fixture(scope='session')
def ham_dummy_val_dataset_dir(tmp_path_factory):
    label_img = ['ak', 'bcc', 'bkl','df','mel','nv','vasc']

    root_dir = tmp_path_factory.mktemp('temp_ham_dummy_dataset_val')

    num_samples = 233
    ds = deeplake.dataset(root_dir)
    with ds:
        ds.create_tensor('images', htype='image',
                         sample_compression='jpeg')
        ds.create_tensor('labels', htype='class_label',
                         class_names=label_img)

    with ds:
        for i in range(num_samples):
            dummy_label = random.choice(label_img)  # nosec
            label_num = label_img.index(dummy_label)

            ds.append({
                'images': np.random.randint(0, 256, size=(256, 256), dtype='uint8'),
                'labels': np.uint32(label_num)
            })

    return str(root_dir)


@pytest.fixture(scope='session')
def ham_dummy_test_dataset_dir(tmp_path_factory):
    label_img = ['ak', 'bcc', 'bkl','df','mel','nv','vasc']

    root_dir = tmp_path_factory.mktemp('temp_ham_dummy_dataset_test')

    num_samples = 155
    ds = deeplake.dataset(root_dir)
    with ds:
        ds.create_tensor('images', htype='image',
                         sample_compression='jpeg')
        # Classification
        ds.create_tensor('labels', htype='class_label',
                         class_names=label_img)

    with ds:
        for i in range(num_samples):
            dummy_label = random.choice(label_img)  # nosec
            label_num = label_img.index(dummy_label)

            ds.append({
                'images': np.random.randint(0, 256, size=(256, 256), dtype='uint8'),
                'labels': np.uint32(label_num)
            })

    return str(root_dir)