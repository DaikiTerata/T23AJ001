import collections
import configparser
import csv
import datetime
from enum import Enum
import os
import pathlib
from typing import Any


# 定数宣言
# スクリプトのあるディレクトリ
CURRENT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
# スクリプトの設定ファイル
CONFIG_PATH = CURRENT_DIR.joinpath("Log_config.ini")
# 1st-log、2ndログ出力先ルートディレクトリ
LOG_ROOT_1ST_DIR = CURRENT_DIR.parent.joinpath("1st-log")
LOG_ROOT_2ND_DIR = CURRENT_DIR.parent.joinpath("2nd-log")


# ログレベル、メッセージレベル定義
class Level(Enum):
    CRITICAL = 50
    INFO = 20
    DEBUG = 10


class ArgError(Exception):
    pass


class LevelNotFoundError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


class LogConfigKeyError(Exception):
    pass


class MessageIdError(Exception):
    pass


class Log(object):
    """ 共通ログ出力機能のクラス定義 """

    def __init__(self, job_id: str, log_level: Level = Level.INFO, fname_1st = None, fname_2nd = None, output_both_flg = True):
        """ログ出力処理初期化

        ジョブIDのディレクトリ作成
        ログレベルとメッセージファイルの内容をメモリ上に保持
        Log_config.iniで定義したメッセージファイルを読み込みます

        Args:
            job_id (str): ジョブID
            log_level (Any, optional): ログレベル. Defaults to Level.INFO
            fname_1st (str): 1st-logのログファイル名. Defaults to None
            fname_2nd (str): 2nd-logのログファイル名. Defaults to None
            output_both_flg (bool): 1st-log出力時に2nd-logにも出力するか判別.True:出力する、False:出力しない Defaults to False

        Raises:
            ArgError: 引数エラーの場合
            FileNotFoundError: ファイルが存在しない場合
            LogConfigKeyError: ログ設定ファイル内に必要なキーがない場合
        """
        # 引数チェック
        if not job_id:
            raise ArgError(f'Argument is None or null string. [job_id:{job_id}]')
        elif not isinstance(job_id, str):
            raise ArgError(f'Argument Type is not string. [job_id:{job_id}]')
        elif not isinstance(log_level, (str, Level)):
            raise ArgError(f'Argument Type is not string or Level. [log_level:{log_level}]')
        elif fname_1st and not isinstance(fname_1st, str):
            raise ArgError(f'Argument Type is not string. [fname_1st:{fname_1st}]')
        elif fname_2nd and not isinstance(fname_2nd, str):
            raise ArgError(f'Argument Type is not string. [fname_2nd:{fname_2nd}]')
        elif not isinstance(output_both_flg, bool):
            raise ArgError(f'Argument Type is not bool. [output_both_flg:{output_both_flg}]')

        # ログレベルのリファレンスチェックと型変換
        if not isinstance(log_level, Level):
            self.log_level = get_Level(log_level)
        else:
            self.log_level = log_level

        # 設定ファイルの存在チェックと読み込み
        if not CONFIG_PATH.exists():
            raise FileNotFoundError(str(CONFIG_PATH.resolve()))

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        # ログ出力先ルートディレクトリ＋ジョブIDのパス生成
        try:
            tool_root_log_dir = pathlib.Path(config['common']['tool_root_log_dir'])
            tool_message_dir = pathlib.Path(config['common']['tool_message_dir'])
        except:
            raise LogConfigKeyError("Config has no attribute (tool_root_log_dir, tool_message_dir)")

        # ジョブIDのディレクトリが存在しない場合作成
        self.logdir_1st = tool_root_log_dir.joinpath('1st-log', job_id)
        self.logdir_2nd = tool_root_log_dir.joinpath('2nd-log', job_id)

        if not self.logdir_1st.exists():
            os.makedirs(self.logdir_1st)
        if not self.logdir_2nd.exists():
            os.makedirs(self.logdir_2nd)

        # メッセージファイルの存在チェックと読み込み
        self.msg = collections.defaultdict(str)
        msgfile_name = 'msg_' + job_id + '.txt'
        msgfile_path = tool_message_dir.joinpath(msgfile_name)
        if not msgfile_path.exists():
            raise FileNotFoundError(str(msgfile_path.resolve()))

        with open(msgfile_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.msg[row[1]] = (row[0], row[2])

        # ログファイル名を設定
        self.log_filename_1st = None
        self.log_filename_2nd = None
        if fname_1st:
            if len(fname_1st) != 0:
                self.log_filename_1st = fname_1st
        if fname_2nd:
            if len(fname_2nd) != 0:
                self.log_filename_2nd = fname_2nd
        # 1st-log出力時に2nd-logにも出力するか判別するフラグを設定
        self.output_both_flg = output_both_flg

        # ジョブIDを設定
        self.job_id = job_id

    def output_1st_log(self, msg_id, hojo_msg: Any = "") -> None:
        """一次切り分けログ（1st-log）出力処理

        メッセージIDに該当するメッセージに補助メッセージを追記し
        一次切り分けログに出力

        Args:
            msg_id (str): メッセージID
            hojo_msg (Any, optional): 補助メッセージ. Defaults to None.

        Raises:
            ArgError: 引数エラーの場合
            MessageIdError: メッセージIDが定義されていない場合
        """
        # 引数チェック
        if not msg_id:
            raise ArgError(f'Argument is None or null string. [msg_id:{msg_id}]')
        elif not isinstance(msg_id, str):
            raise ArgError(f'Argument Type is not string. [msg_id:{msg_id}][hojo_msg:{hojo_msg}]')

        # メッセージIDの定義をチェック
        if msg_id not in self.msg:
            raise MessageIdError(f'msg_id is not in message file. [msg_id:{msg_id}]')

        # 出力メッセージ情報取得
        tmp_msg_level, tmp_msg_text = self.msg.get(msg_id)

        # ログ出力要否を判別
        # メッセージレベルがログレベルを下回る場合、終了(ログ出力なし)
        if get_Level(tmp_msg_level).value < self.log_level.value:
            return None

        # ログファイルのパスを生成
        if self.log_filename_1st:
            tmp_filename = self.log_filename_1st
        else:
            tmp_filename = '1st_' + self.job_id + '_' + datetime.datetime.today().strftime('%Y%m%d') + '.log'
        logpath_1st = self.logdir_1st.joinpath(tmp_filename)

        tmp_msg = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        tmp_msg = "{0} {1} {2} {3} {4}\n".format(tmp_msg, msg_id, tmp_msg_level, tmp_msg_text, hojo_msg)

        # 1stログファイルに書込み
        with open(logpath_1st, 'a', encoding='utf-8') as f:
            f.write(tmp_msg)

        # 2ndログファイルに書込み
        if self.output_both_flg:
            # ログファイルのパスを生成
            if self.log_filename_2nd:
                tmp_filename = self.log_filename_2nd
            elif not self.log_filename_1st:
                # 1st-log出力時に取得した1st_ジョブID_YYYYMMDD.log形式のファイル名を使う（日跨ぎ時の対応）
                tmp_filename = tmp_filename.replace('1st', '2nd')
            else:
                tmp_filename = '2nd_' + self.job_id + '_' + datetime.datetime.today().strftime('%Y%m%d') + '.log'
            logpath_2nd = self.logdir_2nd.joinpath(tmp_filename)
            with open(logpath_2nd, 'a', encoding='utf-8') as f:
                f.write(tmp_msg)

    def output_2nd_log(self, msg_level: Any, msg_text: Any = "") -> None:
        """障害解析ログ（2nd-log）出力処理

        メッセージレベルとメッセージ内容を一次切り分けログに出力

        Args:
            msg_level (str | Level): レベルを示す文字列またはLevelインスタンス
            msg_text (Any, optional): メッセージ内容. Defaults to None.

        Raises:
            ArgError: 引数エラーの場合
        """
        # 引数チェック
        if not msg_level:
            raise ArgError(f'Argument is None or null string. [msg_level:{msg_level}]')
        elif not isinstance(msg_level, (str, Level)):
            raise ArgError(f'Argument Type is not string or Level. [msg_level:{msg_level}]')

        # メッセージレベルのリファレンスチェックと型変換
        if not isinstance(msg_level, Level):
            msg_level = get_Level(msg_level)

        # ログ出力要否を判別
        # メッセージレベルがログレベルを下回る場合、終了(ログ出力なし)
        if msg_level.value < self.log_level.value:
            return None

        # ログファイルのパスを生成
        if self.log_filename_2nd:
            tmp_filename = self.log_filename_2nd
        else:
            tmp_filename = '2nd_' + self.job_id + '_' + datetime.datetime.today().strftime('%Y%m%d') + '.log'
        logpath_2nd = self.logdir_2nd.joinpath(tmp_filename)

        tmp_msg = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        tmp_msg = "{0} {1} {2}\n".format(tmp_msg, msg_level.name, msg_text)

        # ログファイルに書込み
        with open(logpath_2nd, 'a', encoding='utf-8') as f:
            f.write(tmp_msg)


def get_Level(level: str) -> Level:
    """get_Level レベル取得

    レベルを示す文字列から列挙型のレベルを取得する

    Args:
        level (str): レベルを示す文字列(CRITICAL, INFO, DEBUGなど)

    Raises:
        LevelNotFoundError: 該当レベルがない場合

    Returns:
        Level: 対応する列挙型レベル
    """
    try:
        res = eval(f"Level.{level}")
    except:
        raise LevelNotFoundError(f"Level={level} Not Found")

    return res
