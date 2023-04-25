import argparse
from enum import Enum
import ipaddress
from json import JSONDecodeError
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Set, Tuple

from xgnlog.Log import Level, Log

from src.abc_process import Mode, ProcessStatus, SoutSeverity, logtime
from src.eri_smfvo_xcap_process import EriSmfvoXCAPProcess


# 定数宣言
# xGNロガー
JOB_ID = "T23AJ001"
LOGGER = Log(JOB_ID, Level.DEBUG)

# 設定: 対象ノード情報
# ツールローカル設定ディレクトリ
LOCAL_CONFIG_DIR = Path(__file__).resolve().parent.parent.joinpath("config")
TOOL_CONF = LOCAL_CONFIG_DIR.joinpath("xcap-tool.json")
REQUIRED_KEYS = (NF_INFOS, EDNS_INFOS) = ("nf_infos", "edns_infos")

# 実行モード不明
MODE_UNKNOWN = "UNKNOWN"
# NF名不明
NF_NONE = "NF_NONE"

DispMode = {
    Mode.up: "NOT USED",
    Mode.down: "remove an xCAP ipaddr and add a reserved ipaddr",
    Mode.show: "show an xCAP ipaddr status",
    Mode.info: "show tool configuration",
    Mode.list: "show xCAP names"
}


class ToolResult(Enum):
    """NF Registrationツール実行時の結果種別

    """
    init = ""
    """実行中または、判定不能"""
    ng = "NG"
    """ツール実行結果失敗"""
    ok = "OK"
    """ツール実行結果成功"""

    def __str__(self):
        return self.value


