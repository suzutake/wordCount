#!/usr/bin/python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import MeCab
import sys
import re
import glob
from collections import Counter

def execute(name, is_dir):
    """

    メイン実行

    Args:
        name (string): 対象のファイルorディレクトリ名
        is_dir (bool, optional): 対象がディレクトリの場合はTrue

    Returns:
       string[]: 出現単語一覧

    """

    words = []
    if (is_dir):
        files = glob.glob("./{}/*".format(name))
        for file in files:
            words = __file_action(file, words)
    else:
        words = __file_action(name, words)

    return words


def __get_option():
    """
    オプション取得
    """
    argparser = ArgumentParser()
    argparser.add_argument('name', help='file or dir name')
    argparser.add_argument('-d', '--dir', action='store_true',
                           help='select directory (default: file)')
    return argparser.parse_args()


def __file_action(name, words):
    """
    一つのファイルを形態素解析して単語抽出
    """
    # ファイル読み込み
    with open(name) as f:
        data = f.read()

    # パース
    mecab = MeCab.Tagger()
    parse = mecab.parse(data)
    lines = parse.split('\n')
    items = (re.split('[\t,]', line) for line in lines)

    # 名詞をリストに格納
    tmp_words = [
        item[0] for item in items
            if (
                item[0] not in ('EOS', '', 't', 'ー') and
                item[1] == '名詞' and item[2] == '一般')
    ]
    words.extend(tmp_words)
    return words


if __name__ == '__main__':
    args = __get_option()
    words = execute(args.name, args.dir)

    # 頻度順に出力
    counter = Counter(words)
    for word, count in counter.most_common():
        print(f"{word}: {count}")
