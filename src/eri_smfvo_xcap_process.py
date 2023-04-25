from pathlib import Path
import time
from typing import Any, Dict, List, Set

from xgnlog.Log import Level
from textfsm import TextFSM

from src.abc_eri_process import AbcEricssonProcess
from src.abc_process import Mode, ProcessStatus, SoutSeverity, TargetStatus, logtime
from src.eri_connection import SocketTimeoutException

# ツールローカル設定ディレクトリ
LOCAL_CONFIG_DIR = Path(__file__).resolve().parent.parent.joinpath("config")
# xCAPテンプレート
with open(LOCAL_CONFIG_DIR.joinpath("xcap_template.textfsm"), "r") as f:
    XCAP_TEMPLATE: TextFSM = TextFSM(f)


class EriSmfvoXCAPProcess(AbcEricssonProcess):
    """Ericsson SMF xCAPIP更新プロセスクラス

    対応するSMFは以下の通り

    smfvo(voice) / smfvoroout(sliceB)
    """

    def __init__(self,
                 edns_name: str,
                 nf_name: str,
                 mode: Mode,
                 edns_ipaddr: str,
                 ipaddr_list: List[str],
                 stub: bool,
                 job_id: str = None):
        """コンストラクタ

        Args:
            edns_name (str): eDNSホスト名
            nf_name (str): SMFv NF名
            mode (Mode): 実行モード
            edns_ipaddr (str): eDNSホストのIPアドレス
            ipaddr_list (List[str]): SMFvが設定可能なIPアドレスリスト
            stub (bool): スタブモード
            job_id (str, optional): JOB ID. Defaults to None.
        """
        super().__init__(edns_name, nf_name, mode, stub, job_id)
        self.__edns_ipaddr = edns_ipaddr
        self.__remove_ipaddr = edns_ipaddr
        self.__add_ipaddr: str = None
        self.__priority: str = None
        self.__ipaddr_list = ipaddr_list

    @property
    def edns_ipaddr(self) -> str:
        """eDNS IPアドレスプロパティ

        Returns:
            str: eDNS IPアドレス
        """
        return self.__edns_ipaddr

    @property
    def remove_ipaddr(self) -> str:
        """削除対象 IPアドレスプロパティ

        Returns:
            str: 削除対象IPアドレス
        """
        return self.__remove_ipaddr

    @remove_ipaddr.setter
    def remove_ipaddr(self, value: str):
        self.__remove_ipaddr = value

    @property
    def add_ipaddr(self) -> str:
        """追加IPアドレスプロパティ

        Returns:
            str: 追加IPアドレス
        """
        return self.__add_ipaddr

    @add_ipaddr.setter
    def add_ipaddr(self, value: str):
        self.__add_ipaddr = value

    @property
    def priority(self) -> str:
        """優先度プロパティ

        Returns:
            str: 優先度
        """
        return self.__priority

    @priority.setter
    def priority(self, value: str):
        self.__priority = value

    @property
    def ipaddr_list(self) -> List[str]:
        """設定可能IPアドレスリストプロパティ

        Returns:
            List[str]: 設定可能IPアドレスリスト
        """
        return self.__ipaddr_list

    def get_command(self, mode: Mode) -> str:
        """xCAP IPアドレスを変更・確認するコマンドを実行モードを元に取得

        Args:
            mode (Mode): 実行モード

        Returns:
            str: xCAP IPアドレスを変更・確認するコマンド
        """
        command = None
        if mode == Mode.up:
            command = f"epg pgw apn xcap ipv6-name-server {self.add_ipaddr} priority {self.priority}"
        elif mode == Mode.down:
            command = f"no epg pgw apn xcap ipv6-name-server {self.edns_ipaddr}"
        elif mode == Mode.show:
            command = "show running-config epg pgw apn xcap ipv6-name-server"
        return command

    def get_status_word(self, value: TargetStatus) -> str:
        """対象のステータスからステータスを示す文字列取得

        Args:
            value (TargetStatus): ステータス

        Returns:
            str: upの場合はin use、downの場合はout of use、それ以外の場合はunknown
        """
        word = "unknown"
        if value == TargetStatus.up:
            word = "in use"
        elif value == TargetStatus.down:
            word = "out of use"
        return word

    def get_commit_comment(self) -> str:
        """コミット時に適用するコミットコメントを取得する

        Returns:
            str: コミットコメント
        """
        date: str = logtime().replace(" ", "").replace("-", "").replace(":", "")
        return f"{date}_xcap_eDNS_Change"

    def get_status(self) -> TargetStatus:
        """現在のxCAPステータスを取得する

        Returns:
            TargetStatus: 削除IPアドレスがある場合up、ない場合down、例外発生ならNone
        """
        self.logger.output_1st_log("I00321", self.nf_name)

        try:
            # 現状のステータス取得
            command = self.get_command(Mode.show)
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)

            self.get_status_result = result

            up_pattern = self.edns_ipaddr
            # up_patternを含む場合はTargetStatus.up、無ければTargetStatus.down
            status: TargetStatus = TargetStatus.up if result.lower().count(up_pattern.lower()) else TargetStatus.down
        except SocketTimeoutException as e:
            self.sout_message(SoutSeverity.error, "ssh connection timeout was happened. [ UNKNOWN ]")
            self.logger.output_1st_log("E00304", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr状態取得失敗:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return None

        except Exception as e:
            self.sout_message(SoutSeverity.error, "unexpected error occurred. [ UNKNOWN ]")
            self.logger.output_1st_log("E00304", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr状態取得失敗:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return None

        self.logger.output_1st_log("I00322", [self.nf_name, status])

        return status

    def change_status(self) -> ProcessStatus:
        """対象ステータスの状態変更を実施

        Returns:
            ProcessStatus: 正常に状態変更が完了した場合はcommit_ok、保存失敗の場合はcommit_ng、変更失敗の場合はchange_ng
        """
        self.logger.output_1st_log("I00323", self.nf_name)

        # NF取得情報を解析
        self.parse_result(self.get_status_result)

        # 追加(予備)IPアドレスが存在しない場合
        if not self.add_ipaddr:
            # 追加(予備)IPアドレスがない旨を表示
            self.sout_message(SoutSeverity.error,
                              f"xcap ipaddr change was failed due to no reserved ipaddr. current status is"
                              f" {self.get_status_word(self.before_status)}. [ {self.before_status} ]")
            self.logger.output_1st_log("E00321", [self.nf_name, self.mode])

            return ProcessStatus.change_ng

        # 現在の設定を削除 & 追加(予備)IPアドレスへ付け替え
        if not self.to_down() or not self.to_up():
            # 何らかの異常が発生した場合、事前状態に戻す
            self.do_abort()
            # 設定を戻した旨、事前のステータスとともに表示
            self.sout_message(SoutSeverity.error,
                              f"xcap ipaddr change was failed. abort has done. current status is"
                              f" {self.get_status_word(self.before_status)}. [ {self.before_status} ]")
            self.logger.output_1st_log("E00321", [self.nf_name, self.mode])

            return ProcessStatus.change_ng
        elif not self.commit():
            # commitで異常が発生した場合、事前状態に戻す
            self.do_abort()
            # 設定を戻した旨を表示
            self.sout_message(SoutSeverity.error, "commit was failed. abort has done.")
            self.logger.output_1st_log("E00322", [self.nf_name, self.mode])

            return ProcessStatus.commit_ng
        else:
            self.logger.output_1st_log("I00324", self.nf_name)

            return ProcessStatus.commit_ok

    def to_down(self) -> bool:
        """指定されたxCAP IPアドレスを無効(down)にするコマンドを投入。commit実行までは反映されない。

        Returns:
            bool: xCAP IPアドレスの無効化コマンドが投入できた場合True、例外発生ならFalse
        """
        self.logger.output_1st_log("I00325", self.nf_name)

        try:
            command = None
            # 設定変更モード開始
            self.logger.output_1st_log("I00309", "config")
            self.client.enter_config_mode()
            self.logger.output_1st_log("I00310", None)

            command = self.get_command(Mode.down)
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)

        except SocketTimeoutException as e:
            self.sout_message(SoutSeverity.error, "ssh connection timeout was happened. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", [self.nf_name, self.mode])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr削除変更異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        except Exception as e:
            self.sout_message(SoutSeverity.error, "unexpected error occurred. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", [self.nf_name, self.mode])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr削除変更異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        self.logger.output_1st_log("I00326", [self.nf_name, self.mode, True])
        return True

    def to_up(self) -> bool:
        """指定されたxCAP IPアドレスを有効(up)にするコマンドを投入。commit実行までは反映されない。

        Returns:
            bool: xCAP IPアドレスの有効化コマンドが投入できた場合True、例外発生ならFalse
        """
        self.logger.output_1st_log("I00327", self.nf_name)

        try:
            command = None
            # 設定変更モード開始
            self.logger.output_1st_log("I00309", "config")
            self.client.enter_config_mode()
            self.logger.output_1st_log("I00310", None)

            command = self.get_command(Mode.up)
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)

        except SocketTimeoutException as e:
            self.sout_message(SoutSeverity.error, "ssh connection timeout was happened. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", [self.nf_name, self.mode])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr追加変更異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        except Exception as e:
            self.sout_message(SoutSeverity.error, "unexpected error occurred. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", [self.nf_name, self.mode])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr追加変更異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        self.logger.output_1st_log("I00328", [self.nf_name, self.mode, True])
        return True

    def pre_check(self) -> bool:
        """対象ステータスの事前確認を実施

        Returns:
            bool: 変更要否確認が取得できた場合はTrue、それ以外の場合はFalse
        """
        self.logger.output_1st_log("I00329", self.nf_name)
        res = super().pre_check()
        self.logger.output_1st_log("I00330", [self.nf_name, f"pre_check: {res}"])
        return res

    def post_check(self) -> bool:
        """対象ステータスの事後確認を実施

        Returns:
            bool: 変更完了の場合はTrue、それ以外の場合はFalse
        """
        self.logger.output_1st_log("I00331", self.nf_name)
        res = super().post_check()
        self.logger.output_1st_log("I00332", [self.nf_name, f"post_check: {(res)}"])
        return res

    def necessity_check(self, status: TargetStatus) -> ProcessStatus:
        """対象ステータスの変更要否確認を実施

        NFから取得したステータスの事前状態と、実行モードから、変更要否を取得する。

        対象NFがステータスDOWN中に再度DOWNが実行された(または真逆)の場合、
        冪等性の観点からコマンド投入不要と判断して、変更不要とする。

        事前状態が取得できない場合も変更不要とする。

        Args:
            status (TargetStatus): statusの事前状態

        Returns:
            ProcessStatus : 要変更の場合は need_to_change、変更モード以外の場合は show_or_unknown、変更済みの場合は already_changed、それ以外の場合は exception_ng
        """
        self.logger.output_1st_log("I00333", self.nf_name)
        necessity = super().necessity_check(status)
        if necessity == ProcessStatus.show_or_unknown:
            # ステータス表示
            self.sout_message(SoutSeverity.info,
                              f"current xCAP ipaddr is {self.get_status_word(status)}. [ {status} ]")
            self.logger.output_1st_log("I00341", [self.nf_name, self.mode, status])
        elif necessity == ProcessStatus.already_changed:
            # ステータス変更済み表示
            self.sout_message(SoutSeverity.success,
                              f"current xCAP ipaddr is already {self.get_status_word(status)}. [ {status} ]")
            self.logger.output_1st_log("I00341", [self.nf_name, self.mode, status])
        elif necessity == ProcessStatus.need_to_change:
            # ステータス表示
            self.sout_message(SoutSeverity.info,
                              f"current xCAP ipaddr is {self.get_status_word(status)}. [ {status} ]")
            self.logger.output_1st_log("I00342", [self.nf_name, self.mode, status])
        else:
            # ステータス取得失敗
            self.sout_message(SoutSeverity.error,
                              "currentry xCAP ipaddr couldn't get or mismatch. [ UNKNOWN ]")
            self.logger.output_1st_log("E00323", [self.nf_name, self.mode, status])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr事前状態取得失敗:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" MODE: {self.mode}\n"
                                       f" STATUS: {status}")

        self.logger.output_1st_log("I00334", [self.nf_name, f"necessity: {necessity}"])
        return necessity

    def changed_check(self, status: TargetStatus) -> ProcessStatus:
        """変更実行後の変更反映確認を実施

        ステータス変更後の状態の確認を行う。

        DOWN実行後のステータスがDOWN(またはその真逆)の場合、変更成功となる。

        DOWN実行後のステータスがUP(またはその真逆)の場合、変更失敗となる。

        Args:
            status (TargetStatus): statusの事後状態

        Returns:
            ProcessStatus: 変更成功の場合は change_ok、変更失敗の場合は change_ng、それ以外の場合は exception_ng
        """
        self.logger.output_1st_log("I00335", self.nf_name)

        # 削除IPアドレスチェック
        res = super().changed_check(status)

        # 追加IPアドレスチェック
        is_added = bool(self.get_status_result.lower().count(self.add_ipaddr))

        changed: ProcessStatus = res
        if res == ProcessStatus.change_ok and is_added:
            if is_added:
                # ステータス表示
                self.sout_message(SoutSeverity.success,
                                  f"current xCAP ipaddr is {self.get_status_word(status)}. [ {status} ]")
                self.logger.output_1st_log("I00343", [self.nf_name, self.mode, status])
            else:
                changed = ProcessStatus.change_ng
                # ステータス変更失敗表示(追加失敗)
                self.sout_message(SoutSeverity.error,
                                  f"current xCAP ipaddr is {self.get_status_word(status)}. but couldn't add... [ {status} ]")
                self.logger.output_1st_log("E00324", [self.nf_name, self.mode, status])
                self.logger.output_2nd_log(Level.CRITICAL,
                                           f"xCAP ipaddr事後確認変更失敗:\n"
                                           "パラメータ:\n"
                                           f" NF名: {self.nf_name}\n"
                                           f" MODE: {self.mode}\n"
                                           f" STATUS: {status}")
        elif res == ProcessStatus.change_ng:
            # ステータス変更失敗表示(削除失敗)
            self.sout_message(SoutSeverity.error,
                              f"xCAP ipaddr couldn't change... still {self.get_status_word(status)}. [ {status} ]")
            self.logger.output_1st_log("E00324", [self.nf_name, self.mode, status])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr事後確認変更失敗:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" MODE: {self.mode}\n"
                                       f" STATUS: {status}")
        else:
            # ステータス取得失敗
            self.sout_message(SoutSeverity.error,
                              "currentry xCAP ipaddr couldn't get or mismatch. [ UNKNOWN ]")
            self.logger.output_1st_log("E00323", [self.nf_name, self.mode, status])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr事後確認取得失敗:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" MODE: {self.mode}\n"
                                       f" STATUS: {status}")

        self.logger.output_1st_log("I00336", [self.nf_name, f"changed: {changed}"])
        return changed

    def parse_result(self, result: str) -> None:
        """NFから取得したxCAP設定を解析し、付け替えるIPアドレスおよび優先度を取得する

        Args:
            result (str): xCAP設定
        """
        self.logger.output_1st_log("I00337", self.nf_name)
        # NFから取得した結果を辞書型で保存
        XCAP_TEMPLATE.Reset()
        parsed_list: List[Dict[str, Any]] = [
            dict(zip(XCAP_TEMPLATE.header, pr))
            for pr in XCAP_TEMPLATE.ParseText(result)]
        # NFに設定されているxCAP ipaddrのリストを生成
        included_ipaddr_set: Set[str] = {x["ipaddr"] for x in parsed_list}
        # ツール設定で保持しているxCAP ipaddrリストに含まれていないipaddrを付け替えipaddrとして選定
        exclude_ipaddr_set: Set[str] = set(self.ipaddr_list) ^ included_ipaddr_set
        self.add_ipaddr = exclude_ipaddr_set.pop() if exclude_ipaddr_set else None
        # NFから取得した結果から、削除ipaddrに紐づくpriorityを取得
        for element in parsed_list:
            if element["ipaddr"] == self.edns_ipaddr:
                self.priority = element["priority"]
                break
        self.logger.output_1st_log("I00338", [self.nf_name, parsed_list, self.add_ipaddr, self.priority])

    def run(self) -> ProcessStatus:
        """NFに対してxCAP IPアドレスの現状確認・変更処理を実行する

        Returns:
            ProcessStatus: プロセスの完了ステータス
        """
        self.logger.output_1st_log("I00339", self.nf_name)

        # プロセス状態初期化
        status: ProcessStatus = 0
        if not self.open_client():
            # SSH接続に失敗した場合
            status = ProcessStatus.ssh_ng
            self.logger.output_1st_log("I00340", [self.nf_name, f"process status: {status}"])
            return status
        try:
            if not self.pre_check():
                # P-CSCFの事前状態確認に失敗した場合
                status |= ProcessStatus.pre_check_ng
                return status

            if self.necessity in ProcessStatus.need_not_to_change:
                # S-out/S-inの必要がない場合
                status |= ProcessStatus.need_not_to_change
                return status

            if not self.change_status() == ProcessStatus.commit_ok:
                # S-out/S-in処理に失敗した場合
                status |= ProcessStatus.change_ng
                return status

            # 設定変更後の処理待ち
            time.sleep(5)

            if self.post_check():
                # 事後確認が正常に完了した場合
                status = ProcessStatus.post_check_ok
                return status
            else:
                # 事後確認でS-out/S-inに失敗と判定した場合
                status = ProcessStatus.post_check_ng
                return status

        except Exception as e:
            status = ProcessStatus.exception_ng
            # 何らかのExceptionが発生した場合
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"xCAP ipaddr変更プロセス異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" STATUS: {status}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return status

        finally:
            self.logger.output_1st_log("I00340", [self.nf_name, f"process status: {status}"])
            # SSH接続を終了する
            self.close_client()
