import json
import logging
from pathlib import Path
import re
import socket
import time
import paramiko

from xgnlog.Log import Level, Log

paramikologger = logging.getLogger("paramiko")
paramikologger.addHandler(logging.NullHandler())

# 定数宣言
# 共通ロガー
JOB_ID = "T23AJ002"
LOGGER = Log(JOB_ID)

# ツールローカル設定ディレクトリ
LOCAL_CONFIG_DIR = Path(__file__).resolve().parent.parent.joinpath("config")

# E///接続用設定ファイル
CONN_FILE = LOCAL_CONFIG_DIR.joinpath("connections.json")
# 接続設定ファイル読込
with open(CONN_FILE, "r", encoding="utf-8") as f:
    CONN_CONF = json.load(f)
(CONN_COMMON, CONN_CONNECTIONS, CONN_BASTIONS) = ("common", "connections", "bastions")

# shell読込バッファ
READ_SIZE = 10240


def get_sock(bastion_name: str, hostname: str, port: int = 22) -> paramiko.ProxyCommand:
    """get_sock ProxyCommand取得

    SSH接続時に踏み台が必要な場合、ProxyCommandを生成します
    sshコマンドで利用する"-W"オプションで%hや%pといったパラメータは自動展開されません
    hostname、portを指定することで内部で置換を行います

    Args:
        bastion_name (str): 踏み台名
        hostname (str): 対向ホスト名。%hを置換するために利用
        port (int, optional): 対向接続ポート番号 %pを置換するために利用. Defaults to 22.

    Raises:
        ProxyCommandException: ProxyCommand生成で異常があった場合

    Returns:
        paramiko.ProxyCommand: ProxyCommandオブジェクト。commandがない場合はNone
    """
    LOGGER.output_1st_log("I00203")

    proxy_command = CONN_CONF[CONN_BASTIONS].get(bastion_name, {}).get("proxycommand")

    if proxy_command is None:
        LOGGER.output_1st_log("I00204")
        return None
    try:
        proxy_command = proxy_command.replace("%h", hostname).replace("%p", str(port))
        sock = paramiko.ProxyCommand(proxy_command)
    except Exception as e:
        LOGGER.output_1st_log("E00202")
        LOGGER.output_2nd_log(Level.CRITICAL, f"ProxyCommand取得異常:\nパラメータ:\n command: {proxy_command}\n hostname: {hostname}\n port: {port}\n Trace: {e.__class__.__name__} {e}")

        raise ProxyCommandException(bastion_name)

    LOGGER.output_1st_log("I00205")
    return sock