class XcapTool(object):
    """xCAP IPアドレス参照・更新ツール

    """

    def sout_message(self, severity: SoutSeverity, body: str, mode: Mode = "", alias: str = "", nf_name: str = None):
        """標準出力に指定した重大度のメッセージを既定のフォーマットで出力する

        Args:
            severity (SoutSeverity): 重大度
            body (str): ログメッセージ
            mode (Mode, optional): 実行モード. Defaults to "".
            alias (str, optional): エイリアス. Defaults to "".
            nf_name (str, optional): NF名. Defaults to None.
        """
        msg = ""
        msg += f"{severity}:"
        msg += f"{MODE_UNKNOWN if mode is None else self.args.mode}:"
        msg += f"{logtime()}:"
        msg += f"{NF_NONE if alias is None else self.args.edns_name}"
        msg += f"({NF_NONE if nf_name is None else nf_name}):"
        msg += body
        print(msg)

    def check_args(self) -> bool:
        """スクリプト実行時に取得する引数内容をチェック

        Raises:
            ArgumentParserError: 引数異常があった場合

        Returns:
            bool: 正常終了の場合True、異常終了の場合False
        """
        class ArgumentParserError(Exception):
            pass

        class ThrowingArgumentParser(argparse.ArgumentParser):
            def error(self, message):
                raise ArgumentParserError(message)

        def not_null_str(val: str):
            if not val.strip():
                raise ArgumentParserError("Argument is None, null string or blank only.")
            return val

        def csv(val: str):
            ret: List = val.split(",")
            if "" in ret:
                ret.remove("")
            return ret

        LOGGER.output_1st_log("I00103")
        # Parserを準備
        try:
            # 有効なモードを指定(Mode.upを使用しない)
            valid_mode_list = list(Mode)
            valid_mode_list.remove(Mode.up)

            # 第1引数にLISTモードが指定された場合、第1引数にNF NONEを仮設定する
            if sys.argv[1] == Mode.list.value:
                sys.argv.insert(1, NF_NONE)
            parser = ThrowingArgumentParser()
            parser.add_argument("edns_name", help="target eDNS hostname", type=not_null_str)
            parser.add_argument("mode", help="exec MODE", choices=valid_mode_list, type=Mode)
            parser.add_argument("blocked_nflist", help="blocked nf name list", type=csv, nargs="?", default="")
            parser.add_argument("-b", "--batch", help="enable bach mode", action="store_true")
            parser.add_argument("-s", "--stub", help="stab mode", action="store_true")

            # 引数を判定し、取得した引数を格納する
            self.args: argparse.Namespace = parser.parse_args()

        except ArgumentParserError as e:
            argv = sys.argv[1:]
            message = f"failed to analyse arguments {argv}."
            self.sout_message(SoutSeverity.error, message, None, None)
            message = f"[ {ToolResult.ng} ]"
            self.sout_message(SoutSeverity.result, message, None, None)
            LOGGER.output_1st_log("E00102", argv)
            LOGGER.output_2nd_log(Level.CRITICAL,
                                  f"引数解析異常発生:\n"
                                  "パラメータ:\n"
                                  f" 引数: {argv}\n"
                                  f" Trace: {e.__class__.__name__} {e}")
            return False

        LOGGER.output_1st_log("I00104", sys.argv[1:])

        return True

    def load_config(self) -> bool:
        """JSON設定ファイルを読み込む

        Returns:
            bool: 正常終了の場合True、異常終了の場合False
        """
        LOGGER.output_1st_log("I00105")

        # ツール本体設定存在チェック&解析チェック
        with open(TOOL_CONF, "r", encoding="utf-8") as f:
            self.tool_conf: Dict[str, Dict[str, Any]] = json.load(f)

        # nf-module設定、nf-type設定
        for key in REQUIRED_KEYS:
            try:
                # 設定存在チェック&解析チェック
                file_path = LOCAL_CONFIG_DIR.joinpath(self.tool_conf[key])
                # JSON読込
                with open(file_path, "r", encoding="utf-8") as f:
                    self.tool_conf[key] = json.load(f)
            except Exception as e:
                message = f"[ {ToolResult.ng} ]"
                self.sout_message(SoutSeverity.result, message)

                LOGGER.output_1st_log("E00103", file_path)

                if isinstance(e, FileNotFoundError):
                    self.sout_message(SoutSeverity.error, f"configuration files not found. file={file_path}")
                    LOGGER.output_2nd_log(Level.CRITICAL,
                                          f"設定ファイルなし発生:\n"
                                          "パラメータ:\n"
                                          f" ファイルパス: {file_path}\n"
                                          f" Trace: {e.__class__.__name__} {e}")
                elif isinstance(e, JSONDecodeError):
                    self.sout_message(SoutSeverity.error, f"failed to analyse configuration files. file={file_path}")
                    LOGGER.output_2nd_log(Level.CRITICAL,
                                          f"設定ファイルJSON異常発生:\n"
                                          "パラメータ:\n"
                                          f" ファイルパス: {file_path}\n"
                                          f" Trace: {e.__class__.__name__} {e}")
                elif isinstance(e, KeyError):
                    self.sout_message(SoutSeverity.error, f"required json key not found. file={file_path}, key={key}")
                    LOGGER.output_2nd_log(Level.CRITICAL,
                                          f"設定ファイル必須キーなし発生:\n"
                                          "パラメータ:\n"
                                          f" ファイルパス: {file_path}\n"
                                          f" Trace: {e.__class__.__name__} {e}")
                else:
                    self.sout_message(SoutSeverity.error, f"unexpected error occurred. file={file_path}, key={key}")
                    LOGGER.output_2nd_log(Level.CRITICAL,
                                          f"想定外エラー発生:\n"
                                          "パラメータ:\n"
                                          f" ファイルパス: {file_path}\n"
                                          f" Trace: {e.__class__.__name__} {e}")

                return False

        LOGGER.output_1st_log("I00106")

        return True

    def info(self) -> None:
        """info INFO出力

        引数情報、対象ノード情報、対向ノード情報を出力する

        """
        LOGGER.output_1st_log("I00107")
        # 網閉塞管理DBに登録中のNFリストを取得
        blocked = f"\n{''.rjust(12)}".join(self.args.blocked_nflist if self.args.blocked_nflist else ["None"])
        target_info: List[str] = []

        # 画面表示をSMFv NF名の最大長に合わせるため、最大値を取得
        max_length_nfname = max([len(x) for x in self.smfvoice_configs.keys()])
        # 対象NF上の情報を表示するためのヘッダ情報
        message = f"{'smfvo(roout) nf name'.ljust(max_length_nfname)}: [ipaddrs]"
        target_info.append(message)

        for nf_name, value in self.smfvoice_configs.items():
            message = f"{nf_name.ljust(max_length_nfname)}: {value['xCAP']}"
            target_info.append(message)
        # 上記で収集した情報を出力データに追加
        targets = f"\n{''.rjust(12)}".join(target_info)

        messages = ""
        messages += f"{'eDNS Name'.rjust(10)}: {self.args.edns_name}\n"
        messages += f"{'IP ADDR'.rjust(10)}: {self.edns_ip_address}\n"
        messages += f"{'MODE'.rjust(10)}: {self.args.mode}\n"
        messages += f"{'COMMENT'.rjust(10)}: {DispMode[self.args.mode]}\n"
        messages += f"{'BLOCKED NF'.rjust(10)}: {blocked}\n"
        messages += f"{'BATCH'.rjust(10)}: {self.args.batch}\n"
        messages += f"{'TARGET'.rjust(10)}: {targets}\n"
        # 画面に情報を出力
        print(messages)
        LOGGER.output_1st_log("I00108", messages)

    def get_edns_ipaddr(self) -> str:
        """対象のeDNSホスト名に紐づくIPアドレスを取得する

        Raises:
            Exception: eDNSホスト名からIPアドレスの取得に失敗した場合

        Returns:
            str: eDNS IPアドレス
        """
        LOGGER.output_1st_log("I00109")
        ipaddr: str = None
        try:
            # P-CSCF情報取得
            ipaddr = self.tool_conf[EDNS_INFOS][self.args.edns_name]["ipaddr"]
            ipaddress.ip_address(ipaddr)

        except Exception as e:
            self.sout_message(SoutSeverity.error, "eDNS configuration not found.")
            LOGGER.output_1st_log("E00104", self.args.edns_name)
            LOGGER.output_2nd_log(Level.CRITICAL, "eDNS情報取得失敗:\n"
                                  "パラメータ:\n"
                                  f" eDNS: {self.args.edns_name}\n"
                                  f" INFO: {ipaddr}\n"
                                  f" Trace: {e.__class__.__name__} {e}")
            raise e

        LOGGER.output_1st_log("I00110", ipaddr)
        return ipaddr

    def get_smfvoice_configs(self) -> Dict[str, Dict[str, List[str]]]:
        """eDNS IPアドレスを元に対象となるSMFvのツール設定情報を取得する

        Raises:
            ValueError: 指定されたeDNS IPアドレスを含むSMFv NFの設定がない場合
            Exception: 何らかの異常が発生した場合

        Returns:
            Dict[str, Dict[str, List[str]]]: eDNS IPアドレスを含むSMFvツール設定
        """
        LOGGER.output_1st_log("I00111")

        filtered_dict: Dict[str, Dict[str, List[str]]]

        try:
            filtered_dict = dict(filter(lambda item: self.edns_ip_address in item[1]["xCAP"], self.tool_conf[NF_INFOS].items()))
            # 設定が空の場合
            if not any(filtered_dict):
                raise ValueError("filtered_list is empty.")

        except Exception as e:
            self.sout_message(SoutSeverity.error, "smfvoice configuration not found.")
            LOGGER.output_1st_log("E00105")
            LOGGER.output_2nd_log(Level.CRITICAL,
                                  "対向SMFv設定取得失敗:\n"
                                  "パラメータ:\n"
                                  f" eDNS: {self.args.edns_name}\n"
                                  f" 全SMFv: {self.tool_conf[NF_INFOS]}\n"
                                  f" Trace: {e.__class__.__name__} {e}")
            raise e

        LOGGER.output_1st_log("I00112", filtered_dict)
        return filtered_dict

    def main(self) -> bool:
        """main メイン処理

        xCAPツールメイン処理

        Returns:
            bool: 成功の場合True、異常発生の場合Falseとなる
        """
        LOGGER.output_1st_log("I00113")
        # Stubモード表示
        if self.args.stub:
            print("===== STUB MODE [ ON ] =====")

        # eDNS名リスト
        edns_name_list = list(self.tool_conf[EDNS_INFOS].keys())

        # LIST MODE
        if self.args.mode == Mode.list:
            LOGGER.output_1st_log("I00115")
            print("==eDNS LIST==")
            print("\n".join([f" {x}" for x in edns_name_list]))
            LOGGER.output_1st_log("I00116", edns_name_list)
            LOGGER.output_1st_log("I00114")
            return True

        try:
            # 対象eDNSホスト名からip addrを取得する
            self.edns_ip_address: str = self.get_edns_ipaddr()
            # 対象eDNSホストのip addrが設定可能なSMFv設定を取得
            self.smfvoice_configs: Dict[str, Dict[str, List[str]]] = self.get_smfvoice_configs()
        except Exception:
            self.sout_message(SoutSeverity.result, f"[ {ToolResult.ng} ]")
            LOGGER.output_1st_log("I00122", ToolResult.ng)
            LOGGER.output_1st_log("I00114")
            return False

        # 対象内容を表示
        self.info()

        # MODE_INFOの場合はここで終了
        if self.args.mode == Mode.info:
            self.sout_message(SoutSeverity.result, f"[ {ToolResult.ok} ]")
            LOGGER.output_1st_log("I00122", ToolResult.ok)
            LOGGER.output_1st_log("I00114")
            return True

        # batch処理フラグがない場合
        if not self.args.batch:
            (is_continue, choice) = interactive_check("Please input [Y] for next action, or [N] for abort.: ",
                                                      ["y", "ye", "yes"],
                                                      ["n", "no"])
            if not is_continue:
                self.sout_message(SoutSeverity.info, "script was aborted due to an interractive action.")
                LOGGER.output_1st_log("I00123", choice)
                LOGGER.output_1st_log("I00114")
                return True

        print(f"Start Time: {logtime()}", file=sys.stdout)

        LOGGER.output_1st_log("I00117")
        result: ToolResult = ToolResult.init
        success_nf_list: List[str] = []
        failed_nf_list: List[str] = []
        blocked_nf_list: List[str] = []

        # 障害NFリストに含まれるeDNSホスト名を取得
        failed_edns_set: Set[str] = set(self.tool_conf[EDNS_INFOS].keys()) & set(self.args.blocked_nflist)

        for nf_name, config in self.smfvoice_configs.items():

            # SMFv設定内に障害NFリストに含まれるeDNSホスト名のIPアドレスがある場合、対象を削除する
            for failed_edns in failed_edns_set:
                failed_edns_ipaddr = self.tool_conf[EDNS_INFOS][failed_edns]["ipaddr"]
                if failed_edns_ipaddr in config["xCAP"]:
                    config["xCAP"].remove(failed_edns_ipaddr)

            process = EriSmfvoXCAPProcess(self.args.edns_name,
                                          nf_name,
                                          self.args.mode,
                                          self.edns_ip_address,
                                          config["xCAP"],
                                          self.args.stub,
                                          "T23AJ003")

            # プロセス実行
            process_result = process.run()

            # 何らかのNGとなった場合
            if (process_result & ProcessStatus.ng):
                if nf_name in self.args.blocked_nflist:
                    blocked_nf_list.append(nf_name)
                else:
                    failed_nf_list.append(nf_name)
            # OKとなった場合
            else:
                # 正常完了したノードをsuccess_listに追加
                success_nf_list.append(nf_name)

        LOGGER.output_1st_log("I00118")

        result = ToolResult.ng if len(failed_nf_list) else ToolResult.ok

        self.sout_message(SoutSeverity.result, f"[ {result} ]")
        message = f"SUCCESS={len(success_nf_list)}, FAILED={len(failed_nf_list)}, BLOCKED={len(blocked_nf_list)}"
        self.sout_message(SoutSeverity.detail, message)
        self.sout_message(SoutSeverity.detail, f"SUCCESSED NF {success_nf_list}")
        self.sout_message(SoutSeverity.detail, f"FAILED NF {failed_nf_list}")
        self.sout_message(SoutSeverity.detail, f"BLOCKED NF {blocked_nf_list}")

        LOGGER.output_1st_log("I00119", success_nf_list)
        LOGGER.output_1st_log("I00120", failed_nf_list)
        LOGGER.output_1st_log("I00121", blocked_nf_list)
        LOGGER.output_1st_log("I00122", result)

        print(f"End Time: {logtime()}", file=sys.stdout)

        LOGGER.output_1st_log("I00114")
        return False if result == ToolResult.ng else True


