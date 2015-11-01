# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import errno
from PIL import Image
from os import listdir, makedirs
from os.path import join, isdir, exists, dirname
from root import root_path


_ROOT_FOLDER = 'CommemorativeCoinPhoto'
_THUMBNAIL_WIDTH = 320.0


def _generate_all_thumbnails(target_dir, recreate_all):
    files = listdir(target_dir)
    for file in files:
        if _should_be_ignored(file):
            continue

        file_path = join(target_dir, file)
        if isdir(file_path):
            _generate_all_thumbnails(file_path, recreate_all)
        else:
            _generate_thumbnail(file_path, recreate_all)


def _root():
    return root_path(_ROOT_FOLDER)


def _should_be_ignored(file):
    return file in ['.DS_Store']


def _generate_thumbnail(file_path, should_recreate):
    thumbnail_path = _map_to_thumbnail_path(file_path)
    if not should_recreate and exists(thumbnail_path):
        return

    im = Image.open(file_path)
    im.thumbnail(_to_shrink_size(im.size), Image.ANTIALIAS)
    im.save(thumbnail_path, quality=100)

    print("ReGenerated thumbnail for %s" % file_path)


def _map_to_thumbnail_path(original_path):
    target_path = original_path.replace(_ROOT_FOLDER, _ROOT_FOLDER + '/Thumbnails')
    target_dir = dirname(target_path)
    if not exists(target_dir):
        _mkdir_p(target_dir)

    return target_path


def _to_shrink_size(image_size):
    width, height = image_size
    _thumbnail_height = _THUMBNAIL_WIDTH / width * height
    return _THUMBNAIL_WIDTH, _thumbnail_height


def _mkdir_p(path):
    try:
        makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and isdir(path):
            pass
        else:
            raise


if __name__ == '__main__':
    recreate_all = True

    root_dir = _root()
    target_dir = join(root_dir, 'NGC')
    _generate_all_thumbnails(target_dir, recreate_all)
