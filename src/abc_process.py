from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, IntFlag, auto
from typing import Any

from xgnlog.Log import Log


def logtime() -> str:
    """logtime ログ表示時間を取得する

    Returns:
        str: 現在時刻を示す文字列
    """
    return datetime.now().isoformat(sep=" ", timespec="seconds")


class Mode(Enum):
    """ツール実行モード
    """
    up = "UP"
    """対象を有効化する実行モード"""
    down = "DOWN"
    """対象を無効化する実行モード"""
    show = "SHOW"
    """対象の状態を確認する実行モード"""
    info = "INFO"
    """ツール内の対象情報を表示する実行モード"""
    list = "LIST"
    """実行可能な対象名を表示する実行モード"""

    def __str__(self):
        return self.value


class ProcessStatus(IntFlag):
    """各NFにおけるツールプロセスの完了ステータス
    """
    ssh_ng = auto()
    """SSH接続NG"""
    pre_check_ng = auto()
    """事前確認に失敗"""
    show_or_unknown = auto()
    """ツール実行モードがSHOWまたは、事前状態が予期しない状態"""
    already_changed = auto()
    """ツール実行モードがUP/DOWNかつ、事前状態で変更不要と判断"""
    need_not_to_change = show_or_unknown | already_changed
    """事前確認の結果、変更不要な状態"""
    need_to_change = auto()
    """ツール実行モードがUP/DOWNかつ、事前状態で要変更と判断"""
    change_ok = auto()
    """対象の変更が完了"""
    change_ng = auto()
    """対象の変更に失敗"""
    commit_ok = auto()
    """変更結果の保存に成功"""
    commit_ng = auto()
    """変更結果の保存に失敗"""
    post_check_ok = auto()
    """事後確認の結果、変更反映を確認完了"""
    post_check_ng = auto()
    """事後確認に失敗または、事後確認の結果、変更反映されていない"""
    exception_ng = auto()
    """想定外のエラー発生"""
    ok = need_not_to_change | post_check_ok
    """プロセスの実行成功と判定"""
    ng = ssh_ng | pre_check_ng | change_ng | commit_ng | post_check_ng | exception_ng
    """プロセスの実行失敗と判定"""
    hazardous = auto()
    """ハザーダス状態"""
    non_hazardous = auto()
    """ハザーダスでない状態"""
    stop_ng_abort = auto()
    """全断防止判定され処理中断"""
    stop_ng_ongoing = auto()
    """全断防止判定されたが処理続行"""
    stop_ng = stop_ng_abort | stop_ng_ongoing
    """全断防止判定された"""
    warn = stop_ng_abort
    """プロセス実行一部注意と判定"""


class SoutSeverity(Enum):
    """標準出力で表示するメッセージの重大度
    """
    info = "[INFO]"
    """情報 現在の実行対象の状態を通知する場合"""
    error = "[ERROR]"
    """エラー プロセス実行時に何らかのエラーが発生した場合"""
    success = "[SUCCESS]"
    """成功 実行対象の状態変更に成功した場合"""
    result = "[RESULT]"
    """結果 ツール実行結果を通知する場合"""
    detail = "[DETAIL]"
    """詳細 ツール実行結果の詳細を通知する場合"""

    def __str__(self) -> str:
        return self.value


class TargetStatus(Enum):
    """対象ステータス
    """
    up = "UP"
    """対象の状態が取得でき、対象が有効な状態"""
    down = "DOWN"
    """対象の状態が取得でき、対象が無効な状態"""
    unknown = "UNKNOWN"
    """対象の状態が取得できない場合"""

    def __str__(self):
        return self.value