def interactive_check(message: str, continue_list: List[str], abort_list: List[str], case_sensitive: bool = False) -> Tuple[bool, str]:
    """interactive_check 実行継続チェック

    Args:
        message (str): 表示文字列
        continue_list (List[str]): 処理継続文字列リスト
        abort_list (List[str]): 処理中止文字列リスト
        case_sensitive (bool, optional): 大文字と小文字を区別する場合はTrue、区別しない場合はFalse. Defaults to False.

    Returns:
        Tuple[bool, str]: 入力文字列および、継続を示す場合はTrue、中止を示す場合はFalse
    """
    # 大文字と小文字を区別しない場合はそれぞれを小文字に変換する
    continue_list = [x.lower() for x in continue_list] if not case_sensitive else continue_list
    abort_list = [x.lower() for x in abort_list] if not case_sensitive else abort_list
    while True:
        choice = input(message)
        choice = choice.lower() if not case_sensitive else choice
        if choice in continue_list:
            return (True, choice)
        elif choice in abort_list:
            return (False, choice)


if __name__ == "__main__":  # pragma: no cover

    LOGGER.output_1st_log("I00101")
    tool = XcapTool()

    if tool.check_args() and tool.load_config() and tool.main():
        LOGGER.output_1st_log("I00102")
        exit(0)
    else:
        LOGGER.output_1st_log("E00101")
        exit(1)