class NFShellClient(paramiko.SSHClient):
    """NFShellClient E/// NFShell接続用クラス

    """

    def __init__(self, nf_name: str) -> None:
        """インスタンス生成

        Args:
            nf_name (str, optional): NFノード名

        Raises:
            ValueError: nf_nameにNoneが指定された場合
        """
        LOGGER.output_1st_log("I00201", nf_name)
        if nf_name is None:
            LOGGER.output_1st_log("E00201", nf_name)
            LOGGER.output_2nd_log(Level.CRITICAL, f"インスタンス生成異常:\nパラメータ:\n nf_name: {nf_name}")
            raise ValueError("nf_name: None is not allowed value.")
        super().__init__()
        self.nf_name = nf_name
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell: paramiko.Channel = None
        self.prompt: str = None
        self.is_config_mode = False
        LOGGER.output_1st_log("I00202", nf_name)

    def connect(self) -> None:
        """SSH接続開始

        Raises:
            KeyError: _CONN_CONFから値の取得に失敗した場合
            SSHConnectException: SSH接続に失敗した場合
        """
        LOGGER.output_1st_log("I00206", self.nf_name)

        connection_info = CONN_CONF[CONN_CONNECTIONS][self.nf_name]
        common_info = CONN_CONF[CONN_COMMON]
        ipaddr: str = connection_info["ipaddr"]
        port: int = connection_info.get("port", common_info.get("port", 22))
        username: str = connection_info.get("username", common_info.get("username", None))
        password: str = connection_info.get("password", common_info.get("password", None))
        key_filename: str = connection_info.get("key_filename", common_info.get("key_filename", None))
        passphrase: str = connection_info.get("passphrase", common_info.get("passphrase", None))

        # 踏み台設定取得
        bastion = connection_info.get("bastion", None)
        sock = get_sock(bastion, ipaddr)

        # paramiko連携キーワード引数(パスワードは別途指定する)
        paramiko_args = {
            "username": username,
            "port": port,
            "key_filename": key_filename,
            "sock": sock,
            "timeout": 10
        }

        try:
            super().connect(ipaddr, password=password, passphrase=passphrase, **paramiko_args)
            self.shell = super().invoke_shell()
            # ログインプロンプトまで読み飛しプロンプトを取得
            _ = self._read_first()
        except Exception as e:
            LOGGER.output_1st_log("E00203", self.nf_name)
            LOGGER.output_2nd_log(Level.CRITICAL, f"SSH接続異常:\nパラメータ:\n nf_name: {self.nf_name}\n hostname: {ipaddr}\n password: ************\n passphrase: ************\n kwargs: {paramiko_args}\n Trace: {e.__class__.__name__} {e}")
            self.close()
            raise SSHConnectException(str(e))

        LOGGER.output_1st_log("I00207", self.nf_name)

    def close(self) -> None:
        """SSH切断処理
        """
        LOGGER.output_1st_log("I00211", self.nf_name)
        if self._is_shell_enable():
            # shellをクローズ
            self.shell.close()
        # clientをクローズ
        super().close()

        LOGGER.output_1st_log("I00212", self.nf_name)

    def enter_config_mode(self) -> None:
        """設定モード移行

        設定モードではプロンプトが変わるため、プロンプト情報を更新する
        """
        # シェル利用不可の為
        if not self._is_shell_enable():
            LOGGER.output_1st_log("I00216", self.nf_name)
            return None
        # 設定モード中の為
        if self.is_config_mode:
            LOGGER.output_1st_log("I00226", self.nf_name)
            return None

        LOGGER.output_1st_log("I00217", self.nf_name)
        self.shell.send(f"config\n")
        self._read_first()
        self.is_config_mode = True
        LOGGER.output_1st_log("I00218", self.nf_name)

    def exit_config_mode(self, forced=False) -> None:
        """設定モード解除

        設定モードを解除する
        解除後はプロンプトが変わるため、プロンプト情報を更新する

        Args:
            forced (bool, optional): 設定モードの強制終了
        """
        # シェル利用不可の為
        if not self._is_shell_enable():
            LOGGER.output_1st_log("I00216", self.nf_name)
            return None
        # 設定モード外の為
        if not self.is_config_mode:
            LOGGER.output_1st_log("I00227", self.nf_name)
            return None

        if forced:
            self.abort()
        else:
            LOGGER.output_1st_log("I00219", self.nf_name)
            self.shell.send(f"end\n")
            self._read_first()
            self.is_config_mode = False
            LOGGER.output_1st_log("I00220", self.nf_name)

    def abort(self) -> None:
        """設定モード強制終了(元に戻す)

        設定モードを強制終了する
        強制終了すると、設定中の情報を反映せずに元に戻すことができる
        """
        # シェル利用不可の為
        if not self._is_shell_enable():
            LOGGER.output_1st_log("I00216", self.nf_name)
            return None
        # 設定モード外の為
        if not self.is_config_mode:
            LOGGER.output_1st_log("I00227", self.nf_name)
            return None

        LOGGER.output_1st_log("I00221", self.nf_name)
        self.shell.send(f"abort\n")
        self._read_first()
        self.is_config_mode = False
        LOGGER.output_1st_log("I00222", self.nf_name)

    def command(self, command: str, timeout: float = 15.0) -> bytes:
        """コマンド投入

        E///装置に対してコマンドを投入します
        configコマンドでconfigモードに入る必要などありますが、exec_commandでは実現できないため、
        invoke_shellを利用します。

        Args:
            command (str): 投入コマンド
            timeout (float, optional): タイムアウト. Defaults to 15.0.

        Raises:
            SocketTimeoutException: タイムアウトが発生した場合

        Returns:
            bytes: 受信データ
        """
        LOGGER.output_1st_log("I00208", self.nf_name)
        # shellが利用不可能な場合
        if not self._is_shell_enable():
            LOGGER.output_1st_log("I00216", self.nf_name)
            return b""
        LOGGER.output_1st_log("I00209", command)
        self.shell.send(f"{command}\n")
        self.shell.settimeout(timeout)
        try:
            result = self._read()
        except socket.timeout as e:
            LOGGER.output_1st_log("E00204", self.nf_name)
            LOGGER.output_2nd_log(Level.CRITICAL, f"コマンド投入タイムアウト発生:\nパラメータ:\n nf_name: {self.nf_name}\n command: {command}\n timeout: {timeout}\n Trace: {e.__class__.__name__} {e}")
            raise SocketTimeoutException(str(e))
        finally:
            self.shell.settimeout(None)

        LOGGER.output_1st_log("I00210", self.nf_name)
        return result

    def _read(self) -> bytes:
        """データ受信

        invoke_shellで投入したコマンド結果を受信します
        recv_ready()を確認し、recv_ready()がFalseになるまでREAD_SIZEずつ読み込みます
        受信データは投入コマンドおよびプロンプトが前後1行ずつ付与されるため、

        Returns:
            bytes: 受信データ
        """
        LOGGER.output_1st_log("I00213")
        buffer = b""
        # shellが利用不可能な場合
        if not self._is_shell_enable():
            LOGGER.output_1st_log("I00215")
            return buffer
        # プロンプトを受信するまでループ
        while True:
            # 受信待ち状態の場合
            while self.shell.recv_ready():
                buffer += self.shell.recv(READ_SIZE)
            if len(buffer) != 0 and self.prompt == self._get_prompt(buffer):
                break
            time.sleep(0.1)
        LOGGER.output_2nd_log(Level.DEBUG, f"RAW data: {buffer}")

        # 1行目に投入コマンド、最終行にプロンプトが表示されるため、削除
        buffer = b"\n".join((buffer.splitlines())[1:-1])

        LOGGER.output_1st_log("I00215")
        return buffer

    def _read_first(self) -> None:
        """初回読み込み

        ログイン時にプロンプトを取得する必要があるため、個別の読込関数を準備する
        設定モードの移行・解除においてもプロンプトが変化するため本関数を利用する

        Raises:
            Exception: _description_
        """
        LOGGER.output_1st_log("I00223")
        buffer = b""
        if not self._is_shell_enable():
            LOGGER.output_1st_log("I00216", self.nf_name)
            return None
        # 受信待ち状態になるまで待つ
        while not self.shell.recv_ready():
            time.sleep(0.1)

        # 受信待ち状態の間受信する
        while self.shell.recv_ready():
            buffer += self.shell.recv(1024 * 32)
            time.sleep(0.1)

        # 最終行のプロンプトを取得
        self.prompt = self._get_prompt(buffer)
        LOGGER.output_1st_log("I00224", self.prompt)
        LOGGER.output_1st_log("I00225", buffer)

    def _get_prompt(self, buffer: bytes) -> str:
        """プロンプトを取得する

        Args:
            buffer (bytes): 受信メッセージ

        Returns:
            str: プロンプト文字列
        """
        return re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub("", buffer.decode('utf-8').splitlines()[-1])

    def _is_shell_enable(self) -> bool:
        """invoke shell有効・無効を確認する

        Returns:
            bool: invoke shellが有効ならTrue、無効ならFalse
        """
        return not (self.shell is None or self.shell.closed)


class SSHConnectException(Exception):
    """SSHConnectException SSH接続エラー
    """
    pass


class ProxyCommandException(Exception):
    """ProxyCommandException Proxy Commandエラー
    """
    pass


class SocketTimeoutException(Exception):
    """SocketTimeoutException SocketTimeoutエラー
    """
    pass