class AbcProcess(ABC):
    """抽象プロセスクラス
    """
    class LogStub():  # pragma: no cover
        """ログ出力なしクラス
        """

        def output_1stlog(self, *args, **kwargs):
            """一次解析ログスタブ
            """
            pass

        def output_2ndlog(self, *args, **kwargs):
            """障害解析ログスタブ
            """
            pass

    def __init__(self,
                 alias: str,
                 nf_name: str,
                 mode: Mode,
                 job_id: str = None):
        """コンストラクタ

        Args:
            alias (str): エイリアス
            nf_name (str): NF名
            mode (Mode): 実行モード
            job_id (str, optional): JOBID. Defaults to None.
        """
        self.__alias = alias
        self.__nf_name = nf_name
        self.__mode = mode
        self.__before_status: TargetStatus = None
        self.__after_status: TargetStatus = None
        self.__necessity: ProcessStatus = None
        self.__changed: ProcessStatus = None
        if job_id:
            self.__logger: Log = Log(job_id)
        else:
            self.__logger = self.LogStub()

    @property
    def alias(self) -> str:
        """コンストラクタ生成時に指定したエイリアスを取得

        Returns:
            str: エイリアス名
        """
        return self.__alias

    @property
    def nf_name(self) -> str:
        """コンストラクタ生成時に指定したNF名を取得

        Returns:
            str: NF名
        """
        return self.__nf_name

    @property
    def mode(self) -> Mode:
        """コンストラクタ生成時に指定した実行モードを取得

        Returns:
            Mode: 実行モード
        """
        return self.__mode

    @property
    def before_status(self) -> TargetStatus:
        """対象ステータス更新前の状態を取得。事前状態取得前はNoneとなる

        Returns:
            TargetStatus: 事前状態
        """
        return self.__before_status

    @before_status.setter
    def before_status(self, before_status: TargetStatus):
        self.__before_status = before_status

    @property
    def after_status(self) -> TargetStatus:
        """対象ステータス更新後の状態を取得。事後状態取得前はNoneとなる

        Returns:
            TargetStatus: 事後状態
        """
        return self.__after_status

    @after_status.setter
    def after_status(self, after_status: TargetStatus):
        self.__after_status = after_status

    @property
    def necessity(self) -> ProcessStatus:
        """対象ステータス更新の変更要否を取得。変更要否判定取得前はNoneとなる

        Returns:
            ProcessStatus: 変更要否
        """
        return self.__necessity

    @necessity.setter
    def necessity(self, necessity: ProcessStatus):
        self.__necessity = necessity

    @property
    def changed(self) -> ProcessStatus:
        """対象ステータス更新後の変更判定を取得。事後状態取得前はNoneとなる

        Returns:
            ProcessStatus: 変更判定
        """
        return self.__changed

    @changed.setter
    def changed(self, changed: ProcessStatus):
        self.__changed = changed

    @property
    def logger(self) -> Log:
        """共通ログ出力用ロガーを取得。コンストラクタ時にJOB_IDを指定しない場合はログ出力しない

        Returns:
            Log: ロガー
        """
        return self.__logger

    @abstractmethod
    def get_status_word(self, value: Any) -> str:  # pragma: no cover
        """ステータス文字列取得

        Args:
            value (Any): ステータス/モード

        Returns:
            str: ステータス文字列取得
        """
        pass

    @abstractmethod
    def get_status(self, *args, **kwargs) -> TargetStatus:  # pragma: no cover
        """現在の対象ステータス取得

        Returns:
            TargetStatus:
                稼働中の場合 up、
                非稼働の場合 down、
                ステータス取得失敗の場合 unknown、
                例外発生の場合 None
        """
        pass

    @abstractmethod
    def to_down(self, *args, **kwargs) -> bool:  # pragma: no cover
        """対象のステータスを無効(down)にするコマンドを投入。commit実行までは反映されない。

        Returns:
            bool:
                対象ステータスの無効化コマンドが投入できた場合 True、
                例外発生の場合 False
        """
        pass

    @abstractmethod
    def to_up(self, *args, **kwargs) -> bool:  # pragma: no cover
        """対象のステータスを有効(up)にするコマンドを投入。commit実行までは反映されない。

        Returns:
            bool:
                対象ステータスの有効化設定が投入できた場合 True、
                例外発生の場合 False
        """
        pass

    @abstractmethod
    def commit(self, *args, **kwargs) -> bool:  # pragma: no cover
        """対象NFに対して変更内容を保存する

        Returns:
            bool:
                正常終了完了の場合 True、
                例外発生の場合 False
        """
        pass

    @abstractmethod
    def do_abort(self, *args, **kwargs) -> bool:  # pragma: no cover
        """コマンドエラー発生時に設定を元に戻す

        Returns:
            bool:
                正常完了の場合 True、
                異常発生の場合 False
        """
        pass

    @abstractmethod
    def run(self, *args, **kwargs) -> ProcessStatus:  # pragma: no cover
        """NFステータス操作プロセス実行

        Returns:
            ProcessStatus: プロセスの完了ステータス
        """
        pass

    def sout_message(self, severity: SoutSeverity, body: str) -> None:
        """標準出力に指定した重大度のメッセージを既定のフォーマットで出力する

        Args:
            severity (SoutSeverity): 重大度
            body (str): ログメッセージ
        """
        message = f"{severity}:{self.mode}:{logtime()}:{self.alias}({self.nf_name}):{body}"
        print(message)

    def pre_check(self, *args, **kwargs) -> bool:
        """対象ステータスの事前確認を実施

        Returns:
            bool:
                変更要否確認が取得できた場合 True、
                それ以外の場合 False
        """
        self.before_status = self.get_status()
        self.necessity = self.necessity_check(self.before_status)
        return self.before_status is not None and self.necessity is not ProcessStatus.exception_ng

    def post_check(self, *args, **kwargs) -> bool:
        """対象ステータスの事後確認を実施

        Returns:
            bool:
                変更完了の場合 True、
                それ以外の場合 False
        """
        self.after_status = self.get_status()
        self.changed = self.changed_check(self.after_status)
        return self.after_status in (TargetStatus.up, TargetStatus.down) and self.changed is ProcessStatus.change_ok

    def change_status(self, *args, **kwargs) -> ProcessStatus:
        """対象ステータスの状態変更を実施

        Returns:
            ProcessStatus:
                正常に状態変更が完了した場合 commit_ok、
                保存失敗の場合 commit_ng、
                変更失敗の場合 change_ng
        """
        # ステータス変更コマンド取得
        if self.mode == Mode.down:
            changes_status = self.to_down
        else:
            changes_status = self.to_up

        if not changes_status():
            # 何らかの異常が発生した場合、事前状態に戻す
            self.do_abort()
            return ProcessStatus.change_ng
        elif not self.commit():
            # commitで異常が発生した場合、事前状態に戻す
            self.do_abort()
            return ProcessStatus.commit_ng
        else:
            return ProcessStatus.commit_ok

    def necessity_check(self, status: TargetStatus) -> ProcessStatus:
        """対象ステータスの変更要否確認を実施

        NFから取得したステータスの事前状態と、実行モードから、変更要否を取得する。

        対象NFがステータスDOWN中に再度DOWNが実行された(または真逆)の場合、
        冪等性の観点からコマンド投入不要と判断して、変更不要とする。

        事前状態が取得できない場合も変更不要とする。

        Args:
            status (TargetStatus): statusの事前状態

        Returns:
            ProcessStatus:
                要変更の場合 need_to_change、
                変更モード以外の場合 show_or_unknown、
                変更済みの場合 already_changed、
                それ以外の場合 exception_ng
        """
        # 変更可否確認
        if (self.mode, status) in [(Mode.show, TargetStatus.down), (Mode.show, TargetStatus.up)]:
            # SHOWモードかつ、事前ステータスがDOWNまたはUPの場合
            # 変更モード以外
            return ProcessStatus.show_or_unknown
        elif (self.mode, status) in [(Mode.up, TargetStatus.up), (Mode.down, TargetStatus.down)]:
            # UPモードかつ事前ステータスUPまたは、DOWNモードかつ事前ステータスDOWNの場合
            # 変更済み
            return ProcessStatus.already_changed
        elif (self.mode, status) in [(Mode.up, TargetStatus.down), (Mode.down, TargetStatus.up)]:
            # UPモードかつ事前ステータスDOWNまたは、DOWNモードかつ事前ステータスUPの場合
            # 要変更
            return ProcessStatus.need_to_change
        else:
            # 上記以外の場合
            # 取得失敗
            return ProcessStatus.exception_ng

    def changed_check(self, status: TargetStatus) -> ProcessStatus:
        """変更実行後の変更反映確認を実施

        ステータス変更後の状態の確認を行う。

        DOWN実行後のステータスがDOWN(またはその真逆)の場合、変更成功となる。

        DOWN実行後のステータスがUP(またはその真逆)の場合、変更失敗となる。

        Args:
            status (TargetStatus): statusの事後状態

        Returns:
            ProcessStatus:
                変更成功の場合 change_ok、
                変更失敗の場合 change_ng、
                それ以外の場合 exception_ng
        """
        if (self.mode, status) in [(Mode.up, TargetStatus.up), (Mode.down, TargetStatus.down)]:
            # UPモードかつ事後ステータスUPまたは、DOWNモードかつ事後ステータスDOWNの場合
            # 変更成功
            return ProcessStatus.change_ok
        elif (self.mode, status) in [(Mode.up, TargetStatus.down), (Mode.down, TargetStatus.up)]:
            # UPモードかつ事後ステータスDOWNまたは、DOWNモードかつ事後ステータスUPの場合
            # 変更失敗
            return ProcessStatus.change_ng
        else:
            # 上記以外の場合
            # 変更失敗
            return ProcessStatus.exception_ng
