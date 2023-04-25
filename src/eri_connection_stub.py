import json
from pathlib import Path
import re
import time
import paramiko

from xgnlog.Log import Log

from src.abc_process import Mode

# ツールローカル設定ディレクトリ
LOCAL_CONFIG_DIR = Path(__file__).resolve().parent.parent.joinpath("config")

TOOL_CONF = LOCAL_CONFIG_DIR.joinpath("stub.json")

with open(TOOL_CONF, "r", encoding="utf-8") as f:
    stub_dict = json.load(f)

JOB_ID = "T23AJ002"
LOGGER = Log(JOB_ID)


def get_sock(proxy_command: str, hostname: str, port: int = 22) -> paramiko.ProxyCommand:
    """
    """
    LOGGER.output_1st_log("I00203")
    LOGGER.output_1st_log("I00205")
    return object


class NFStubShellClient(paramiko.SSHClient):
    """
    """

    def __init__(self, mode: Mode, nf_name: str = None) -> None:
        """
        """
        LOGGER.output_1st_log("I00201")
        self.client = object
        self.shell = None
        self.flags = []
        self.mode = mode
        self.nf_name = nf_name
        self.blocked_nfs = []
        LOGGER.output_1st_log("I00202")

    def connect(self) -> None:
        """
        """
        LOGGER.output_1st_log("I00206", self.nf_name)
        try:
            time.sleep(1)
            # ログインプロンプトを読み飛ばす
            if self.nf_name in self.blocked_nfs:
                raise Exception()
        except Exception as e:
            raise super.SSHConnectException(str(e))

        LOGGER.output_1st_log("I00207", self.nf_name)

    def command(self, command: str, timeout: float = 10.0, wait: int = 0.5) -> bytes:
        """
        """
        LOGGER.output_1st_log("I00208", self.nf_name)
        # shellが利用不可能な場合
        time.sleep(0)
        LOGGER.output_1st_log("I00209", command)
        LOGGER.output_1st_log("I00213")

        reply = "error".encode()
        for key, value in stub_dict.items():
            if re.match(str(value["command"]), command):
                if key in self.flags:
                    before_after = "after"
                else:
                    before_after = "before"
                reply = str(value["reply"][self.mode.value][before_after]).encode()
                flag = value.get("flag", None)
                if flag:
                    self.flags.append(flag)
                time.sleep(value["wait"])
                break

        LOGGER.output_1st_log("I00215")
        LOGGER.output_1st_log("I00210", self.nf_name)
        return reply

    def close(self) -> None:
        """
        """
        LOGGER.output_1st_log("I00211", self.nf_name)
        LOGGER.output_1st_log("I00212", self.nf_name)

    def enter_config_mode(self) -> None:
        """
        """
        LOGGER.output_1st_log("I00217", self.nf_name)
        time.sleep(0.1)
        LOGGER.output_1st_log("I00218", self.nf_name)

    def exit_config_mode(self, forced=False) -> None:
        """
        """
        if forced:
            self.abort()
        else:
            LOGGER.output_1st_log("I00219", self.nf_name)
            time.sleep(0.1)
            LOGGER.output_1st_log("I00220", self.nf_name)

    def abort(self) -> None:
        """
        """
        LOGGER.output_1st_log("I00221", self.nf_name)
        time.sleep(0.1)
        LOGGER.output_1st_log("I00222", self.nf_name)
