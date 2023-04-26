import pathlib
import socket
from typing import Any, List
import paramiko

import pytest
import pytest_mock
from xgnlog.Log import Level

import src.eri_connection as nfshell

JOB_ID = "T23AJ002"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_eri_connection.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_eri_connection.log")


class MockLog():
    def __init__(self, job_id: str, init_level: Level, log_dir: str) -> None:
        self.job_id = job_id
        self.init_level = init_level
        self.log_path_1st = get_1st_log_path(log_dir)
        self.log_path_2nd = get_2nd_log_path(log_dir)

    def output_1st_log(self, msg_id: str, add_info: Any = None) -> None:
        with open(self.log_path_1st, "a", encoding="utf-8", newline="\n") as f:
            f.write("job_id:{0}, message_id:{1}, add_info:{2}\n".format(self.job_id, msg_id, add_info))

    def output_2nd_log(self, level: Level, add_info: Any = None) -> None:
        with open(self.log_path_2nd, "a", encoding="utf-8", newline="\n") as f:
            f.write("job_id:{0}, level:{1}, add_info:{2}\n".format(self.job_id, level.name, add_info))


class Proxy():
    def __init__(self, command: str):
        self.cmd = command.split(" ")


def test_get_sock01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_get_sock01 get_sock試験01 proxycommandなし

    試験条件
    ・踏み台: なし
    ・接続先: "10.2.100.6"
    ・port: なし(デフォルト)

    試験結果
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がNoneであること
    """
    bastion_name = None
    hostname = "10.2.100.6"
    port = 22
    proxycommand = "".replace("%h", hostname).replace("%p", str(port))

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00203", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00204", None)
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    respose = nfshell.get_sock(bastion_name, hostname)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose is None
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_sock02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_get_sock02 get_sock試験02 正常proxycommand取得

    試験条件
    ・踏み台: "director-1-a1-er-s01-vm-002"
    ・接続先: "10.2.100.6"
    ・port: なし(デフォルト)

    試験結果
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がProxyCommandインスタンスであること
    ・ProxyCommandが想定通りのcmdを保持していること
    """
    bastion_name = "director-1-a1-er-s01-vm-002"
    hostname = "10.2.100.6"
    port = 22
    proxycommand = "ssh -i /home/ansible/xgn/5g_lab_key -o StrictHostkeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p eccd@10.2.101.51".replace("%h", hostname).replace("%p", str(port))
    bast_conf = {"bastions": {"director-1-a1-er-s01-vm-002": {"proxycommand": "ssh -i /home/ansible/xgn/5g_lab_key -o StrictHostkeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p eccd@10.2.101.51"}}}

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00203", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00205", None)
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)
    mocker.patch("src.eri_connection.CONN_CONF", new=bast_conf)
    mocker.patch("paramiko.ProxyCommand", new=Proxy)

    respose = nfshell.get_sock(bastion_name, hostname)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose is not None
    assert isinstance(respose, Proxy)
    assert " ".join(respose.cmd) == proxycommand
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_sock03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_get_sock03 get_sock試験03 正常proxycommand取得(ポート指定あり)

    試験条件
    ・踏み台: "director-1-a1-er-s01-vm-002"
    ・接続先: "10.2.100.6"
    ・port: 2022

    試験結果
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がProxyCommandインスタンスであること
    ・ProxyCommandが想定通りのcmdを保持していること
    """
    bastion_name = "director-1-a1-er-s01-vm-002"
    hostname = "10.2.100.6"
    port = 2022
    proxycommand = "ssh -i /home/ansible/xgn/5g_lab_key -o StrictHostkeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p eccd@10.2.101.51".replace("%h", hostname).replace("%p", str(port))
    bast_conf = {"bastions": {"director-1-a1-er-s01-vm-002": {"proxycommand": "ssh -i /home/ansible/xgn/5g_lab_key -o StrictHostkeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p eccd@10.2.101.51"}}}

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00203", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00205", None)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)
    mocker.patch("src.eri_connection.CONN_CONF", new=bast_conf)
    mocker.patch("paramiko.ProxyCommand", new=Proxy)

    respose = nfshell.get_sock(bastion_name, hostname, port)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose is not None
    assert isinstance(respose, Proxy)
    assert " ".join(respose.cmd) == proxycommand
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_sock04(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_get_sock04 get_sock試験04 異常proxycommand

    試験条件
    ・踏み台: "director-1-a1-er-s01-vm-002"
    ・接続先: "10.2.100.6"
    ・port: なし

    試験結果
    ・eri_connection.ProxyCommandExceptionが発生すること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログが想定しているlevel、add_infoあること
    """
    bastion_name = "director-1-a1-er-s01-vm-002"
    hostname = "10.2.100.6"
    port = 22
    proxycommand = "ssh -i /home/ansible/xgn/5g_lab_key -o StrictHostkeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p eccd@10.2.101.51".replace("%h", hostname).replace("%p", str(port))
    bast_conf = {"bastions": {"director-1-a1-er-s01-vm-002": {"proxycommand": "ssh -i /home/ansible/xgn/5g_lab_key -o StrictHostkeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p eccd@10.2.101.51"}}}

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00203", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00202", None)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:ProxyCommand取得異常:\n",
        "パラメータ:\n",
        f" command: {proxycommand}\n",
        f" hostname: {hostname}\n",
        f" port: {port}\n",
        " Trace: FileNotFoundError File Not Found\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)
    mocker.patch("src.eri_connection.CONN_CONF", new=bast_conf)
    mocker.patch("paramiko.ProxyCommand", side_effect=FileNotFoundError("File Not Found"))

    with pytest.raises(nfshell.ProxyCommandException) as exc_info:
        respose = nfshell.get_sock(bastion_name, hostname)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert exc_info.type is nfshell.ProxyCommandException
    assert str(exc_info.value) == bastion_name
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_init01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_init01 __init__試験01 インスタンス生成(nf_name: a1-er-s01-smfvo-001)

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert client is not None
    assert isinstance(client, nfshell.NFShellClient)
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_init02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_init02 __init__試験02 インスタンス生成異常(nf_name: None)

    試験条件
    ・nf_name: None

    試験結果
    ・ValueErrorが発生すること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログが想定しているlevel、add_infoあること
    """
    nf_name = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00201", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:インスタンス生成異常:\n",
        "パラメータ:\n",
        f" nf_name: {nf_name}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    with pytest.raises(ValueError) as exc_info:
        client = nfshell.NFShellClient(nf_name)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert exc_info.type is ValueError
    assert str(exc_info.value) == "nf_name: None is not allowed value."
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_connect01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_connect01 connect試験01 SSH接続成功

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・get_sock()が1回呼ばれること
    ・super().connect()が1回呼ばれること
    ・super().invoke_shell()が1回呼ばれること
    ・self._read()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がNoneであること
    """
    """test_connect01 connect試験01 SSH接続成功
    """
    nf_name = "a1-er-s01-smfvo-001"

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00206", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00207", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.connect = mocker.Mock(side_effect=[True])
    test_mock.invoke_shell = mocker.Mock(side_effect=["shell"])
    test_mock.get_sock = mocker.Mock(side_effect=[True])
    test_mock._read_first = mocker.Mock(side_effect=["_read_first"])

    mocker.patch("paramiko.SSHClient.connect", test_mock.connect)
    mocker.patch("paramiko.SSHClient.invoke_shell", test_mock.invoke_shell)

    mocker.patch("src.eri_connection.get_sock", test_mock.get_sock)
    mocker.patch.object(client, "_read_first", test_mock._read_first)

    respose = client.connect()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose is None
    assert test_mock.get_sock.called is True
    assert test_mock.get_sock.call_count == 1
    assert test_mock.connect.called is True
    assert test_mock.connect.call_count == 1
    assert test_mock.invoke_shell.called is True
    assert test_mock.invoke_shell.call_count == 1
    assert test_mock._read_first.called is True
    assert test_mock._read_first.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_connect02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_connect02 connect試験02 SSH接続失敗

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・eri_connection.SSHConnectionExceptionが発生すること
    ・get_sock()が1回呼ばれること
    ・super().connect()が1回呼ばれること
    ・super().invoke_shell()が呼ばれないこと
    ・self._read()が呼ばれないこと
    ・self.close()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    nf_name = "a1-er-s01-smfvo-001"

    kwargs = {
        "username": "kddiadmin",
        "port": 22,
        "key_filename": None,
        "sock": "sock",
        "timeout": 10
    }
    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00206", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00203", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:SSH接続異常:\n",
        "パラメータ:\n",
        f" nf_name: {nf_name}\n",
        " hostname: 10.2.100.197\n",
        " password: ************\n",
        " passphrase: ************\n",
        f" kwargs: {kwargs}\n",
        " Trace: AuthenticationException AuthenticationException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.connect = mocker.Mock(side_effect=[paramiko.AuthenticationException("AuthenticationException")])
    test_mock.invoke_shell = mocker.Mock(side_effect=["shell"])
    test_mock.get_sock = mocker.Mock(side_effect=["sock"])
    test_mock._read = mocker.Mock(side_effect=["_read"])
    test_mock.close = mocker.Mock(side_effect=[True])

    mocker.patch("paramiko.SSHClient.connect", test_mock.connect)
    mocker.patch("paramiko.SSHClient.invoke_shell", test_mock.invoke_shell)

    mocker.patch("src.eri_connection.get_sock", test_mock.get_sock)
    mocker.patch.object(client, "_read", test_mock._read)
    mocker.patch.object(client, "close", test_mock.close)

    with pytest.raises(nfshell.SSHConnectException) as exc_info:
        respose = client.connect()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert exc_info.type is nfshell.SSHConnectException
    assert str(exc_info.value) == "AuthenticationException"
    # assert respose is None
    assert test_mock.get_sock.called is True
    assert test_mock.get_sock.call_count == 1
    assert test_mock.connect.called is True
    assert test_mock.connect.call_count == 1
    assert test_mock.invoke_shell.called is False
    assert test_mock.invoke_shell.call_count == 0
    assert test_mock._read.called is False
    assert test_mock._read.call_count == 0
    assert test_mock.close.called is True
    assert test_mock.close.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_connect03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_connect03 connect試験03 CONN_CONF取得失敗

    試験条件
    ・nf_name: HOGEHOGE

    試験結果
    ・KeyErrorが発生すること
    ・get_sock()が呼ばれないこと
    ・super().connect()が呼ばれないこと
    ・super().invoke_shell()が呼ばれないこと
    ・self._read()が呼ばれないこと
    ・self.close()が呼ばれないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "HOGEHOGE"

    kwargs = {
        "username": "kddiadmin",
        "port": 22,
        "key_filename": None,
        "sock": "sock"
    }

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00206", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.connect = mocker.Mock(side_effect=[paramiko.AuthenticationException("AuthenticationException")])
    test_mock.invoke_shell = mocker.Mock(side_effect=["shell"])
    test_mock.get_sock = mocker.Mock(side_effect=["sock"])
    test_mock._read = mocker.Mock(side_effect=["_read"])
    test_mock.close = mocker.Mock(side_effect=[True])

    mocker.patch("paramiko.SSHClient.connect", test_mock.connect)
    mocker.patch("paramiko.SSHClient.invoke_shell", test_mock.invoke_shell)

    mocker.patch("src.eri_connection.get_sock", test_mock.get_sock)
    mocker.patch.object(client, "_read", test_mock._read)
    mocker.patch.object(client, "close", test_mock.close)

    with pytest.raises(KeyError) as exc_info:
        respose = client.connect()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert exc_info.type is KeyError
    assert str(exc_info.value) == "'HOGEHOGE'"
    # assert respose is None
    assert test_mock.get_sock.called is False
    assert test_mock.get_sock.call_count == 0
    assert test_mock.connect.called is False
    assert test_mock.connect.call_count == 0
    assert test_mock.invoke_shell.called is False
    assert test_mock.invoke_shell.call_count == 0
    assert test_mock._read.called is False
    assert test_mock._read.call_count == 0
    assert test_mock.close.called is False
    assert test_mock.close.call_count == 0
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_close01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_close01 close試験01 SSH未接続の場合

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.close()が呼ばれないこと
    ・super().close()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がNoneであること
    """
    nf_name = "a1-er-s01-smfvo-001"

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00211", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00212", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(side_effect=[False])
    test_mock.close = mocker.Mock(side_effect=[True])
    test_mock.super_close = mocker.Mock(side_effect=[True])

    mocker.patch("paramiko.SSHClient.close", test_mock.super_close)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "shell", test_mock)

    respose = client.close()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose is None
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.close.called is False
    assert test_mock.close.call_count == 0
    assert test_mock.super_close.called is True
    assert test_mock.super_close.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_close02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_close01 close試験02 SSH接続中の場合

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.close()が1回呼ばれること
    ・super().close()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がNoneであること
    """
    nf_name = "a1-er-s01-smfvo-001"

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00211", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00212", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(side_effect=[True])
    test_mock.close = mocker.Mock(side_effect=[True])
    test_mock.super_close = mocker.Mock(side_effect=[True])

    mocker.patch("paramiko.SSHClient.close", test_mock.super_close)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "shell", test_mock)

    respose = client.close()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose is None
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.close.called is True
    assert test_mock.close.call_count == 1
    assert test_mock.super_close.called is True
    assert test_mock.super_close.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_command01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_command01 command試験01 

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・timeout: デフォルト

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.send()が1回呼ばれること
    ・self.shell.settimeout()が2回呼ばれること
    ・self.shell.settimeout()の引数がそれぞれ15.0,Noneであること
    ・self._read()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = "send command"
    expected_value = b"get response_value\r\n"
    timeout = 15.0

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00208", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00209", command),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00210", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=True)
    test_mock._read = mocker.Mock(return_value=expected_value)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock.settimeout = mocker.Mock(return_value=None)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read", test_mock._read)
    mocker.patch.object(client, "shell", test_mock)

    respose = client.command(command)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bytes)
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is True
    assert test_mock.send.call_count == 1
    assert test_mock.settimeout.called is True
    assert test_mock.settimeout.call_count == 2
    assert test_mock.settimeout.call_args_list[0][0] == (timeout,)
    assert test_mock.settimeout.call_args_list[1][0] == (None,)
    assert test_mock._read.called is True
    assert test_mock._read.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_command02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_command02 command試験02 デフォルトパラメータ指定

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・timeout: 10.0

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.send()が1回呼ばれること
    ・self.shell.settimeout()が2回呼ばれること
    ・self.shell.settimeout()の引数がそれぞれ10.0,Noneであること
    ・self._read()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = "send command"
    expected_value = b""
    timeout = 10.0

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00208", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00209", command),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00210", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=True)
    test_mock._read = mocker.Mock(return_value=expected_value)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock.settimeout = mocker.Mock(return_value=None)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read", test_mock._read)
    mocker.patch.object(client, "shell", test_mock)

    respose = client.command(command, timeout)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bytes)
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is True
    assert test_mock.send.call_count == 1
    assert test_mock.settimeout.called is True
    assert test_mock.settimeout.call_count == 2
    assert test_mock.settimeout.call_args_list[0][0] == (timeout,)
    assert test_mock.settimeout.call_args_list[1][0] == (None,)
    assert test_mock._read.called is True
    assert test_mock._read.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_command03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_command03 command試験03 SSH未接続

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・timeout: デフォルト

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.send()が呼ばれないこと
    ・self.shell.settimeout()が呼ばれないこと
    ・self._read()が呼ばれないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = "send command"
    expected_value = b""
    timeout = None
    wait = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00208", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00216", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.sleep = mocker.Mock(return_value=True)
    test_mock._is_shell_enable = mocker.Mock(return_value=False)
    test_mock._read = mocker.Mock(return_value=expected_value)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock.settimeout = mocker.Mock(return_value=None)

    mocker.patch("time.sleep", test_mock.sleep)
    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read", test_mock._read)
    mocker.patch.object(client, "shell", test_mock)

    respose = client.command(command)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bytes)
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is False
    assert test_mock.send.call_count == 0
    assert test_mock.settimeout.called is False
    assert test_mock.settimeout.call_count == 0
    assert test_mock.sleep.called is False
    assert test_mock.sleep.call_count == 0
    assert test_mock._read.called is False
    assert test_mock._read.call_count == 0
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_command04(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_command04 command試験04 socket.timeout発生

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・timeout: 100.0

    試験結果
    ・eri_connection.SocketTimeoutExceptionが発生すること
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.send()が1回呼ばれること
    ・self.shell.settimeout()が2回呼ばれること
    ・self.shell.settimeout()の引数がそれぞれ100.0,Noneであること
    ・self._read()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = "send command"
    expected_value = b"get response_value\r\n"
    timeout = 100.0

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00208", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00209", command),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00204", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:コマンド投入タイムアウト発生:\n",
        "パラメータ:\n",
        f" nf_name: {nf_name}\n",
        f" command: {command}\n",
        f" timeout: {timeout}\n",
        " Trace: TimeoutError socket.timeout\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(side_effect=[True])
    test_mock._read = mocker.Mock(side_effect=[socket.timeout("socket.timeout")])
    test_mock.send = mocker.Mock(side_effect=[None])
    test_mock.settimeout = mocker.Mock(side_effect=[None, None])

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read", test_mock._read)
    mocker.patch.object(client, "shell", test_mock)

    with pytest.raises(nfshell.SocketTimeoutException) as exc_info:
        respose = client.command(command, timeout)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert exc_info.type is nfshell.SocketTimeoutException
    assert str(exc_info.value) == "socket.timeout"
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is True
    assert test_mock.send.call_count == 1
    assert test_mock.settimeout.called is True
    assert test_mock.settimeout.call_count == 2
    assert test_mock.settimeout.call_args_list[0][0] == (timeout,)
    assert test_mock.settimeout.call_args_list[1][0] == (None,)
    assert test_mock._read.called is True
    assert test_mock._read.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_read01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_read01 _read試験01 正常試験

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.recv_ready()が2回呼ばれること
    ・self.shell.recv()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = b"send command"
    expected_value = b"get response_value"
    cmd_prompt = b"prompt#"
    recv_data = b"\r\n".join([command, expected_value, cmd_prompt])

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00213", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00215", None)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.DEBUG.name}, add_info:RAW data: {recv_data}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=True)
    test_mock._get_prompt = mocker.Mock(return_value=cmd_prompt.decode("utf-8"))
    test_mock.recv_ready = mocker.Mock(side_effect=[True, False])
    test_mock.recv = mocker.Mock(return_value=recv_data)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_get_prompt", test_mock._get_prompt)
    mocker.patch.object(client, "shell", test_mock)

    client.prompt = cmd_prompt.decode("utf-8")
    respose = client._read()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bytes)
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.recv_ready.called is True
    assert test_mock.recv_ready.call_count == 2
    assert test_mock.recv.called is True
    assert test_mock.recv.call_count == 1
    assert test_mock._get_prompt.called is True
    assert test_mock._get_prompt.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_read02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_read02 _read試験02 正常試験 (バッファ複数回取得)

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.recv_ready()が4回呼ばれること
    ・self.shell.recv()が3回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = b"send command"
    expected_value = b"get response_value"
    cmd_prompt = b"prompt#"
    recv_data = b"\r\n".join([command, expected_value, cmd_prompt])

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00213", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00215", None)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.DEBUG.name}, add_info:RAW data: {recv_data}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=True)
    test_mock._get_prompt = mocker.Mock(return_value=cmd_prompt.decode("utf-8"))
    test_mock.recv_ready = mocker.Mock(side_effect=[False, True, True, True, False])
    test_mock.recv = mocker.Mock(side_effect=[command + b"\r\n", expected_value + b"\r\n", cmd_prompt])

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_get_prompt", test_mock._get_prompt)
    mocker.patch.object(client, "shell", test_mock)

    client.prompt = cmd_prompt.decode("utf-8")
    respose = client._read()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bytes)
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.recv_ready.called is True
    assert test_mock.recv_ready.call_count == 5
    assert test_mock.recv.called is True
    assert test_mock.recv.call_count == 3
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_read03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_read03 _read試験03 準正常試験 (shell利用不可)

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.recv_ready()が呼ばれないこと
    ・self.shell.recv()が呼ばれないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    command = b"send command"
    expected_value = b"get response_value"
    cmd_prompt = b"prompt#"
    recv_data = b"\r\n".join([command, expected_value, cmd_prompt])

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00213", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00215", None)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=False)
    test_mock._get_prompt = mocker.Mock(return_value=cmd_prompt.decode("utf-8"))
    test_mock.recv_ready = mocker.Mock(side_effect=[True, False])
    test_mock.recv = mocker.Mock(return_value=recv_data)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_get_prompt", test_mock._get_prompt)
    mocker.patch.object(client, "shell", test_mock)

    respose = client._read()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == b""
    assert isinstance(respose, bytes)
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.recv_ready.called is False
    assert test_mock.recv_ready.call_count == 0
    assert test_mock.recv.called is False
    assert test_mock.recv.call_count == 0
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_is_shell_enable01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_is_shell_enable01 _is_shell_enable試験01 正常試験

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・shell: not None
    ・shell.closed: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がTrueであること
    """
    nf_name = "a1-er-s01-smfvo-001"
    expected_value = True

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.closed = False

    mocker.patch.object(client, "shell", test_mock)

    respose = client._is_shell_enable()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bool)
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_is_shell_enable02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_is_shell_enable02 _is_shell_enable試験02 正常試験

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・shell: not None
    ・shell.closed: True

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がFalseであること
    """
    nf_name = "a1-er-s01-smfvo-001"
    expected_value = False

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.closed = True

    mocker.patch.object(client, "shell", test_mock)

    respose = client._is_shell_enable()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bool)
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_is_shell_enable03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_is_shell_enable03 _is_shell_enable試験03 正常試験

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・shell: None
    ・shell.closed: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がFalseであること
    """
    nf_name = "a1-er-s01-smfvo-001"
    expected_value = False

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.closed = False

    mocker.patch.object(client, "shell", None)

    respose = client._is_shell_enable()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bool)
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_is_shell_enable04(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_is_shell_enable04 _is_shell_enable試験04 正常試験

    試験条件
    ・nf_name: a1-er-s01-smfvo-001
    ・shell: not None
    ・shell.closed: True

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果がFalseであること
    """
    nf_name = "a1-er-s01-smfvo-001"
    expected_value = False

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock.closed = True

    mocker.patch.object(client, "shell", None)

    respose = client._is_shell_enable()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert isinstance(respose, bool)
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_enter_config_mode01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_enter_config_mode01 enter_config_mode01 準正常試験

    試験条件
    ・self._is_shell_enable: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = False
    is_config_mode = False
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00216", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.is_config_mode = is_config_mode
    respose = client.enter_config_mode()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_enter_config_mode02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_enter_config_mode02 enter_config_mode 準正常試験

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: True

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = True
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00226", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.is_config_mode = is_config_mode
    respose = client.enter_config_mode()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == True
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_enter_config_mode03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_enter_config_mode03 enter_config_mode 正常試験

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = False
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00217", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00218", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock._read_first = mocker.Mock(return_value=None)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read_first", test_mock._read_first)
    mocker.patch.object(client, "shell", test_mock)

    client.is_config_mode = is_config_mode
    respose = client.enter_config_mode()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == True
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is True
    assert test_mock.send.call_count == 1
    assert test_mock._read_first.called is True
    assert test_mock._read_first.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_exit_config_mode01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_exit_config_mode01 exit_config_mode01 準正常試験

    試験条件
    ・self._is_shell_enable: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = False
    is_config_mode = False
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00216", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.is_config_mode = is_config_mode
    respose = client.exit_config_mode()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_exit_config_mode02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_exit_config_mode02 exit_config_mode 準正常試験

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = False
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00227", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.is_config_mode = is_config_mode
    respose = client.exit_config_mode()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_exit_config_mode03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_exit_config_mode03 exit_config_mode 正常試験

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: True

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = True
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00219", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00220", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock._read_first = mocker.Mock(return_value=None)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read_first", test_mock._read_first)
    mocker.patch.object(client, "shell", test_mock)

    client.is_config_mode = is_config_mode
    respose = client.exit_config_mode()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is True
    assert test_mock.send.call_count == 1
    assert test_mock._read_first.called is True
    assert test_mock._read_first.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_exit_config_mode04(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_exit_config_mode04 exit_config_mode 正常試験(強制モード)

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: True

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = True
    forced = True
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)
    test_mock.abort = mocker.Mock(return_value=None)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock._read_first = mocker.Mock(return_value=None)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "abort", test_mock.abort)
    mocker.patch.object(client, "_read_first", test_mock._read_first)
    mocker.patch.object(client, "shell", test_mock)

    client.is_config_mode = is_config_mode
    respose = client.exit_config_mode(forced=forced)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.abort.called is True
    assert test_mock.abort.call_count == 1
    assert test_mock.send.called is False
    assert test_mock._read_first.called is False
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_abort01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_abort01 abort 準正常試験

    試験条件
    ・self._is_shell_enable: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = False
    is_config_mode = False
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00216", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.is_config_mode = is_config_mode
    respose = client.abort()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_abort02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_abort02 abort 準正常試験

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: False

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = False
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00227", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.is_config_mode = is_config_mode
    respose = client.abort()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_abort03(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_abort03 abort 正常試験

    試験条件
    ・self._is_shell_enable: True
    ・self.is_config_mode: True

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    is_shell_enable = True
    is_config_mode = True
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00221", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00222", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=is_shell_enable)
    test_mock.send = mocker.Mock(return_value=None)
    test_mock._read_first = mocker.Mock(return_value=None)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_read_first", test_mock._read_first)
    mocker.patch.object(client, "shell", test_mock)

    client.is_config_mode = is_config_mode
    respose = client.abort()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.is_config_mode == False
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.send.called is True
    assert test_mock.send.call_count == 1
    assert test_mock._read_first.called is True
    assert test_mock._read_first.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_read_first01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_read_first01 _read_first 正常試験

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.recv_ready()が4回呼ばれること
    ・self.shell.recv()が1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    expected_value = None
    cmd_prompt = b"prompt#"
    recv_data = b"\r\n".join([b"", cmd_prompt])

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00223", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00224", cmd_prompt.decode("utf-8")),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00225", recv_data)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=True)
    test_mock._get_prompt = mocker.Mock(return_value=cmd_prompt.decode("utf-8"))
    test_mock.recv_ready = mocker.Mock(side_effect=[False, True, True, False])
    test_mock.recv = mocker.Mock(return_value=recv_data)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)
    mocker.patch.object(client, "_get_prompt", test_mock._get_prompt)
    mocker.patch.object(client, "shell", test_mock)

    client.prompt = cmd_prompt.decode("utf-8")
    respose = client._read_first()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert client.prompt == cmd_prompt.decode("utf-8")
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert test_mock.recv_ready.called is True
    assert test_mock.recv_ready.call_count == 4
    assert test_mock.recv.called is True
    assert test_mock.recv.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_read_first02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """test_read_first02 _read_first 準正常試験(シェル利用不可)

    試験条件
    ・nf_name: a1-er-s01-smfvo-001

    試験結果
    ・Exceptionが発生しないこと
    ・self._is_shell_enable()が1回呼ばれること
    ・self.shell.recv_ready()が4回呼ばれること
    ・self.shell.recv()が3回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が指定した結果であること
    """
    nf_name = "a1-er-s01-smfvo-001"
    expected_value = None
    cmd_prompt = b"prompt#"
    recv_data = b"\r\n".join([b"", cmd_prompt])

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00201", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00202", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00223", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00216", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_connection.LOGGER", new=logger)

    client = nfshell.NFShellClient(nf_name)

    test_mock = mocker.MagicMock()
    test_mock._is_shell_enable = mocker.Mock(return_value=False)

    mocker.patch.object(client, "_is_shell_enable", test_mock._is_shell_enable)

    client.prompt = cmd_prompt.decode("utf-8")
    respose = client._read_first()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert respose == expected_value
    assert test_mock._is_shell_enable.called is True
    assert test_mock._is_shell_enable.call_count == 1
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_prompt01(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """get_prompt01 get_prompt 正常試験

    試験条件
    ・buffer: \x1b[?7hkddiadmin@eric-cm-yang-provider-c676ff7f9-cfk9w#

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果が指定した結果であること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    prompt = b"\x1b[?7hkddiadmin@eric-cm-yang-provider-c676ff7f9-cfk9w#"
    expected_value = "kddiadmin@eric-cm-yang-provider-c676ff7f9-cfk9w#"

    client = nfshell.NFShellClient(nf_name)

    respose = client._get_prompt(prompt)

    # 結果確認
    assert respose == expected_value


def test_get_prompt02(tmpdir, capsys: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture):
    """get_prompt02 get_prompt 正常試験(設定モード)

    試験条件
    ・buffer: \x1b[?7hkddiadmin@eric-cm-yang-provider-c676ff7f9-cfk9w#

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果が指定した結果であること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    nf_name = "a1-er-s01-smfvo-001"
    prompt = b"\x1b[?7hkddiadmin@eric-cm-yang-provider-c676ff7f9-cfk9w(Config)#"
    expected_value = "kddiadmin@eric-cm-yang-provider-c676ff7f9-cfk9w(Config)#"

    client = nfshell.NFShellClient(nf_name)

    respose = client._get_prompt(prompt)

    # 結果確認
    assert respose == expected_value
